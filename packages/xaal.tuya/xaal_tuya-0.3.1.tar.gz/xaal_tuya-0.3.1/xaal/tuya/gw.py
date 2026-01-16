from xaal.lib import tools, AsyncEngine
from xaal import schemas
from . import devices

import logging

PACKAGE_NAME = 'xaal.tuya'
logger = logging.getLogger(__name__)

CFG_MAP = {
    'power_relay': devices.PowerRelay,
    'smart_plug': devices.SmartPlug,
    'lamp': devices.Lamp,
    'lamp_dimmer': devices.LampDimmer,
    'lamp_rgb': devices.LampRGB,
}

# Minimium value between 2 reconnect attempts
RECONNECT_DELAY = 30


class GW:
    def __init__(self, engine: AsyncEngine):
        self.engine = engine
        self.devices = {}
        self.config()
        self.setup()
        engine.on_start(self.boot)
        engine.on_stop(self.quit)
        engine.add_timer(self.update, 4 * 60)
        engine.add_timer(self.monitor, 1)

    def config(self):
        cfg = tools.load_cfg(PACKAGE_NAME)
        if not cfg:
            cfg = tools.new_cfg(PACKAGE_NAME)
            cfg['devices'] = {}
            logger.warning("Created an empty config file")
            cfg.write()
        self.cfg = cfg

    def setup(self):
        addr = tools.get_uuid(self.cfg['config']['addr'])
        gw = schemas.devices.gateway(addr)
        gw.vendor_id = 'Rambo'
        gw.product_id = 'Pytuya Gateway'
        gw.info = 'Tuya Gateway'
        gw.attributes['embedded'] = []
        gw.attributes['inactive'] = []
        self.gw = gw

        devs = self.cfg.get('devices', [])
        for d in devs:
            cfg = devs.get(d, {})
            tmp = cfg.get('type', 'PowerRelay')
            dev_type = CFG_MAP.get(tmp, None)
            if dev_type:
                dev = dev_type(d, cfg, self)
                if dev.is_valid:
                    self.add_device(d, dev)
                else:
                    logger.warning(f"Config error for {d}")
            else:
                logger.warning(f"Unsupported device type {tmp} {d}")

        # loaded all devices
        self.engine.add_device(gw)

    def add_device(self, tuya_id, dev):
        self.devices[tuya_id] = dev
        for d in dev.devices:
            self.engine.add_device(d)
            self.gw.attributes['embedded'].append(d.address)

    async def boot(self):
        logger.info('Booted')
        for dev in self.devices.values():
            await dev.connect()
        self.update_inactive()

    def update_inactive(self):
        r = []
        for dev in self.devices.values():
            if not dev.connected:
                r = r + [k.address for k in dev.devices]
        if set(self.gw.attributes['inactive']) != set(r):
            self.gw.attributes['inactive'] = r

    async def update(self):
        """Force an update on all devices, not really needed for 3.4 protocol"""
        for dev in self.devices.values():
            await dev.request_dps()

    async def monitor(self):
        """Find disconnected devices, and reconnect"""
        update = False
        for dev in self.devices.values():
            if not dev.connected and dev.last_connect + RECONNECT_DELAY < devices.now():
                await dev.connect()
                update = True
        if update:
            self.update_inactive()

    def quit(self):
        cfg = tools.load_cfg(PACKAGE_NAME)
        if cfg != self.cfg:
            logger.info('Saving configuration file')
            self.cfg.write()


def setup(eng):
    GW(eng)
    return True
