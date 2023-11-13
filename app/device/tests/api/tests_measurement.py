from django.test import TestCase

import json

from device.models import Device, DeviceMeasuredParameter


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
    
    def test_simple_create(self):
        """
        Простое добавление измерений без ошибок
        """
        
        payload = {
            "device": self._device.mac_address,
            "values": json.dumps({
                "temperature": 23,
                "humidity": 56,
                "pressure": 78
            }),
            "dispatch_time": "2023-11-04T08:46:17-0000"
        }
        response = self.client.post(path=self.URL,
                                    data=payload)
        self.assertEqual(response.status_code, 201)
        
    
    def test_in_values_extra_item(self):
        """
        Один из параметров ключа `values` не соответсвует схеме
        """
        
        payload = {
            "device": self._device.mac_address,
            "values": json.dumps({
                "temperature": 23,
                "humidity": 56,
                "pressure": 78,
                "extra": 0
            }),
            "dispatch_time": "2023-11-04T08:46:17-0000"
        }
        response = self.client.post(path=self.URL,
                                    data=payload)
        
        self.assertEqual(response.status_code, 400)
        self.assertTrue(response.json()["non_field_errors"])
        
        