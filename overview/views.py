from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render
from .forms import StudentAddCourseForm
from exercise.models import Course, CourseCollection
from course.forms import CourseForm
from exercise import populate
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from course.views import *

def get_course_list(username):
    user = User.objects.get(username=username)
    userGroups = list(user.groups.all().values_list('name',flat=True))
    print(userGroups)
    course_list = []
    if 'Student' in userGroups:
        for each in user.coursecollection.courses.all():
            course_list.append((each.name, each.description))
    if 'Lecturer' in userGroups:
        for each in user.coursecollection.courses.all():
            course_list.append((each.name, each.description))
        for each in Course.objects.all():
            if list(each.administrators.all().values_list('username', flat=True)):
                course_list.append((each.name, each.description))
    print(course_list)
    return course_list


@login_required()
def courses(request):
    current_user = request.user
    if request.method == 'POST':
        if request.POST['course-select']:
            selected_course = request.POST['course-select']
            if current_user.groups.filter(name='Lecturer').exists():
                return HttpResponseRedirect('/course/'+selected_course+'/')
            else:
                return HttpResponseRedirect('/course/'+selected_course+'/')

    else:
        if current_user.groups.filter(name='Lecturer').exists():
            form = CourseForm()
        else:
            form = StudentAddCourseForm()
    course_list = get_course_list(request.user.username)
    return render(request, 'overview.html', {'courseList': course_list, 'form': form})
