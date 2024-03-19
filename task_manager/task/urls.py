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
    path('delete/<int:id>/', views.delete, name='delete'),
    path('reset_all', views.reset_all, name='reset_all'),
    path('new_category/', views.new_category, name='new_category'),
]