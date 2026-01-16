from __future__ import annotations

import inspect
from pathlib import Path
from types import UnionType
from typing import Any
from typing import get_args
from typing import get_origin
from typing import Literal
from typing import TypeGuard
from typing import Union

import typer
from pydantic import Field

import latticeflow.go.cli.utils.arguments as cli_args
from latticeflow.go.cli.dtypes import CLICreateEvaluation
from latticeflow.go.cli.dtypes import CLICreateModel
from latticeflow.go.cli.dtypes import CLICreateRunConfig
from latticeflow.go.cli.utils.env_vars import get_cli_env_vars
from latticeflow.go.cli.utils.helpers import app_callback
from latticeflow.go.cli.utils.schema_mappers import CLIDeclarativeTaskDefinitionTemplate
from latticeflow.go.cli.utils.schema_mappers import CLIError
from latticeflow.go.cli.utils.single_commands import with_callback
from latticeflow.go.models import LFBaseModel


class DummyParameterSpec(LFBaseModel):
    type: str = Field(..., description="The type of the parameter.")
    key: str = Field(..., description="The key of the parameter.")
    display_name: str = Field(
        ..., min_length=1, description="The display name of the parameter."
    )


ALWAYS_PRESENT_OPTIONAL_FIELDS = {
    "run.model_adapters",
    "run.models",
    "run.dataset_generators",
    "run.datasets",
    "run.tasks",
    "run.evaluation",
}


def _get_default_item_type_for_path(path: str) -> type:
    if path.endswith(".config_spec.[i]"):
        return DummyParameterSpec
    if path == "run.tasks.[i].definition":
        return CLIDeclarativeTaskDefinitionTemplate
    if path == "run.models.[i]":
        return CLICreateModel
    if path == "run.evaluation":
        return CLICreateEvaluation
    raise CLIError(f"Requested default item type for unknown path: '{path}'")


def _get_indented_string(indent: int, string: str) -> str:
    return " " * indent + string


def _render_model(
    model_type: type[LFBaseModel], *, indent: int, path: str
) -> list[str]:
    model_type.model_rebuild()
    lines: list[str] = []
    for field_name, field in model_type.model_fields.items():
        field_path = f"{path}.{field_name}" if path else field_name
        if not field.is_required() and field_path not in ALWAYS_PRESENT_OPTIONAL_FIELDS:
            continue

        desc = field.description
        if desc:
            for desc_line in desc.splitlines():
                lines.append(_get_indented_string(indent, f"# {desc_line}"))

        field_lines = _render_field(
            field_name, field.annotation, indent=indent, path=field_path
        )
        if field_lines:
            lines.extend(field_lines)
            # NOTE: We want to spread the top-level keys and give them more spacing.
            if indent == 0:
                lines.append("")

    # We remove trailing empty lines.
    while lines and lines[-1] == "":
        lines.pop()

    return lines


def _is_pydantic_model_type(type: Any) -> TypeGuard[type[LFBaseModel]]:
    try:
        return inspect.isclass(type) and issubclass(type, LFBaseModel)
    except Exception:
        return False


def _is_list(origin: Any | None) -> bool:
    return origin is list


def _is_literal(origin: Any | None) -> bool:
    return origin is Literal


def _is_union(origin: Any | None) -> bool:
    return origin is Union or origin is UnionType


def _render_field(
    field_name: str, annotation: type[Any] | None, *, indent: int, path: str
) -> list[str]:
    key_prefix = _get_indented_string(indent, f"{field_name}:")

    if _is_pydantic_model_type(annotation):
        lines = [key_prefix]
        nested = _render_model(annotation, indent=indent + 2, path=path)
        lines.extend(nested)
        return lines

    origin = get_origin(annotation)

    if _is_list(origin):
        item_type = get_args(annotation)[0] if get_args(annotation) else Any
        item_path = f"{path}.[i]"

        item_origin = get_origin(item_type)
        if _is_union(item_origin):
            item_type = _get_default_item_type_for_path(item_path)

        lines = [key_prefix]
        if _is_pydantic_model_type(item_type):
            nested = _render_model(item_type, indent=indent + 4, path=item_path)
            if len(nested) > 0:
                nested[0] = _get_indented_string(indent + 2, "- ") + nested[0].lstrip()
            lines.extend(nested)
        else:
            lines.append(_get_indented_string(indent + 2, "-"))
        return lines

    if _is_literal(origin):
        literal_values = list(get_args(annotation))
        if literal_values:
            return [f"{key_prefix} {literal_values[0]}"]
        return [key_prefix]

    if _is_union(origin):
        item_type = _get_default_item_type_for_path(path)
        return _render_field(field_name, item_type, indent=indent, path=path)

    # NOTE: We do not differentiate between primitives, enums, dicts...
    return [key_prefix]


def register_template_command(app: typer.Typer) -> None:
    app.command(
        name="template", short_help="Generate a YAML template for a run config."
    )(with_callback(lambda: app_callback(get_cli_env_vars))(_template))


def _template(
    output: Path = typer.Option(
        ...,
        "--output",
        "-o",
        help="Path to output the YAML template.",
        callback=cli_args.check_path_not_empty,
    ),
) -> None:
    """Generate a YAML template for a run config."""
    output.write_text(
        (
            (
                "# LatticeFlow Run Configuration Template\n"
                "# This template can be used as a starting point for your run configuration.\n"
                "# To fill it out, read the documentation available at https://aigo.latticeflow.io/docs/cli-reference-run.\n"
                "\n"
            )
            + "\n".join(_render_model(CLICreateRunConfig, indent=0, path="run"))
            + "\n"
        ),
        encoding="utf-8",
    )
