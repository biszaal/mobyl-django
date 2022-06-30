from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm

# Create your views here.


def home(request):
    return render(request, 'base/home.html')


def loginPage(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)

        except:
            messages.error(request, 'User does not exist.')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or Password does not exist.')

    return render(request, 'base/login.html', {'page': page})


def logoutUser(request):
    logout(request)
    return redirect('home')


def registerPage(request):
    form = UserCreationForm()
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        firstName = request.POST.get('firstName')
        lastName = request.POST.get('lastName')
        username = request.POST.get('username').lower()
        email = request.POST.get('email').lower()
        password = request.POST.get('password1')
        confirmPassword = request.POST.get('password2')

        if password == confirmPassword:
            user = User.objects.create_user(username, email, password)
            user.first_name = firstName
            user.last_name = lastName
            user.save()
            login(request, user)
            return redirect('home')

        else:
            messages.error('Passwords does not match')

    return render(request, 'base/login.html', {'form': form})
