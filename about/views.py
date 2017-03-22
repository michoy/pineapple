from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.shortcuts import render
from about.forms import LoginForm
from about.forms import RegisterForm
from django.contrib.auth.views import login

def login_view(request):
    if request.method=='POST':
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

