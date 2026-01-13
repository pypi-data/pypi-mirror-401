import ast
from typing import Type, Annotated
from pydantic import create_model, Field, TypeAdapter
from pydantic.json_schema import WithJsonSchema
from .models import IntentIO


def _try_json_schema(x):
    try:
        TypeAdapter(x).json_schema()
        return True
    except Exception:
        return False


def _is_type(obj) -> bool:
    if hasattr(obj, "__origin__"):
        return True
    if isinstance(obj, type):
        return True
    return False


def create_io(**field_definitions) -> Type[IntentIO] | IntentIO:
    fields = {}
    values = {}
    has_values = False

    for field_name, definition in field_definitions.items():
        if len(definition) != 2:
            raise ValueError(
                f"Field '{field_name}' must be a tuple of (value_or_type, description)")

        first, second = definition
        if _is_type(first):
            ok = _try_json_schema(first)
            field_type = first if ok else Annotated[first, WithJsonSchema({})]
            fields[field_name] = (field_type, Field(description=second))
        else:
            ok = _try_json_schema(type(first))
            field_type = type(first) if ok else Annotated[type(
                first), WithJsonSchema({})]
            fields[field_name] = (field_type, Field(description=second))
            values[field_name] = first
            has_values = True

    model_class = create_model("_", __base__=IntentIO, **fields)
    if has_values:
        return model_class(**values)
    else:
        return model_class


def extract_valid_python(code: str) -> str | None:
    lines = code.splitlines()
    n = len(lines)
    best_candidate = None
    for start in range(n):
        for end in range(n, start, -1):
            snippet = "\n".join(lines[start:end]).strip()
            if not snippet:
                continue
            try:
                tree = ast.parse(snippet)
            except SyntaxError:
                continue
            if not tree.body:
                continue
            if best_candidate is None or len(snippet) > len(best_candidate):
                best_candidate = snippet
    return best_candidate if best_candidate is not None else code
