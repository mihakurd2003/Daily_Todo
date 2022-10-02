from django.contrib import messages
from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from .models import Todo
from .forms import TodoForm


def home(request):
    return render(request, 'todo/home.html')


def signup_user(request):
    if request.method == 'POST':
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    username=request.POST['username'],
                    password=request.POST['password1'],
                )
                user.save()
                login(request, user)
                return redirect('current_todos')
            except IntegrityError:
                return render(request, 'todo/signup_user.html', {'form': UserCreationForm(), 'error': 'Username didn\'t match'})
        else:
            return render(request, 'todo/signup_user.html', {'form': UserCreationForm(), 'error': 'Password didn\'t match'})

    return render(request, 'todo/signup_user.html', {'form': UserCreationForm()})


def login_user(request):
    if request.method == 'POST':
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'todo/login_user.html', {'form': AuthenticationForm(), 'error': 'Invalid data, try again'})

        login(request, user)
        return redirect('home')

    return render(request, 'todo/login_user.html', {'form': AuthenticationForm()})


@login_required
def logout_user(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


@login_required
def create_todos(request):
    if request.method == 'POST':
        try:
            form = TodoForm(request.POST)
            new_form = form.save(commit=False)
            new_form.user = request.user
            new_form.save()
            return redirect('current_todos')
        except ValueError:
            return render(request, 'todo/create_todos.html', {'form': TodoForm(), 'error': 'ValueError'})
    else:
        form = TodoForm()

    return render(request, 'todo/create_todos.html', {'form': form})


@login_required
def current_todos(request):
    try:
        todos = Todo.objects.filter(user=request.user, date_completed__isnull=True)
        return render(request, 'todo/current_todos.html', {'todos': todos})
    except TypeError:
        return render(request, 'todo/home.html', {'error': 'Please, log in or sign up'})


@login_required
def completed_todos(request):
    try:
        todos = Todo.objects.filter(user=request.user, date_completed__isnull=False).order_by('-date_completed')
        return render(request, 'todo/completed_todos.html', {'todos': todos})
    except TypeError:
        return render(request, 'todo/home.html', {'error': 'Please, log in or sign up'})


@login_required
def see_todo(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id, user=request.user)
    form = TodoForm(instance=todo)
    if request.method == 'POST':
        try:
            form = TodoForm(request.POST, instance=todo)
            form.save()
            return redirect('current_todos')
        except ValueError:
            return render(request, 'todo/see_todo.html', {'todo': todo, 'form': form, 'error': 'ValueError'})

    return render(request, 'todo/see_todo.html', {'todo': todo, 'form': form})


@login_required
def complete_todo(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id, user=request.user)
    if request.method == 'POST':
        todo.date_completed = timezone.now()
        todo.save()
        return redirect('current_todos')


@login_required
def delete_todo(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id, user=request.user)

    if request.method == 'POST':
        todo.delete()
        return redirect('current_todos')


@login_required
def restore_todo(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id, user=request.user)

    if request.method == 'POST':
        todo.date_completed = None
        todo.save()
        return redirect('completed_todos')
