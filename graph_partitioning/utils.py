import random
from typing import (
    Optional,
    Tuple,
    Iterable,
    Any
)

from networkx import gnm_random_graph

from graph_partitioning.local_types import Graph


class ErrorCodes:
    REQUIRED = 'required'
    INVALID_VALUE = 'invalid value'


def generate_random_edges(
    nodes_count: int,
    edges_count: Optional[int] = None,
    edge_weight_from: int = 1,
    edge_weight_to: int = 20
) -> Tuple[Tuple[Any, Any, Any], ...]:
    if edges_count is None:
        edges_count = nodes_count - 1
    elif edges_count < nodes_count - 1:
        raise ValueError(
            "Edges count should be equal or more than nodes count - 1"
        )

    edges_view: Iterable[Tuple[int, int]] = gnm_random_graph(
        n=nodes_count,
        m=edges_count
    ).edges
    return tuple(
        (
            first_edge,
            second_edge,
            random.randint(edge_weight_from, edge_weight_to)
        )
        for first_edge, second_edge in edges_view
    )


def generate_random_graph(
    nodes_count: int,
    edges_count: Optional[int] = None,
    edge_weight_from: int = 1,
    edge_weight_to: int = 20
) -> Graph:
    random_edges = generate_random_edges(
        nodes_count,
        edges_count,
        edge_weight_from,
        edge_weight_to
    )
    graph = {node: {} for node in range(nodes_count)}
    for first, second, weight in random_edges:
        graph[first][second] = graph[second][first] = weight

    return graph
