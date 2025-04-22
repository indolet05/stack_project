from django.shortcuts import render

def home(request):
    welcome_message = (
        f'Привет, {request.user.username}!' 
        if request.user.is_authenticated 
        else 'Добро пожаловать в Cafe Shop!'
    )
    return render(request, 'home.html', {'welcome_message': welcome_message})

def custom_404(request, exception):
    return render(request, '404.html', status=404)

def custom_500(request):
    return render(request, '500.html', status=500)