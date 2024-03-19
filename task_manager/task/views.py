from django.shortcuts import render, redirect
from .models import Task, Category
from reporting.models import TaskHistory
from django.utils import timezone

def index(request):
    todos = Task.objects.filter(completed=False, in_progress=False).all()
    completed = Task.objects.filter(completed=True).order_by('-completed_at').all()
    in_progress = Task.objects.filter(in_progress=True).all()
    categories = Category.objects.all()
    context = {
        "tasks_todo": todos,
        "tasks_completed": completed,
        "tasks_in_progress": in_progress,
        "categories": categories,
    }
    return render(request, 'task/tasks_list.html', context)

def in_progress(request, id):
    task = Task.objects.get(id=id)
    task.in_progress = not task.in_progress
    task.save()
    return redirect('task:index')

def completed(request, id):
    task = Task.objects.get(id=id)
    task.completed = not task.completed
    task.completed_at = timezone.now()
    task.in_progress = False
    task.save()
    TaskHistory.objects.create(title=task.title, created_at=task.created_at, completed_at=task.completed_at, category=task.category)
    return redirect('task:index')

def create(request):
    if request.method == 'POST':
        title = request.POST['title']
        task = Task.objects.create(title=title, category=Category.objects.get(id=request.POST['category']))
        task.save()
    return redirect('task:index')

def update(request, id):
    task = Task.objects.get(id=id)
    task.completed = not task.completed
    task.save()
    return render(request, 'task/tasks_list.html')

def delete(request, id):
    task = Task.objects.get(id=id)
    task.delete()
    return redirect('task:index')

def reset_all(request):
    Task.objects.all().delete()
    return redirect('task:index')

def new_category(request):
    if request.method == 'POST':
        name = request.POST['category']
        category = Category.objects.create(name=name)
        category.save()
    return redirect('task:index')