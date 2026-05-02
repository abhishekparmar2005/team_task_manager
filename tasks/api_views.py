from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Task
from .serializers import TaskSerializer
from projects.models import Project


class TaskListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if user.profile.is_admin():
            tasks = Task.objects.filter(project__created_by=user)
        else:
            tasks = Task.objects.filter(assigned_to=user)

        # filter by project
        project_id = request.query_params.get('project')
        if project_id:
            tasks = tasks.filter(project_id=project_id)

        # filter by status
        status = request.query_params.get('status')
        if status:
            tasks = tasks.filter(status=status)

        return Response(TaskSerializer(tasks, many=True).data)

    def post(self, request):
        if not request.user.profile.is_admin():
            return Response({'error': 'Only admins can create tasks'}, status=403)

        serializer = TaskSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            project = serializer.validated_data['project']
            if project.created_by != request.user:
                return Response({'error': 'Not your project'}, status=403)
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class TaskDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_task(self, pk, user):
        task = get_object_or_404(Task, pk=pk)
        if user.profile.is_admin() and task.project.created_by != user:
            return None, Response({'error': 'Not your task'}, status=403)
        if user.profile.is_member() and task.assigned_to != user:
            return None, Response({'error': 'Task not assigned to you'}, status=403)
        return task, None

    def get(self, request, pk):
        task, err = self.get_task(pk, request.user)
        if err:
            return err
        return Response(TaskSerializer(task).data)

    def patch(self, request, pk):
        task, err = self.get_task(pk, request.user)
        if err:
            return err
        serializer = TaskSerializer(task, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        if not request.user.profile.is_admin():
            return Response({'error': 'Only admins can delete tasks'}, status=403)
        task = get_object_or_404(Task, pk=pk, project__created_by=request.user)
        task.delete()
        return Response({'message': 'Task deleted'}, status=204)
