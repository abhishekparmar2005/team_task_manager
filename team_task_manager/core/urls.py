from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('projects/', include('projects.urls')),
    path('tasks/', include('tasks.urls')),
    path('api/', include('users.api_urls')),
    path('api/', include('projects.api_urls')),
    path('api/', include('tasks.api_urls')),
    path('dashboard/', include('users.dashboard_urls')),
    path('', RedirectView.as_view(url='/dashboard/', permanent=False)),
]
