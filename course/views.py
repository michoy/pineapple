from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from exercise.models import *
from django.http import HttpResponseRedirect
@login_required
def student_course_view(request, fagkode):
    if fagkode == '':
        return HttpResponseRedirect('/overview')  # Redirekt hvis ingen fagkode har blitt valgt
    if request.method == 'POST':
        if request.POST['exercise-select']:
            print('yah')
            selected_ex = request.POST['exercise-select']
            return HttpResponseRedirect('/exercise/' + selected_ex + '/')
    else:
    #elif request.method == 'GET':
        exercise_name_list = list(Exercise.objects.filter(course__name=fagkode).values_list('title', flat=True))
        return render(request, 'student_course.html', {'exercises':exercise_name_list, 'course':fagkode})

@login_required
def lecturer_course_view(request, fagkode=''):
    if fagkode == '':
        return HttpResponseRedirect('/overview')  # Redirekt hvis ingen fagkode har blitt valgt
    if request.method == 'GET':
        exercise_name_list = list(Exercise.objects.filter(course__name=fagkode).filter(private=False).values_list('title', flat=True))
        return render(request, 'lecturer_course.html', {'exercises': exercise_name_list, 'course': fagkode})
    #elif request.method == 'POST':
    #    if request.method["exercise-select"]:
    #        selected_ex = request.method["exercise-select"]
    #        return HttpResponseRedirect('/exercise/' + selected_ex + '/')

@login_required
def delegate_course_view(request, fagkode=''):
    current_user = request.user
    if current_user.groups.filter(name='Lecturer').exists():
        return lecturer_course_view(request,fagkode)
    else:
        return student_course_view(request,fagkode)
