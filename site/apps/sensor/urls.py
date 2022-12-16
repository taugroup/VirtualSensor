from django.urls import path

from apps.sensor.views import SensorList, SensorCreate, SensorDetail, SensorDelete, SensorUpdate

urlpatterns = [
    path('list/', SensorList.as_view(), name='sensor_list'),
    path('create/', SensorCreate.as_view(), name='sensor_create'),
    path('detail/<int:pk>/', SensorDetail.as_view(), name='sensor_detail'),
    path('update/<int:pk>/', SensorUpdate.as_view(), name='sensor_update'),
    path('delete/<int:pk>/', SensorDelete.as_view(), name='sensor_delete'),
]