from typing import Optional, Tuple, List, Dict

from .models import ErrorLogDevice
from device.models import Device, Measurement, DeviceMeasuredParameter




class ErrorLogDeviceWriter:
    
    def __init__(self, measurement: "Measurement") -> None:
        self._measurement = measurement
        
        self._device: Device = measurement.device
        self._values: Dict[str, float] = measurement.values
        
        self._dmparametrs = DeviceMeasuredParameter.objects.filter(device=self._device).all()
    
    def get_error_params(self,) -> List[str]:
        """
        Returns:
            List[str]: список параметров, которые не соответсвуют условию
        """
        error_params = []
        for dmp in self._dmparametrs:
            parametr = dmp.measured_parameter
            value = self._values[parametr]
            if dmp.is_critical(value):
                error_params.append(parametr)
        return error_params
    
    def write_errors_to_error_log_if_exist(self,) -> int:
        """Записать ошибки в модель `ErrorLogDevice`

        Returns:
            int: количество записанных ошибок
        """
         
        error_params = self.get_error_params()
        for error_param in error_params:
            dmp = DeviceMeasuredParameter.objects.filter(device=self._device,
                                                         measured_parameter=error_param).first()
            current_value = self._values[error_param]
            min_max_cur_values = (dmp.min_value, dmp.max_value, current_value)
            description = self.report(error_param, min_max_cur_values)
            ErrorLogDevice.objects.create(device=self._device,
                                          description=description,
                                          is_critical=True, 
                                          is_sent=False,)
        return len(error_params)
    
    def report(self, error_param: str, min_max_cur_values: Tuple[float, float, float]) -> str:
        """_summary_

        Args:
            error_param (str): нименование параметра
            min_max_cur_values (Tuple[float, float, float]): минимальное, максимальное, текущее значение

        Returns:
            str: текст ошибки
        """
        min_value, max_value, current_value = min_max_cur_values
        return f"Параметр '{error_param}' не соответсвует условию: {min_value} < {current_value} < {max_value}"
    
    
    
        