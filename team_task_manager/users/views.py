from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.utils import timezone
from .forms import SignupForm
from projects.models import Project
from tasks.models import Task


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Account created! Welcome, {user.username}.')
            return redirect('dashboard')
    else:
        form = SignupForm()

    return render(request, 'users/signup.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()

    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard_view(request):
    user = request.user
    profile = user.profile

    if profile.is_admin():
        # admin sees all projects they created
        my_projects = Project.objects.filter(created_by=user).order_by('-created_at')
        all_tasks = Task.objects.filter(project__created_by=user).select_related('assigned_to', 'project')
        overdue_tasks = all_tasks.filter(
            due_date__lt=timezone.now().date(),
            status__in=['pending', 'in_progress']
        )

        stats = {
            'total_projects': my_projects.count(),
            'total_tasks': all_tasks.count(),
            'pending': all_tasks.filter(status='pending').count(),
            'in_progress': all_tasks.filter(status='in_progress').count(),
            'completed': all_tasks.filter(status='completed').count(),
            'overdue': overdue_tasks.count(),
        }

        context = {
            'projects': my_projects[:5],
            'recent_tasks': all_tasks.order_by('-id')[:8],
            'overdue_tasks': overdue_tasks[:5],
            'stats': stats,
        }
        return render(request, 'users/admin_dashboard.html', context)

    else:
        # member sees only assigned stuff
        my_tasks = Task.objects.filter(assigned_to=user).select_related('project').order_by('-id')
        my_projects = Project.objects.filter(members=user).distinct()
        overdue_tasks = my_tasks.filter(
            due_date__lt=timezone.now().date(),
            status__in=['pending', 'in_progress']
        )

        stats = {
            'total_tasks': my_tasks.count(),
            'pending': my_tasks.filter(status='pending').count(),
            'in_progress': my_tasks.filter(status='in_progress').count(),
            'completed': my_tasks.filter(status='completed').count(),
            'overdue': overdue_tasks.count(),
        }

        context = {
            'projects': my_projects,
            'my_tasks': my_tasks[:10],
            'overdue_tasks': overdue_tasks,
            'stats': stats,
        }
        return render(request, 'users/member_dashboard.html', context)
