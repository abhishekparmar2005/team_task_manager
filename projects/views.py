from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from .models import Project
from .forms import ProjectForm
from tasks.models import Task
from django.utils import timezone


def admin_required(view_func):
    """simple decorator to check admin role"""
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not hasattr(request.user, 'profile') or not request.user.profile.is_admin():
            return HttpResponseForbidden("You don't have permission to do this.")
        return view_func(request, *args, **kwargs)
    return wrapper


@login_required
def project_list(request):
    user = request.user
    if user.profile.is_admin():
        projects = Project.objects.filter(created_by=user).order_by('-created_at')
    else:
        projects = Project.objects.filter(members=user).distinct().order_by('-created_at')

    return render(request, 'projects/project_list.html', {'projects': projects})


@login_required
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    user = request.user

    # check access
    if user.profile.is_admin():
        if project.created_by != user:
            return HttpResponseForbidden("This is not your project.")
    else:
        if not project.members.filter(id=user.id).exists():
            return HttpResponseForbidden("You are not a member of this project.")

    if user.profile.is_admin():
        tasks = project.tasks.all().select_related('assigned_to')
    else:
        tasks = project.tasks.filter(assigned_to=user)

    today = timezone.now().date()
    overdue = tasks.filter(due_date__lt=today, status__in=['pending', 'in_progress'])

    return render(request, 'projects/project_detail.html', {
        'project': project,
        'tasks': tasks,
        'overdue_tasks': overdue,
        'stats': project.get_task_stats(),
    })


@admin_required
def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.created_by = request.user
            project.save()
            form.save_m2m()
            messages.success(request, f'Project "{project.name}" created!')
            return redirect('project_detail', pk=project.pk)
    else:
        form = ProjectForm()
    return render(request, 'projects/project_form.html', {'form': form, 'action': 'Create'})


@admin_required
def project_edit(request, pk):
    project = get_object_or_404(Project, pk=pk, created_by=request.user)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, 'Project updated!')
            return redirect('project_detail', pk=pk)
    else:
        form = ProjectForm(instance=project)
    return render(request, 'projects/project_form.html', {'form': form, 'action': 'Edit', 'project': project})


@admin_required
def project_delete(request, pk):
    project = get_object_or_404(Project, pk=pk, created_by=request.user)
    if request.method == 'POST':
        name = project.name
        project.delete()
        messages.success(request, f'Project "{name}" deleted.')
        return redirect('project_list')
    return render(request, 'projects/project_confirm_delete.html', {'project': project})
