from typing import Dict, List, Optional

from django.test import TestCase
from django.urls import reverse, resolve
from django.utils.http import urlencode

from device.models import Device, DeviceMeasuredParameter

class MeasurementCreateAPITestCase(TestCase):
    
    URL: str = "/api/v1/device/parameters"
    
    def _url_with_query_string(self, query: Optional[Dict[str, str]]) -> str:
        if query: return self.URL + f"?{urlencode(query)}"
        return self.URL
    
    def setUp(self) -> None:
        
        """Создаем устройство №1. Задаем ему определенные параметры"""
        self._device1 = Device.objects.create(
            mac_address="ESP-82-66:1",
            delta=2)
        
        _measured_parameters1 = ["temperature", "humidity", "pressure"]
        for measured_parameter in _measured_parameters1:
            DeviceMeasuredParameter.objects.create(device=self._device1,
                                                   measured_parameter=measured_parameter, 
                                                   max_value=100, min_value=0)
        
        
        """Создаем устройство №2. Задаем ему определенные параметры"""
        self._device2 = Device.objects.create(
            mac_address="ESP-82-66:2",
            delta=2)
        
        _measured_parameters2 = ["temperature"]
        for measured_parameter in _measured_parameters2:
            DeviceMeasuredParameter.objects.create(device=self._device2,
                                                   measured_parameter=measured_parameter, 
                                                   max_value=100, min_value=0)
    
    def test_get_device_1(self):
        """Тестирование API и фильтров для первого устройства"""
        url = self._url_with_query_string({
            "device": "ESP-82-66:1"
        })
        
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        """У устройства `ESP-82-66:1` только 3 измеряемых параметра"""
        self.assertEqual(len(response.json()), 3)
        
    def test_get_device_2(self):
        """Тестирование API и фильтров для первого устройства"""
        url = self._url_with_query_string({
            "device": "ESP-82-66:2"
        })
        
        response = self.client.get(url)
        print(response.json())
        self.assertEqual(response.status_code, 200)
        """У устройства `ESP-82-66:2` только 1 измеряемых параметра"""
        self.assertEqual(len(response.json()), 1)

        