from __future__ import annotations

from io import BytesIO
from pathlib import Path

import typer

import latticeflow.go.cli.utils.arguments as cli_args
import latticeflow.go.cli.utils.exceptions as cli_exc
import latticeflow.go.cli.utils.printing as cli_print
from latticeflow.go.cli.dataset_generators import (
    create_or_update_single_dataset_generator,
)
from latticeflow.go.cli.datasets import create_or_update_single_dataset
from latticeflow.go.cli.dtypes import CLICreateDataset
from latticeflow.go.cli.dtypes import CLICreateDatasetGenerator
from latticeflow.go.cli.dtypes import CLICreateEvaluation
from latticeflow.go.cli.dtypes import CLICreateModel
from latticeflow.go.cli.dtypes import CLICreateModelAdapter
from latticeflow.go.cli.dtypes import CLICreateRunConfig
from latticeflow.go.cli.dtypes import CLICreateTask
from latticeflow.go.cli.dtypes import CLIProviderAndModelKey
from latticeflow.go.cli.model_adapters import create_or_update_single_model_adapter
from latticeflow.go.cli.models import add_model_from_provider
from latticeflow.go.cli.models import map_and_add_single_custom_model
from latticeflow.go.cli.tasks import create_or_update_single_task
from latticeflow.go.cli.utils.dependency_resolving import build_run_config_dependencies
from latticeflow.go.cli.utils.dependency_resolving import (
    get_run_config_processing_order,
)
from latticeflow.go.cli.utils.env_vars import get_cli_env_vars
from latticeflow.go.cli.utils.helpers import app_callback
from latticeflow.go.cli.utils.helpers import assign_tags_to_entity
from latticeflow.go.cli.utils.helpers import get_client_from_env
from latticeflow.go.cli.utils.helpers import load_ai_app_key
from latticeflow.go.cli.utils.printing import summarize_exception_chain
from latticeflow.go.cli.utils.schema_mappers import EntityByIdentifiersMap
from latticeflow.go.cli.utils.schema_mappers import map_dataset_cli_to_api_entity
from latticeflow.go.cli.utils.schema_mappers import (
    map_dataset_generator_cli_to_api_entity,
)
from latticeflow.go.cli.utils.schema_mappers import map_evaluation_cli_to_api_entity
from latticeflow.go.cli.utils.schema_mappers import map_model_adapter_cli_to_api_entity
from latticeflow.go.cli.utils.schema_mappers import map_task_cli_to_api_entity
from latticeflow.go.cli.utils.single_commands import with_callback
from latticeflow.go.cli.utils.yaml_utils import load_yaml_recursively
from latticeflow.go.client import Client
from latticeflow.go.models import EvaluationAction
from latticeflow.go.models import StoredAIApp
from latticeflow.go.models import StoredDataset
from latticeflow.go.models import StoredDatasetGenerator
from latticeflow.go.models import StoredEvaluation
from latticeflow.go.models import StoredModel
from latticeflow.go.models import StoredModelAdapter
from latticeflow.go.models import StoredTag
from latticeflow.go.models import StoredTask
from latticeflow.go.models import UploadTaskResultLogBody
from latticeflow.go.types import File
from latticeflow.go.utils.resolution import YAMLOriginInfo


def register_run_command(app: typer.Typer) -> None:
    app.command(
        name="run",
        short_help="Create and run an evaluation and its dependencies from a run config file.",
        help=(
            "Create and run an evaluation along with its dependencies (models, model adapters, "
            "dataset generators, datasets, and tasks) as specified in a run config YAML file. "
            "You can optionally validate the configuration."
        ),
    )(with_callback(lambda: app_callback(get_cli_env_vars))(_run))


