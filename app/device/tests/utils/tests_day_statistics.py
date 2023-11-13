from django.test import TestCase

import json

from datetime import datetime, timedelta

from device.models import Device, DeviceMeasuredParameter

from device.utils import UpdatedDayStatisticsManager
from device.models import MadeDetails, Measurement, TimeWork, DayStatistics



class UpdatedDayStatisticsManagerTestCase(TestCase):
    
    
    def setUp(self) -> None:
        self._device = Device.objects.create(mac_address="ESP-82-66")
        self._today = datetime.now()
        
        
        for param in ["temperature", "pressure"]:
            DeviceMeasuredParameter.objects.create(
                device=self._device,
                measured_parameter=param,
                max_value=1010,
                min_value=20)
        
        for _ in range(2):
            MadeDetails.objects.create(
                device=self._device,
                qty_good_details=10,
                qty_bad_details=5,
                dispatch_time=self._today)
        
        
        for i in range(5):
            Measurement.objects.create(
                device=self._device,
                values={
                    "temperature": 100+i,
                    "pressure": 100-i
                },
                dispatch_time=self._today)
        
        
        for i in range(5):
            TimeWork.objects.create(
                device=self._device,
                start_work=self._today-timedelta(hours=i+1),
                end_work=self._today-timedelta(hours=i))
    
    def test_simple_update_day_statistic(self):
        UpdatedDayStatisticsManager(self._device, self._today).fit()
        
        self.assertTrue(DayStatistics.objects.exists())
        ds = DayStatistics.objects.filter(device=self._device, date=self._today).first()
        self.assertFalse(ds is None)
        
        
        self.assertEqual(ds.qty_good_details, 20)
        self.assertEqual(ds.qty_bad_details, 10)
        self.assertEqual(set(ds.average_values.keys()), {"temperature", "pressure"})
        self.assertEqual(set(ds.max_values.keys()), {"temperature", "pressure"})
        self.assertEqual(ds.time_work, timedelta(hours=5))
        
        
        
        
        
        
            
        