from __future__ import annotations

from typing import Annotated
from typing import Any
from typing import Literal
from typing import Union

from pydantic import Field

from latticeflow.go.cli.dtypes.utils import TemplateValue
from latticeflow.go.cli.dtypes.utils import UserOrLFKeyField
from latticeflow.go.models import LFBaseModel


class EmptySynthesizerTemplate(LFBaseModel):
    type: Literal["empty"] = Field(..., description="The type of the synthesizer.")


class LLMSynthesizerTemplate(LFBaseModel):
    type: Literal["llm"] = Field(..., description="The type of the synthesizer.")
    model_key: UserOrLFKeyField | TemplateValue | None = Field(
        None,
        description="The key of the chat completion model to be used as a synthesizer.",
    )
    system_prompt_template: str | TemplateValue = Field(
        description="The Jinja template used to create the system prompt. The source "
        "sample is available in the Jinja context as ``source``."
    )
    user_prompt_template: str | TemplateValue = Field(
        description="The Jinja template used to create the user prompt. The source "
        "sample is available in the Jinja context as ``source``."
    )
    system_prompt_format_instructions: str | TemplateValue | None = Field(
        None,
        description="Format instructions appended to the system prompt. If not "
        "provided, they will be derived from the ``sample_properties``. When parsing "
        "the model output, it is expected to be valid JSON contained in "
        "<output_json>...</output_json> tags, meaning that the "
        "format instructions should instruct the model to follow this format.",
    )
    sample_properties: dict[str, Any] = Field(
        description="The 'properties' field of the JSON schema for the output samples."
    )
    use_structured_outputs: bool | None = Field(
        None,
        description="Whether to use structured outputs. If not specified, structured "
        "outputs are used if and only if the default model is used. It is recommended "
        "to enable structured outputs if the custom model supports it.",
    )


class QuestionAnsweringSynthesizerTemplate(LFBaseModel):
    type: Literal["question_answering"] = Field(
        ..., description="The type of the synthesizer."
    )
    model_key: UserOrLFKeyField | TemplateValue | None = Field(
        None,
        description="The key of the chat completion model to be used as a synthesizer.",
    )
    qa_type: Literal["multiple_choice", "open_ended"] = Field(
        description="The type of question answering synthesizer. Supports "
        "'multiple_choice' and 'open_ended'."
    )
    content_column: str | TemplateValue | None = Field(
        default="text",
        description="The name of the text content column in the dataset. "
        "This defines the source text when generating QA dataset. Defaults to 'text'.",
    )
    title_column: str | TemplateValue | None = Field(
        default="document_title",
        description="The name of the title column in the dataset. "
        "This is supplementary information and not required for generating QA dataset. "
        "Defaults to 'document_title'.",
    )
    summary_column: str | TemplateValue | None = Field(
        default="document_summary",
        description="The name of the summary column in the dataset. "
        "This is supplementary information and not required for generating QA dataset. "
        "Defaults to 'document_summary'.",
    )
    system_prompt: str | TemplateValue | None = Field(
        None,
        description="The system prompt to use. If not provided, a default prompt will be used.",
    )
    user_prompt: str | TemplateValue | None = Field(
        None,
        description="The user prompt to use. If not provided, a default prompt will be used.",
    )
    additional_instructions: str | TemplateValue | None = Field(
        # If set to 'none' or left as None, this will be treated as an empty string in
        # the template, which is acceptable.
        default="none",
        description="Additional instructions to provide to the generator model.",
        title="Additional Instructions",
    )


class TemplateSynthesizerTemplate(LFBaseModel):
    type: Literal["template"] = Field(..., description="The type of the synthesizer.")
    template: str | TemplateValue | list[str | TemplateValue] = Field(
        description="The template string used for synthesis."
    )
    fields: dict[str, list[Any]] = Field(
        description="A dictionary where keys are placeholder names in the template "
        "string, and values are lists of possible values for those placeholders."
    )


class PythonSynthesizerTemplate(LFBaseModel):
    type: Literal["python"] = Field(..., description="The type of the synthesizer.")
    synthesize_snippet: str | TemplateValue = Field(
        description="""The Python snippet defining how output samples are generated \
from a single source sample. It must define a `synthesize` function, with the \
following API:

```
def synthesize(source: dict[str, Any]) -> list[dict[str, Any]]:
```

where:
- `source` is a dictionary representing a single source sample.
- The return value is a list of dictionaries, each representing an output sample.
""",
        title="The synthesize snippet",
    )


DatasetGeneratorSynthesizerTemplate = Annotated[
    Union[
        EmptySynthesizerTemplate,
        LLMSynthesizerTemplate,
        QuestionAnsweringSynthesizerTemplate,
        TemplateSynthesizerTemplate,
        PythonSynthesizerTemplate,
    ],
    Field(discriminator="type"),
]
