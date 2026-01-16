from __future__ import annotations

from pathlib import Path
from typing import Annotated
from typing import Any
from typing import Dict
from typing import List
from typing import Literal
from typing import Union

from pydantic import Field
from pydantic import field_validator

from latticeflow.go.cli.dtypes.scorers import TaskScorerTemplate
from latticeflow.go.cli.dtypes.solvers import TaskSolverTemplate
from latticeflow.go.cli.dtypes.utils import optional_user_or_lf_key_field
from latticeflow.go.cli.dtypes.utils import user_or_lf_key_field
from latticeflow.go.cli.dtypes.utils import UserKey
from latticeflow.go.cli.dtypes.utils import UserOrLFKey
from latticeflow.go.cli.dtypes.utils import UserOrProviderKey
from latticeflow.go.models import AIAppKeyInformation
from latticeflow.go.models import BooleanParameterSpec
from latticeflow.go.models import CategoricalParameterSpec
from latticeflow.go.models import DatasetColumnParameterSpec
from latticeflow.go.models import DatasetGenerationRequest
from latticeflow.go.models import DatasetGeneratorDataSourceTemplate
from latticeflow.go.models import DatasetGeneratorSynthesizerTemplate
from latticeflow.go.models import DatasetParameterSpec
from latticeflow.go.models import EvaluatedEntityType
from latticeflow.go.models import FloatParameterSpec
from latticeflow.go.models import IntParameterSpec
from latticeflow.go.models import LFBaseModel
from latticeflow.go.models import ListParameterSpec
from latticeflow.go.models import MLTask
from latticeflow.go.models import Mode
from latticeflow.go.models import ModelAdapterCodeSnippet
from latticeflow.go.models import ModelAdapterProvider
from latticeflow.go.models import ModelCustomConnectionConfig
from latticeflow.go.models import ModelParameterSpec
from latticeflow.go.models import ModelProviderConnectionConfig
from latticeflow.go.models import StringParameterSpec


class ResolvedData(LFBaseModel):
    path: Path
    data: Any


class EnvVars(LFBaseModel):
    base_url: str
    api_key: str
    verify_ssl: bool
    timeout: float | None


ParameterSpecType = Union[
    FloatParameterSpec,
    IntParameterSpec,
    BooleanParameterSpec,
    StringParameterSpec,
    ModelParameterSpec,
    DatasetParameterSpec,
    DatasetColumnParameterSpec,
    ListParameterSpec,
    CategoricalParameterSpec,
]
ConfigSpecType = List[ParameterSpecType]


class _BaseCLIModel(LFBaseModel):
    display_name: str = Field(
        ..., description="The model's name displayed to the user.", min_length=1
    )
    description: str | None = Field(None, description="Short description of the model.")
    rate_limit: int | None = Field(
        None, description="The maximum allowed number (integer) of requests per minute."
    )
    task: MLTask = Field(
        MLTask.CHAT_COMPLETION,
        description="The ML task of the model. Supported tasks are: `chat_completion` "
        "and `custom`. Default is: `chat_completion`.",
    )
    adapter: UserOrLFKey = Field(
        UserOrLFKey(key="latticeflow$identity"),
        description="The model adapter responsible for converting the endpoint "
        "inputs and outputs into a standardized format.",
    )


class CLICreateModel(_BaseCLIModel, UserOrProviderKey):
    config: ModelCustomConnectionConfig = Field(
        ...,
        discriminator="connection_type",
        description="Model connection configuration as a custom endpoint.",
    )


class CLIExportModel(_BaseCLIModel, UserOrLFKey):
    config: Union[ModelCustomConnectionConfig, ModelProviderConnectionConfig] = Field(
        ...,
        discriminator="connection_type",
        description="Model connection configuration which can be either "
        "a well-known model provider or a custom endpoint.",
    )


