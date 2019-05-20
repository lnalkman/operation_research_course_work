import random
from typing import Optional

from networkx import gnm_random_graph

from .local_types import Graph


def generate_random_graph(
    nodes_count: int,
    edges_count: Optional[int] = None,
    edge_weight_from: Optional[int] = 1,
    edge_weight_to: Optional[int] = 20
) -> Graph:
    if edges_count < nodes_count - 1:
        raise ValueError(
            "Edges count should be equal or more than nodes count - 1"
        )

    graph = {node: {} for node in range(nodes_count)}
    edge_view = gnm_random_graph(n=nodes_count, m=edges_count)
    for first, second in edge_view:
        random_weight = random.randint(edge_weight_from, edge_weight_to)
        graph[first][second], graph[second][first] = random_weight

    return graph
