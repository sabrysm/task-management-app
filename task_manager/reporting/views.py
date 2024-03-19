from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from .models import TaskHistory
from django.utils import timezone

def tasks_history(request):
    # Get Tasks completed
    completed = TaskHistory.objects.all().order_by('-completed_at')
    paginator = Paginator(completed, 10)
    page = request.GET.get('page')
    completed = paginator.get_page(page)
    context = {
        "page": completed,
    }
    return render(request, 'reporting/tasks_history.html', context)

def clear_history(request):
    TaskHistory.objects.all().delete()
    return redirect('reporting:tasks_history')