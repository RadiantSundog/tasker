from django.shortcuts import render, redirect
from projects.models import Project
from tasks.models import Task
from django.contrib.auth.decorators import login_required
from projects.forms import CreateForm


# Create your views here.
@login_required
def list_projects(request):
    projects = Project.objects.filter(owner=request.user)
    context = {
        "list_projects": projects,
    }
    return render(request, "projects/list.html", context)


@login_required
def show_project(request, id):
    project_object = Project.objects.get(id=id)
    task_object = Task.objects.filter(project_id=id)
    context = {"project_object": project_object, "task_object": task_object}
    return render(request, "projects/detail.html", context)


@login_required
def create_project(request):
    if request.method == "POST":
        form = CreateForm(request.POST)
        if form.is_valid():
            projects = form.save(commit=False)
            projects.owner = request.user
            projects.save()
            return redirect("list_projects")
    else:
        form = CreateForm()

    context = {
        "form": form,
    }
    return render(request, "projects/create_project.html", context)
