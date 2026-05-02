from django.urls import path
from .api_views import SignupAPIView, LoginAPIView, LogoutAPIView, CurrentUserAPIView, UserListAPIView

urlpatterns = [
    path('auth/signup/', SignupAPIView.as_view(), name='api-signup'),
    path('auth/login/', LoginAPIView.as_view(), name='api-login'),
    path('auth/logout/', LogoutAPIView.as_view(), name='api-logout'),
    path('auth/me/', CurrentUserAPIView.as_view(), name='api-me'),
    path('users/', UserListAPIView.as_view(), name='api-users'),
]
