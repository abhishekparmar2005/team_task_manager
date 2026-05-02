from django.urls import path
from .api_views import ProjectListCreateAPIView, ProjectDetailAPIView

urlpatterns = [
    path('projects/', ProjectListCreateAPIView.as_view(), name='api-projects'),
    path('projects/<int:pk>/', ProjectDetailAPIView.as_view(), name='api-project-detail'),
]
