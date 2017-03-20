from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.shortcuts import render


#Spartansk placeholder
def login_view(request):
    if request.method=='POST':
        if 'login-submit' in request.POST:
            form = LoginForm(request.POST or None)
            if form.is_valid():
                user = form.login(request)
                if user:
                    login(request, user)
                    return HttpResponseRedirect("/courses/")  # Redirect to a success page.
            return render(request, 'index.html', {'form': form })        # Redirect etter feilet innlogging
        elif 'register-submit' in request.POST:
            form = RegisterForm(request.POST or None)
            if form.is_valid():
                form.register()
                return render(request, 'index.html')  # Redirect etter registrering
            else:
                return render(request, 'index.html', {'form': form })  # Redirect etter feilet registrering
    else:
        return render(request, 'index.html')

