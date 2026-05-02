from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Task
from projects.models import Project


class TaskSerializer(serializers.ModelSerializer):
    assigned_to_name = serializers.SerializerMethodField()
    project_name = serializers.SerializerMethodField()
    is_overdue = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'project', 'project_name',
            'assigned_to', 'assigned_to_name', 'status', 'due_date',
            'created_at', 'is_overdue'
        ]
        read_only_fields = ['created_at']

    def get_assigned_to_name(self, obj):
        return obj.assigned_to.username if obj.assigned_to else None

    def get_project_name(self, obj):
        return obj.project.name

    def get_is_overdue(self, obj):
        return obj.is_overdue()

    def validate(self, data):
        request = self.context.get('request')
        if request and request.user.profile.is_member():
            # members can only update status
            allowed = {'status'}
            incoming = set(data.keys())
            if incoming - allowed:
                raise serializers.ValidationError("Members can only update task status.")
        return data