class _BaseCLIModelAdapter(LFBaseModel):
    display_name: str = Field(
        ..., description="The model adapter's name displayed to the user.", min_length=1
    )
    description: str | None = Field(
        None, description="Short description of the model adapter."
    )
    long_description: str | None = Field(
        None,
        description="Long description of the model adapter. Supports Markdown "
        "formatting.",
    )
    provider: ModelAdapterProvider = Field(
        ModelAdapterProvider.USER,
        description="Provider of the model adapter. Supported values are `user` and "
        "`latticeflow`. Default is `user`.",
    )
    task: MLTask = Field(
        MLTask.CHAT_COMPLETION,
        description="The ML task of the model. Supported tasks are: `chat_completion` "
        "and `custom`. Default is: `chat_completion`.",
    )
    process_input: ModelAdapterCodeSnippet | None = Field(
        None,
        description="The transform of the model inputs in AI GO! format into the body "
        "of the HTTP request.",
    )
    process_output: ModelAdapterCodeSnippet | None = Field(
        None,
        description="The transform of the model's HTTP response body into the AI GO! "
        "format.",
    )


class CLICreateModelAdapter(_BaseCLIModelAdapter, UserKey):
    pass


class CLIExportModelAdapter(_BaseCLIModelAdapter, UserOrLFKey):
    pass


class _BaseCLITask(LFBaseModel):
    display_name: str = Field(
        ..., min_length=1, description="The task's name displayed to the user."
    )
    description: str = Field(..., description="Short description of the task.")
    long_description: str | None = Field(
        None, description="Long description of the task. Supports Markdown formatting."
    )
    tasks: List[MLTask] = Field(
        [], description="ML tasks supported by the task. Default is an empty list."
    )
    evaluated_entity_type: EvaluatedEntityType = Field(
        EvaluatedEntityType.MODEL,
        description="Type of entity being evaluated. Supported values are: `dataset` "
        "and `model`. Default is `model`.",
    )
    config_spec: ConfigSpecType = Field(
        [], description="Configuration specification of the task."
    )
    definition: Union[
        CLIDeclarativeTaskDefinitionTemplate, CLIPredefinedTaskDefinition
    ] = Field(..., discriminator="type", description="Definition of the task.")

    @field_validator("definition", mode="before")
    @classmethod
    def _default_discriminator(cls, field_value: Any) -> dict | Any:
        if isinstance(field_value, dict) and "type" not in field_value:
            field_value = {**field_value, "type": "declarative_task"}
        return field_value


class CLICreateTask(_BaseCLITask, UserKey):
    tags: list[str] = Field(
        [],
        description=(
            "Tags to be associated with the task. If a tag does not exist,"
            " it will be created with a random color."
        ),
    )


class CLIExportTask(_BaseCLITask, UserOrLFKey):
    tags: list[str] = Field(..., description="Tags associated with the task.")


class CLIPredefinedTaskDefinition(LFBaseModel):
    type: Literal["predefined"] = Field(
        ..., description="Type of the task definition which is set to `predefined`."
    )


class CLIDeclarativeTaskDefinitionTemplate(LFBaseModel):
    # The default value here is only relevant for the docs generation.
    # `_default_discriminator` makes "declarative_task" the default when not specified.
    # Putting the default value here causes it to be shown as an optional field, which
    # reflects this behavior.
    type: Literal["declarative_task"] = Field(
        "declarative_task",
        description="Type of the task definition which is set to `declarative_task`.",
    )
    dataset: CLITaskDatasetTemplate = Field(
        ..., description="Dataset used by the task."
    )
    solver: TaskSolverTemplate = Field(..., description="Solver used by the task.")
    scorers: List[Annotated[TaskScorerTemplate, Field(discriminator="type")]] = Field(
        ..., description="List of scorers used by the task."
    )


class CLITaskDatasetTemplate(LFBaseModel):
    key: str = Field(..., description="Key of the dataset to be used for the task.")
    fast_subset_size: Union[int, str] = Field(
        200, description="Size of the fast subset. Default is 200."
    )


