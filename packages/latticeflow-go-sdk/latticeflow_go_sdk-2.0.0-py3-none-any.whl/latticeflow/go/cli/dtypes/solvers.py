from __future__ import annotations

from typing import Annotated
from typing import List
from typing import Literal
from typing import Union

from pydantic import Field

from latticeflow.go.cli.dtypes.utils import TemplateValue
from latticeflow.go.cli.dtypes.utils import UserOrLFKeyField
from latticeflow.go.models import ChatCompletionRole
from latticeflow.go.models import LFBaseModel
from latticeflow.go.models import TerminationCondition


###########
# Solvers #
###########


class SingleTurnSolverTemplate(LFBaseModel):
    type: Literal["single_turn_solver"] = Field(
        ..., description="The type of the solver."
    )
    input_builder: Union[
        GeneralInputBuilderTemplate, ChatCompletionInputBuilderTemplate
    ] = Field(..., discriminator="type")


class MultiTurnSolverTemplate(LFBaseModel):
    type: Literal["multi_turn_solver"] = Field(
        ..., description="The type of the solver."
    )
    message_builders: List[
        Annotated[
            Union[
                ChatMessageBuilderTemplate,
                GenerateTemplate,
                GenerateMessageTemplate,
                GenerateLoopTemplate,
            ],
            Field(discriminator="type"),
        ]
    ] = Field(..., min_length=1)


class GroupedSingleTurnSolverTemplate(LFBaseModel):
    type: Literal["grouped_single_turn_solver"] = Field(
        ..., description="The type of the solver."
    )
    input_builder: GeneralInputBuilderTemplate = Field(..., discriminator="type")


TaskSolverTemplate = Annotated[
    Union[
        SingleTurnSolverTemplate,
        MultiTurnSolverTemplate,
        GroupedSingleTurnSolverTemplate,
    ],
    Field(discriminator="type"),
]

##################
# Input Builders #
##################


class GeneralInputBuilderTemplate(LFBaseModel):
    type: Literal["generic"] = Field(..., description="The type of the input builder.")
    template: str | TemplateValue = Field(
        ...,
        examples=['{"question": "What is the capital of {{ sample.country }}?"}'],
        description="Jinja template that takes the sample as input and produces the input in JSON form. Use curly braces `{{ sample.attribute }}` to denote variables that will be dynamically populated for each sample in the dataset. Full Jinja is supported for the prompt.",
    )


class ChatCompletionInputBuilderTemplate(LFBaseModel):
    type: Literal["chat_completion"] = Field("chat_completion")
    input_messages: List[ChatCompletionMessage]


######################################
# Multi-Turn Solver Message Builders #
######################################


class ChatMessageBuilderTemplate(LFBaseModel):
    type: Literal["chat_message"]
    content: str | TemplateValue
    role: ChatCompletionRole | TemplateValue


class GenerateTemplate(LFBaseModel):
    """Generates a message using the evaluated model."""

    type: Literal["generate"]
    terminate_if: TerminationCondition | None = None


class GenerateMessageTemplate(LFBaseModel):
    """Generate a message using the specified model (and custom instructions, specified
    via extra input messages).
    """

    type: Literal["generate_message"]
    model_key: UserOrLFKeyField | TemplateValue
    extra_input_messages: List[ChatMessageBuilderTemplate] = Field(
        ...,
        min_length=1,
        description="Additional input messages (in addition to the existing messages) "
        "given as input to the model.",
    )
    output_role: ChatCompletionRole | TemplateValue | None = Field(
        None, description="The role of the output message."
    )
    terminate_if: TerminationCondition | None = None


class GenerateLoopTemplate(LFBaseModel):
    """Execute a loop, where at each iteration the sequence of message builders is
    executed. Each message builder can specify when to terminate the loop. There is a
    maximum number of iterations.
    """

    type: Literal["loop"]
    message_builders: List[
        Annotated[
            Union[
                ChatMessageBuilderTemplate,
                GenerateTemplate,
                GenerateMessageTemplate,
                GenerateLoopTemplate,
            ],
            Field(discriminator="type"),
        ]
    ]
    max_iterations: int | TemplateValue = Field(10, ge=0)


###############
# Other Types #
###############


class ChatCompletionMessage(LFBaseModel):
    role: ChatCompletionRole | TemplateValue = Field(
        description="The role of the message sender, can be `system`, `user`, or "
        "`assistant`."
    )
    content: str | TemplateValue = Field(
        ...,
        examples=["You are a helpful assistant."],
        description="Prompts given to the model. Use curly braces "
        "`{{ sample.attribute }}` to denote variables that will be dynamically "
        "populated for the current sample in the dataset. Full Jinja is supported for "
        "the prompt.",
    )
