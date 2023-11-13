import json

from django.test import TestCase
from django.utils import timezone

from device.models import Device, DeviceMeasuredParameter, Measurement

from errorlog.utils import ErrorLogDeviceWriter
from errorlog.models import ErrorLogDevice



class MeasurementCreateAPITestCase(TestCase):
    
    URL: str = "/api/v1/device/measurement/create"
    
    def setUp(self) -> None:
        self._device = Device.objects.create(
            mac_address="ESP-82-66",
            delta=2)
        
        _measured_parameters = ["temperature", "humidity", "pressure"]
        for measured_parameter in _measured_parameters:
            DeviceMeasuredParameter.objects.create(device=self._device,
                                                   measured_parameter=measured_parameter, 
                                                   max_value=100, min_value=0)
            
        self.error_measurement3 = Measurement.objects.create(device=self._device,
                                                       values={
                                                           "temperature": 101,
                                                           "humidity": -1,
                                                           "pressure": 101
                                                       },
                                                       dispatch_time=timezone.now())
        
        self.error_measurement2 = Measurement.objects.create(device=self._device,
                                                       values={
                                                           "temperature": 101,
                                                           "humidity": 50,
                                                           "pressure": 101
                                                       },
                                                       dispatch_time=timezone.now())
        
    def test_error_measurement(self):
        qty_errors3 = ErrorLogDeviceWriter(self.error_measurement3).write_errors_to_error_log_if_exist()
        self.assertEqual(qty_errors3, 3)

        qty_errors2 = ErrorLogDeviceWriter(self.error_measurement2).write_errors_to_error_log_if_exist()
        self.assertEqual(qty_errors2, 2)
        
        self.assertEqual(ErrorLogDevice.objects.count(), 5)