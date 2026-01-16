from __future__ import annotations

import datetime
import io
import json
import zipfile
from pathlib import Path
from typing import Callable

import typer

import latticeflow.go.cli.utils.arguments as cli_args
import latticeflow.go.cli.utils.exceptions as cli_exc
import latticeflow.go.cli.utils.printing as cli_print
from latticeflow.go.cli.utils.helpers import dump_entity_to_yaml_file
from latticeflow.go.cli.utils.helpers import get_client_from_env
from latticeflow.go.cli.utils.helpers import load_ai_app_key
from latticeflow.go.cli.utils.helpers import register_app_callback
from latticeflow.go.cli.utils.schema_mappers import EntityByIdentifiersMap
from latticeflow.go.cli.utils.schema_mappers import (
    map_api_entities_used_in_evaluation_to_cli_run_config,
)
from latticeflow.go.cli.utils.time import datetime_to_str
from latticeflow.go.cli.utils.time import timestamp_to_localized_datetime
from latticeflow.go.client import Client
from latticeflow.go.models import DatasetProvider
from latticeflow.go.models import StoredDataset
from latticeflow.go.models import StoredEvaluation
from latticeflow.go.models import StoredTaskResult
from latticeflow.go.types import File


def _get_progress(task_result: StoredTaskResult) -> str:
    progress = task_result.progress
    if progress is None:
        return ""

    if progress.num_total_samples is None or progress.num_processed_samples is None:
        return f"{progress.progress:.1%}"

    return f"{progress.progress:.1%} ({progress.num_processed_samples}/{progress.num_total_samples})"


def _get_runtime(task_result: StoredTaskResult) -> str:
    if task_result.started_at is not None and task_result.finished_at is not None:
        delta = datetime.timedelta(
            seconds=task_result.finished_at - task_result.started_at
        )
        return f"{delta}s"

    return "-"


PRETTY_ENTITY_NAME = "evaluation"
EVALUATION_TABLE_COLUMNS: list[tuple[str, Callable[[StoredEvaluation], str]]] = [
    ("ID", lambda evaluation: evaluation.id),
    ("Name", lambda evaluation: evaluation.display_name),
    ("Key", lambda evaluation: evaluation.key),
    (
        "Created",
        lambda evaluation: datetime_to_str(
            timestamp_to_localized_datetime(evaluation.created_at)
        ),
    ),
    ("Status", lambda evaluation: evaluation.execution_status.value),
]
TASK_RESULTS_TABLE_COLUMNS: list[tuple[str, Callable[[StoredTaskResult], str]]] = [
    ("Task Result ID", lambda task_result: task_result.id),
    ("Task Name", lambda task_result: task_result.display_name),
    ("Task Execution Status", lambda task_result: task_result.execution_status.value),
    (
        "Task Result Status",
        lambda task_result: task_result.result_status.value
        if task_result.result_status is not None
        else "-",
    ),
    ("Task Execution Progress", _get_progress),
    ("Task Execution Runtime", _get_runtime),
]
evaluation_app = typer.Typer(help="Evaluation commands")
register_app_callback(evaluation_app)


@evaluation_app.command("list")
def list_evaluations(is_json_output: bool = cli_args.json_flag_option) -> None:
    """List all evaluations as JSON or in a table."""
    if is_json_output:
        cli_print.suppress_logging()
    ai_app_key = load_ai_app_key()

    client = get_client_from_env()
    ai_app = client.ai_apps.get_ai_app_by_key(ai_app_key)
    try:
        stored_evaluations = client.evaluations.get_evaluations(
            app_id=ai_app.id
        ).evaluations
        if is_json_output:
            cli_print.print_entities_as_json(stored_evaluations)
        else:
            cli_print.print_table(
                "Evaluations", stored_evaluations, EVALUATION_TABLE_COLUMNS
            )
    except Exception as error:
        raise cli_exc.CLIListError(PRETTY_ENTITY_NAME) from error


@evaluation_app.command("overview")
def _overview(
    id: str = typer.Argument(
        ...,
        help=f"ID of the {PRETTY_ENTITY_NAME} for which the overview should be shown.",
    ),
    is_json_output: bool = cli_args.json_flag_option,
) -> None:
    """Show an overview of the evaluation with the provided ID for the provided AI App as JSON or in a table."""
    if is_json_output:
        cli_print.suppress_logging()
    ai_app_key = load_ai_app_key()

    client = get_client_from_env()

    ai_app = client.ai_apps.get_ai_app_by_key(ai_app_key)
    try:
        evaluation = client.evaluations.get_evaluation(
            app_id=ai_app.id, evaluation_id=id
        )
        if is_json_output:
            cli_print.print_entities_as_json(evaluation)
        else:
            cli_print.log_info(
                f"Evaluation ID: {id}\n"
                f"Evaluation Name: {evaluation.display_name}\n"
                f"Evaluation Key: {evaluation.key}\n"
                f"Status: {evaluation.execution_status.value}\n"
                f"Created at: {datetime_to_str(timestamp_to_localized_datetime(evaluation.created_at))}\n"
            )
            cli_print.print_table(
                f"Tasks results for evaluation with ID '{id}'",
                evaluation.task_results,
                TASK_RESULTS_TABLE_COLUMNS,
            )
    except Exception as error:
        raise cli_exc.CLIOverviewEvaluationError(id) from error


@evaluation_app.command("download")
def _download(
    id: str = typer.Argument(
        ...,
        help=f"ID of the {PRETTY_ENTITY_NAME} for which the "
        "results will be downloaded (as a ZIP file).",
    ),
    output: Path = typer.Option(
        ...,
        "--output",
        "-o",
        help="Path to output the ZIP file.",
        callback=cli_args.check_path_not_empty,
    ),
    link_logs: bool = typer.Option(
        False,
        "--link-logs",
        help="Whether to link task result logs in the downloaded configuration.",
    ),
) -> None:
    """Download the evaluation results as a ZIP file."""
    ai_app_key = load_ai_app_key()
    client = get_client_from_env()
    ai_app = client.ai_apps.get_ai_app_by_key(ai_app_key)
    try:
        task_results_zip_file = client.evaluations.download_evaluation_result(
            app_id=ai_app.id, evaluation_id=id
        )
    except Exception as error:
        raise cli_exc.CLIExportError(
            PRETTY_ENTITY_NAME, id, identifier_type="id", output_path=output
        ) from error

    output.mkdir(exist_ok=True, parents=True)
    zip_bytes = task_results_zip_file.payload.getbuffer()
    with zipfile.ZipFile(io.BytesIO(zip_bytes), "r") as zip_ref:
        zip_ref.extractall(output)

    try:
        entities_used_in_evaluation = (
            client.evaluations.get_entities_used_in_evaluation(
                app_id=ai_app.id, evaluation_id=id
            )
        )
        user_datasets = [
            dataset
            for dataset in entities_used_in_evaluation.datasets.datasets
            if dataset.provider == DatasetProvider.USER
        ]
        dataset_output_paths = _dump_datasets_to_files(
            datasets=user_datasets,
            client=client,
            ai_app_id=ai_app.id,
            evaluation_id=id,
            output=output,
        )

        # Create a mapping from task result IDs to their corresponding log paths (if
        # requested). The downloaded `task_results` folder contains a manifest JSON,
        # which maps task result IDs to their corresponding log paths (within the
        # `task_results` folder.
        task_result_id_to_log_path = {}
        manifest_path = output / "task_results" / "manifest.json"
        if link_logs and manifest_path.exists():
            with manifest_path.open("r") as f:
                manifest = json.load(f)

            id_to_path = manifest["items"]

            for task_result in entities_used_in_evaluation.evaluation.task_results:
                if task_result.id not in id_to_path:
                    continue

                task_result_log_path = output / id_to_path[task_result.id]
                if task_result_log_path.exists():
                    task_result_id_to_log_path[task_result.id] = (
                        task_result_log_path.relative_to(output)
                    )

        cli_run_config = map_api_entities_used_in_evaluation_to_cli_run_config(
            api_entities_used_in_evaluation=entities_used_in_evaluation,
            model_adapters_map=EntityByIdentifiersMap(
                entities_used_in_evaluation.model_adapters.model_adapters
            ),
            models_map=EntityByIdentifiersMap(
                entities_used_in_evaluation.models.models
            ),
            datasets_map=EntityByIdentifiersMap(
                entities_used_in_evaluation.datasets.datasets
            ),
            tasks_map=EntityByIdentifiersMap(entities_used_in_evaluation.tasks.tasks),
            dataset_output_paths=dataset_output_paths,
            task_result_id_to_log_path=task_result_id_to_log_path,
        )
        dump_entity_to_yaml_file(
            output / f"{entities_used_in_evaluation.evaluation.key}.yaml",
            cli_run_config,
        )
    except Exception as error:
        raise cli_exc.CLIExportError(
            PRETTY_ENTITY_NAME, id, identifier_type="id", output_path=output
        ) from error

    cli_print.log_export_success_info(
        PRETTY_ENTITY_NAME, output, id, identifier_type="id"
    )


def _dump_datasets_to_files(
    datasets: list[StoredDataset],
    client: Client,
    ai_app_id: str,
    evaluation_id: str,
    output: Path,
) -> dict[str, Path]:
    """
    Dump the provided datasets to files in the provided output directory + '/datasets'.
    This function should be called so that it is guaranteed the datasets are of provider
    USER when this function is called.
    """
    exported_dataset_paths = {}
    for dataset in datasets:
        file = client.evaluations.get_dataset_data_used_in_evaluation(
            app_id=ai_app_id, evaluation_id=evaluation_id, dataset_id=dataset.id
        )
        if not isinstance(file, File):
            raise cli_exc.CLIError(
                f"Could not download data for dataset with key '{dataset.key}'."
            )
        datasets_dir = output / "datasets"
        datasets_dir.mkdir(parents=True, exist_ok=True)

        filename = f"{dataset.key}.jsonl"
        with open(datasets_dir / filename, "w", encoding="utf-8") as f:
            for line in file.payload:
                obj = json.loads(line)
                f.write(json.dumps(obj, ensure_ascii=False))
                f.write("\n")

        exported_dataset_paths[dataset.key] = (datasets_dir / filename).relative_to(
            output
        )
    return exported_dataset_paths
