from __future__ import annotations

from typing import Annotated
from typing import Literal
from typing import Union

from pydantic import Field

from latticeflow.go.cli.dtypes.utils import TemplateValue
from latticeflow.go.cli.dtypes.utils import UserOrLFKeyField
from latticeflow.go.models import LFBaseModel


class EmptyDataSourceTemplate(LFBaseModel):
    type: Literal["empty"] = Field(..., description="The type of the data source.")
    num_samples: int | TemplateValue = Field(
        1, ge=1, description="The number of (empty) source samples returned."
    )


class DatasetSampleDataSourceTemplate(LFBaseModel):
    type: Literal["dataset_samples"] = Field(
        ..., description="The type of the data source."
    )
    dataset_key: UserOrLFKeyField | TemplateValue = Field(
        description="The ID of the dataset whose samples should be used."
    )


class DatasetSampleCombinationsDataSourceTemplate(LFBaseModel):
    type: Literal["dataset_sample_combinations"] = Field(
        ..., description="The type of the data source."
    )
    dataset_keys: list[UserOrLFKeyField | TemplateValue] = Field(
        description="The datasets whose samples should be used to generate combinations."
    )


DatasetGeneratorDataSourceTemplate = Annotated[
    Union[
        EmptyDataSourceTemplate,
        DatasetSampleDataSourceTemplate,
        DatasetSampleCombinationsDataSourceTemplate,
    ],
    Field(discriminator="type"),
]
