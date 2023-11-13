
from rest_framework import serializers
from machine.models import Machine 
from rest_framework.exceptions import ErrorDetail, ValidationError

from .models import DayStatistics, Measurement, MadeDetails, Device, TimeWork, DeviceMeasuredParameter



class DeviceMeasuredParameterSerializer(serializers.ModelSerializer):
    """
    Example:
    ```json
    ```
    """
    class Meta:
        model = DeviceMeasuredParameter
        fields = '__all__'

class DeviceSerializer(serializers.ModelSerializer):
    """
    Example:
    ```json
    ```
    """
    machine = serializers.SlugRelatedField(slug_field='id',
                                           required=False,
                                           allow_null=True, 
                                           queryset=Machine.objects.all())
    
    delta = serializers.IntegerField(required=False)
    
    class Meta:
        model = Device
        fields = '__all__'
        


class MadeDetailSerializer(serializers.ModelSerializer):
    """
    Example:
    ```json
    {
        "id": 1,
        "qty_good_details": 5,
        "qty_bad_details": 10,
        "dispatch_time": "2023-10-25T16:30:14Z",
        "device": "ESP-82-66"
    }
    ```
    """
    class Meta:
        model = MadeDetails
        fields = '__all__'
        

class TimeWorkSerializer(serializers.ModelSerializer):
    """
    Example:
    ```json
    {
        "id": 1,
        "start_work": "2023-10-25T16:30:14Z",
        "end_work": "2023-10-25T16:30:14Z",
        "device": "ESP-82-66"
    }
    ```
    """
    class Meta:
        model = TimeWork
        fields = '__all__'



class MeasurementSerializer(serializers.ModelSerializer):
    """
    Example:
    ```json
    {
        "id": 1,
        "values": {
            "temperature1": 45,
            "temperature2": 67
        },
        "device": "ESP-82-66",
        "dispatch_time": "2023-10-25T16:30:14Z",
    }
    ```
    """
    
    class Meta:
        model = Measurement
        fields = '__all__'
    
    
    def validate(self, data):
        """
        Проверка соответсвия входных параметров параметра `values` c схемой в 
        таблице `DeviceMeasuredParameter`
        """
        device = Device.objects.get(pk=data["device"])
        values =data["values"]
        is_match = DeviceMeasuredParameter.objects.match(device, values)
        if not is_match:
            raise ValidationError("Данные не совпадают")
        return data