from django.shortcuts import render

# Create your views here.
from rest_framework import generics

from .serializers import ErrorLogDeviceSerializer, ErrorLogMachineSerializer, AbstractErrorLog
from .models import ErrorLogMachine, ErrorLogDevice 



class AbstractErrorLogListAPI(generics.ListAPIView):
    
    def get_queryset(self):
        if self.request.query_params.get('is_critical') is not None:
            return self.queryset.filter(is_critical=True)
        return super().get_queryset()

class ErrorLogMachineListAPI(AbstractErrorLogListAPI):
    queryset = ErrorLogMachine.objects.all()
    serializer_class = ErrorLogMachineSerializer
    

class ErrorLogDeviceListAPI(AbstractErrorLogListAPI):
    queryset = ErrorLogDevice.objects.all()
    serializer_class = ErrorLogDeviceSerializer
    
    