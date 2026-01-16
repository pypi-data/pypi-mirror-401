from __future__ import annotations

from typing import Annotated
from typing import Literal
from typing import Union

from pydantic import Field

from latticeflow.go.cli.dtypes.metrics import TaskMetricTemplate
from latticeflow.go.cli.dtypes.utils import optional_user_key_field
from latticeflow.go.cli.dtypes.utils import TemplateValue
from latticeflow.go.cli.dtypes.utils import UserOrLFKeyField
from latticeflow.go.models import LFBaseModel


# TODO: Should we remove defaults here and instead make it optional?


class _BaseScorerTemplate(LFBaseModel):
    key: str | None = optional_user_key_field
    metrics: list[Annotated[TaskMetricTemplate, Field(discriminator="type")]] | None = (
        Field(
            None,
            description="The metrics associated with this scorer, which will produce per-task metrics.",
        )
    )


class BLEUScorerTemplate(_BaseScorerTemplate):
    type: Literal["bleu"] = Field(..., description="The type of the scorer.")
    ground_truth: str | TemplateValue = Field(
        description="""Jinja string used to specify the ground-truth. Use curly braces
        `{{ sample.attribute }}` to denote variables that will be dynamically
        populated for each sample in the dataset. Full Jinja is supported for the
        prompt. The BLEU score between the model's raw output and this ground-truth
        string is used to the score a sample. Available variables in the Jinja context:
        (1) sample: The sample dictionary, i.e. the current row of the dataset in
        dictionary format (with a key for each dataset column)""",
        title="Ground Truth",
        json_schema_extra={"string_kind": "jinja"},
        examples=["{{ sample.country }}", "A constant"],
    )


class StringEqualsScorerTemplate(_BaseScorerTemplate):
    type: Literal["string_equals"] = Field(..., description="The type of the scorer.")
    ground_truth: str | TemplateValue = Field(
        description="""Jinja string used to specify the ground-truth. Use curly braces
        `{{ sample.attribute }}` to denote variables that will be dynamically
        populated for each sample in the dataset. Full Jinja is supported for the
        prompt. The model's raw output is compared to this ground-truth string when
        evaluating a sample. Available variables in the Jinja context:
        (1) sample: The sample dictionary, i.e. the current row of the dataset in
        dictionary format (with a key for each dataset column)""",
        title="Ground Truth",
        json_schema_extra={"string_kind": "jinja"},
        examples=["{{ sample.country }}", "YES"],
    )


class StringEqualsMCQAScorerTemplate(_BaseScorerTemplate):
    type: Literal["string_equals_mcqa"] = Field(
        ..., description="The type of the scorer."
    )
    ground_truth_choice_field: str | TemplateValue = Field(
        description="Column in the dataset that contains the ground truth choice. "
        "The first character of the model's raw output is string matched "
        "(string equality) against this value to evaluate a sample.",
        title="Ground truth choice field",
        json_schema_extra={"allowed_values_source": "dataset_column"},
    )
    choices_field: str | TemplateValue = Field(
        description="Column in the dataset that contains the ground truth choices e.g. "
        "a column containing `['A', 'B', 'C', 'D']`.",
        title="Choices field",
        json_schema_extra={"allowed_values_source": "dataset_column"},
    )


class ModelAsAJudgeClassifierScorerTemplate(_BaseScorerTemplate):
    type: Literal["model_as_a_judge_classifier"] = Field(
        ..., description="The type of the scorer."
    )
    model_key: UserOrLFKeyField | TemplateValue = Field(
        description="The model to be used as the judge.",
        title="Model",
        json_schema_extra={"allowed_values_source": "available_models"},
    )

    system_prompt: str | TemplateValue = Field(
        description="The system prompt given to the judge model. "
        "Use curly braces `{{ sample.attribute }}` to denote variables that will be "
        "dynamically populated for each sample in the dataset. "
        "Use curly braces `{{ input_prompt }}` to access the output of the model being judged."
        "Full Jinja is supported for the prompt. Available variables in the Jinja context:"
        "(1) sample: The sample dictionary, i.e. the current row of the dataset in dictionary format (with a key for each dataset column)"
        "(2) input_prompt: The output of the model being judged.",
        default="You are a helpful assistant and will be used to judge the output of another model.",
        title="System prompt",
        json_schema_extra={"string_kind": "jinja"},
    )
    user_prompt: str | TemplateValue = Field(
        description="User prompt given to the judge model. "
        "Use curly braces `{{ sample.attribute }}` to denote variables that will be "
        "dynamically populated for each sample in the dataset. "
        "Use curly braces `{{ input_prompt }}` to access the output of the model being judged."
        "Full Jinja is supported for the prompt. Available variables in the Jinja context:"
        "(1) sample: The sample dictionary, i.e. the current row of the dataset in dictionary format (with a key for each dataset column)"
        "(2) input_prompt: The output of the model being judged.",
        default="Classify whether the capital for a given country matches the correct capital:\n"
        "Q: What is the capital of {{ sample.country }}?\n"
        "Generated answer: {{ input_prompt }}\n"
        "Correct answer: {{ sample.capital }}\n"
        "Is the generated answer correct? Respond with class labels 'yes' or 'no'.",
        title="User prompt",
        json_schema_extra={"string_kind": "jinja"},
    )

    correct_labels: list[str | TemplateValue] = Field(
        description="The list of labels predicted by the judge that are considered correct.",
        title="Correct labels",
    )
    incorrect_labels: list[str | TemplateValue] = Field(
        description="The list of labels predicted by the judge that are considered incorrect.",
        title="Incorrect labels",
    )
    use_structured_outputs: bool = Field(
        description="Whether to use structured outputs. It is recommended to enable "
        "this if the model supports it.",
        default=False,
    )