class _BaseCLIAIApp(UserKey):
    display_name: str = Field(
        ..., description="The AI app's name displayed to the user.", min_length=1
    )
    description: str | None = Field(
        None, description="Short text description of the AI app."
    )
    long_description: str | None = Field(
        None,
        description="Long description of the AI app. Supports Markdown formatting.",
    )
    key_info: AIAppKeyInformation | None = Field(
        None, description="Key information for the AI application."
    )


class CLICreateAIApp(_BaseCLIAIApp):
    tags: list[str] = Field(
        [],
        description=(
            "Tags to be associated with the AI app. If a tag does not exist,"
            " it will be created with a random color."
        ),
    )


class CLIExportAIApp(_BaseCLIAIApp):
    tags: List[str] = Field(..., description="Tags associated with the AI app.")


class _BaseCLIDatasetGenerator(LFBaseModel):
    display_name: str = Field(
        ...,
        min_length=1,
        description="The dataset generator's name displayed to the user.",
    )
    description: str = Field(
        ..., description="Short description of the dataset generator."
    )
    long_description: str | None = Field(
        None,
        description="Long description of the dataset generator. Supports "
        "Markdown formatting.",
    )
    config_spec: ConfigSpecType = Field(
        [], description="Configuration specification for the dataset generator."
    )
    definition: CLIDeclarativeDatasetGeneratorDefinitionTemplate = Field(
        ...,
        description="Declarative dataset generator definition. It must "
        "be of type `CLIDeclarativeDatasetGeneratorDefinitionTemplate`.",
    )

    @field_validator("definition", mode="before")
    @classmethod
    def _default_discriminator(cls, field_value: Any) -> dict | Any:
        if isinstance(field_value, dict) and "type" not in field_value:
            field_value = {**field_value, "type": "declarative_dataset_generator"}
        return field_value


class CLICreateDatasetGenerator(_BaseCLIDatasetGenerator, UserKey):
    pass


class CLIExportDatasetGenerator(_BaseCLIDatasetGenerator, UserOrLFKey):
    pass


class CLIDeclarativeDatasetGeneratorDefinitionTemplate(LFBaseModel):
    # The default value here is only relevant for the docs generation.
    # `_default_discriminator` makes "declarative_dataset_generator" the default when
    # not specified. Putting the default value here causes it to be shown as an optional
    # field, which reflects this behavior.
    type: Literal["declarative_dataset_generator"] = Field(
        "declarative_dataset_generator",
        description="Refers to user-defined dataset generators.",
    )
    data_source: DatasetGeneratorDataSourceTemplate = Field(
        ..., description="Data source used by the dataset generator."
    )
    synthesizer: DatasetGeneratorSynthesizerTemplate = Field(
        ..., description="Data synthesizer configuration by the dataset generator."
    )


class CLIDatasetGeneratorSpecification(DatasetGenerationRequest):
    dataset_generator_key: str = Field(
        ..., description="Key of the dataset generator to use."
    )


class _BaseCLIDataset(LFBaseModel):
    display_name: str = Field(
        ..., description="The dataset's name displayed to the user.", min_length=1
    )
    description: str | None = Field(
        None, description="Short description of the dataset."
    )
    file_path: Path | None = Field(
        None,
        description="File containing the dataset's data. "
        "Supported formats are CSV and JSONL. Required if dataset generator "
        "is not used.",
    )
    generator_specification: CLIDatasetGeneratorSpecification | None = Field(
        None,
        description="Config for the dataset generator that will be used to generate "
        "the dataset. Required if the data file is not provided.",
    )


class CLICreateDataset(_BaseCLIDataset, UserKey):
    pass


class CLIExportDataset(_BaseCLIDataset, UserOrLFKey):
    pass


class _BaseCLIEvaluation(LFBaseModel):
    display_name: str = Field(
        ..., min_length=1, description="The evaluation's name displayed to the user."
    )
    mode: Mode = Field(
        ...,
        description="The mode of evaluation to be performed. Supported modes are "
        "'fast', 'debug' and `full`.",
    )
    task_specifications: List[CLITaskSpecification] = Field(
        ..., description="List of task specifications for the evaluation."
    )


