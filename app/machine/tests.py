from django.test import TestCase

# Create your tests here.
from django.urls import reverse, resolve
from django.utils.http import urlencode

from .models import Machine, LimitValue, NormDetail, TypeMachine
from .serializers import MachineSerializer, NormDetailSerializer, LimitValueSerializer




class MachineAPITestCase(TestCase):
    
    url_create: str = '/api/v1/machine/create'
    url_get_update_delete: str = '/api/v1/machine'
    
    def setUp(self) -> None:
        self._machine = Machine.objects.create(
            name="Станочик который съел деда",
            type=TypeMachine.MILLING,
            is_cnc=False)
    
    
    def test_create_route(self):
        self.assertEqual(reverse('create-machine'), self.url_create)
        res = resolve(self.url_create)
        self.assertEqual(res.view_name, 'create-machine')
    
    def test_get_update_delete_route(self):
        pass
        #self.assertEqual(reverse('update-get-delete-machine'), self.url_get_update_delete)
        # res = resolve(self.url_get_update_delete)
        # self.assertEqual(res.view_name, 'update-get-delete-machine')
        
    def test_get(self):
        response = self.client.get(self.url_get_update_delete + f'/{self._machine.pk}')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertFalse(data["is_cnc"])
        self.assertEqual(data["type"], "MILLING")
    
    
    def test_patch(self):
        payload = {
            "name": "16K20",
        }
        _url = self.url_get_update_delete + f'/{self._machine.pk}'
        res = self.client.patch(_url, data=payload, content_type="application/json")
        self.assertEqual(res.status_code, 200)
        
        response = self.client.get(self.url_get_update_delete + f'/{self._machine.pk}')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertFalse(data["is_cnc"])
        self.assertEqual(data["name"], "16K20")
    
    def test_create(self):
        payload = {
            "name": "Станочик который съел дед23а",
            "type": TypeMachine.MILLING,
            "is_cnc": True,
        }
        response = self.client.post(self.url_create, data=payload, content_type="application/json")
        self.assertEqual(response.status_code, 201)
        
        data = response.json()
        self.assertTrue(data["is_cnc"])
        self.assertEqual(data["type"], TypeMachine.MILLING)
        self.assertEqual(data["name"], "Станочик который съел дед23а")
        
        
        
        