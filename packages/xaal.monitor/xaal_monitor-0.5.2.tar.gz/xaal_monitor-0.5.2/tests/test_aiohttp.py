"""
Simple web-frontend that use aiohttp
- pip install aiohttp
Open http://localhost:4444/
"""

from aiohttp import web
import platform
from xaal.lib import AsyncEngine
from xaal.lib import helpers, tools
from xaal.monitor import Monitor
from xaal.schemas import devices

PORT = 4444
mon = None
routes = web.RouteTableDef()


@routes.get('/')
async def dev_list(request):
    assert mon is not None
    r = '<ul>'
    for dev in mon.devices:
        r = r + f'<li><a href="/devices/{dev.address}"><tt>{dev.address}</tt></a> {dev.dev_type}</li>'
    r = r + '<ul>'
    return html("Devices list<br>%s" % r)


@routes.get('/devices/{addr}')
async def dev_info(request):
    assert mon is not None
    addr = tools.get_uuid(request.match_info['addr'])
    dev = mon.devices.get_with_addr(addr)
    r = ''
    if dev:
        return html(
            f"<h1>Device: {dev.address} / {dev.dev_type}</h1> <h2>Attributes</h2><pre>{dev.attributes}</pre> <h2>Description</h2><pre>{dev.description}</pre>"
        )
    else:
        return html('device not found')


def html(content):
    content = f'<html><body>\n{content}\n</body></html>'
    return web.Response(text=content, content_type='text/html')


# setup log & Engine
helpers.setup_console_logger()
eng = AsyncEngine()

# Monitoring device
dev = devices.hmi()
dev.info = "AioHTTP Monitor example"
dev.url = f'http://{platform.node()}:{PORT}'
eng.add_device(dev)

# Let's start
mon = Monitor(dev)
eng.start()
# eng.get_loop().set_debug(True)

# Web apps..
app = web.Application()
app.add_routes(routes)
web.run_app(app, port=PORT, loop=eng.get_loop())
