from __future__ import annotations

from typing import Annotated
from typing import Literal
from typing import Union

from pydantic import Field

from latticeflow.go.cli.dtypes.utils import optional_user_or_lf_key_field
from latticeflow.go.cli.dtypes.utils import TemplateValue
from latticeflow.go.models import LFBaseModel


class _BaseMetricTemplate(LFBaseModel):
    key: str | None = optional_user_or_lf_key_field


class PythonMetricTemplate(_BaseMetricTemplate):
    type: Literal["python"] = Field(..., description="The type of the metric.")
    compute_metrics_snippet: str | TemplateValue = Field(
        description="The Python snippet that defines a "
        "`compute_metrics(scores: dict[str, Any]) -> dict[str, int \| float]` function "
        "that computes the metric values.",
        title="The compute_metrics snippet",
        examples=[
            """
def compute_metrics(scores: dict[str, Any]) -> dict[str, int | float]:
    total = sum(score['is_correct'] for score in scores)
    return {'accuracy': total / len(scores)}
"""
        ],
    )


class BinaryClassificationMetricTemplate(_BaseMetricTemplate):
    type: Literal["binary-classification"] = Field(
        ..., description="The type of the metric."
    )
    field_gt: str | TemplateValue = Field(
        description="The field in the scores containing the ground-truth answer.",
        title="Ground-Truth Field",
    )
    field_pred: str | TemplateValue = Field(
        description="The field in the scores containing the predicted answer.",
        title="Prediction Field",
    )
    positive_answer: str | TemplateValue = Field(
        description="The answer treated as a positive. The answer field is converted to a string "
        "before comparison."
    )
    negative_answer: str | TemplateValue = Field(
        description="The answer treated as a negative. The answer field is converted to a string "
        "before comparison."
    )


class MulticlassClassificationMetricTemplate(_BaseMetricTemplate):
    type: Literal["multiclass-classification"] = Field(
        ..., description="The type of the metric."
    )
    field_gt: str | TemplateValue = Field(
        description="The field in the scores containing the ground-truth answer.",
        title="Ground-Truth Field",
    )
    field_pred: str | TemplateValue = Field(
        description="The field in the scores containing the predicted answer.",
        title="Prediction Field",
    )


class MeanMetricTemplate(_BaseMetricTemplate):
    type: Literal["mean"] = Field(..., description="The type of the metric.")
    field: str | TemplateValue = Field(
        description="The field over which to compute the mean.", title="Field"
    )
    name: str | TemplateValue | None = Field(
        default=None,
        description="The name given to the metric value. If not specified, it is `{field}_mean`",
    )


class MaxMetricTemplate(_BaseMetricTemplate):
    type: Literal["max"] = Field(..., description="The type of the metric.")
    field: str | TemplateValue = Field(
        description="The field over which to compute the max.", title="Field"
    )
    name: str | TemplateValue | None = Field(
        default=None,
        description="The name given to the metric value. If not specified, it is `{field}_max`",
    )


class MinMetricTemplate(_BaseMetricTemplate):
    type: Literal["min"] = Field(..., description="The type of the metric.")
    field: str | TemplateValue = Field(
        description="The field over which to compute the min.", title="Field"
    )
    name: str | TemplateValue | None = Field(
        default=None,
        description="The name given to the metric value. If not specified, it is `{field}_min`",
    )


class StdDevMetricTemplate(_BaseMetricTemplate):
    type: Literal["std_dev"] = Field(..., description="The type of the metric.")
    field: str | TemplateValue = Field(
        description="The field over which to compute the standard deviation.",
        title="Field",
    )
    name: str | TemplateValue | None = Field(
        default=None,
        description="The name given to the metric value. If not specified, it is `{field}_std_dev`",
    )


class FrequencyMetricTemplate(_BaseMetricTemplate):
    type: Literal["frequency"] = Field(..., description="The type of the metric.")
    field: str | TemplateValue = Field(
        description="The field over which to compute the relative frequency.",
        title="Field",
    )


class RecallMetricTemplate(_BaseMetricTemplate):
    type: Literal["recall"] = Field("recall")
    num_true_positives_field: str = Field(
        description="The field that contains the number of true positives.",
        title="Number of True Positives Field",
    )
    num_false_negatives_field: str = Field(
        description="The field that contains the number of false negatives.",
        title="Number of False Negatives Field",
    )
    name: str | None = Field(
        default=None,
        description="The name given to the metric value. If not specified, it is `recall`.",
    )


class PrecisionMetricTemplate(_BaseMetricTemplate):
    type: Literal["precision"] = Field("precision")
    num_true_positives_field: str = Field(
        description="The field that contains the number of true positives.",
        title="Number of True Positives Field",
    )
    num_false_positives_field: str = Field(
        description="The field that contains the number of false positives.",
        title="Number of False Positives Field",
    )
    name: str | None = Field(
        default=None,
        description="The name given to the metric value. If not specified, it is `precision`.",
    )


class F1ScoreMetricTemplate(_BaseMetricTemplate):
    type: Literal["f1_score"] = Field("f1_score")
    num_true_positives_field: str = Field(
        description="The field that contains the number of true positives.",
        title="Number of True Positives Field",
    )
    num_false_positives_field: str = Field(
        description="The field that contains the number of false positives.",
        title="Number of False Positives Field",
    )
    num_false_negatives_field: str = Field(
        description="The field that contains the number of false negatives.",
        title="Number of False Negatives Field",
    )
    name: str | None = Field(
        default=None,
        description="The name given to the metric value. If not specified, it is `f1_score`.",
    )


TaskMetricTemplate = Annotated[
    Union[
        PythonMetricTemplate,
        BinaryClassificationMetricTemplate,
        MulticlassClassificationMetricTemplate,
        MeanMetricTemplate,
        MaxMetricTemplate,
        MinMetricTemplate,
        StdDevMetricTemplate,
        FrequencyMetricTemplate,
        RecallMetricTemplate,
        PrecisionMetricTemplate,
        F1ScoreMetricTemplate,
    ],
    Field(discriminator="type"),
]
