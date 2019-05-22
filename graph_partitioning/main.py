import pathlib
import logging
import sys

import aiohttp_jinja2
import jinja2
from aiohttp import web

from graph_partitioning.views import (
    index,
    RandomGraphGeneration
)


PROJECT_ROOT = pathlib.Path(__file__).parent


def setup_routes(app):
    app.router.add_get('/', index),
    app.router.add_view('/random_graph/', RandomGraphGeneration)

    setup_static_routes(app)


def setup_static_routes(app):
    app.router.add_static(
        '/static/',
        path=PROJECT_ROOT / 'static',
        name='static'
    )


async def init_app(argv=None):

    app = web.Application()

    app['config'] = {}

    # setup Jinja2 template renderer
    aiohttp_jinja2.setup(
        app,
        loader=jinja2.PackageLoader('graph_partitioning', 'templates')
    )

    # setup views and routes
    setup_routes(app)

    return app


def main(argv):
    logging.basicConfig(level=logging.DEBUG)

    app = init_app(argv)

    web.run_app(
        app,
        host='localhost',
        port=8001
    )


if __name__ == '__main__':
    main(sys.argv[1:])
