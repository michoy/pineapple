from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from exercise.populate import add_user


def about(request):
    return render(request, 'about.html')


def do_register(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect("/login/")
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        if User.objects.filter(username=username).exists():  # username allready taken
            return render(request, 'registration/register.html', {'username_taken': True})
        else:  # user can be created
            user = add_user(username, email, password)
            login(request, user)
            return render(request, 'overview.html')
    else:
        return render(request, 'registration/register.html')


@login_required()
def do_logout(request):
    logout(request)
    return HttpResponseRedirect('/about')


def do_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect("/overview/")
        else:
            error = True
            return render(request, 'registration/login.html', {'error': error})
    return render(request, 'registration/login.html')
