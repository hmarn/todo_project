from django.urls import path
from . import views

urlpatterns = [
    path('', views.task_list, name='task_list'),
    path('add/', views.add_task, name='add_task'),
    path('remove/<int:task_id>/', views.remove_task, name='remove_task'),
    path('start_timer/<int:task_id>/', views.start_timer, name='start_timer'),
    path('stop_timer/<int:task_id>/', views.stop_timer, name='stop_timer'),
    path('get_timer_duration/<int:task_id>/', views.get_timer_duration, name='get_timer_duration'),
]