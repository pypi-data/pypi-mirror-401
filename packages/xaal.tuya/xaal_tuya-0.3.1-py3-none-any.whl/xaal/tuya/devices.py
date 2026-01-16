import colorsys
import functools
import logging
import time

from xaal.lib import tools
from xaal.schemas import devices
from xaal.tuya import pytuya

logger = logging.getLogger(__name__)

# =============================================================================
# Tools
# =============================================================================


def get_dps(dps, idx):
    return dps.get(str(idx), None)


def now():
    return time.time()


class TuyaDev(pytuya.TuyaListener):
    def __init__(self, tuya_id, cfg, gw):
        self.tuya_id = tuya_id
        self.cfg = cfg
        self.gw = gw
        # xAAL devices
        self.devices = []
        # default: invalid cfg, no debug & not connected
        self.is_valid = False
        self.debug = False
        self.connected = False
        self.last_connect = 0
        self.name = ""
        # Init stuff
        self.load_config()
        if self.is_valid:
            self.setup()
            self.init_properties()
        self.tuya_dev = None

    def load_config(self):
        cfg = self.cfg
        addr = tools.get_uuid(cfg.get('base_addr', None))
        ip = cfg.get('ip', None)
        key = cfg.get('key', None)
        proto = cfg.get('protocol', None)
        self.debug = cfg.get('debug', self.debug)
        # invalid file ?
        if not ip or not key:
            logger.error(f"{self.tuya_id}: ip or key invalid")
            return

        if addr is None:
            addr = tools.get_random_base_uuid()
            cfg['base_addr'] = str(addr)
        if proto is None:
            cfg['protocol'] = 3.3
        self.base_addr = addr
        self.is_valid = True
        self.name = "%s@%s" % (self.tuya_id, ip)

    def init_properties(self):
        for dev in self.devices:
            dev.vendor_id = 'IHSEV / Tuya'
            dev.hw_id = self.tuya_id
            dev.info = 'Tuya %s: @ %s' % (self.__class__.__name__, self.name)
            if len(self.devices) > 1:
                dev.group_id = self.base_addr + 0xFF

    async def _connect(self):
        cfg = self.cfg
        logger.debug(f"Connecting to device {self.name}")
        self.connected = False
        if self.tuya_dev is not None:
            logger.debug(f"Closing previous connection to {self.name}")
            if self.tuya_dev.transport:
                logger.debug(f"Resetting {self.name} device")
                await self.tuya_dev.reset()
            await self.tuya_dev.close()
        self.last_connect = now()
        self.tuya_dev = await pytuya.connect(
            address=cfg['ip'],
            device_id=self.tuya_id,
            local_key=cfg['key'],
            protocol_version=cfg['protocol'],
            enable_debug=self.debug,
            listener=self,
        )
        await self.request_dps()
        self.tuya_dev.start_heartbeat()

    async def connect(self):
        try:
            await self._connect()
        except Exception as e:
            logger.error(f"Error connecting to device {self.name}: {e}")

    def status_updated(self, status):
        if not self.connected:
            logger.debug(f"{self.name} connected")
        self.connected = True
        if self.debug:
            logger.debug(f"{self.name} new status: {status}")
        self.on_dps(status)

    def disconnected(self):
        if self.connected:
            self.connected = False
            logger.warning(f"{self.name} disconnected")

    async def check_connected(self):
        if self.tuya_dev is None or self.tuya_dev.transport is None:
            self.connected = False
            await self.connect()

    async def post_dps(self, data):
        assert self.tuya_dev
        await self.check_connected()
        if self.debug:
            logger.debug(f"POST {self.name} DPS: {data}")
        try:
            await self.tuya_dev.set_dps(data)
        except Exception as e:
            logger.warning(f"POST Error {self.name} {e}")
            self.disconnected()

    async def request_dps(self):
        assert self.tuya_dev
        await self.check_connected()
        if self.debug:
            logger.debug(f"REQUEST {self.name} DPS")
        try:
            status = await self.tuya_dev.status()
            self.status_updated(status)
        except Exception as e:
            logger.warning(f"REQUEST Error {self.name} {e}")
            self.disconnected()

    def setup(self):
        logger.warning('Please override setup()')

    def on_dps(self, dps):
        logger.warning('Please implement on_status in your class')


class PowerRelay(TuyaDev):
    def setup(self):
        dps = self.cfg.get('dps', ['1'])
        addr = self.base_addr + 1
        self.dps_to_dev = {}
        for k in dps:
            dev = devices.powerrelay_toggle(addr)
            dev.methods['turn_on'] = functools.partial(self.turn_on, k, dev)
            dev.methods['turn_off'] = functools.partial(self.turn_off, k, dev)
            dev.methods['toggle'] = functools.partial(self.toggle, k, dev)
            self.dps_to_dev.update({k: dev})
            self.devices.append(dev)
            addr = addr + 1

    async def turn_on(self, idx, dev):
        await self.post_dps({idx: True})

    async def turn_off(self, idx, dev):
        await self.post_dps({idx: False})

    async def toggle(self, idx, dev):
        await self.post_dps({idx: not dev.attributes[0].value})

    def on_dps(self, dps):
        for k in dps:
            tmp = self.dps_to_dev.get(k, None)
            if tmp:
                tmp.attributes['power'] = dps[k]


