from django.shortcuts import render, redirect
from tasks.models import Task
from django.contrib.auth.decorators import login_required
from tasks.forms import CreateTaskForm

# Create your views here.


@login_required
def create_task(request):
    if request.method == "POST":
        form = CreateTaskForm(request.POST)
        if form.is_valid():
            tasks = form.save()
            tasks.save()
            return redirect("list_projects")
    else:
        form = CreateTaskForm()

    context = {
        "form": form,
    }
    return render(request, "tasks/create_task.html", context)


@login_required
def show_my_tasks(request):
    tasks = Task.objects.filter(assignee=request.user)
    context = {
        "show_my_tasks": tasks,
    }
    return render(request, "tasks/show_my_tasks.html", context)
