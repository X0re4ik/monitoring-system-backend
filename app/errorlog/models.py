from django.db import models
from django.core.validators import MinLengthValidator

# Create your models here.


class AbstractErrorLog(models.Model):
    """AbstractErrorLog

    Абстрактный класс логирования ошибок
    
    Propirties:
        - `is_critical` (bool): ошибка критическая? 
            (Ошибка считается критическая, если состояние станочного оборудования отличается от предельных знчений)
        - `description` (str): поянснение к ошибке
    """
    
    is_critical = models.BooleanField(default=False, verbose_name="Ошибка критична?")
    description = models.CharField(validators=[MinLengthValidator(5)], verbose_name="Описание ошибки")
    is_sent = models.BooleanField(default=False, verbose_name="Ошибка отправлена на почту?")
    
    class Meta:
        abstract = True
        

class ErrorLogDevice(AbstractErrorLog):
    """ErrorLogDevice

    Ошибки устройства
    """
    
    device = models.ForeignKey("device.Device", on_delete=models.CASCADE, verbose_name="Устройство")
    
    class Meta:
        verbose_name = "Ошибка устройства"
        verbose_name_plural = "Ошибки устройства"
        

class ErrorLogMachine(AbstractErrorLog):
    """ErrorLogDevice

    Ошибки станочного оборудования
    """
    
    machine = models.ForeignKey("machine.Machine", on_delete=models.CASCADE, verbose_name="Станок")
    
    class Meta:
        verbose_name = "Ошибка станка"
        verbose_name_plural = "Ошибки станков"