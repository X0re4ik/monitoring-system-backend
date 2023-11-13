from rest_framework import serializers

from .models import Machine, NormDetail


class NormDetailSerializer(serializers.ModelSerializer):
    """
    Example:
    ```json
    {
        "machine": 2,
        "min_qty_detail": 50
    }
    ```
    """
    class Meta:
        model = NormDetail
        fields = '__all__'



class MachineSerializer(serializers.ModelSerializer):
    """
    Example:
    ```json
    {
        "id": 5,
        "name": "СК16Р56-67",
        "type": "MILLING",
        "is_cnc": true
    }
    ```
    """
    class Meta:
        model = Machine
        fields = '__all__'