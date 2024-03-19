from django.shortcuts import render, redirect
from .models import Task
from django.utils import timezone

def index(request):
    todos = Task.objects.filter(completed=False, in_progress=False).all()
    completed = Task.objects.filter(completed=True).order_by('-completed_at').all()
    in_progress = Task.objects.filter(in_progress=True).all()
    context = {
        "tasks_todo": todos,
        "tasks_completed": completed,
        "tasks_in_progress": in_progress
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
    return redirect('task:index')

def create(request):
    if request.method == 'POST':
        title = request.POST['title']
        task = Task.objects.create(title=title)
        task.save()
    return redirect('task:index')

def update(request, id):
    task = Task.objects.get(id=id)
    task.completed = not task.completed
    task.save()
    return render(request, 'task/tasks_list.html')

def delete_all(request):
    Task.objects.all().delete()
    return redirect('task:index')