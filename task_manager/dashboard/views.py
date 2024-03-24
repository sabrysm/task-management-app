from django.shortcuts import render, redirect
# user
from django.contrib.auth.models import User
from django.http import HttpResponseNotFound, HttpResponseServerError
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import Task, Category
from reporting.models import CompletedTask
from django.utils import timezone
import time

@login_required
def index(request):
    todos = Task.objects.filter(completed=False, in_progress=False, user=request.user)
    # show today's completed tasks only starting from 00:00:00
    completed = Task.objects.filter(completed=True, user=request.user).order_by('-completed_at').filter(completed_at__gte=timezone.now().replace(hour=0, minute=0, second=0, microsecond=0))
    in_progress = Task.objects.filter(in_progress=True, user=request.user)
    categories = Category.objects.filter(user=request.user)
    context = {
        "tasks_todo": todos,
        "tasks_completed": completed,
        "tasks_in_progress": in_progress,
        "categories": categories,
    }
    return render(request, 'dashboard/tasks_list.html', context)

@login_required
def in_progress(request, id):
    task = Task.objects.get(id=id, user=request.user)
    task.in_progress = not task.in_progress
    task.save()
    return redirect('dashboard:index')

@login_required
def completed(request, id):
    try:
        task = Task.objects.get(id=id, user=request.user)
        task.completed = not task.completed
        task.completed_at = timezone.now()
        task.in_progress = False
        task.save()
        if task.completed:
            CompletedTask.objects.create(title=task.title, created_at=task.created_at, completed_at=task.completed_at, category=task.category.name, user=task.user)
        return redirect('dashboard:index')

    except Task.DoesNotExist:
        # Handle the case where the task does not exist
        return HttpResponseNotFound("Task not found.")

    except Exception as e:
        # Print or log the exception for debugging
        print(f"An error occurred: {e}")
        # Return an HTTP response with a meaningful error message
        return HttpResponseServerError("An error occurred while processing your request. Please try again later.")


@login_required
def create(request):
    if request.method == 'POST':
        title = request.POST['title']
        if 'category' not in request.POST:
            category = Category.objects.create(user=request.user)
            category.save()
            time.sleep(0.5)
            Task.objects.create(title=title, category=category, user=request.user)
        else:
            Task.objects.create(title=title, category=Category.objects.get(id=request.POST['category']), user=request.user)
    return redirect('dashboard:index')

@login_required
def update(request, id):
    task = Task.objects.get(id=id, user=request.user)
    task.completed = not task.completed
    task.save()
    return render(request, 'dashboard/tasks_list.html')

@login_required
def delete(request, id):
    task = Task.objects.get(id=id, user=request.user)
    task.delete()
    return redirect('dashboard:index')

@login_required
def reset_all(request):
    Task.objects.filter(user=request.user).delete()
    return redirect('dashboard:index')

@login_required
def new_category(request):
    if request.method == 'POST':
        name = request.POST['category']
        category = Category.objects.create(name=name, user=request.user)
        category.save()
    return redirect('dashboard:index')

@staff_member_required
def clear_categories(request):
    Category.objects.all().delete()
    return redirect('dashboard:index')