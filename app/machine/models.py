from django.db import models

from django.core.validators import (
    MinLengthValidator, MaxLengthValidator,
    MinValueValidator, MaxValueValidator)

# Create your models here.

class TypeMachine(models.TextChoices):
    MILLING = ("MILLING", "Фрезерный")
    LATHE = ("LATHE", "Токарный")


class Machine(models.Model):
    """Machine
    
    Primary Key: `id`
    
    Property:
        - `name` (str):      температура станочного оборудования
        - `type` (str):       вибрация на станочного оборудования
        - `is_cnc` (bool):    скорость вращения шпинделя
    """
    
    name = models.CharField(validators=[MinLengthValidator(1), MaxLengthValidator(100)], verbose_name="Название станка")
    
    type = models.CharField(choices=TypeMachine.choices, verbose_name="Тип оборудования")
    is_cnc = models.BooleanField(verbose_name="Станок с ЧПУ?")
    
    class Meta:
        verbose_name = "Станочное оборудование"
        verbose_name_plural = "Станочное оборудование"


class NormDetail(models.Model):
    """NormDetail

    Норма выробатки деталей
    
    Primary Key:
        - `machine` (`Machine`): станочное оборудование
    
    property:
        - `min_qty_detail` (int): минимальная выработка деталей
    """
    machine = models.OneToOneField("Machine", 
                                   on_delete=models.CASCADE, 
                                   primary_key=True,
                                   verbose_name=Machine._meta.verbose_name)
    min_qty_detail = models.IntegerField(validators=[MinValueValidator(0)], 
                                         verbose_name="Минимальная выработка деталей")
    
    class Meta:
        verbose_name = "Норма детали"
        verbose_name_plural = "Норма деталей"