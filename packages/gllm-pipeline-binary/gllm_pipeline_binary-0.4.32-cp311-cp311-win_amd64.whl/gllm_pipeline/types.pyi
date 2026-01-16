from _typeshed import Incomplete
from dataclasses import dataclass
from pydantic import BaseModel
from typing import Any

@dataclass(frozen=True)
class Val:
    """A value wrapper that represents a fixed/literal input.

    Attributes:
        value (object): The literal value of the input.
    """
    value: object

class PipelineInvocation(BaseModel):
    '''A model representing the invocation parameters for a pipeline.

    This model is used to validate the structure of data returned by
    pre_invoke_transform functions. It ensures the data has the correct
    format for pipeline invocation.

    Examples:
        ```python
        invocation = PipelineInvocation(
            input={"user_query": "What is AI?"},
            config={"session_id": "abc123"}
        )

        # With no config
        invocation = PipelineInvocation(input={"query": "test"})
        ```

    Attributes:
        input (dict[str, Any]): The input data to pass to the pipeline.
            This is a required field and must be a dictionary.
        config (dict[str, Any] | None): Optional configuration for the
            pipeline execution. Must be a dictionary if provided.
    '''
    model_config: Incomplete
    input: dict[str, Any]
    config: dict[str, Any] | None
