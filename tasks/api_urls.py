from django.urls import path
from .api_views import TaskListCreateAPIView, TaskDetailAPIView

urlpatterns = [
    path('tasks/', TaskListCreateAPIView.as_view(), name='api-tasks'),
    path('tasks/<int:pk>/', TaskDetailAPIView.as_view(), name='api-task-detail'),
]