def out_hysteresis(value, new_value, tol):
    if value is None:
        return True
    mini = value - tol
    maxi = value + tol
    if mini < new_value < maxi:
        return False
    return True


class SmartPlug(PowerRelay):

    def setup(self):
        self.pmeter_dps = self.cfg.get('pmeter_dps', ['4', '5', '6'])
        pmeter = devices.powermeter_extended(self.base_addr)
        energy = pmeter.get_attribute('energy')
        if energy is not None:
            # energy is not supported by the device, remove it
            pmeter.del_attribute(energy)
        pmeter.unsupported_attributes = ['energy']
        self.devices.append(pmeter)
        PowerRelay.setup(self)
        # related power relays
        pmeter.attributes['devices'] = [k.address for k in self.devices[1:]]

    def debug_dps(self, dps):
        k_dps = list(self.dps_to_dev.keys())
        k_dps = k_dps + self.pmeter_dps
        r = ''
        for k, v in dps.items():
            if k not in k_dps:
                r = r + f"'{k}'->{v}    "
        if len(r) > 0:
            logger.info(f"{self.tuya_id} unknow DPS: {r}")

    def on_dps(self, dps):
        if self.debug:
            self.debug_dps(dps)
        PowerRelay.on_dps(self, dps)
        pmeter_attr = self.devices[0].attributes
        # current
        current = get_dps(dps, self.pmeter_dps[0])
        if current is not None:
            tmp = round(int(current) / 1000, 2)
            if out_hysteresis(pmeter_attr['current'], tmp, 0.02):
                pmeter_attr['current'] = tmp
        # power
        power = get_dps(dps, self.pmeter_dps[1])
        if power is not None:
            tmp = round(int(power) / 10)
            if out_hysteresis(pmeter_attr['power'], tmp, 2):
                pmeter_attr['power'] = tmp
        # voltage
        voltage = get_dps(dps, self.pmeter_dps[2])
        if voltage is not None:
            tmp = round(int(voltage) / 10)
            if out_hysteresis(pmeter_attr['voltage'], tmp, 2):
                pmeter_attr['voltage'] = tmp


class Lamp(TuyaDev):
    def setup(self):
        dev = devices.lamp_toggle(self.base_addr + 1)
        dev.methods['turn_on'] = self.turn_on
        dev.methods['turn_off'] = self.turn_off
        dev.methods['toggle'] = self.toggle
        self.devices.append(dev)

    async def turn_on(self):
        await self.post_dps({1: True})

    async def turn_off(self):
        await self.post_dps({1: False})

    async def toggle(self):
        await self.post_dps({1: not self.devices[0].attributes['light']})

    def on_dps(self, dps):
        state = get_dps(dps, 1)
        if state is None:
            self.devices[0].attributes['light'] = state


class AdvLampMixin:
    """
    Dimming Lamp & RGB Lamp shares the config & API, but the dps (in & out) are
    really differents
    """

    def setup_mixin(self, dev):
        dev.methods['turn_on'] = self.turn_on
        dev.methods['turn_off'] = self.turn_off
        dev.methods['set_white_temperature'] = self.set_white_temperature
        dev.methods['set_brightness'] = self.set_brightness
        dev.methods['toggle'] = self.toggle
        self.devices.append(dev)

        # setting up white balance min/max
        white_temp = self.cfg.get('white_temp', None)
        if white_temp:
            self.white_min = int(white_temp[0])
            self.white_max = int(white_temp[1])
        else:
            self.white_min = 1500
            self.white_max = 6500

    def brightness_to_dps(self, value):
        try:
            res = round(int(value) * 255 / 100)
        except ValueError:
            return
        if res < 25:
            res = 25
        if res > 255:
            res = 255
        return res

    def temperature_to_dps(self, value):
        try:
            res = int(value)
        except ValueError:
            return
        delta = (self.white_max - self.white_min) / 255.0
        target = int((res - self.white_min) / delta)
        if target > 255:
            target = 255
        if target < 0:
            target = 0
        return target