def _run(
    path: Path = cli_args.single_config_path_argument("run"),
    should_validate_only: bool = cli_args.should_validate_only_option,
) -> None:
    """Create and run an evaluation along with its dependencies from a run config file."""
    ai_app_key = load_ai_app_key()
    client = get_client_from_env()

    if should_validate_only:
        _validate_run_config(path)
        return

    stored_ai_app = client.ai_apps.get_ai_app_by_key(ai_app_key)
    run_config, origin_info = _get_cli_run_config_from_file(path)

    models_map = EntityByIdentifiersMap(client.models.get_models().models)
    model_adapters_map = EntityByIdentifiersMap(
        client.model_adapters.get_model_adapters().model_adapters
    )
    dataset_generators_map = EntityByIdentifiersMap(
        client.dataset_generators.get_dataset_generators().dataset_generators
    )
    datasets_map = EntityByIdentifiersMap(client.datasets.get_datasets().datasets)
    tasks_map = EntityByIdentifiersMap(client.tasks.get_tasks().tasks)
    tags_value_to_stored_tag_map = {
        tag.value: tag for tag in client.tags.get_tags().tags
    }
    ordered_entities = get_run_config_processing_order(
        cli_run_config=run_config,
        dependencies=build_run_config_dependencies(
            cli_dataset_generators=run_config.dataset_generators,
            cli_datasets=run_config.datasets,
            config_file=path,
            dataset_generators_map=dataset_generators_map,
        ),
    )

    added_model_adapters = 0
    added_models = 0
    added_dataset_generators = 0
    added_datasets = 0
    added_tasks = 0
    added_evaluations = 0
    started_evaluation = False

    # NOTE: We need this to preserve the original order of datasets for origin info mapping.
    dataset_index_map = {
        dataset.key: original_i
        for original_i, dataset in enumerate(run_config.datasets)
    }
    dataset_origin_infos: YAMLOriginInfo | None = None
    for entity in ordered_entities:
        if isinstance(entity, CLICreateModelAdapter):
            new_model_adapter = _add_single_model_adapter(
                cli_model_adapter=entity,
                model_adapters_map=model_adapters_map,
                config_file=path,
                client=client,
            )
            if new_model_adapter is not None:
                added_model_adapters += 1
        elif isinstance(entity, (CLICreateModel, CLIProviderAndModelKey)):
            new_model = _add_single_model(
                cli_model=entity,
                model_adapters_map=model_adapters_map,
                models_map=models_map,
                config_file=path,
                client=client,
            )
            if new_model is not None:
                added_models += 1
        elif isinstance(entity, CLICreateDatasetGenerator):
            new_dataset_generator = _add_single_dataset_generator(
                cli_dataset_generator=entity,
                dataset_generators_map=dataset_generators_map,
                datasets_map=datasets_map,
                models_map=models_map,
                config_file=path,
                client=client,
            )
            if new_dataset_generator is not None:
                added_dataset_generators += 1
        elif isinstance(entity, CLICreateDataset):
            if dataset_origin_infos is None:
                dataset_origin_infos = origin_info.get("datasets")
            new_dataset = _add_single_dataset(
                cli_dataset=entity,
                dataset_generators_map=dataset_generators_map,
                datasets_map=datasets_map,
                models_map=models_map,
                config_file=path,
                client=client,
                origin_info=origin_info,
                dataset_origin_infos=dataset_origin_infos,
                dataset_original_index=dataset_index_map[entity.key],
            )
            if new_dataset is not None:
                added_datasets += 1
        elif isinstance(entity, CLICreateTask):
            new_task = _add_single_task(
                cli_task=entity,
                tasks_map=tasks_map,
                datasets_map=datasets_map,
                models_map=models_map,
                config_file=path,
                client=client,
                tags_value_to_stored_tag_map=tags_value_to_stored_tag_map,
            )
            if new_task is not None:
                added_tasks += 1
        elif isinstance(entity, CLICreateEvaluation):
            new_evaluation = _create_evaluation(
                client=client,
                cli_evaluation=entity,
                stored_ai_app=stored_ai_app,
                config_file=path,
                models_map=models_map,
                datasets_map=datasets_map,
                tasks_map=tasks_map,
                tags_value_to_stored_tag_map=tags_value_to_stored_tag_map,
            )
            if new_evaluation is not None:
                added_evaluations = 1
                _upload_logs_if_needed(
                    client=client,
                    cli_evaluation=entity,
                    stored_evaluation=new_evaluation,
                    config_file=path,
                )
                started_evaluation = _start_evaluation(
                    client, new_evaluation, stored_ai_app
                )

    total_entities_to_be_added = (
        len(run_config.model_adapters)
        + len(run_config.models)
        + len(run_config.dataset_generators)
        + len(run_config.datasets)
        + len(run_config.tasks)
        + (1 if run_config.evaluation is not None else 0)
    )
    total_added_entities = (
        added_model_adapters
        + added_models
        + added_dataset_generators
        + added_datasets
        + added_tasks
        + added_evaluations
    )
    if total_added_entities < total_entities_to_be_added or not started_evaluation:
        raise typer.Exit(code=1)


