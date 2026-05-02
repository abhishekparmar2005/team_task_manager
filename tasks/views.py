from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.utils import timezone
from .models import Task
from .forms import TaskForm, TaskStatusForm
from projects.models import Project


@login_required
def task_list(request):
    user = request.user
    if user.profile.is_admin():
        tasks = Task.objects.filter(project__created_by=user).select_related('project', 'assigned_to').order_by('-created_at')
    else:
        tasks = Task.objects.filter(assigned_to=user).select_related('project').order_by('-created_at')

    # filter by status if provided
    status_filter = request.GET.get('status', '')
    if status_filter:
        tasks = tasks.filter(status=status_filter)

    today = timezone.now().date()
    for task in tasks:
        task.overdue = task.due_date and task.due_date < today and task.status != 'completed'

    return render(request, 'tasks/task_list.html', {
        'tasks': tasks,
        'status_filter': status_filter,
    })


@login_required
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    user = request.user

    if user.profile.is_admin():
        if task.project.created_by != user:
            return HttpResponseForbidden("Not your task.")
    else:
        if task.assigned_to != user:
            return HttpResponseForbidden("This task is not assigned to you.")

    return render(request, 'tasks/task_detail.html', {'task': task})


@login_required
def task_create(request, project_pk):
    if not request.user.profile.is_admin():
        return HttpResponseForbidden("Only admins can create tasks.")

    project = get_object_or_404(Project, pk=project_pk, created_by=request.user)

    if request.method == 'POST':
        form = TaskForm(project, request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = project
            task.save()
            messages.success(request, f'Task "{task.title}" added to {project.name}.')
            return redirect('project_detail', pk=project_pk)
    else:
        form = TaskForm(project)

    return render(request, 'tasks/task_form.html', {'form': form, 'project': project, 'action': 'Create'})


@login_required
def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk)
    user = request.user

    if user.profile.is_admin():
        if task.project.created_by != user:
            return HttpResponseForbidden("Not your task.")
        form_class = TaskForm
        form_kwargs = {'project': task.project}
    else:
        # members can only update status of their own tasks
        if task.assigned_to != user:
            return HttpResponseForbidden("This task is not assigned to you.")
        form_class = TaskStatusForm
        form_kwargs = {}

    if request.method == 'POST':
        if user.profile.is_admin():
            form = form_class(task.project, request.POST, instance=task)
        else:
            form = form_class(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task updated!')
            return redirect('task_detail', pk=pk)
    else:
        if user.profile.is_admin():
            form = form_class(task.project, instance=task)
        else:
            form = form_class(instance=task)

    return render(request, 'tasks/task_form.html', {'form': form, 'task': task, 'action': 'Edit'})


@login_required
def task_delete(request, pk):
    if not request.user.profile.is_admin():
        return HttpResponseForbidden("Only admins can delete tasks.")

    task = get_object_or_404(Task, pk=pk, project__created_by=request.user)
    if request.method == 'POST':
        project_pk = task.project.pk
        task.delete()
        messages.success(request, 'Task deleted.')
        return redirect('project_detail', pk=project_pk)
    return render(request, 'tasks/task_confirm_delete.html', {'task': task})


@login_required
def task_update_status(request, pk):
    """Quick status update - member can advance their task status"""
    task = get_object_or_404(Task, pk=pk)
    user = request.user

    if task.assigned_to != user:
        return HttpResponseForbidden("This task is not yours.")

    next_status = task.next_status()
    if next_status and request.method == 'POST':
        task.status = next_status
        task.save()
        messages.success(request, f'Task moved to "{task.get_status_display()}".')

    next_page = request.POST.get('next', '')
    if next_page == 'dashboard':
        return redirect('dashboard')
    return redirect('task_detail', pk=pk)


@login_required
def overdue_tasks(request):
    if not request.user.profile.is_admin():
        return HttpResponseForbidden("Admins only.")

    today = timezone.now().date()
    tasks = Task.objects.filter(
        project__created_by=request.user,
        due_date__lt=today,
        status__in=['pending', 'in_progress']
    ).select_related('project', 'assigned_to').order_by('due_date')

    return render(request, 'tasks/overdue_tasks.html', {'tasks': tasks, 'today': today})
