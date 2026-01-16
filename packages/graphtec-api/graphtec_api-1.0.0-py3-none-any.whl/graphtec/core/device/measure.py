from graphtec.core.device.base import BaseModule
from graphtec.core.commands import MEAS
from graphtec.core.exceptions import CommandError, ResponseError
from graphtec.utils import get_last_token
import logging
logger = logging.getLogger(__name__)

class MeasureModule(BaseModule):
    """Grupo MEAS: Ajustes de medición"""
    # -------------------------
    # Helpers
    # -------------------------
    @staticmethod
    def _to_str(response):
        if response is None:
            return ""
        if isinstance(response, (bytes, bytearray)):
            return response.decode(errors="replace").strip()
        return str(response).strip()


    def start_measurement(self):
        self.connection.send(MEAS.START_MEASUREMENT)
        logger.debug("[GL-MEAS] Iniciando medición...")

    def stop_measurement(self):
        self.connection.send(MEAS.STOP_MEASUREMENT)
        logger.debug("[GL-MEAS] Medición detenida.")

    def read_once(self):
        response = self.connection.query(MEAS.READ_ONCE)
        return response
    
    def get_meas_time(self):
        response = self.connection.query(MEAS.GET_MEASUREMENT_TIME)
        text = self._to_str(response)
        if not text:
            raise ResponseError(f"Sin respuesta a Tiempo de medición")
        return get_last_token(text)
    
    def get_capture_points(self):
        response = self.connection.query(MEAS.GET_CAPTURE_POINTS)
        text = self._to_str(response)
        if not text:
            raise ResponseError(f"Sin respuesta a Tiempo de medición")
        return get_last_token(text)