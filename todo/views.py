from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Task
from django.template import loader
from datetime import timedelta
from django.utils import timezone


def task_list(request):
    tasks = Task.objects.all()
    for task in tasks:
        # Calculate the duration of the timer if running
        if task.timer_start and not task.timer_end:
            duration = timezone.now() - task.timer_start
        elif task.timer_start and task.timer_end:
            duration = task.timer_end - task.timer_start
        else:
            duration = timedelta(0)
        
        task.duration_minutes = duration.seconds // 60
        task.duration_seconds = duration.seconds % 60

    # return render(request, 'todo/task_list.html', {'tasks': tasks})
    template = loader.get_template('todo/task_list.html')
    context = {
      'tasks': tasks,
    }
    return HttpResponse(template.render(context, request))


def add_task(request):
    if request.method == "POST":
        title = request.POST.get('title')
        if title:
            Task.objects.create(title=title)
    return redirect('task_list')


def remove_task(request, task_id):
    Task.objects.filter(id=task_id).delete()
    return redirect('task_list')

      
def start_timer(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    task.start_timer()
    return JsonResponse({'status': 'Timer started'})


def stop_timer(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    task.stop_timer()
    return JsonResponse({'status': 'Timer stopped', 'duration': str(task.get_timer_duration())})


def get_timer_duration(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    # Calculate the duration
    duration = task.get_timer_duration()
    return JsonResponse({'duration': str(duration)})
