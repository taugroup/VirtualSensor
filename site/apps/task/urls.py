from django.urls import path

from apps.task.views import TaskList, TaskCreate, TaskDetail, TaskDelete, TaskUpdate

urlpatterns = [
    path('list/', TaskList.as_view(), name='task_list'),
    path('create/', TaskCreate.as_view(), name='task_create'),
    path('create/<int:pk>/', TaskCreate.as_view(), name='task_create'),
    path('detail/<int:pk>/', TaskDetail.as_view(), name='task_detail'),
    path('update/<int:pk>/', TaskUpdate.as_view(), name='task_update'),
    path('delete/<int:pk>/', TaskDelete.as_view(), name='task_delete'),
]