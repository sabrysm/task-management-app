from django.urls import path
from . import views

app_name = 'reporting'

urlpatterns = [
    path('tasks_history/', views.tasks_history, name='tasks_history'),
    path('clear_history5364/', views.clear_history, name='clear_history'),
]