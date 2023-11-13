from django_filters import rest_framework as filters
from django.db.models import Q

from .models import (DeviceMeasuredParameter, DayStatistics,
                     MadeDetails, TimeWork, Measurement,)


class DeviceMeasuredParameterFilter(filters.FilterSet):
    """Фитьтрация для модели `DeviceMeasuredParameter`
    
    Фильтрация по параметрам:
        - `device`
    """
    class Meta:
        model = DeviceMeasuredParameter
        fields = ['device']
        
        
class DayStatisticsFilter(filters.FilterSet):
    """Фитьтрация для модели `DayStatisticsFilter`
    
    Фильтрация по параметрам:
        - `device` - устройство
        - `date` - дата
    """
    class Meta:
        model = DayStatistics
        fields = ['device', 'date']
        
        
class MadeDetailsFilter(filters.FilterSet):
    """Фитьтрация для модели `MadeDetailsFilter`
    
    Фильтрация по параметрам:
        - `device` - устройство
        - `date` - дата
    """
    
    date = filters.DateFilter(method='filter_date')
    
    class Meta:
        model = MadeDetails
        fields = ['device', 'date']
        
    def filter_date(self, queryset, name, value):
        return queryset.filter(dispatch_time__date=value)
    
    
class TimeWorkFilter(filters.FilterSet):
    """Фитьтрация для модели `TimeWorkFilter`
    
    Фильтрация по параметрам:
        - `device` - устройство
        - `date` - дата
    """
    
    date = filters.DateFilter(method='filter_date')
    
    class Meta:
        model = TimeWork
        fields = ['device', 'date']
        
    def filter_date(self, queryset, name, value):
        return queryset.filter(Q(start_work__date=value) & Q(end_work__date=value))