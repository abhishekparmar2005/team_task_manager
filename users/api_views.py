from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .serializers import SignupSerializer, UserSerializer


class SignupAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'message': 'Account created successfully', 'user': UserSerializer(user).data}, status=201)
        return Response(serializer.errors, status=400)


class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return Response({'message': 'Login successful', 'user': UserSerializer(user).data})
        return Response({'error': 'Invalid credentials'}, status=400)


class LogoutAPIView(APIView):
    def post(self, request):
        logout(request)
        return Response({'message': 'Logged out'})


class CurrentUserAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)


class UserListAPIView(APIView):
    """Admins use this to get list of members for task assignment"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not hasattr(request.user, 'profile') or not request.user.profile.is_admin():
            return Response({'error': 'Only admins can view user list'}, status=403)
        users = User.objects.select_related('profile').all()
        return Response(UserSerializer(users, many=True).data)