class CLICreateEvaluation(_BaseCLIEvaluation, UserKey):
    tags: list[str] = Field(
        [],
        description=(
            "Tags to be associated with the evaluation. If a tag does not exist,"
            " it will be created with a random color."
        ),
    )


class CLIExportEvaluation(_BaseCLIEvaluation, UserOrLFKey):
    tags: list[str] = Field(..., description="Tags associated with the evaluation.")


class CLITaskSpecification(LFBaseModel):
    task_key: str = user_or_lf_key_field
    task_config: Dict[str, Any] = Field(
        {},
        description="Configuration for the specified task. Must match the task's config spec.",
    )
    model_key: str | None = optional_user_or_lf_key_field
    dataset_key: str | None = optional_user_or_lf_key_field
    display_name: str | None = Field(
        None,
        description="The task specification's name displayed to the user.",
        min_length=1,
    )
    task_result_log_path: str | None = Field(
        None, description="Path to the task result log file."
    )


class CLIProviderAndModelKey(LFBaseModel):
    provider_and_model_key: str = Field(
        alias="$provider",
        description=(
            "A string representing a third-party provider and model"
            " key in the format `$provider: <provider>/<model_key>`."
        ),
    )


class CLICreateRunConfig(LFBaseModel):
    model_adapters: list[CLICreateModelAdapter] = Field(
        [],
        description=(
            "List of all model adapters to be created/updated before running the evaluation."
        ),
    )
    models: list[CLICreateModel | CLIProviderAndModelKey] = Field(
        [],
        description=(
            "List of all models to be created/updated before running the evaluation."
            " Can be either a full model definition or a string representing a third-party"
            " provider and model key in the format `$provider: <provider>/<model_key>`."
        ),
    )

    @field_validator("models", mode="before")
    @classmethod
    def reject_plain_strings(cls, value: Any) -> Any:
        if not isinstance(value, list):
            return value

        for i, item in enumerate(value):
            if isinstance(item, str):
                raise ValueError(
                    f"models[{i}]: plain strings are not allowed. "
                    "If you want a provider model, use: $provider: '<provider>/<model_key>'."
                    " Otherwise specify the full model definition either by laying out all fields"
                    " or using a reference file (e.g., `$ref: 'path/to/model.yaml'`)."
                )
        return value

    dataset_generators: list[CLICreateDatasetGenerator] = Field(
        [],
        description=(
            "List of all dataset generators to be created/updated before running the evaluation."
        ),
    )
    datasets: list[CLICreateDataset] = Field(
        [],
        description=(
            "List of all datasets to be created/updated before running the evaluation."
        ),
    )
    tasks: list[CLICreateTask] = Field(
        [],
        description=(
            "List of all tasks to be created/updated before running the evaluation."
        ),
    )
    evaluation: CLICreateEvaluation | None = Field(
        None, description=("The evaluation to be run.")
    )


class CLIExportRunConfig(LFBaseModel):
    model_adapters: list[CLIExportModelAdapter] = Field(
        [],
        description=(
            "List of all model adapters to be created/updated before running the evaluation."
        ),
    )
    models: list[CLIExportModel | CLIProviderAndModelKey] = Field(
        [],
        description=(
            "List of all models to be created/updated before running the evaluation."
            " Can be either a full model definition or a string representing a third-party"
            " provider and model key in the format `$provider: <provider>/<model_key>`."
        ),
    )
    dataset_generators: list[CLIExportDatasetGenerator] = Field(
        [],
        description=(
            "List of all dataset generators to be created/updated before running the evaluation."
        ),
    )
    datasets: list[CLIExportDataset] = Field(
        [],
        description=(
            "List of all datasets to be created/updated before running the evaluation."
        ),
    )
    tasks: list[CLIExportTask] = Field(
        [],
        description=(
            "List of all tasks to be created/updated before running the evaluation."
        ),
    )
    evaluation: CLIExportEvaluation | None = Field(
        None, description=("The evaluation to be run.")
    )