def _get_cli_run_config_from_file(
    config_file: Path,
) -> tuple[CLICreateRunConfig, YAMLOriginInfo]:
    try:
        loaded_dict, origin_info = load_yaml_recursively(config_file)
        return CLICreateRunConfig.model_validate(
            loaded_dict, ignore_extra=False
        ), origin_info
    except Exception as error:
        raise cli_exc.CLIInvalidConfigError("run config", config_file, None) from error


def _validate_run_config(config_file: Path) -> None:
    try:
        _get_cli_run_config_from_file(config_file)
        cli_print.log_validation_success_info(config_file)
    except Exception as error:
        cli_print.log_validation_fail_error(config_file, error)
        raise cli_exc.CLIValidationError("run config") from error


def _add_single_model_adapter(
    *,
    cli_model_adapter: CLICreateModelAdapter,
    model_adapters_map: EntityByIdentifiersMap[StoredModelAdapter],
    config_file: Path,
    client: Client,
) -> StoredModelAdapter | None:
    try:
        model_adapter = map_model_adapter_cli_to_api_entity(
            cli_model_adapter=cli_model_adapter, config_file=config_file
        )
        stored_model_adapter = model_adapters_map.get_entity_by_key(
            cli_model_adapter.key
        )
        new_stored_model_adapter = create_or_update_single_model_adapter(
            client, model_adapter, stored_model_adapter, verbosity="low"
        )
        model_adapters_map.update_entity(new_stored_model_adapter)
        return new_stored_model_adapter
    except Exception as error:
        cli_print.log_create_update_fail_error("model adapter", config_file, error)
        return None


def _add_single_model(
    *,
    cli_model: CLICreateModel | CLIProviderAndModelKey,
    model_adapters_map: EntityByIdentifiersMap[StoredModelAdapter],
    models_map: EntityByIdentifiersMap[StoredModel],
    config_file: Path,
    client: Client,
) -> StoredModel | None:
    try:
        if isinstance(cli_model, CLIProviderAndModelKey):
            new_stored_model = add_model_from_provider(
                cli_model.provider_and_model_key, models_map, client, verbosity="low"
            )
        else:
            new_stored_model = map_and_add_single_custom_model(
                client=client,
                cli_model=cli_model,
                model_adapters_map=model_adapters_map,
                models_map=models_map,
                config_file=config_file,
                verbosity="low",
            )
        models_map.update_entity(new_stored_model)
        return new_stored_model
    except Exception as error:
        cli_print.log_create_update_fail_error("model", config_file, error)
        return None


