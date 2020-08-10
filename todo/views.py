"""
>here we are using the built in user form of django for signup
>we have got the names of the html forms of the django form by inspect that form in the browser
> putting '@login_required' this peice of line will not allow to user access that page until they login
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import TodoForm
from .models import Todo
from django.utils import timezone
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'todo/home.html')


def signupuser(request):
    if request.method == "GET":
        return render(request, 'todo/signupuser.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                # creating a user obj
                user.save()
                # saving the user object
                login(request, user)
                # logining the user so that we can redirect him/her to another page, here currenttodos,
                # it will search for this in the url.py file
                return redirect('currenttodos')
            except IntegrityError:
                # if a new user wants to sign up but the username already taken is called 'IntegrityError'
                return render(request, 'todo/signupuser.html', {'form': UserCreationForm(), 'error': 'Username is '
                                                                                                     'already take!'})
        else:
            return render(request, 'todo/signupuser.html', {'form': UserCreationForm(), 'error': 'Password did not '
                                                                                                 'match!'})


@login_required
def currenttodos(request):
    todos = Todo.objects.filter(user=request.user, dateCompleted__isnull=True)
    # Those whose dateCompleted filed is null/blank
    return render(request, 'todo/currenttodos.html', {'todos': todos})


@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


def loginuser(request):
    if request.method == 'GET':
        return render(request, 'todo/loginuser.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'todo/loginuser.html', {'form': AuthenticationForm(), 'error': 'Username or '
                                                                                                  'Password is '
                                                                                                  'incorrect'})
        else:
            login(request, user)
            return redirect('currenttodos')


@login_required
def createtodo(request):
    if request.method == 'GET':
        return render(request, 'todo/createtodo.html', {'form': TodoForm})
    else:
        try:
            form_data = TodoForm(request.POST)
            newtodo = form_data.save(commit=False)
            # commit=False means it will not save the into the db will store it initially
            newtodo.user = request.user
            newtodo.save()
            # now the data will be saved to the db
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/createtodo.html', {'form': TodoForm, 'error': 'Bad data passed in. Try again'})


@login_required
def viewtodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    # filtering the todo with the pk and username so that the user can't see the others users todo by changing the
    #  todo id in the address bar
    if request.method == "GET":
        form = TodoForm(instance=todo)
        # in django if we create a form class and instantiate with its own obj then it will be filled for automatically
        return render(request, 'todo/viewtodo.html', {'todo': todo, 'form': form})
    else:
        try:
            form = TodoForm(request.POST, instance=todo)
            # here we are getting the edited items but we can't overwrite user_id that's why we are passing the
            # 'instance=todo' so that the django can understand that we don't need to overwrite user_id
            form.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/viewtodo.html', {'todo': todo, 'form': form, 'error': 'Bad info'})


@login_required
def completetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == "POST":
        todo.dateCompleted = timezone.now()
        todo.save()
        return redirect('currenttodos')


@login_required
def deletetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == "POST":
        todo.delete()
        return redirect('currenttodos')


@login_required
def completed(request):
    todos = Todo.objects.filter(user=request.user, dateCompleted__isnull=False).order_by('-dateCompleted')
    return render(request, 'todo/completed.html', {'todos': todos})
