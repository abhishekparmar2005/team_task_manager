from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Project


class ProjectMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class ProjectSerializer(serializers.ModelSerializer):
    created_by = ProjectMemberSerializer(read_only=True)
    members = ProjectMemberSerializer(many=True, read_only=True)
    member_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=User.objects.all(), write_only=True, source='members', required=False
    )
    task_stats = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'created_by', 'members', 'member_ids', 'created_at', 'task_stats']
        read_only_fields = ['created_by', 'created_at']

    def get_task_stats(self, obj):
        return obj.get_task_stats()

    def create(self, validated_data):
        members = validated_data.pop('members', [])
        project = Project.objects.create(**validated_data)
        project.members.set(members)
        return project

    def update(self, instance, validated_data):
        members = validated_data.pop('members', None)
        for attr, val in validated_data.items():
            setattr(instance, attr, val)
        instance.save()
        if members is not None:
            instance.members.set(members)
        return instance
