from __future__ import annotations

from typing import Annotated

from pydantic import Field

from latticeflow.go.models import LFBaseModel


user_or_provider_key_field = Field(
    ...,
    max_length=250,
    min_length=1,
    pattern="^((local|together|zenguard|gemini|openai|fireworks|sambanova|anthropic|novita)\\$)?[a-z0-9_-]+$",
    description="Key: 1-250 chars, allowed: 'a-z 0-9 _ -'.",
)
user_key_field = Field(
    ...,
    max_length=250,
    min_length=1,
    pattern="^[a-z0-9_\\-]+$",
    description="Unique identifier that can be used to identify an entity in AI GO!. "
    "Key: 1-250 chars, allowed: 'a-z 0-9 _ - $'.",
)
user_or_lf_key_field = Field(
    ...,
    max_length=250,
    min_length=1,
    pattern="^[a-z0-9_\\-\\$]+$",
    description="Key: 1-250 chars, allowed: 'a-z 0 9 _ - $'.",
    json_schema_extra={"lf_docs_type": "user_or_lf_key_field"},
)
optional_user_key_field = Field(
    None,
    max_length=250,
    min_length=1,
    pattern="^[a-z0-9_\\-]+$",
    description="Unique identifier that can be used to identify an entity in AI GO!."
    "Key: 1-250 chars, allowed: 'a-z 0-9 _ - $'.",
)
optional_user_or_lf_key_field = Field(
    None,
    max_length=250,
    min_length=1,
    pattern="^[a-z0-9_\\-\\$]+$",
    description="Optional key: 1-250 chars, allowed: 'a-z 0 9 _ - $'.",
)


class UserOrProviderKey(LFBaseModel):
    key: str = user_or_provider_key_field


class UserKey(LFBaseModel):
    key: str = user_key_field


class UserOrLFKey(LFBaseModel):
    key: str = user_or_lf_key_field


TemplateValue = Annotated[
    str,
    Field(
        ...,
        description="A string value that can reference configuration values using `<<config.my_param>>`.",
        json_schema_extra={"lf_docs_type": "template_value"},
    ),
]

UserOrLFKeyField = Annotated[str, user_or_lf_key_field]
