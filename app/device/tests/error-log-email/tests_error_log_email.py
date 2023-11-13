from django.test import TestCase

import json

from datetime import datetime, timedelta

from device.models import Device, DeviceMeasuredParameter

from device.utils import UpdatedDayStatisticsManager
from device.models import MadeDetails, Measurement, TimeWork, DayStatistics

from django.core import mail
from device.utils import EmailErrorLog

class EmailErrorLogTestCase(TestCase):
    
    
    
    
    def setUp(self) -> None:
        self._device = Device.objects.create(mac_address="ESP-82-66")
        self._today = datetime.now()
        
        
        for param in ["temperature", "pressure"]:
            DeviceMeasuredParameter.objects.create(
                device=self._device,
                measured_parameter=param,
                max_value=100,
                min_value=20)
                
        self._measurement_with_error = Measurement.objects.create(device=self._device,
                                   values={"temperature": 101, "pressure": 102},
                                   dispatch_time=self._today)
        
        self._measurement_without_error = Measurement.objects.create(device=self._device,
                                   values={"temperature": 50, "pressure": 50},
                                   dispatch_time=self._today)
    
    
    def test_measurement_with_error(self):
        result = EmailErrorLog(self._device,
                               self._measurement_with_error).send()
        self.assertTrue(result != -1)
        self.assertTrue(mail.outbox[0].body)
        
    
    def test_measurement_without_error(self):
        result = EmailErrorLog(self._device,
                               self._measurement_without_error).send()
        self.assertTrue(result == -1)
        self.assertTrue(len(mail.outbox) == 0)
        