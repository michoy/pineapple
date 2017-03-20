from django.shortcuts import render

from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.models import User

# Create your views here.

def getCourseList(username):
    user = User.objects.get(username=username)
    courseList = []
    for each in user.coursecollection.courses.all():
        courseList.append((each.name,each.description))
    return courseList


def courses(request):
    courseList = getCourseList(request.user.username)
    return render(request,'courses.html', {'courseList': courseList})

