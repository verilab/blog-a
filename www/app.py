import logging

logging.basicConfig(level=logging.INFO)

import asyncio, os, json, time
from datetime import datetime
from aiohttp import web


def index(request):
    return web.Response(body=b'<h1>Hello, Blog A!</h1>')


@asyncio.coroutine
def init(loop):
    app = web.Application(loop=loop)
    app.router.add_route('GET', '/', index)
    server = yield from loop.create_server(app.make_handler(), '0.0.0.0', 8080)
    logging.info('server started on port 8080...')
    return server


loop = asyncio.get_event_loop()
loop.run_until_complete(init(loop))
loop.run_forever()
