from langgraph.graph import StateGraph
from typing import Any

def create_edge(graph: StateGraph, sources: str | list[str], target: str) -> None:
    """Create edges from source nodes to target node in the graph.

    Special handling:
    - START cannot participate in a fan-in. If present, add a direct START -> target edge
      separately and only fan-in non-START sources.

    Args:
        graph (StateGraph): The graph to add edges to.
        sources (str | list[str]): The source nodes. If str or list of 1 element,
            connect directly. If list > 1 elements, use the list for fan-in. If empty list,
            do nothing.
        target (str): The target node.
    """
def check_non_parallelizable_steps(branches: dict[str, Any], non_parallelizable_types: tuple[type, ...]) -> list[str]:
    """Check branches for non-parallelizable step instances.

    This function recursively searches through branches to find any steps that
    are instances of the specified non-parallelizable types.

    Args:
        branches (dict[str, Any]): Dictionary mapping branch names to branch contents.
            Branch contents can be single steps or lists of steps.
        non_parallelizable_types (tuple[type, ...]): Tuple of step types that cannot
            be safely executed in parallel.

    Returns:
        list[str]: List of descriptions of found non-parallelizable steps, including
            their name, type, location, and branch name.
    """
