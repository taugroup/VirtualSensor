from django.urls import path

from apps.project.views import ProjectList, ProjectCreate, ProjectDetail, ProjectDelete, ProjectUpdate

urlpatterns = [
    path('list/', ProjectList.as_view(), name='project_list'),
    path('create/', ProjectCreate.as_view(), name='project_create'),
    path('detail/<int:pk>/', ProjectDetail.as_view(), name='project_detail'),
    path('update/<int:pk>/', ProjectUpdate.as_view(), name='project_update'),
    path('delete/<int:pk>/', ProjectDelete.as_view(), name='project_delete'),
]