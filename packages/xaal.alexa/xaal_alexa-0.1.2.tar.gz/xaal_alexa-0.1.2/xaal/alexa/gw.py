import platform
import logging

from xaal.schemas.devices import gateway
from xaal.lib import tools

import time
import shlex
import atexit
import asyncio

from .devices import Echo, LastEcho

PACKAGE_NAME = "xaal.alexa"
logger = logging.getLogger(PACKAGE_NAME)


DEFAULT_LAST_ALEXA_CACHE = 60


def now():
    return time.time()

class GW(object):
    
    def __init__(self,engine):
        self.devices = []
        self.engine = engine
        self._last_alexa_time = 0
        self.config()
        atexit.register(self._exit)
        self.setup_echo()
        self.setup_gw()

    def config(self):
        self.save_config = False
        cfg = tools.load_cfg(PACKAGE_NAME)
        if not cfg:
            logger.info('Missing config file, building a new one')
            cfg = tools.new_cfg(PACKAGE_NAME)
            cfg['config']['remote_script'] = 'alexa_remote_control.sh'
            cfg['config']['last_alexa_cache'] = DEFAULT_LAST_ALEXA_CACHE
            cfg['devices'] = {"last_alexa":{}}
            cfg.write()
        self.cfg = cfg
        self.remote_script = cfg['config']['remote_script']
   
    async def async_run(self,cmd):
        t0 = now()
        cmd = self.remote_script + " " + cmd
        args = shlex.split(cmd)
        logger.info(f"Launching: {cmd}")
        proc = await asyncio.create_subprocess_exec(*args,stdout=asyncio.subprocess.PIPE,stderr=asyncio.subprocess.PIPE)
        stdout, stderr = await proc.communicate()
        logger.info(f"Run {cmd}: {proc.returncode}")
        output = stdout.decode().strip()
        logger.debug(f"{output}")
        logger.warning(f'{cmd} done=> {now()-t0}')
        return output

    async def async_run_lastalexa(self,cmd):
        if self.last_alexa_expired():
            self.last_alexa = await self.async_run('-lastalexa')
            self._last_alexa_time = now()
        cmd = f'-d "{self.last_alexa}" ' + cmd
        return await self.async_run(cmd)

    def run_script(self,cmd):
        asyncio.ensure_future(self.async_run(cmd))

    def run_script_lastalexa(self,cmd):
        asyncio.ensure_future(self.async_run_lastalexa(cmd))

    def setup_echo(self):
        cfg_list = self.cfg.get('devices',[])
        for k in cfg_list:
            if k=='last_alexa':
                dev = LastEcho(k,cfg_list[k],self)
            else:
                dev = Echo(k,cfg_list[k],self)
            self.engine.add_devices(dev.embedded())

    def setup_gw(self):
        # last step build the GW device
        gw            = gateway()
        gw.address    = tools.get_uuid(self.cfg['config']['addr'])
        gw.vendor_id  = "IHSEV"
        gw.product_id = "Alexa gateway"
        gw.version    = 0.1
        gw.url        = "http://alexa.amazon.com"
        gw.info       = "%s@%s" % (PACKAGE_NAME,platform.node())
        self.engine.add_device(gw)
        self.gw = gw

    def last_alexa_expired(self):
        cache = int(self.cfg['config'].get('last_alexa_cache',DEFAULT_LAST_ALEXA_CACHE))
        now_ = now()
        if (self._last_alexa_time + cache) < now_:
            return True
        return False

    def _exit(self):
        cfg = tools.load_cfg(PACKAGE_NAME)
        if cfg != self.cfg:
            logger.info('Saving configuration file')
            self.cfg.write()
        
def setup(eng):
    gw=GW(eng)
    return True
