



from rest_framework import serializers

from device.models import Device
from machine.models import Machine

from .models import ErrorLogDevice, ErrorLogMachine, AbstractErrorLog



class AbstractErrorLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AbstractErrorLog
        fields = '__all__'
        abstract = True
        

class ErrorLogDeviceSerializer(AbstractErrorLogSerializer):

    device = serializers.SlugRelatedField(slug_field='mac_address', 
                                           queryset=Device.objects.all())
    class Meta:
        model = ErrorLogDevice
        fields = '__all__'
        
    
class ErrorLogMachineSerializer(AbstractErrorLogSerializer):

    machine = serializers.SlugRelatedField(slug_field='id', 
                                           queryset=Machine.objects.all())
    class Meta:
        model = ErrorLogMachine
        fields = '__all__'