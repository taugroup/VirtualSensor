from django.urls import path

from apps.input.views import InputList, InputCreate, InputDetail, InputDelete, InputUpdate

urlpatterns = [
    path('list/', InputList.as_view(), name='input_list'),
    path('create/', InputCreate.as_view(), name='input_create'),
    path('create/<int:pk>/', InputCreate.as_view(), name='input_create'),
    path('detail/<int:pk>/', InputDetail.as_view(), name='input_detail'),
    path('update/<int:pk>/', InputUpdate.as_view(), name='input_update'),
    path('delete/<int:pk>/', InputDelete.as_view(), name='input_delete'),
]