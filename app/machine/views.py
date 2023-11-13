

from rest_framework import generics
from .serializers import (
    MachineSerializer, 
    NormDetailSerializer)

from .models import Machine, NormDetail


def show_test_norm_detail(request):
    from django.shortcuts import render
    
    context = {
        "machines": Machine.objects.all(),
        "norm_details": NormDetail.objects.all()
    }
    return render(request, "index.html", context)


class NormDetailCreateAPI(generics.CreateAPIView):
    """
    Example:
    ```HTTP
    PATCH /api/v1/machine/limit_value/7 HTTP/1.1
    Host: 127.0.0.1:8000
    Content-Length: 56

    {
        "temperature": 1000,
        "spindle_speed": 200
    }
    ```
    """
    serializer_class = NormDetailSerializer
    queryset = NormDetail.objects.all()

 
class NormDetailRetrieveUpdateDestroyAPIViewAPI(generics.RetrieveUpdateDestroyAPIView):
    """
    Example:
    ```HTTP
    POST /api/v1/machine/limit_value/create HTTP/1.1
    Host: 127.0.0.1:8000
    Content-Length: 94

    {
        "machine": 7,
        "temperature": 50,
        "vibration": 50,
        "spindle_speed": 50
    }
    ```
    """
    serializer_class = NormDetailSerializer
    queryset = NormDetail.objects.all()


class MachineCreateAPI(generics.CreateAPIView):
    """
    Example:
    ```HTTP
    POST /api/v1/machine/create HTTP/1.1
    Host: 127.0.0.1:8000
    Content-Type: application/json
    Content-Length: 75

    {
        "name": "СК16Р56-67",
        "type": "MILLING",
        "is_cnc": true
    }
    ```
    """
    serializer_class = MachineSerializer
    queryset = Machine.objects.all()


class MachineRetrieveUpdateDestroyAPI(generics.RetrieveUpdateDestroyAPIView):
    """
    Example:
    ```HTTP
    PATCH /api/v1/machine/1 HTTP/1.1
    Host: 127.0.0.1:8000
    Content-Type: application/json
    Content-Length: 25

    {
        "is_cnc": false
    }
    ```
    """
    serializer_class = MachineSerializer
    queryset = Machine.objects.all()