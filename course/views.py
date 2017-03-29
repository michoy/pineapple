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
            selected_ex = request.POST['exercise-select']
            return HttpResponseRedirect('/exercise/' + selected_ex + '/')
    else:
        exercise_name_list = list(Exercise.objects.filter(course__name=fagkode).filter(private=False)
                                  .values_list('title', flat=True))
        user = User.objects.get(username=request.user)
        exercise_name_list.extend(user.pecollector.exercises.filter(course=fagkode))
        return render(request, 'student_course.html', {'exercises': exercise_name_list, 'course': fagkode})


@login_required
def lecturer_course_view(request, fagkode=''):
    if fagkode == '':
        return HttpResponseRedirect('/overview')  # Redirekt hvis ingen fagkode har blitt valgt
    if request.method == 'POST':
        if request.POST['exercise-select']:
            selected_ex = request.POST['exercise-select']
            return HttpResponseRedirect('/exercise/' + selected_ex + '/')
    else:
        exercise_name_list = list(Exercise.objects.filter(course__name=fagkode).filter(private=False)
                                  .values_list('title', flat=True))
        user = User.objects.get(username=request.user)
        exercise_name_list.extend(user.pecollector.exercises.filter(course=fagkode))
        return render(request, 'student_course.html', {'exercises': exercise_name_list, 'course': fagkode})


@login_required
def delegate_course_view(request, fagkode=''):
    current_user = request.user
    if current_user.groups.filter(name='Lecturer').exists():
        return lecturer_course_view(request, fagkode)
    else:
        return student_course_view(request, fagkode)


def lecturer_course(request):
    return render(request, 'lecturer_course.html')
