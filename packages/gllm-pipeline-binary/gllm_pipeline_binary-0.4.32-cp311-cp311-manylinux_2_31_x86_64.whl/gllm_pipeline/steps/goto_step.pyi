from _typeshed import Incomplete
from gllm_core.utils.retry import RetryConfig
from gllm_datastore.cache.cache import BaseCache
from gllm_pipeline.alias import InputMapSpec as InputMapSpec, PipelineState as PipelineState
from gllm_pipeline.exclusions import ExclusionSet as ExclusionSet
from gllm_pipeline.steps.pipeline_step import BasePipelineStep as BasePipelineStep
from gllm_pipeline.steps.step_error_handler.step_error_handler import BaseStepErrorHandler as BaseStepErrorHandler
from gllm_pipeline.types import Val as Val
from gllm_pipeline.utils.async_utils import execute_callable as execute_callable
from gllm_pipeline.utils.graph import create_edge as create_edge
from gllm_pipeline.utils.has_inputs_mixin import HasInputsMixin as HasInputsMixin
from gllm_pipeline.utils.input_map import shallow_dump as shallow_dump
from langchain_core.runnables import RunnableConfig as RunnableConfig
from langgraph.runtime import Runtime
from langgraph.types import Command, RetryPolicy
from typing import Any, Callable

class GoToStep(BasePipelineStep, HasInputsMixin):
    '''A pipeline step that enables dynamic flow control by jumping to specified nodes.

    This step allows for dynamic routing in pipelines by jumping to different nodes
    based on runtime conditions. The target can be a static node name, a state key,
    or a callable that determines the target at runtime.

    Attributes:
        name (str): A unique identifier for the pipeline step.
        target (Val | str | Callable[[dict[str, Any]], str]): The target node specification.
        input_map (dict[str, str | Val]): Mapping of argument names to either a state/config key (str)
            or a fixed value (Val). Inherited from HasInputsMixin.
        output_state (str | None): The state key to store the resolved target.
        allow_end (bool): Whether jumping to \'END\' is allowed.
        retry_policy (RetryPolicy | None): Configuration for retry behavior using LangGraph\'s RetryPolicy.
            Inherited from BasePipelineStep.
        cache_store ("BaseCache" | None): The cache store used for caching step results, if configured.
            Inherited from BasePipelineStep.
        is_cache_enabled (bool): Property indicating whether caching is enabled for this step.
            Inherited from BasePipelineStep.
    '''
    target: Incomplete
    output_state: Incomplete
    allow_end: Incomplete
    def __init__(self, name: str, target: Val | str | Callable[[dict[str, Any]], str], input_map: InputMapSpec | None = None, output_state: str | None = None, allow_end: bool = True, retry_config: RetryConfig | None = None, error_handler: BaseStepErrorHandler | None = None, cache_store: BaseCache | None = None, cache_config: dict[str, Any] | None = None) -> None:
        """Initializes a new instance of the GoToStep class.

        Args:
            name (str): The name of the step.
            target (Val | str | Callable): The target node specification.
            input_map (InputMapSpec | None, optional): Unified input map. Defaults to None.
            output_state (str | None, optional): State key to store resolved target. Defaults to None.
            allow_end (bool, optional): Whether jumping to 'END' is allowed. Defaults to True.
            retry_config (RetryConfig | None, optional): Retry configuration. Defaults to None.
            error_handler (BaseStepErrorHandler | None, optional): Error handler. Defaults to None.
            cache_store (BaseCache | None, optional): Cache store instance. Defaults to None.
            cache_config (dict[str, Any] | None, optional): Cache configuration. Defaults to None.
        """
    async def execute(self, state: PipelineState, runtime: Runtime, config: RunnableConfig | None = None) -> Command:
        """Executes the goto step and returns a LangGraph Command.

        Args:
            state (PipelineState): The current pipeline state.
            runtime (Runtime): The runtime context containing config.
            config (RunnableConfig | None, optional): Optional runnable configuration. Defaults to None.

        Returns:
            Command: A LangGraph Command with goto parameter for routing.

        Raises:
            ValueError: If the resolved target is invalid.
            KeyError: If state key is missing for string targets.
        """
    async def execute_direct(self, state: PipelineState, runtime: Runtime, config: RunnableConfig | None = None) -> dict[str, Any] | None:
        """Executes the goto step and returns a state update.

        Args:
            state (PipelineState): The current pipeline state.
            runtime (Runtime): The runtime context containing config.
            config (RunnableConfig | None, optional): Optional runnable configuration. Defaults to None.

        Returns:
            dict[str, Any] | None: State update with resolved target if output_state
                is specified, None otherwise.

        Raises:
            ValueError: If the resolved target is invalid.
            KeyError: If state key is missing for string targets.
        """
    def add_to_graph(self, graph: Any, previous_endpoints: list[str], retry_policy: RetryPolicy | None = None) -> list[str]:
        """Adds the GoToStep to the graph and creates edges.

        Args:
            graph (Any): The LangGraph graph to add the step to.
            previous_endpoints (list[str]): List of source node names to connect from.
            retry_policy (RetryPolicy | None, optional): Optional retry policy to override
                the step's default. Defaults to None.

        Returns:
            list[str]: List of endpoint names after adding this step.
        """
    def get_mermaid_diagram(self, indent: int = 0) -> str:
        """Generates a Mermaid diagram representation of this goto step.

        Args:
            indent (int, optional): Number of spaces to indent the diagram. Defaults to 0.

        Returns:
            str: The Mermaid diagram string.
        """
    is_excluded: Incomplete
    def apply_exclusions(self, exclusions: ExclusionSet) -> None:
        """Applies exclusions to this goto step.

        Args:
            exclusions (ExclusionSet): The exclusion set to apply.
        """
