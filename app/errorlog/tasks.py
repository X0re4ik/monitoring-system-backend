
from celery import shared_task

from .models import ErrorLogDevice, ErrorLogMachine


from machine.models import Machine, LimitValue
from device.models import Device, Measurement


@shared_task
def check_condition_of_machine(device_mac_address: str, measurement_id: int, send_by_email: bool = True):
    measurement = Measurement.objects.get(pk=measurement_id)
    
    device = Device.objects.get(pk=device_mac_address)
    machine=Machine.objects.filter(device=device).first()
    limit_value = LimitValue.objects.filter(machine=machine).first()
    
    if limit_value is not None:
        attrs = ["temperature", "spindle_speed", "vibration"]

        for attr in attrs:
            measurement_value = getattr(measurement, attr)
            limit_value_value = getattr(limit_value, attr)
            if measurement_value > limit_value_value:
                description = f"Параметр '{attr}' больше нормального значения ({measurement_value} > {limit_value_value})."
                ErrorLogMachine.objects.create(
                    machine=machine,
                    is_critical=True,
                    description=description,
                    is_sent=False)
        

@shared_task
def report_machine_error_by_mail(error_log_machine_id):
    pass