class LampDimmer(Lamp, AdvLampMixin):
    def setup(self):
        dev = devices.lamp_dimmer(self.base_addr + 1)
        self.setup_mixin(dev)

    def on_dps(self, dps):
        attrs = self.devices[0].attributes
        # state
        result = get_dps(dps, 1)
        if result is None:
            attrs['light'] = result
        # brightness
        result = get_dps(dps, 2)
        if result:
            value = int(result) * 100 / 255
            attrs['brightness'] = int(value)
        # white_temperature
        result = get_dps(dps, 3)
        if result:
            delta = (self.white_max - self.white_min) / 255.0
            value = int(result) * delta + self.white_min
            attrs['white_temperature'] = round(value)

    async def set_white_temperature(self, _white_temperature):
        tmp = self.temperature_to_dps(_white_temperature)
        await self.post_dps({3: tmp})

    async def set_brightness(self, _brightness, _smooth=0):
        # smooth is not supported
        tmp = self.brightness_to_dps(_brightness)
        await self.post_dps({2: tmp})


def color_to_hex(hsv):
    """
    Converts the hsv list in a hexvalue.

    Args:
        hue is 0 to 360, sat & brighness between 0 to 1"
    """
    # ensure we received a list
    hsv = list(hsv)
    hsv[0] = hsv[0] / 360.0
    h, s, v = hsv
    rgb = [int(i * 255) for i in colorsys.hsv_to_rgb(h, s, v)]

    # This code from the original pytuya lib
    hexvalue = ""
    for value in rgb:
        temp = str(hex(int(value))).replace("0x", "")
        if len(temp) == 1:
            temp = "0" + temp
        hexvalue = hexvalue + temp

    hsvarray = [int(hsv[0] * 360), int(hsv[1] * 255), int(hsv[2] * 255)]
    hexvalue_hsv = ""
    for value in hsvarray:
        temp = str(hex(int(value))).replace("0x", "")
        if len(temp) == 1:
            temp = "0" + temp
        hexvalue_hsv = hexvalue_hsv + temp
    if len(hexvalue_hsv) == 7:
        hexvalue = hexvalue + "0" + hexvalue_hsv
    else:
        hexvalue = hexvalue + "00" + hexvalue_hsv
    return hexvalue


def hexvalue_to_hsv(hexvalue):
    """
    Converts the hexvalue used by tuya for colour representation into
    an HSV value.

    Args:
        hexvalue(string): The hex representation generated by BulbDevice._rgb_to_hexvalue()
    """
    h = int(hexvalue[7:10], 16)
    s = int(hexvalue[10:12], 16) / 255
    v = int(hexvalue[12:14], 16) / 255
    return (h, s, v)


class LampRGB(Lamp, AdvLampMixin):
    SCENES = ['scene_1', 'scene_2', 'scene_3', 'scene_4']

    def setup(self):
        dev = devices.lamp_color(self.base_addr + 1)
        dev.methods['set_hsv'] = self.set_hsv
        dev.methods['set_mode'] = self.set_mode
        dev.methods['get_scenes'] = self.get_scenes
        dev.methods['set_scene'] = self.set_scene
        self.setup_mixin(dev)

    def on_dps(self, dps):
        attrs = self.devices[0].attributes
        # state
        result = get_dps(dps, 1)
        if result is None:
            attrs['light'] = result
        # color / white
        result = get_dps(dps, 2)
        if result == 'colour':
            attrs['mode'] = 'color'
        if result == 'white':
            attrs['mode'] = 'white'
        if result and result.startswith('scene'):
            attrs['mode'] = 'scene'
        # brightness
        result = get_dps(dps, 3)
        if result:
            value = int(result) * 100 / 255
            attrs['brightness'] = int(value)
        # white_temperature
        result = get_dps(dps, 4)
        if result:
            delta = (self.white_max - self.white_min) / 255.0
            value = int(result) * delta + self.white_min
            attrs['white_temperature'] = round(value)
        # color value (hsv)
        result = get_dps(dps, 5)
        if result:
            attrs['hsv'] = hexvalue_to_hsv(result)

    async def set_white_temperature(self, _white_temperature):
        tmp = self.temperature_to_dps(_white_temperature)
        await self.post_dps({2: 'white', 4: tmp})

    async def set_brightness(self, _brightness, _smooth=0):
        # smooth is not supported
        tmp = self.brightness_to_dps(_brightness)
        await self.post_dps({2: 'white', 3: tmp})

    async def set_hsv(self, _hsv, _smooth=0):
        hsv = [float(k) for k in list(_hsv.split(','))]
        result = color_to_hex(hsv)
        await self.post_dps({2: 'colour', 5: result})

    async def set_mode(self, _mode):
        if _mode == 'color':
            await self.post_dps({2: 'colour'})
        if _mode == 'white':
            await self.post_dps({2: 'white'})
        if _mode == 'scene':
            await self.post_dps({2: 'scene_4'})

    def get_scenes(self):
        return LampRGB.SCENES

    async def set_scene(self, _scene):
        if _scene in LampRGB.SCENES:
            await self.post_dps({2: _scene})