def _add_single_dataset_generator(
    *,
    cli_dataset_generator: CLICreateDatasetGenerator,
    dataset_generators_map: EntityByIdentifiersMap[StoredDatasetGenerator],
    datasets_map: EntityByIdentifiersMap[StoredDataset],
    models_map: EntityByIdentifiersMap[StoredModel],
    config_file: Path,
    client: Client,
) -> StoredDatasetGenerator | None:
    try:
        dataset_generator = map_dataset_generator_cli_to_api_entity(
            cli_dataset_generator=cli_dataset_generator,
            datasets_map=datasets_map,
            models_map=models_map,
            config_file=config_file,
        )
        stored_dataset_generator = dataset_generators_map.get_entity_by_key(
            dataset_generator.key
        )
        new_stored_dataset_generator = create_or_update_single_dataset_generator(
            client, dataset_generator, stored_dataset_generator, verbosity="low"
        )
        dataset_generators_map.update_entity(new_stored_dataset_generator)
        return new_stored_dataset_generator
    except Exception as error:
        cli_print.log_create_update_fail_error("dataset generator", config_file, error)
        return None


def _add_single_dataset(
    *,
    cli_dataset: CLICreateDataset,
    dataset_generators_map: EntityByIdentifiersMap[StoredDatasetGenerator],
    datasets_map: EntityByIdentifiersMap[StoredDataset],
    models_map: EntityByIdentifiersMap[StoredModel],
    config_file: Path,
    client: Client,
    origin_info: YAMLOriginInfo,
    dataset_origin_infos: YAMLOriginInfo,
    dataset_original_index: int,
) -> StoredDataset | None:
    try:
        (dataset, dataset_file_path, dataset_generation_request_with_id) = (
            map_dataset_cli_to_api_entity(
                cli_dataset=cli_dataset,
                models_map=models_map,
                datasets_map=datasets_map,
                dataset_generators_map=dataset_generators_map,
                origin_info=dataset_origin_infos.get(dataset_original_index),
            )
        )
        stored_dataset = datasets_map.get_entity_by_key(cli_dataset.key)
        new_stored_dataset = create_or_update_single_dataset(
            client,
            dataset,
            dataset_file_path,
            dataset_generation_request_with_id,
            stored_dataset,
            verbosity="low",
        )
        datasets_map.update_entity(new_stored_dataset)
        return new_stored_dataset
    except Exception as error:
        cli_print.log_create_update_fail_error(
            "dataset", origin_info.get_file_path(), error
        )
        return None


def _add_single_task(
    *,
    cli_task: CLICreateTask,
    tasks_map: EntityByIdentifiersMap[StoredTask],
    datasets_map: EntityByIdentifiersMap[StoredDataset],
    models_map: EntityByIdentifiersMap[StoredModel],
    config_file: Path,
    client: Client,
    tags_value_to_stored_tag_map: dict[str, StoredTag],
) -> StoredTask | None:
    try:
        task = map_task_cli_to_api_entity(
            cli_task=cli_task,
            models_map=models_map,
            datasets_map=datasets_map,
            config_file=config_file,
        )
        stored_task = tasks_map.get_entity_by_key(task.key)
        new_stored_task = create_or_update_single_task(
            client, task, stored_task, verbosity="low"
        )
        tasks_map.update_entity(new_stored_task)
        assign_tags_to_entity(
            current_tags={tag.value for tag in new_stored_task.tags},
            tags_from_cli_entity=set(cli_task.tags),
            client=client,
            tags_value_to_stored_tag_map=tags_value_to_stored_tag_map,
            update_fn=lambda tag_ids: client.tasks.update_task_tags(
                new_stored_task.id, tag_ids
            ),
        )
        return client.tasks.get_task(new_stored_task.id)
    except Exception as error:
        cli_print.log_create_update_fail_error("task", config_file, error)
        return None


