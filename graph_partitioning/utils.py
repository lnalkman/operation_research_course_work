import random
from typing import (
    Optional,
    Tuple,
    Iterable,
    Any,
    Set
)

from networkx import gnm_random_graph

from graph_partitioning.local_types import (
    Graph,
    Subgraph
)


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

    alone_nodes = {i for i in range(nodes_count)}
    for first_edge, second_edge in edges_view:
        if first_edge in alone_nodes:
            alone_nodes.remove(first_edge)
        if second_edge in alone_nodes:
            alone_nodes.remove(second_edge)

    if alone_nodes:
        return generate_random_edges(
            nodes_count,
            edges_count,
            edge_weight_from,
            edge_weight_to
        )
    else:
        return tuple(
            (
                first_edge + 1,
                second_edge + 1,
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


def get_sequential_partitioning(nodes_count: int) -> Tuple[Set[int], ...]:
    """
    Return tuple with 3 graph partitions, every graph node sequentially
    distributed on partitions (first partition will have first nodes, second
    partition will have nodes after first partition...)
    """
    avg_nodes_per_partition, rest_nodes = (nodes_count // 3, nodes_count % 3)

    if rest_nodes:
        first_partition = (0, avg_nodes_per_partition + 1)
    else:
        first_partition = (0, avg_nodes_per_partition)

    if rest_nodes == 2:
        second_partition = (
            first_partition[1],
            first_partition[1] + avg_nodes_per_partition + 1
        )
    else:
        second_partition = (
            first_partition[1],
            first_partition[1] + avg_nodes_per_partition
        )

    third_partition = (
        second_partition[1],
        second_partition[1] + avg_nodes_per_partition
    )
    
    return (
        set(i + 1 for i in range(*first_partition)),
        set(i + 1 for i in range(*second_partition)),
        set(i + 1 for i in range(*third_partition))
    )


def get_partitions_cost(graph: Graph, partitions: Tuple[Subgraph, ...]) -> int:
    """Count summary weights of edges that connect different partitions"""
    partitions_cost = 0
    for partition in partitions:
        for node in partition:
            for other_node in graph[node]:
                if other_node not in partition:
                    partitions_cost += graph[node][other_node]

    return partitions_cost
