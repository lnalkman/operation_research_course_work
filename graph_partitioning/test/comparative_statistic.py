import os
import time
from collections import defaultdict

from graph_partitioning.kernighan_lin import (
    fast_kernighan_lin,
    precise_kernighan_lin
)
from graph_partitioning.utils import (
    get_sequential_partitioning,
    get_partitions_cost
)


fixtures_directory = os.path.join(
    os.path.dirname(__file__),
    'fixtures/'
)
fixtures_names = os.listdir(fixtures_directory)


def with_time(func):
    def inner(*args, **kwargs):
        start = time.time_ns()
        return func(*args, **kwargs), time.time() - start

    return inner

fast_kernighan_lin = with_time(fast_kernighan_lin)
precise_kernighan_lin = with_time(precise_kernighan_lin)


for fixture_name in fixtures_names:
    fixture_path = os.path.join(
        fixtures_directory,
        fixture_name
    )
    with open(fixture_path) as f:
        edges = (
            [int(d) for d in line.split(', ')]
            for line in f.readlines()
        )
        graph = defaultdict(dict)
        for edge in edges:
            graph[edge[0]][edge[1]] = edge[2]
            graph[edge[1]][edge[0]] = edge[2]

    nodes_count = len(graph.keys())
    fast_kernighan_partition = get_sequential_partitioning(nodes_count)
    precise_kernighan_partition = get_sequential_partitioning(nodes_count)

    _, fast_kernighan_time = fast_kernighan_lin(
        graph,
        fast_kernighan_partition
    )
    _, precise_kernighan_time = precise_kernighan_lin(
        graph,
        precise_kernighan_partition
    )
    time_difference_percent = fast_kernighan_time / precise_kernighan_time * 100

    fast_kernighan_result = get_partitions_cost(
        graph,
        fast_kernighan_partition
    )
    precise_kernighan_result = get_partitions_cost(
        graph,
        precise_kernighan_partition
    )
    result_difference_percent = (
            100 - precise_kernighan_result / fast_kernighan_result * 100
    )

    print(time_difference_percent, result_difference_percent)