class ModelAsAJudgeScorerScorerTemplate(_BaseScorerTemplate):
    type: Literal["model_as_a_judge_scorer"] = Field(
        ..., description="The type of the scorer."
    )
    model_key: UserOrLFKeyField | TemplateValue = Field(
        description="The model to be used as the judge.",
        title="Model",
        json_schema_extra={"allowed_values_source": "available_models"},
    )
    system_prompt: str | TemplateValue = Field(
        description="The system prompt given to the judge model. "
        "Use curly braces `{{ sample.attribute }}` to denote variables that will be "
        "dynamically populated for each sample in the dataset. "
        "Use curly braces `{{ input_prompt }}` to access the output of the model being "
        "judged. Full Jinja is supported for the prompt. Available variables in the "
        "Jinja context:"
        "(1) sample: The sample dictionary, i.e. the current row of the dataset in "
        "dictionary format (with a key for each dataset column)"
        "(2) input_prompt: The output of the model being judged.",
        default="You are a helpful assistant and will be used to judge the output of "
        "another model.",
        title="System prompt",
        json_schema_extra={"string_kind": "jinja"},
    )
    user_prompt: str | TemplateValue = Field(
        description="User prompt given to the judge model. "
        "Use curly braces `{{ sample.attribute }}` to denote variables that will be "
        "dynamically populated for each sample in the dataset. "
        "Use curly braces `{{ input_prompt }}` to access the output of the model being "
        "judged. Full Jinja is supported for the prompt. Available variables in the "
        "Jinja context:"
        "(1) sample: The sample dictionary, i.e. the current row of the dataset in "
        "dictionary format (with a key for each dataset column)"
        "(2) input_prompt: The output of the model being judged.",
        default="Score how 'grounded' the response is given the context.\n"
        "The score should be between 0.0 (hallucination) to 1.0 (well grounded in the context):\n"
        "Context: {{ sample.context }}\n"
        "Generated response: {{ input_prompt }}",
        title="User prompt",
        json_schema_extra={"string_kind": "jinja"},
    )
    score_min: float | TemplateValue = Field(
        description="The minimum score that the judge model can predict.",
        title="Minimum score value",
        default=0.0,
    )
    score_max: float | TemplateValue = Field(
        description="The maximum score that the judge model can predict.",
        title="Maximum score value",
        default=1.0,
    )
    use_structured_outputs: bool = Field(
        description="Whether to use structured outputs. It is recommended to enable "
        "this if the model supports it.",
        default=False,
    )


class PythonScorerScorerTemplate(_BaseScorerTemplate):
    type: Literal["python"] = Field(..., description="The type of the scorer.")
    compute_scores_snippet: str | TemplateValue = Field(
        description="The Python code snippet that defines a `def compute_scores(sample: dict[str, Any], model_input: dict[str, Any], model_output: dict[str, Any]) -> dict[str, Any]` function that computes scores for the sample.",
        title="The compute_scores snippet",
        examples=[
            """def compute_scores(sample: dict, solver_output) -> dict:
    # Given the dataset row ('sample'), the model input and the model output, produce
    # a dictionary of scores, containing the evaluation of the model output.
    # Example (geography evaluator):
    # 'What is the capital of {{ sample.country }}?'


    # If system prompt is set, the user prompt containing the question is at index 1:
    question = model_input['messages'][1]['content']
    # If system prompt is NOT set, comment the above and uncomment the line below
    # as the user prompt containing the question is at index 0:
    # question = model_input['messages'][0]['content']

    model_completion = solver_output.output['choices'][0]['message']['content']
    return {
        'country': sample['country'],
        'capital': sample['capital'],
        'question': question,
        'model_completion': model_completion,
        'is_correct': model_completion.lower().strip() == sample['capital'].lower()
    }"""
        ],
        json_schema_extra={"string_kind": "python"},
    )


RAGCheckerScores = Literal[
    "recall",
    "precision",
    "f1_score",
    "claim_recall",
    "context_precision",
    "context_utilization",
    "noise_sensitivity_in_relevant",
    "noise_sensitivity_in_irrelevant",
    "hallucination",
    "self_knowledge",
    "faithfulness",
]


class RAGCheckerScorerTemplate(_BaseScorerTemplate):
    type: Literal["rag_checker"] = Field(..., description="The type of the scorer.")
    query_column: str | TemplateValue = Field(
        default="query",
        description="The name of the sample column containing the query.",
        title="Query Column",
    )
    target_column: str | TemplateValue = Field(
        default="target",
        description="The name of the sample column containing the target.",
        title="Target Column",
    )
    judge_model_key: UserOrLFKeyField | TemplateValue | None = Field(
        default=None,
        description="The registered chat completion model to be used as a claim extractor and checker. If no model is specified, GPT-4 will be used by default.",
        title="Judge Model",
        json_schema_extra={"allowed_values_source": "available_models"},
    )
    scores_to_compute: list[RAGCheckerScores] | None = Field(
        default=None,
        description="The scores to compute. If set to None, all scores are computed.",
        title="Scores to Compute",
    )


TaskScorerTemplate = Annotated[
    Union[
        BLEUScorerTemplate,
        StringEqualsScorerTemplate,
        StringEqualsMCQAScorerTemplate,
        ModelAsAJudgeClassifierScorerTemplate,
        ModelAsAJudgeScorerScorerTemplate,
        PythonScorerScorerTemplate,
        RAGCheckerScorerTemplate,
    ],
    Field(discriminator="type"),
]
