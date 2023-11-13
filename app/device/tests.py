import random
from typing import Type, List

from django.test import TestCase
from django.urls import reverse, resolve
from django.utils.http import urlencode

from machine.models import TypeMachine, Machine

from .models import Device
from .serializers import DeviceSerializer
from .views import DeviceCreateAPI, DeviceRetrieveUpdateDestroyAPI



class DeviceCreateAPITestCase(TestCase):

    url: str = '/api/v1/device/create'
    view_name: str = 'create-device'
    api_class: Type[DeviceCreateAPI] = DeviceCreateAPI
    
    def setUp(self) -> None:
        self._machines = []
        
        for i in range(5):
            self._machines.append(
                Machine.objects.create(
                    name="Станочик который съел деда",
                    type=TypeMachine.MILLING,
                    is_cnc=False))
    
    
    def test_route(self):
        self.assertEqual(reverse('create-device'), self.url)
        res = resolve(self.url)
        self.assertEqual(res.view_name, self.view_name)
        self.assertEqual(res.func.cls, self.api_class)
    
    
    def test_create(self):
        random_machine = random.choice(self._machines)
        payload = {
            "machine": random_machine.id,
            "mac_address": "ESP8266:45UT:65FD:43DF"
        }
        response = self.client.post(self.url, data=payload, content_type="application/json")
        self.assertEqual(response.status_code, 201)
        
        data = response.json()
        self.assertEqual(data["delta"], 2)
        self.assertEqual(data["machine"], random_machine.id)
        self.assertEqual(data["mac_address"], "ESP8266:45UT:65FD:43DF")



class DeviceRetrieveUpdateDestroyAPITestCase(TestCase):
    
    url: str = '/api/v1/device'
    view_name: str = 'update-get-delete-device'
    api_class: Type[DeviceCreateAPI] = DeviceCreateAPI
    
    def setUp(self) -> None:
        self._machines: List[Machine] = []
        
        for _ in range(5):
            self._machines.append(
                Machine.objects.create(
                    name="Станочик который съел деда",
                    type=TypeMachine.MILLING,
                    is_cnc=False))
        
        
        for _, machine in enumerate(self._machines):
            Device.objects.create(
                mac_address=f"ESP8266-{machine.id}",
                machine=machine,
                ip='127.177.98.64'
            )
    
    
    def test_get(self):
        random_machine = random.choice(self._machines)
        random_machine.is_cnc = True
        random_machine.save()
        
        _url = self.url + f'/ESP8266-{random_machine.id}'
        response = self.client.get(_url, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertTrue(data["machine"])
        self.assertEqual(data["machine"], random_machine.id)

        
