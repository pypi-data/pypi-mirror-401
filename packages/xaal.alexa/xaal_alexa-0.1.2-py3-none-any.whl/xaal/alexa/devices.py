import logging
from xaal.schemas import devices
from xaal.lib import tools

logger = logging.getLogger(__name__)

class Echo(object):
    def __init__(self,name,cfg,gw):
        self.name = name
        self.gw = gw
        self.cfg = cfg
        self.setup_base_addr()
        self.setup_embedded()

    def setup_base_addr(self):
        b_addr = self.cfg.get('base_addr',None)
        if b_addr != None:
            self.base_addr = tools.get_uuid(b_addr)
        else:
            self.base_addr = tools.get_random_base_uuid()
            self.cfg['base_addr'] = self.base_addr

    def setup_embedded(self):
        # TTS
        self.setup_tts()
        # set some default infos on embedded
        for dev in self.embedded():
            dev.vendor_id  = "IHSEV"
            dev.version = 0.1

    def embedded(self):
        return [self.tts,]

    def setup_tts(self):
        tts = devices.tts(self.base_addr+1)
        tts.methods['say'] = self.say
        tts.product_id = "TTS for Alexa"
        tts.info = f'TTS on Echo:{self.name}'
        self.tts = tts

    def say(self,_msg,_lang=None,_voice=None):
        if _lang or _voice:
            logger.warning("Unable to change lang or voice right now")            
        self.gw.run_script(f'-d "{self.name}" -e speak:"{_msg}"')


class LastEcho(Echo):
    def say(self,_msg,_lang=None,_voice=None):
        if _lang or _voice:
            logger.warning("Unable to change lang or voice right now")            
        self.gw.run_script_lastalexa(f'-e speak:"{_msg}"')
