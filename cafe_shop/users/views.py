from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from .forms import LoginForm, RegisterForm
from django.views.generic import TemplateView

@require_http_methods(["GET", "POST"])
def user_login(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Добро пожаловать, {username}!')
                return redirect('home')
        messages.error(request, 'Неверное имя пользователя или пароль')
    else:
        form = LoginForm()

    return render(request, 'users/login.html', {'form': form})

@login_required
def user_logout(request):
    logout(request)
    messages.success(request, "Вы успешно вышли из системы")
    return redirect('home') 

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Аккаунт {username} создан!')
            return redirect('login')
    else:
        form = RegisterForm()
    
    return render(request, 'users/register.html', {'form': form})

class ProfileView(TemplateView):
    template_name = 'users/profile.html'