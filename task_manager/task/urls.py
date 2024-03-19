from django.urls import path
from . import views

app_name = 'task'

urlpatterns = [
    # index, create, update, delete
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
    path('in-progress/<int:id>/', views.in_progress, name='in_progress'),
    path('completed/<int:id>/', views.completed, name='completed'),
    path('update/<int:id>/', views.update, name='update'),
    path('delete_all', views.delete_all, name='delete_all'),
]