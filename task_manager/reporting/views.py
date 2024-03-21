from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib.admin.views.decorators import staff_member_required
from .models import CompletedTask
from django.utils import timezone

@login_required
def tasks_history(request):
    # Get Tasks completed
    completed = CompletedTask.objects.filter(user=request.user).order_by('-completed_at')
    paginator = Paginator(completed, 10)
    page = request.GET.get('page')
    completed = paginator.get_page(page)
    context = {
        "page": completed,
    }
    return render(request, 'reporting/tasks_history.html', context)

@staff_member_required
def clear_history(request):
    CompletedTask.objects.all().delete()
    return redirect('reporting:tasks_history')