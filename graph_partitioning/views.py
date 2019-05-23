import asyncio
from functools import partial

import aiohttp_jinja2
from aiohttp import web

from graph_partitioning.utils import (
    ErrorCodes,
    generate_random_edges
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
