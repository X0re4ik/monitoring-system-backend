from django.urls import re_path, path

from .consumers import JoinAndLeave, RetrievingMeasurementData

websocket_urlpatterns = [
    path('', JoinAndLeave.as_asgi()),
    path('<str:mac_address>', RetrievingMeasurementData.as_asgi(), name="ws")
]