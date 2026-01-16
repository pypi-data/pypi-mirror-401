from gllm_pipeline.utils.typing_compat import is_typeddict as is_typeddict
from typing import Any

def is_typeddict_or_basemodel(type_hint: type) -> bool:
    """Check if a type is a TypedDict or Pydantic BaseModel.

    Args:
        type_hint (type): The type to check.

    Returns:
        bool: True if the type is a TypedDict or BaseModel, False otherwise.
    """
def filter_output_by_schema(result: Any, schema: type) -> dict[str, Any]:
    """Filter the output result to match the provided schema.

    Args:
        result (Any): The result to filter.
        schema (type): The schema (TypedDict or BaseModel) to filter against.

    Returns:
        dict[str, Any]: The filtered result as a dictionary.

    Raises:
        ValueError: If the schema is not a TypedDict or Pydantic BaseModel.
    """
