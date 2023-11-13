import time

from statistics import mean
from typing import Optional, Dict, Type, Tuple
from datetime import date, timedelta, datetime

from django.db.models import Sum
from django.db.models import QuerySet

from device.models import (DayStatistics, MadeDetails, 
                           Measurement, TimeWork, 
                           Device, DeviceMeasuredParameter)


class UpdatedDayStatisticsManager:
    """
    Обнрвление дневной статистики устройства
    """
    
    def __init__(self, 
                 device: Device, 
                 today: date = date.today()) -> None:
        self._device = device
        self._today = today
        
        self._update()
        
    
    def fit(self):
        self.update_made_details()
        self.update_time_work()
        self.update_measurements()
    
    
    def update_made_details(self):
        """
        Обновление количества деталей
        """
        made_details = self._get_objects(MadeDetails)
        results = made_details.aggregate(qty_good_details=Sum("qty_good_details", default=0), 
                                         qty_bad_details=Sum("qty_bad_details", default=0))
        self._update(results) 
            
            
    def update_time_work(self):
        """
        Обновление статистики по количеству времени работы оборудования
        """
        times_work =TimeWork.objects.filter(device=self._device, start_work__date=self._today).all()
        
        sum_timedelta = timedelta(seconds=0)
        for time_work in times_work:
            sum_timedelta += time_work.end_work - time_work.start_work
            
        self._update({"time_work": sum_timedelta})
    
    def update_measurements(self):
        """
        Обновление статистики по максимальным и средним показаниям с устройства
        """
        
        measured_parameters = DeviceMeasuredParameter.objects.get_measured_parameters(self._device)
        values = self._get_objects(Measurement).all().values_list("values", flat=True)
        
        max_values: Dict[str, float] = {}
        average_values: Dict[str, float] = {}
        for measured_parameter in measured_parameters:
            max_values[measured_parameter] = max(values, key=lambda data: data[measured_parameter])[measured_parameter]
            average_values[measured_parameter] = mean([value[measured_parameter] for value in values])
            
        self._update({"max_values": max_values,
                      "average_values": average_values})
            
    
    def _update(self, results: dict = {}):
        ob, _ = DayStatistics.objects.update_or_create(device=self._device, 
                                                       date=self._today, 
                                                       defaults=results)
        return ob
        
    def _get_objects(self, type_: Type) -> "QuerySet[Type]":
        return type_.objects.filter(device=self._device, 
                                    dispatch_time__date=self._today)


def update_statistics_by_day():
    for device in Device.objects.all():
        update_manager = UpdatedDayStatisticsManager(device)
        update_manager.fit()



from machine.models import Machine
from django.core.mail import EmailMessage

from django.core import mail
from django.test import TestCase
from app.settings import EMAIL_HOST_USER

class EmailErrorLog:
    
    def __init__(self, 
                 device: Device, 
                 measurement: Measurement):
        
        self._machine: Machine = device.machine
        self._device: Device = device
        self._measurement: Measurement = measurement
        
        self._company_email = "xoore4ik@gmail.com" # Надо откудата брать
        
        self._parameters = list(DeviceMeasuredParameter.objects.filter(device=self._device)\
            .all().values_list("measured_parameter", flat=True))
    
    
    def get_min_max_current_values(self, parameter: str) -> Tuple[float, float, float]:
        """Получить минимальное, максимальное и текущее значение параметра

        Args:
            parameter (str): наименование параметра

        Returns:
            Tuple[float, float, float]: мин. макс. текущее значения
        """
        values = self._measurement.values
        
        value = values[parameter]
        min_limit_value = DeviceMeasuredParameter.objects.get(device=self._device, 
                                                              measured_parameter=parameter).min_value
        max_limit_value = DeviceMeasuredParameter.objects.get(device=self._device, 
                                                              measured_parameter=parameter).max_value
        return (min_limit_value, max_limit_value, value)
    
    def is_critical(self, parameter: str) -> bool:
        """Значение по параметру критическое?

        Args:
            parameter (str): наименование параметра

        Returns:
            bool: параметр критичен
        """
        (min_limit_value, max_limit_value, value) = self.get_min_max_current_values(parameter)
        return not (min_limit_value <= value <= max_limit_value)
    
    def report(self, parameter: str) -> Optional[str]:
        if self.is_critical(parameter):
            (min_limit_value, max_limit_value, value) = self.get_min_max_current_values(parameter)
            return f"Параметр '{parameter}' не соответсвует условию: {min_limit_value} <= {value} <= {max_limit_value}"
        return None
    
    
    def send(self) -> int:
        errors = []
        for parameter in self._parameters:
            report = self.report(parameter)
            if report: errors.append(report)
        
        if len(errors):
            return mail.send_mail(
                "Сообщение об ошибке!",
                '\n'.join(errors),
                EMAIL_HOST_USER,
                [self._company_email])
        return -1
    
           