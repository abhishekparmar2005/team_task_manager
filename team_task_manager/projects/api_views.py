from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Project
from .serializers import ProjectSerializer


class ProjectListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if user.profile.is_admin():
            projects = Project.objects.filter(created_by=user)
        else:
            projects = Project.objects.filter(members=user).distinct()
        return Response(ProjectSerializer(projects, many=True).data)

    def post(self, request):
        if not request.user.profile.is_admin():
            return Response({'error': 'Only admins can create projects'}, status=403)
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class ProjectDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_project(self, pk, user):
        project = get_object_or_404(Project, pk=pk)
        if user.profile.is_admin() and project.created_by != user:
            return None, Response({'error': 'Not your project'}, status=403)
        if user.profile.is_member() and not project.members.filter(id=user.id).exists():
            return None, Response({'error': 'You are not a member'}, status=403)
        return project, None

    def get(self, request, pk):
        project, err = self.get_project(pk, request.user)
        if err:
            return err
        return Response(ProjectSerializer(project).data)

    def put(self, request, pk):
        if not request.user.profile.is_admin():
            return Response({'error': 'Only admins can update projects'}, status=403)
        project = get_object_or_404(Project, pk=pk, created_by=request.user)
        serializer = ProjectSerializer(project, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        if not request.user.profile.is_admin():
            return Response({'error': 'Only admins can delete projects'}, status=403)
        project = get_object_or_404(Project, pk=pk, created_by=request.user)
        project.delete()
        return Response({'message': 'Project deleted'}, status=204)
