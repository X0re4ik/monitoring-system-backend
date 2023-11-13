from django.contrib import admin
from django.urls import path, include


from .views import ErrorLogDeviceListAPI, ErrorLogMachineListAPI

urlpatterns = [
    path('device', ErrorLogDeviceListAPI.as_view(), name="error-log-device-list"),
    path('machine', ErrorLogDeviceListAPI.as_view(), name="error-log-machine-list"),
]