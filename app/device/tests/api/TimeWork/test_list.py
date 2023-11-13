from typing import Dict, List, Optional

from django.test import TestCase
from django.urls import reverse, resolve
from django.utils.http import urlencode

from device.models import Device, DeviceMeasuredParameter, TimeWork
from datetime import datetime, timedelta

class MeasurementCreateAPITestCase(TestCase):
    
    URL: str = "/api/v1/device/time_work/statistics"
    
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
        
        for i in range(5):
            start_work = datetime(2023, 8, 23, 13+i)
            end_work = start_work + timedelta(hours=1)
            TimeWork.objects.create(device=self._device1,
                                    start_work=start_work,
                                    end_work=end_work)
        
        
        for i in range(5):
            start_work = datetime(2023, 8, 24, 13+i)
            end_work = start_work + timedelta(hours=1)
            TimeWork.objects.create(device=self._device1,
                                    start_work=start_work,
                                    end_work=end_work)
        
        
        """Создаем устройство №2. Задаем ему определенные параметры"""
        self._device2 = Device.objects.create(
            mac_address="ESP-82-66:2",
            delta=2)
        
        _measured_parameters2 = ["temperature"]
        for measured_parameter in _measured_parameters2:
            DeviceMeasuredParameter.objects.create(device=self._device2,
                                                   measured_parameter=measured_parameter, 
                                                   max_value=100, min_value=0)
            
        for i in range(2):
            start_work = datetime(2023, 8, 23, 13+i)
            end_work = start_work + timedelta(hours=1)
            TimeWork.objects.create(device=self._device2,
                                    start_work=start_work,
                                    end_work=end_work)
    
    def test_get_device_1(self):
        """Тестирование API и фильтров для первого устройства"""
        url = self._url_with_query_string({
            "device": "ESP-82-66:1",
            "date": datetime(2023, 8, 23).date()
        })
        print(url)
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        """У устройства `ESP-82-66:1` только 5 измеряемых параметра"""
        self.assertEqual(len(response.json()), 5)

        