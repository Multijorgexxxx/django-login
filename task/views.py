from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.utils import timezone
from django.contrib.auth.decorators import login_required


from task.models import tareas
from .forms import tareasForm
# Create your views here.


def home(request):
    return render(request, 'home.html')


def signup(request):

    if request.method == 'GET':
        print("Enviando")
        return render(request, 'signup.html', {'form': UserCreationForm})
    else:
        print('Recibiendo')
        print(request.POST)

        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password2'])
                user.save()
                login(request, user)
                return redirect('tasks')
            except:
                return render(request, 'signup.html', {'form': UserCreationForm, 'error': 'Error del Procesado'})

        else:
            return render(request, 'signup.html', {'form': UserCreationForm, 'error': 'Contraseñas no coinciden'})


@login_required
def tasks(request):

    tareas_list = tareas.objects.filter(
        usuario=request.user, dia_competado__isnull=True)

    return render(request, 'tasks.html', {'tareas': tareas_list})


@login_required
def tasks_completed(request):

    tareas_list = tareas.objects.filter(
        usuario=request.user, dia_competado__isnull=False).order_by('-dia_competado')

    return render(request, 'tasks.html', {'tareas': tareas_list})


@login_required
def signout(request):
    logout(request)
    return redirect('signin')


def signin(request):
    if request.method == 'GET':
        form = AuthenticationForm
        return render(request, 'signin.html', {'form': form})
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])

        if user is None:
            form = AuthenticationForm
            return render(request, 'signin.html', {'form': form, 'error': 'Usario o Clave Incorrecta!'})
        else:
            login(request, user)
            return redirect('home')


@login_required
def createtasks(request):
    if request.method == "GET":
        form = tareasForm()
        return render(request, 'create_task.html', {"form": form})
    else:
        try:
            form = tareasForm(request.POST)
            new_tarea = form.save(commit=False)
            new_tarea.usuario = request.user
            new_tarea.save()
            print(new_tarea)
            return redirect('tasks')
        except ValueError:
            return render(request, 'create_task.html', {"form": form, "error": 'Por favor validar datos'})


@login_required
def task_detail(request, task_id):
    if request.method == 'GET':
        tarea = get_object_or_404(tareas, pk=task_id, usuario=request.user)
        form = tareasForm(instance=tarea)
        print(tarea)
        return render(request, 'tasks_detail.html', {'tarea': tarea, 'form': form})
    else:
        try:
            tarea = get_object_or_404(tareas, pk=task_id, usuario=request.user)
            form = tareasForm(request.POST, instance=tarea)
            edit_tarea = form.save(commit=False)
            edit_tarea.usuario = request.user
            edit_tarea.save()
            print(edit_tarea)
            return redirect('tasks')
        except ValueError:
            return render(request, 'tasks_detail.html', {'tarea': tarea, "form": form, "error": 'Por favor validar datos'})


@login_required
def task_complete(request, task_id):
    if request.method == 'GET':
        tarea = get_object_or_404(tareas, pk=task_id, usuario=request.user)
        form = tareasForm(instance=tarea)
        print(tarea)
        return render(request, 'tasks_detail.html', {'tarea': tarea, 'form': form})
    else:
        try:
            tarea = get_object_or_404(tareas, pk=task_id, usuario=request.user)
            tarea.dia_competado = timezone.now()
            tarea.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'tasks_detail.html', {'tarea': tarea, "form": form, "error": 'Por favor validar datos'})


@login_required
def task_delete(request, task_id):
    if request.method == 'GET':
        tarea = get_object_or_404(tareas, pk=task_id, usuario=request.user)
        form = tareasForm(instance=tarea)
        print(tarea)
        return render(request, 'tasks_detail.html', {'tarea': tarea, 'form': form})
    else:
        try:
            tarea = get_object_or_404(tareas, pk=task_id, usuario=request.user)
            tarea.delete()
            return redirect('tasks')
        except ValueError:
            return render(request, 'tasks_detail.html', {'tarea': tarea, "form": form, "error": 'Por favor validar datos'})
