from itertools import combinations
from typing import (
    Iterable,
    Tuple,
    Optional
)

from graph_partitioning.local_types import (
    Graph,
    Subgraph
)


def fast_kernighan_lin(graph: Graph, subgraphs: Iterable[Subgraph]) -> bool:
    improved = False

    for first_subgraph, second_subgraph in combinations(subgraphs, 2):
        improved_iteration = True
        while improved_iteration:
            improved_iteration = False

            # Count D value for every node in chosen subgraphs
            d = {}
            pairs = (
                (first_subgraph, second_subgraph),
                (second_subgraph, first_subgraph)
            )
            for subgraph, other_subgraph in pairs:
                for node in subgraph:
                    d[node] = sum(
                        weight if other_node in other_subgraph
                        else -weight if other_node in subgraph
                        else 0
                        for other_node, weight in graph[node].items()
                    )

            best_nodes_pair: Optional[Tuple[int, int]] = None
            best_rating = 0
            for first_subgraph_node in first_subgraph:
                for second_subgraph_node in second_subgraph:
                    rating = (
                        d[first_subgraph_node]
                        + d[second_subgraph_node]
                        - 2 * graph[first_subgraph_node].get(
                            second_subgraph_node, 0
                        )
                    )
                    if rating > best_rating:
                        best_rating = rating
                        best_nodes_pair = (
                            first_subgraph_node, second_subgraph_node
                        )

            # Swap nodes with the best rating
            if best_nodes_pair is not None:
                first_subgraph.remove(best_nodes_pair[0])
                second_subgraph.remove(best_nodes_pair[1])

                first_subgraph.add(best_nodes_pair[1])
                second_subgraph.add(best_nodes_pair[0])
                improved_iteration = True
                improved = True

    return improved


def precise_kernighan_lin(graph: Graph, subgraphs: Iterable[Subgraph]):
    while fast_kernighan_lin(graph, subgraphs):
        pass
