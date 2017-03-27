from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from about.forms import LoginForm
from about.forms import RegisterForm


def about(request):
    return render(request, 'about.html')


def register(request):
    return render(request, 'registration/register.html')


def login_view(request):
    if request.method == 'POST':
        #if 'login-submit' in request.POST:
        form = LoginForm(request.POST or None)
        if form.is_valid():
            user = form.login(request)
            if user:
                login(request, user)
                return HttpResponseRedirect("/overview/")  # Redirect to a success page.
        return render(request, 'registration/login.html', {'form': form })        # Redirect etter feilet innlogging
        #elif 'register-submit' in request.POST:
        #    form = RegisterForm(request.POST or None)
        #    if form.is_valid():
        #        form.register()
        #        return render(request, 'base.html')  # Redirect etter registrering
        #    else:
        #        return render(request, 'registration/login.html', {'form': form })  # Redirect etter feilet registrering
    return render(request, 'registration/login.html', {'form': LoginForm(request.POST or None)})


@login_required()
def do_logout(request):
    logout(request)
    return HttpResponseRedirect('/about')


def do_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print(username)
        print(password)
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect("/overview/")
        else:
            error = True
            return render(request, 'registration/login.html', {'error': error})
    return render(request, 'registration/login.html')
