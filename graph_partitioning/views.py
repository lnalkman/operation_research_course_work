import copy
import asyncio
import time
from functools import partial
from collections import defaultdict

import aiohttp_jinja2
from aiohttp import web

from graph_partitioning.kernighan_lin import (
    fast_kernighan_lin,
    precise_kernighan_lin
)
from graph_partitioning.utils import (
    ErrorCodes,
    generate_random_edges,
    get_sequential_partitioning,
)


@aiohttp_jinja2.template('index.html')
def index(request):
    return {}


class RandomGraphGeneration(web.View):
    REQUIRED_PARAMS = (
        'nodes_count',
        'edges_count'
    )
    OPTIONAL_PARAMS = (
        'edge_weight_from',
        'edge_weight_to'
    )

    async def get(self):
        query = self.request.query
        random_graph_params = {}
        try:
            for graph_param in self.REQUIRED_PARAMS:
                random_graph_params[graph_param] = int(
                    query.getone(graph_param)
                )

            for graph_param in self.OPTIONAL_PARAMS:
                param_value = query.getone(graph_param, None)
                if param_value is not None:
                    random_graph_params[graph_param] = int(param_value)
        except KeyError as e:
            return web.json_response(
                {
                    'success': False,
                    'error': {
                        'field': e.args[0],
                        'code': ErrorCodes.REQUIRED,
                        'text': 'Поле повинно бути заповнено'
                    }
                },
                status=400
            )
        except (ValueError, TypeError):
            return web.json_response(
                {
                    'success': False,
                    'error': {
                        'field': graph_param,
                        'code': ErrorCodes.INVALID_VALUE,
                        'text': 'Невірне значення поля'
                    }
                },
                status=400
            )

        loop = asyncio.get_event_loop()
        edges = await loop.run_in_executor(
            executor=None,
            func=partial(
                generate_random_edges,
                **random_graph_params
            )
        )

        return web.json_response({
            'success': True,
            'data': edges
        })


class KernighanLinSolve(web.View):

    def get_graph(self):
        graph_string = self.request.query.getone('graph_description')
        graph = defaultdict(dict)
        for line in graph_string.split('\r\n'):
            first_node, second_node, weight = (
                int(d)
                for d in line.split(', ')
            )
            graph[first_node][second_node] = weight
            graph[second_node][first_node] = weight

        return graph

    async def get(self):
        try:
            graph = self.get_graph()

            fast_kernighan_partition = get_sequential_partitioning(
                len(graph.keys())
            )
            start = time.time()
            improved = fast_kernighan_lin(graph, fast_kernighan_partition)
            fast_kernighan_time = time.time() - start

            precise_kernighan_partition = None
            precise_kernighan_time = 0
            if improved:
                precise_kernighan_partition = copy.deepcopy(
                    fast_kernighan_partition
                )
                start = time.time()
                precise_kernighan_lin(
                    graph,
                    precise_kernighan_partition
                )
                precise_kernighan_time = time.time() - start
        except Exception as e:
            return web.Response(body=str(e))

        return web.json_response(
            {
                'success': True,
                'data': {
                    'kernighan_lin': {
                        'partition': [
                            list(partition)
                            for partition in fast_kernighan_partition
                        ],
                        'target_function': 55,
                        'time': fast_kernighan_time
                    },
                    'modified_algorithm': {
                        'partition': precise_kernighan_partition and [
                            list(partition)
                            for partition in
                            fast_kernighan_partition
                        ],
                        'target_function': 55,
                        'time': (
                                precise_kernighan_partition and
                                precise_kernighan_time
                        )
                    }
                }
            }
        )

