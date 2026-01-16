# import pdb
from logging import getLogger

# from zwave_js_server.event import Event
from zwave_js_server.model.node import Node
from zwave_js_server.model.value import Value
from zwave_js_server.const import CommandClass

from xaal.schemas import devices
from xaal.lib import tools, bindings, AsyncEngine, Device


from . import const

logger = getLogger(__name__)

BASE_ADDR = tools.get_uuid('74fd7cf2-a349-46af-bbaf-41d98fab0000')


def get_property_id(value: Value):
    if value.property_ in ["value", "currentValue", "targetValue"]:
        return value.property_key_name
    return "--" + str(value.property_name)


def value_dump(value: Value):
    print(f"[{value}] {'0x%x'%value.command_class} {value.endpoint} {get_property_id(value)} => {value.value}")


def value_is_command_class(value: Value, command_class: CommandClass):
    return value.command_class == command_class.value


def value_is_value(value: Value):
    # return value.property_ in ["value", "currentValue", "targetValue"]
    return value.property_ in ["targetValue"]


def build_devices(node: Node, eng: AsyncEngine):
    config = node.device_config
    logger.info(f"{node.node_id} {config.manufacturer}/{config.label} ")
    # node.on("value updated", self.value_updated)
    # pdb.set_trace()
    #
    assert BASE_ADDR
    base_addr = BASE_ADDR + node.node_id * 128
    for k in node.values:
        value = node.values.get(k)
        if value is None or not value_is_value(value):
            continue
        base_addr = base_addr + 1
        value_dump(value)

        obj = None
        if value_is_command_class(value, CommandClass.SWITCH_BINARY):
            obj = PowerRelay(node, value, base_addr)

        if value_is_command_class(value, CommandClass.SWITCH_MULTILEVEL):
            obj = Lamp(node, value, base_addr)

        if value_is_command_class(value, CommandClass.METER):
            obj = PowerMeter(node, value, base_addr)
            pass

        if obj is not None and obj.dev:
            obj.setup()
            eng.add_device(obj.dev)
            logger.warning(obj.dev)

    # if node.node_id == 5:
    # pdb.set_trace()


class ZwaveDevice(object):
    def __init__(self, node: Node):
        self.node = node
        self.dev: Device | None = None

    def setup(self):
        assert self.dev
        dev = self.dev
        dev.vendor_id = f"ZwaveJS/{self.node.device_config.manufacturer}"
        dev.product_id = f"{self.node.device_config.label}"
        dev.info = f"{self.node.node_id}"
        self.node.on(const.EVT_VALUE_UPDATED, self.update)

    def update(self, event: dict):
        print(event)


class PowerRelay(ZwaveDevice):
    def __init__(self, node: Node, value: Value, base_addr: bindings.UUID):
        super().__init__(node)
        dev = devices.powerrelay(base_addr)
        dev.methods["turn_on"] = self.turn_on
        dev.methods["turn_off"] = self.turn_off
        dev.attributes["power"] = value.value
        self.dev = dev
        self.state = value

    def update(self, event: dict):
        if self.dev:
            value = event['value']
            if self.state == value:
                self.dev.attributes["power"] = value.value

    async def turn_on(self):
        await self.node.async_set_value(self.state, True)

    async def turn_off(self):
        await self.node.async_set_value(self.state, False)


class PowerMeter(ZwaveDevice):
    def __init__(self, node: Node, value: Value, base_addr: bindings.UUID):
        super().__init__(node)
        self.state = value
        dev = devices.powermeter(base_addr)
        dev.unsupported_attributes = ['devices']
        dev.attributes['power'] = value.value
        self.dev = dev
        self.power = value

    def update(self, event: dict):
        if self.dev:
            value = event['value']
            if self.power == value:
                self.dev.attributes["power"] = value.value


class Lamp(ZwaveDevice):
    def __init__(self, node: Node, value: Value, base_addr: bindings.UUID):
        super().__init__(node)
        dev = devices.lamp(base_addr)
        dev.methods["turn_on"] = self.turn_on
        dev.methods["turn_off"] = self.turn_off
        dev.attributes["light"] = value.value
        self.dev = dev
        self.state = value

    async def turn_on(self):
        await self.node.async_set_value(self.state, 99)

    async def turn_off(self):
        await self.node.async_set_value(self.state, 0)
