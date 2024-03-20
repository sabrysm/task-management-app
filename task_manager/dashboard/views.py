from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import Task, Category
from reporting.models import TaskHistory
from django.utils import timezone

@login_required
def index(request):
    todos = Task.objects.filter(completed=False, in_progress=False, user=request.user).all()
    completed = Task.objects.filter(completed=True, user=request.user).order_by('-completed_at')
    in_progress = Task.objects.filter(in_progress=True, user=request.user).all()
    categories = Category.objects.filter(user=request.user).all()
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
    task = Task.objects.get(id=id, user=request.user)
    task.completed = not task.completed
    task.completed_at = timezone.now()
    task.in_progress = False
    task.save()
    TaskHistory.objects.create(title=task.title, created_at=task.created_at, completed_at=task.completed_at, category=task.category, user=task.user)
    return redirect('dashboard:index')

@login_required
def create(request):
    if request.method == 'POST':
        title = request.POST['title']
        if 'category' not in request.POST:
            category = Category.objects.create(user=request.user)
            category.save()
            task = Task.objects.create(title=title, category=category, user=request.user)
            task.save()
        else:
            task = Task.objects.create(title=title, category=Category.objects.get(id=request.POST['category']), user=request.user)
            task.save()
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