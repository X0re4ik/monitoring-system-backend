
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request

from django_filters import rest_framework as filters

from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED

from device.models import (Measurement, 
                           Device, 
                           MadeDetails, 
                           TimeWork)

from .models import Device, Measurement, DeviceMeasuredParameter
from .serializers import (DeviceSerializer, 
                          MadeDetailSerializer,
                          TimeWorkSerializer,
                          MeasurementSerializer,
                          DeviceMeasuredParameterSerializer)
from .filters import (DeviceMeasuredParameterFilter,
                      DayStatisticsFilter,
                      MadeDetailsFilter, TimeWorkFilter)

class DeviceMeasuredParametersListAPI(generics.ListAPIView):
    """"""
    queryset = DeviceMeasuredParameter.objects.all()
    serializer_class = DeviceMeasuredParameterSerializer
    
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = DeviceMeasuredParameterFilter
    
    
class DeviceCreateAPI(generics.CreateAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    
    def create(self, request, *args, **kwargs):
        device_ip = request.META.get('REMOTE_ADDR')
                                    #HTTP_X_FORWARDED_FOR
        request.data["ip"] = device_ip
        return super().create(request, *args, **kwargs)


class DeviceRetrieveUpdateDestroyAPI(generics.RetrieveUpdateDestroyAPIView):
    """"""
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer




class MadeDetailCreateAPI(generics.CreateAPIView):
    """
    Example:
    ```HTTP
    POST /api/v1/device/made_detail/create HTTP/1.1
    Host: 127.0.0.1:8000
    Content-Type: application/json
    Content-Length: 132

    {
        "device": "ESP-82-66",
        "qty_good_details": 5,
        "qty_bad_details": 10,
        "dispatch_time": "2023-10-25T16:30:14"
    }
    ```
    """
    
    queryset = MadeDetails.objects.all()
    serializer_class = MadeDetailSerializer
    

class MadeDetailsListAPI(generics.ListAPIView):
    """
    """
    
    queryset = MadeDetails.objects.all()
    serializer_class = MadeDetailSerializer
    
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = MadeDetailsFilter





class TimeWorkCreateAPI(generics.CreateAPIView):
    """
    Example:
    ```HTTP
    POST /api/v1/device/time_work/create HTTP/1.1
    Host: 127.0.0.1:8000
    Content-Type: application/json
    Content-Length: 132

    {
        "device": "ESP-82-66",
        "qty_good_details": 5,
        "qty_bad_details": 10,
        "dispatch_time": "2023-10-25T16:30:14"
    }
    ```
    """
    
    queryset = TimeWork.objects.all()
    serializer_class = TimeWorkSerializer

class TimeWorksListAPI(generics.ListAPIView):
    """
    """
    
    queryset = TimeWork.objects.all()
    serializer_class = TimeWorkSerializer
    
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = TimeWorkFilter



class MeasurementCreateAPI(generics.CreateAPIView):
    """
    Example:
    ```HTTP
    POST /api/v1/device/made_detail/create HTTP/1.1
    Host: 127.0.0.1:8000
    Content-Type: application/json
    Content-Length: 132

    {
        "device": "ESP-82-66",
        "qty_good_details": 5,
        "qty_bad_details": 10,
        "dispatch_time": "2023-10-25T16:30:14"
    }
    ```
    """
    
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer