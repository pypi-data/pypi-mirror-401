from graphtec.core.device.base import BaseModule
from graphtec.core.commands import ALARM
from graphtec.core.exceptions import *
from graphtec.utils.utils import get_last_token,validate_channel,normalize_choice
import logging
from types import MappingProxyType

logger = logging.getLogger(__name__)


class AlarmModule(BaseModule):
    """Grupo ALARM: Configuración y lectura de alarmas"""

    # =========================================================
    # MAPEO
    # =========================================================
    HIGH_LOW_MAP = MappingProxyType({
        "HI": "HI", "HIGH": "HI","UP":"HI","H":"HI",
        "LO": "LO", "LOW": "LO","DOWN":"LO","L":"LO",
        "OFF":"OFF","NONE":"OFF",
    })

    ON_OFF_MAP = MappingProxyType({
        "ON":"ON", "1":"ON", "TRUE":"ON","ENABLE":"ON",
        "OFF":"OFF","NONE":"OFF", "0":"OFF", "FALSE":"OFF","DISABLE":"OFF",
    })

    ALARM_MODE_MAP = MappingProxyType({
        "LEVEL":"LEVEL", 
        "OFF":"OFF","NONE":"OFF",
    })

    # =========================================================
    # SETTERS
    # =========================================================
    def set_alarm_mode(self, mode: str):
        """ mode: LEVEL / OFF"""
        mode = normalize_choice(mode, self.ALARM_MODE_MAP)

        self.connection.send(ALARM.SET_ALARM_MODE.format(mode=mode))
        logger.debug(f"[GL-ALARM] Alarm FUNC -> {mode}")

    def set_alarm_level(self, channel:int, mode: str, level):
        """
        mode: HIGH / LOW / OFF
        level: valor numérico/umbral (según el equipo)
        """
        channel = validate_channel(channel)
        mode = normalize_choice(mode, self.HIGH_LOW_MAP)

        if level is None:
            raise CommandError("level no puede ser None")

        self.connection.send(ALARM.SET_ALARM_LEVEL.format(ch=channel, mode=mode, level=level))
        logger.debug(f"[GL-ALARM] Alarm CH{channel} SET -> mode={mode}, level={level}")

    def set_alarm_output(self, mode: str):
        """ mode: ON / OFF """
        mode = normalize_choice(mode, self.ON_OFF_MAP)

        self.connection.send(ALARM.SET_ALARM_OUTPUT.format(mode=mode))
        logger.debug(f"[GL-ALARM] Alarm OUTP -> {mode}")

    def set_alarm_exec(self, mode: str):
        """ mode: ON / OFF """
        mode = normalize_choice(mode, self.ON_OFF_MAP)

        self.connection.send(ALARM.SET_ALARM.format(mode=mode))
        logger.debug(f"[GL-ALARM] Alarm EXEC -> {mode}")

    # =========================================================
    # GETTERS
    # =========================================================
    def get_alarm_mode(self):
        return get_last_token(self.connection.query(ALARM.GET_ALARM_MODE))
    
    def get_alarm_status(self, ch):
        ch = validate_channel(ch)
        return get_last_token(self.connection.query(ALARM.GET_ALARM_STATUS.format(ch=ch)))

    def get_alarm_level(self, ch):
        ch = validate_channel(ch)
        return get_last_token(self.connection.query(ALARM.GET_ALARM_LEVEL.format(ch=ch)))

    def get_alarm_exec(self):
        return get_last_token(self.connection.query(ALARM.GET_ALARM))

    def get_alarm_output(self):
        return get_last_token(self.connection.query(ALARM.GET_ALARM_OUTPUT))