def _create_evaluation(
    client: Client,
    cli_evaluation: CLICreateEvaluation,
    stored_ai_app: StoredAIApp,
    config_file: Path,
    models_map: EntityByIdentifiersMap[StoredModel],
    datasets_map: EntityByIdentifiersMap[StoredDataset],
    tasks_map: EntityByIdentifiersMap[StoredTask],
    tags_value_to_stored_tag_map: dict[str, StoredTag],
) -> StoredEvaluation | None:
    try:
        evaluation = map_evaluation_cli_to_api_entity(
            cli_evaluation=cli_evaluation,
            models_map=models_map,
            datasets_map=datasets_map,
            tasks_map=tasks_map,
            config_file=config_file,
        )
        new_stored_evaluation = client.evaluations.create_evaluation(
            stored_ai_app.id, evaluation
        )
        cli_print.log_create_success_info(
            "evaluation", new_stored_evaluation.id, "ID", verbosity="low"
        )
        assign_tags_to_entity(
            current_tags={tag.value for tag in new_stored_evaluation.tags},
            tags_from_cli_entity=set(cli_evaluation.tags),
            client=client,
            tags_value_to_stored_tag_map=tags_value_to_stored_tag_map,
            update_fn=lambda tag_ids: client.evaluations.update_evaluation_tags(
                stored_ai_app.id, new_stored_evaluation.id, tag_ids
            ),
        )
        return client.evaluations.get_evaluation(
            app_id=stored_ai_app.id, evaluation_id=new_stored_evaluation.id
        )
    except Exception as error:
        cli_print.log_error(
            f"Could not create/update evaluation from config at path '{config_file}':"
            f"\n{summarize_exception_chain(error)}"
        )
        return None


def _upload_logs_if_needed(
    *,
    client: Client,
    cli_evaluation: CLICreateEvaluation,
    stored_evaluation: StoredEvaluation,
    config_file: Path,
) -> None:
    # This works because the BE guarantees that the returned task results are in the
    # same order as the order of the task specifications (at the time of the create-eval
    # API call).
    for cli_spec, task_result in zip(
        cli_evaluation.task_specifications, stored_evaluation.task_results, strict=True
    ):
        if cli_spec.task_result_log_path is None:
            continue

        log_path = Path(cli_spec.task_result_log_path)

        # Resolve relative paths relative to the run config file
        if not log_path.is_absolute():
            log_path = (config_file.parent / log_path).resolve()

        if not log_path.exists():
            cli_print.log_warning(
                f"[TaskResult(ID={task_result.id})] Log file not found at '{log_path}'. Skipping upload for task '{task_result.display_name}'."
            )
            continue

        try:
            client.task_results.upload_task_result_log(
                task_result_id=task_result.id,
                body=UploadTaskResultLogBody(
                    task_result_log=File(
                        payload=BytesIO(log_path.read_bytes()),
                        file_name="task_result_log.json",
                        mime_type="application/json",
                    )
                ),
            )
            cli_print.log_info(
                f"[TaskResult(ID={task_result.id})] Task result log uploaded successfully for task '{task_result.display_name}'."
            )
        except Exception as error:
            cli_print.log_error(
                f"[TaskResult(ID={task_result.id})] Failed to upload log for task result '{task_result.display_name}': {str(error)}"
            )


def _start_evaluation(
    client: Client, stored_evaluation: StoredEvaluation, stored_ai_app: StoredAIApp
) -> bool:
    try:
        client.evaluations.execute_action_evaluation(
            stored_ai_app.id, stored_evaluation.id, action=EvaluationAction.START
        )
        cli_print.log_info(
            f'[Evaluation(ID="{stored_evaluation.id}")] Started successfully.'
        )
        base_url = client.base_url.rstrip("/")
        cli_print.log_char_full_width("-")
        cli_print.log_info(
            f"""\
Evaluation overview available at:

{base_url}/ai-apps/{stored_ai_app.id}/evaluations

Or in the CLI using:

lf evaluation overview {stored_evaluation.id}
"""
        )

        return True
    except Exception as error:
        cli_print.log_error(
            f"Could not start evaluation with ID '{stored_evaluation.id}':"
            f"\n{summarize_exception_chain(error)}"
        )
        return False
