from django.urls import path

from apps.file.views import file_create, file_delete

urlpatterns = [
    path('create/<int:pk>/', file_create, name='file_create'),
    path('delete/<int:pk>/', file_delete, name='file_delete'),
]
