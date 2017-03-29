"""pineapple URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
import overview.views
import exercise.views
import about.views
import course.views
import botTester.views

urlpatterns = [
    url(r'^$', about.views.about),
    url(r'^admin/', admin.site.urls),
    url(r'^base/', exercise.views.base),
    # url(r'^login/$', auth_views.login, {'template_name':'registration/login.html'}, name='login'),
    # url(r'^login/$', about.views.login_view, name='/login/'),
    url(r'^login/$', about.views.do_login),
    url(r'^logout/$', about.views.do_logout),
    url(r'^register/$', about.views.do_register),
    url(r'^about/', about.views.about),
    url(r'^overview/$', overview.views.courses),
    url(r'^course/$', course.views.lecturer_course_view, name='/course/'),
    url(r'^course/(?P<fagkode>[\w]{7})/$', course.views.delegate_course_view),  # TODO VI KAN KUN HA 7-TEGN FAGKODER!
    url(r'^lecturer_course/$', course.views.lecturer_course),
    url(r'^exercise/$', exercise.views.do_exercise),
    url(r'^exercise/(?P<exer_id>[0-9]+)/$', exercise.views.do_exercise),
]
