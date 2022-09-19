from urllib.request import Request
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TaskForm
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required
# Create your views here.


def inicio(request):
    return render(request, "inicio.html")


def productos(request):
    return render(request, "productos.html")


def nosotros(request):
    return render(request, "nosotros.html")


def contactenos(request):
    return render(request, "contactenos.html")


def iniciosesion(request):
    if request.method == "GET":

        return render(request, "iniciar_sesion.html", {
            "userLoginForm": AuthenticationForm
        })

    else:
        user = authenticate(
            request, username=request.POST["username"], password=request.POST["password"])

        if user is None:
            return render(request, "iniciar_sesion.html", {
                "userLoginForm": AuthenticationForm,
                "error": "Usuario o contraseña es incorrecta"
            })

        else:
            login(request, user)
            return redirect("productos")

@login_required
def cerrarsesion(request):
    logout(request)
    return redirect("inicio")


def registrarse(request):

    if request.method == "GET":
        #print("enviando datos")
        return render(request, "registrarse.html", {
            "userCreateForm": UserCreationForm
        })
    else:
        if request.POST["password1"] == request.POST["password2"]:
            # register user
            try:
                user = User.objects.create_user(
                    username=request.POST["username"], password=request.POST["password1"])
                user.save()
                login(request, user)
                # return HttpResponse("Usuario creado satisfactoriamente")
                return redirect("productos")

            except IntegrityError:
                return render(request, "registrarse.html", {
                    "userCreateForm": UserCreationForm,
                    "error": "El usuario ya existe"
                })

        return render(request, "registrarse.html", {
            "userCreateForm": UserCreationForm,
            "error": "Las contraseñas no coinciden"
        })

@login_required
def tasks(request):

    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, "task.html", {"tasks": tasks})

@login_required
def create_task(request):

    if request.method == "GET":
        return render(request, "create_task.html", {
            "taskForm": TaskForm
        })

    else:
        try:

            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect("tasks")
        except ValueError:
            return render(request, "create_task.html", {
            "taskForm": TaskForm,
            "error": "Por favor povea informacion valida"
            })


@login_required
def task_detail(request, task_id):

    if request.method == "GET":

        task = get_object_or_404(Task, pk=task_id, user=request.user)
        form = TaskForm(instance=task)
        return render(request, "task_detail.html", {"task": task, "form": form})

    else:
        try:

            task = get_object_or_404(Task, pk=task_id, user=request.user)
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect("tasks")
        except ValueError:
            return render(request, "task_detail.html", {"task": task, "form": form, "error": "Error al actualizar tarea"})

@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == "POST":
        task.datecompleted = timezone.now()
        task.save()
        return redirect("tasks")

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == "POST":
        task.delete()
        return redirect("tasks") 

@login_required
def tasks_completed(request):
    
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=False).order_by("-datecompleted")
    return render(request, "task.html", {"tasks": tasks})
