# from xaal.lib import tools

import asyncio
import logging

from aiohttp.client import ClientSession
from zwave_js_server.client import Client as ZwaveClient

from xaal.lib import AsyncEngine
from xaal.schemas import devices

from .cmdclass import COMMAND_CLASS
from .const import EVT_VALUE_UPDATED
from .devices import build_devices

PACKAGE_NAME = 'xaal.zwavejs'

logger = logging.getLogger(__name__)
# Disable zwave-js-server logs
logging.getLogger("zwave_js_server").setLevel(logging.WARNING)


URL = "ws://10.77.3.143:3000"
# URL = "ws://localhost:3000"

DEBUG = True


class GW:
    def __init__(self, engine: AsyncEngine):
        self.engine = engine
        logger.debug("ZwaveJS gateway initialized")
        engine.on_start(self.start)
        gw = devices.gateway()
        gw.new_attribute("gw", self)
        engine.add_device(gw)

    async def start(self):
        sess = ClientSession()
        self.client = ZwaveClient(URL, sess)
        await self.client.connect()
        self.ready = asyncio.Event()
        self.engine.new_task(self.client.listen(self.ready))
        # await self.client.listen(ready)
        logger.warning("Done")
        await self.run()

    async def run(self):
        await self.ready.wait()
        assert self.client.driver
        logger.warning("ZwaveJS ready")
        nodes = self.client.driver.controller.nodes
        for node in nodes.values():
            if node.ready:
                build_devices(node, self.engine)
                if DEBUG:
                    node.on(EVT_VALUE_UPDATED, self.dump_event)

    def dump_event(self, event):
        cmd_class = int(event["args"]["commandClass"])
        nodeId = event["nodeId"]
        value = event["value"]
        # pdb.set_trace()
        prop = event["args"]["property"]
        if prop in ["value", "currentValue", "targetValue"]:
            prop = value.property_key_name
        logger.warning(f"{nodeId}.{value.endpoint} {COMMAND_CLASS(cmd_class)}={prop}=>{event["args"]["newValue"]}")


def setup(eng):
    GW(eng)
    return True
