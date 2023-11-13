from django.contrib import admin
from django.urls import path, include


from .views import (DeviceCreateAPI, DeviceRetrieveUpdateDestroyAPI, 
                    MeasurementCreateAPI,
                    MadeDetailCreateAPI, MadeDetailsListAPI,
                    TimeWorkCreateAPI, TimeWorksListAPI, 
                    DeviceMeasuredParametersListAPI,)

urlpatterns = [
     path('create', DeviceCreateAPI.as_view(), name="create-device"),

     path('measurement/create', 
          MeasurementCreateAPI.as_view(), name="measurement-create"),

     path('time_work/create', 
          TimeWorkCreateAPI.as_view(), name="time-work-create"),
     path('time_work/statistics', 
          TimeWorksListAPI.as_view(), name="time-work-statistics"),

     path('made_detail/create', 
          MadeDetailCreateAPI.as_view(), name="made-detail-create"),
     path('made_detail/statistics', 
          MadeDetailsListAPI.as_view(), name="made-detail-statistics"),

     path('parameters', DeviceMeasuredParametersListAPI.as_view(), name='device-measured-parameters')
    
]