from collections.abc import Iterable
import json

from typing import Dict, Optional, Tuple
from datetime import datetime, timedelta


from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator


from machine.models import Machine
from django.core.mail import EmailMessage

from django.core import mail
from django.test import TestCase
from app.settings import EMAIL_HOST_USER


class Device(models.Model):
    """
    Устройство
    """
    
    mac_address = models.CharField(primary_key=True, verbose_name="Мак адресс устройства")
    
    machine = models.OneToOneField("machine.Machine", 
                                   on_delete=models.CASCADE, 
                                   verbose_name="Связанный станок",
                                   blank=True, null=True)
    
    delta = models.IntegerField(default=2, validators=[MinValueValidator(1), MaxValueValidator(10)], verbose_name="Период измерения")
    
    date_join = models.DateTimeField(default=timezone.now, editable=False, verbose_name="Дата присоединения")
    date_update = models.DateTimeField(auto_now=True, editable=False, verbose_name="Дата обновления")
    
    class Meta:
        verbose_name = "Контроллер"
        verbose_name_plural = "Контроллеры"
        
    def __str__(self) -> str:
         return self.mac_address
        



class DayStatistics(models.Model):
    """
    Таблица дневной статистики по работе датчика
    """
    
    device = models.ForeignKey("Device", 
                               on_delete=models.CASCADE, 
                               verbose_name=Device._meta.verbose_name)
    
    time_work = models.DurationField(verbose_name="Время работы", 
                                     default=timedelta(seconds=0))
    
    qty_good_details = models.IntegerField(verbose_name="Кол-во качественных деталей", default=0)
    qty_bad_details = models.IntegerField(verbose_name="Кол-во плохих деталей", default=0)
    
    max_values = models.JSONField(verbose_name="Максимальное значение", default=dict)
    average_values = models.JSONField(verbose_name="Среднее значение", default=dict)
    
    date = models.DateField(default=timezone.now, verbose_name="Дата")
    
    class Meta:
        verbose_name = "Дневная статистика"
        verbose_name_plural = "Дневные статистики"


class MadeDetails(models.Model):
    """
    Таблица выполненных деталей
    """
    
    device = models.ForeignKey("Device", on_delete=models.CASCADE, verbose_name=Device._meta.verbose_name)
    
    qty_good_details = models.IntegerField(validators=[MinValueValidator(0)], verbose_name="Количество хороших деталей")
    qty_bad_details = models.IntegerField(validators=[MinValueValidator(0)], verbose_name="Количество плохих деталей")
    
    dispatch_time = models.DateTimeField(verbose_name="Время получения данных")
    
    class Meta:
            verbose_name = "Измерение"
            verbose_name_plural = "Измерения"

        
class TimeWork(models.Model):
    """
    Периоды работы оборудования
    """
    
    device = models.ForeignKey("Device", 
                               on_delete=models.CASCADE, 
                               verbose_name=Device._meta.verbose_name)
    
    start_work = models.DateTimeField(verbose_name="Начало работы")
    end_work = models.DateTimeField(verbose_name="Конец работы")
    
    
    @property
    def period(self):
        return self.end_work - self.start_work
    
    class Meta:
            verbose_name = "Измерение"
            verbose_name_plural = "Измерения"

    def save(self, *args, **kwargs) -> None:
        if self.start_work >= self.end_work:
            raise ValueError("end_work must be more that start_work")

        return super().save(*args, **kwargs)
            

class Measurement(models.Model):
    """
    Таблица измерений с датчиков
    """
    
    device = models.ForeignKey("Device", 
                               on_delete=models.CASCADE, 
                               verbose_name=Device._meta.verbose_name)
    
    values = models.JSONField(verbose_name="Результаты измерения")
    
    dispatch_time = models.DateTimeField(verbose_name="Время получения данных")
    
    class Meta:
        verbose_name = "Числовое измерение"
        verbose_name_plural = "Числовые измерения"
         


class MeasuredParameterChoices(models.TextChoices):
    """
    ENUM стандартный параметром измерения
    """
    TEMPERATURE = ("temperature", "температура") 
    PRESSURE = ("pressure", "давление")
    HUMIDITY = ("humidity", "влажность")
    DISPATCH_TIME = ("dispatch_time", "влажность")
    
 
class DeviceMeasuredParameterManager(models.Manager):
    """
    Менеджер для модели `DeviceMeasuredParameter`
    """
    
    def match(self, device: "Device", data: Dict[str, float]) -> bool:
        candidate_keys = set(data.keys())
        device_keys = set(self.get_measured_parameters(device))
        return device_keys == candidate_keys
    
    def get_measured_parameters(self, device: "Device"):
        measured_parameters = self.filter(device=device).all()
        return measured_parameters.values_list("measured_parameter", flat=True)
    
    def get_limit_min_max(self, device: "Device", parameter: str) -> Tuple[float, float]:
        """Получить предельные значения параметра `parameter` устройства `device` 

        Args:
            device (Device): устройство
            parameter (str): параметр

        Returns:
            Tuple[float, float]: минимальное и максимальное значения
        """
        dmp = DeviceMeasuredParameter.objects.get(device=self.device, measured_parameter=parameter)
        return (dmp.min_value, dmp.max_value)


class DeviceMeasuredParameter(models.Model):
    """
    Схема соотношения измеряемого параметра у устройства
    """
    
    objects = DeviceMeasuredParameterManager()
    
    device = models.ForeignKey("Device", 
                               on_delete=models.CASCADE, 
                               verbose_name=Device._meta.verbose_name)
    
    measured_parameter = models.CharField(choices=MeasuredParameterChoices.choices, 
                                          verbose_name="Измерямеый параметр")
    
    measurement_system = models.CharField(verbose_name="Система измерений")
    
    max_value = models.FloatField(verbose_name="Максимальное значение", 
                                  null=True, blank=True)
    
    min_value = models.FloatField(verbose_name="Минимальное значение", 
                                  null=True, blank=True)
    
    class Meta:
        verbose_name = "Числовое измерение"
        verbose_name_plural = "Числовые измерения"
        
    def is_critical(self, value):
        return not self.is_valid(value)
    
    def is_valid(self, value):
        return self.min_value < value < self.max_value
        
    
    def save(self, *args, **kwargs) -> None:
        if self.max_value <= self.min_value:
            raise ValueError("max_value должно быть меньше min_value")
        return super().save(*args, **kwargs)
