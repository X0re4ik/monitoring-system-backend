from typing import Type, List, Optional

from django.test import TestCase
from django.urls import reverse, resolve
from django.utils.http import urlencode

# Create your tests here.

from device.models import Device

from .models import ErrorLogDevice, ErrorLogMachine, AbstractErrorLog
from .views import ErrorLogDeviceListAPI, ErrorLogMachineListAPI



class AbstractErrorLogAPITestCase(TestCase):
    url: str = None
    view_name: None
    api_class: Type[ErrorLogDevice] = None

class ErrorLogDeviceAPITestCase(AbstractErrorLogAPITestCase):
    
    url: str = '/api/v1/errorlog/device'
    view_name: str = 'error-log-device-list'
    api_class: Type[ErrorLogDevice] = ErrorLogDeviceListAPI
    
    def setUp(self) -> None:
        self._devices: List[Device] = []
        
        for i in range(5):
            self._devices.append(
                Device.objects.create(
                    mac_address=f"ESP-{i}",
                    ip='192.167.87.1',))
        
        for i, device in enumerate(self._devices):
            ErrorLogDevice.objects.create(
                is_critical=(i%2==0),
                description="Что-то сломалось",
                device=device
            )
    
    def _reverse_with_query_string(self, query: Optional[dict]) -> str:
        url = reverse(self.view_name)
        if query: return url + f"?{urlencode(query)}"
        return url
    
    def test_get(self):
        response = self.client.get(self.url, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 5)
    
    
    def test_get_with_query_string(self):
        _url = self._reverse_with_query_string({"is_critical": True})
        response = self.client.get(_url, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertEqual(len(data), 3)
