from graphtec.core.device.base import BaseModule
from graphtec.core.commands import AMP
from graphtec.core.exceptions import CommandError
from graphtec.utils.utils import get_last_token,validate_channel,normalize_choice, validate_range
import logging
from types import MappingProxyType

logger = logging.getLogger(__name__)



class AmpModule(BaseModule):
    """Grupo AMP: Configuración de canales analógicos del GL100."""

    # =========================================================
    # MAPEO
    # =========================================================

    # Tipos de entrada disponibles por tipo de sensor
    TIPOS_ENTRADA = {
        "VT": ["OFF", "TEMP", "DC_V"], # Módulo GS-4VT
        "TSR": ["OFF", "TEMP"], # Módulo GS-4TSR
        "AC": ["AC1_2", "AC1_3", "AC3_3"], # Módulo GS-DPA-AC
        "TH":[], # Módulo GS-TH
        "AT":[], # Módulo GS-3AT
        "LU":[], # Módulo GS-LU
        "CO2":[], # Módulo GS-CO2
        "CO2_TH":[], # Módulo GS-CO2-TH
        "CO2_LU":[], # Módulo GS-CO2-LU
        "LU_TH":[] # Módulo GS-LU-TH
    }

    #Rangos compatibles por tipo de entrada
    RANGOS_COMPATIBLES = {
    "DC_V": ["NONE","20MV", "50MV", "100MV", "200MV", "500MV", "1V", "2V", "5V", "10V", "20V", "50V","1_5V"],
    "TEMP": ["NONE","TCK", "TCT"],
    "LXUV": ["NONE","2000LX", "20000LX","200000LX"],
    "ACC": ["NONE","2G", "5G", "10G","20MPSS","50MPSS","100MPSS"],
    "AC": ["OFF","50A", "100A", "200A"]
    }

    # Opciones de clampeo
    CLAMP_OPTIONS = {"AC1_2", "AC1_3", "AC3_3"}
    CLAMP_VOLTAGE_RANGE = [90, 264]  # Rango de Voltaje para clampeo
    CLAMP_PF_RANGE = [0.3, 1.0]  # Rango de Factor de Potencia para clampeo

    # Opciones de conteo
    COUNT_OPTION_MAP = MappingProxyType({
        "HI": "HI", "HIGH": "HI","UP":"HI","H":"HI",
        "LO": "LO", "LOW": "LO","DOWN":"LO","L":"LO",
        })
    COUNT_C_RANGE = [-20, 85]  # Rango de umbral en °C
    COUNT_F_RANGE = [-4, 185]  # Rango de umbral en °F

    CALIBRATION_ON_OFF_MAP = MappingProxyType({
        "ON":"ON", "1":"ON", "TRUE":"ON","ENABLE":"ON",
        "OFF":"OFF","NONE":"OFF", "0":"OFF", "FALSE":"OFF","DISABLE":"OFF",
    })
   

    def __init__(self, device):
        super().__init__(device)
        self.channels = {ch: {"type": "", "input": "", "range": ""} for ch in range(1, 5)}
        logger.debug("[GL-AMP] Módulo de canales inicializado.")

    
    # =========================================================
    # SETTERS
    # =========================================================
    def set_channel(self, channel: int, ch_input: str, ch_range: str):
        channel = validate_channel(channel)
        if ch_input:
            self.device.amp.set_channel_input(channel=channel,ch_input=ch_input)
        if ch_range:
            self.device.amp.set_channel_range(channel=channel,ch_range=ch_range)

        return self.device.amp.get_channel(channel)

    def set_channel_input(self, channel: int, ch_input: str):
        channel = validate_channel(channel)
        tipo_actual = self.channels[channel]["type"]
        # Si no hemos consultado tipo todavía, primero lo obtenenemos
        if tipo_actual == "":
            tipo_actual = self.get_channel_type(channel)

        if self._validate_type(tipo_actual, ch_input):
            cmd = AMP.SET_CHANNEL_INPUT.format(ch=channel, mode=ch_input)
            self.connection.send(cmd)
            self.channels[channel]["input"] = ch_input
            logger.debug(f"[GL-AMP] CH{channel} INPUT <- {ch_input}")
        else:
            raise CommandError(f"Modo de entrada inválido para CH{channel}: {ch_input} no es compatible con el tipo {self.channels[channel]['type']}")

    def set_channel_range(self, channel: int, ch_range: str):
        channel = validate_channel(channel)
        modo_actual = self.channels[channel]["input"]
        # Si no hemos consultado el modo todavía, primero lo obtenenemos
        if modo_actual == "":
            modo_actual = self.get_channel_input(channel)

        if self._validate_range(modo_actual, ch_range):
            cmd = AMP.SET_CHANNEL_RANGE.format(ch=channel, value=ch_range)
            self.connection.send(cmd)
            self.channels[channel]["range"] = ch_range
            logger.debug(f"[GL-AMP] CH{channel} RANGE <- {ch_range}")
        else:
            raise CommandError(f"Configuración inválida para CH{channel}: {modo_actual} no es compatible con {ch_range}")

    def set_clamp(self, channel: int, mode: str|None=None, voltage: int|None=None, power_factor: float|None=None):
        channel = validate_channel(channel)

        if mode is not None:
            self.set_clamp_channel(channel, mode)
            logger.debug(f"[GL-AMP] CH{channel} CLAMP -> {mode}")

        if voltage is not None:
            self.set_clamp_voltage(channel, voltage)
            logger.debug(f"[GL-AMP] CH{channel} CLAMP VOLTAGE -> {voltage}V")

        if power_factor is not None:
            self.set_clamp_pf(channel, power_factor)
            logger.debug(f"[GL-AMP] CH{channel} CLAMP PF -> {power_factor}")

    def set_clamp_channel(self, channel: int, mode: str):
        channel = validate_channel(channel)
        mode = normalize_choice(mode,self.CLAMP_OPTIONS)

        cmd = AMP.SET_CHANNEL_CLAMP.format(ch=channel, mode=mode)
        self.connection.send(cmd)
        logger.debug(f"[GL-AMP] CH{channel} CLAMP -> {mode}")

    def set_clamp_voltage(self, channel: int, voltage: int):
        channel = validate_channel(channel)
        volt = validate_range(voltage, int, self.CLAMP_VOLTAGE_RANGE[0], self.CLAMP_VOLTAGE_RANGE[1])

        cmd = AMP.SET_CLAMP_VOLTAGE_REF.format(n=channel, value=volt)
        self.connection.send(cmd)
        logger.debug(f"[GL-AMP] CH{channel} CLAMP VOLTAGE -> {volt}V")

    def set_clamp_pf(self, channel: int, power_factor: float):
        channel = validate_channel(channel)
        pf = validate_range(power_factor, float, self.CLAMP_PF_RANGE[0], self.CLAMP_PF_RANGE[1])

        cmd = AMP.SET_CHANNEL_PF.format(n=channel, value=pf)
        self.connection.send(cmd)
        logger.debug(f"[GL-AMP] CH{channel} CLAMP PF -> {pf}")

    def set_accelerometer_calibration(self, channel: int, mode: str):
        """ mode: ON / OFF """
        channel = validate_channel(channel)
        mode = normalize_choice(mode,self.CALIBRATION_ON_OFF_MAP)
        
        cmd = AMP.SET_CHANNEL_ACC_CALIBRATE.format(n=channel, mode=mode)
        self.connection.send(cmd)
        logger.debug(f"[GL-AMP] CH{channel} ACC CALIBRATION -> {mode}")

    def execute_accelerometer_calibration(self, channel: int):
        channel = validate_channel(channel)
        cmd = AMP.SET_CHANNEL_ACC_CALIBRATE_EXEC.format(n=channel)

        self.connection.send(cmd)
        logger.debug(f"[GL-AMP] CH{channel} ACC CALIBRATION EXECUTED")

    def set_co2_calibration(self, channel: int, mode: str):
        """ mode: ON / OFF """
        channel = validate_channel(channel)
        mode = normalize_choice(mode,self.CALIBRATION_ON_OFF_MAP)

        cmd = AMP.SET_CHANNEL_CO2_CALIBRATE.format(n=channel, mode=mode)
        self.connection.send(cmd)
        logger.debug(f"[GL-AMP] CH{channel} CO2 CALIBRATION -> {mode}")

    def set_accumulator_count(self, channel: int, mode: str, value: int,temp_unit:str='C'):
        """
        mode: HI / LO 
        value: Nivel de umbral
        temp_unit: 'C' o 'F' (unidad de temperatura para el umbral)
        """
        channel = validate_channel(channel)
        mode = normalize_choice(mode,self.COUNT_OPTION_MAP)

        if temp_unit == 'C':
            temp_value = validate_range(value, int, self.COUNT_C_RANGE[0], self.COUNT_C_RANGE[1])
        elif temp_unit == 'F':
            temp_value = validate_range(value, int, self.COUNT_F_RANGE[0], self.COUNT_F_RANGE[1])
        else:
            raise CommandError(f"Unidad de temperatura inválida: {temp_unit} (válidos: 'C', 'F')") # Tristemente obligado por pylance, en tiempo de ejecución no se puede dar este caso

        cmd = AMP.SET_CHANNEL_COUNT.format(ch=channel, mode=mode, value=temp_value)
        self.connection.send(cmd)
        logger.debug(f"[GL-AMP] CH{channel} ACCUMULATOR COUNT -> {mode} {temp_value}")

    # =========================================================
    # GETTERS
    # =========================================================

    def get_channels(self) -> dict:
        """Devuelve la configuración actual de todos los canales."""
        for ch in range(1, 5):
            self.get_channel(ch)
        return self.channels

    def get_channel(self,channel:int) -> dict:
        """Devuelve la configuración actual de un canal específico."""
        channel = validate_channel(channel)

        ch_type = self.get_channel_type(channel)
        ch_input = self.get_channel_input(channel)
        ch_range = self.get_channel_range(channel)

        self.channels[channel]["type"] = ch_type
        self.channels[channel]["input"] = ch_input
        self.channels[channel]["range"] = ch_range

        logger.info(f"[GL-AMP] CH{channel} - TYPE: {ch_type}, INPUT: {ch_input}, RANGE: {ch_range}")

        return self.channels[channel]

    def get_channel_type(self,channel:int):
        channel = validate_channel(channel)
        cmd = AMP.GET_CHANNEL_TYPE.format(ch=channel)
        resp = self.connection.query(cmd)
        response = get_last_token(resp)
        return response

    def get_channel_input(self,channel:int):
        channel = validate_channel(channel)
        cmd = AMP.GET_CHANNEL_INPUT.format(ch=channel)
        resp = self.connection.query(cmd)
        response = get_last_token(resp.decode().strip())
        return response

    def get_channel_range(self,channel:int):
        channel = validate_channel(channel)
        cmd = AMP.GET_CHANNEL_RANGE.format(ch=channel)
        resp = self.connection.query(cmd)
        response = get_last_token(resp.decode().strip())
        return response

    def get_clamps(self):
        clamps = {}
        for ch in range(1, 5):
            clamps[ch] = {
                "mode": self.get_channel_clamp(ch),
                "voltage": self.get_clamp_voltage(ch),
                "power_factor": self.get_clamp_pf(ch)
            }
        return clamps

    def get_clamp(self, channel: int):
        channel = validate_channel(channel)
        return {
            "mode": self.get_channel_clamp(channel),
            "voltage": self.get_clamp_voltage(channel),
            "power_factor": self.get_clamp_pf(channel)
        }

    def get_channel_clamp(self, channel: int):
        channel = validate_channel(channel)
        cmd = AMP.GET_CHANNEL_CLAMP.format(ch=channel)
        resp = self.connection.query(cmd)
        response = get_last_token(resp.decode().strip())
        return response

    def get_clamp_voltage(self, channel: int):
        channel = validate_channel(channel)
        cmd = AMP.GET_CLAMP_VOLTAGE_REF.format(ch=channel)
        resp = self.connection.query(cmd)
        response = get_last_token(resp.decode().strip())
        return response

    def get_clamp_pf(self, channel: int):
        channel = validate_channel(channel)
        cmd = AMP.GET_CHANNEL_PF.format(ch=channel)
        resp = self.connection.query(cmd)
        response = get_last_token(resp.decode().strip())
        return response

    def get_accelerometer_calibration(self, channel: int):
        channel = validate_channel(channel)
        cmd = AMP.GET_CHANNEL_ACC_CALIBRATE.format(ch=channel)
        resp = self.connection.query(cmd)
        response = get_last_token(resp.decode().strip())
        return response

    def get_co2_calibration(self, channel: int):
        channel = validate_channel(channel)
        cmd = AMP.GET_CHANNEL_CO2_CALIBRATE.format(ch=channel)
        resp = self.connection.query(cmd)
        response = get_last_token(resp.decode().strip())
        return response

    def get_accumulator_count(self, channel: int):
        channel = validate_channel(channel)
        cmd = AMP.GET_CHANNEL_COUNT.format(ch=channel)
        resp = self.connection.query(cmd)
        response = get_last_token(resp.decode().strip())
        return response


    # =========================================================
    # UTILIDAD INTERNA
    # =========================================================

    def _validate_range(self, mode: str, value: str):
        """Verifica si el rango es compatible con el tipo de entrada."""
        if mode in self.RANGOS_COMPATIBLES:
            if value not in self.RANGOS_COMPATIBLES[mode]:
                logger.error(f"[GL-AMP] Error: {value} no es compatible con el modo {mode}")
                return False
        return True

    def _validate_type(self, ch_type: str, ch_input: str):
        """Verifica si el tipo de entrada es compatible con el tipo de sensor."""
        if ch_type in self.TIPOS_ENTRADA:
            if ch_input not in self.TIPOS_ENTRADA[ch_type]:
                logger.error(f"[GL-AMP] Error: {ch_input} no es compatible con el tipo {ch_type}")
                return False
        return True

    def _validate_clamp(self, mode=None, voltage=None, power_factor=None):
        """Verifica si los parámetros de clampeo son válidos."""
        if mode is not None and mode not in self.CLAMP_OPTIONS:
            logger.error(f"[GL-AMP] Error: Fuente de clampeo inválida: {mode}")
            return False
        if voltage is not None and not (self.CLAMP_MIN_VOLTAGE <= voltage <= self.CLAMP_MAX_VOLTAGE):
            logger.error(f"[GL-AMP] Error: Voltaje de clampeo inválido({self.CLAMP_MIN_VOLTAGE}-{self.CLAMP_MAX_VOLTAGE}V): {voltage}V")
            return False
        if power_factor is not None and not (self.CLAMP_MIN_PF <= power_factor <= self.CLAMP_MAX_PF):
            logger.error(f"[GL-AMP] Error: Factor de potencia de clampeo inválido ({self.CLAMP_MIN_PF}-{self.CLAMP_MAX_PF}): {power_factor}")
            return False
        return True
