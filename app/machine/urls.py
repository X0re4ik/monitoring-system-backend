from django.contrib import admin
from django.urls import path, include


from .views import (MachineCreateAPI, MachineRetrieveUpdateDestroyAPI,
                    NormDetailCreateAPI, NormDetailRetrieveUpdateDestroyAPIViewAPI)

from .views import show_test_norm_detail

urlpatterns = [
     path('create', 
          MachineCreateAPI.as_view(), name="create-machine"),
     
     path('<int:pk>', 
          MachineRetrieveUpdateDestroyAPI.as_view(), name="update-get-delete-machine"),
     
     path('show_test_norm_detail', 
          show_test_norm_detail, name="show-test-norm-detail"),
     
     path('norm_detail/create', 
          NormDetailCreateAPI.as_view(), name="update-get-delete-machine"),
     
     path('norm_detail/<int:pk>', 
          NormDetailRetrieveUpdateDestroyAPIViewAPI.as_view(), name="update-get-delete-machine"),
]