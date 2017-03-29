from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from exercise.models import *
from botTester.AssistantBot import gen_exercise, make_rec


@login_required
def student_course_view(request, fagkode):
    current_user = request.user
    if fagkode == '':
        return HttpResponseRedirect('/overview')  # Redirekt hvis ingen fagkode har blitt valgt
    if request.method == 'POST':
        if request.POST.get('exercise_select', False):
            selected_ex = request.POST['exercise_select']
            print(selected_ex)
            return HttpResponseRedirect('/exercise/' + selected_ex + '/')
        elif request.POST.get('generate_exercise', False):
            reccomendation = make_rec(current_user.username, fagkode)
            new_exercise = gen_exercise(10, reccomendation, current_user.username, fagkode)
            current_user.pecollector.exercises.add(new_exercise)
            return HttpResponseRedirect('/course/' + fagkode + '/')
    else:
        exercises = list(Exercise.objects.filter(course__name=fagkode).filter(private=False))
        context = {
            'exercises': exercises,
            'course': fagkode,
        }
        return render(request, 'student_course.html', context)


@login_required
def lecturer_course_view(request, fagkode=''):
    if fagkode == '':
        return HttpResponseRedirect('/overview')  # Redirekt hvis ingen fagkode har blitt valgt
    if request.method == 'POST':
        if request.POST['exercise-select']:
            selected_ex = request.POST['exercise-select']
            return HttpResponseRedirect('/exercise/' + selected_ex + '/')
    else:
        exercise_id_list = list(Exercise.objects.filter(course__name=fagkode).filter(private=False)
                                  .values_list('id', flat=True))
        user = User.objects.get(username=request.user)
        exercise_id_list.extend(user.pecollector.exercises.filter(course=fagkode))
        return render(request, 'student_course.html', {'exercises': exercise_id_list, 'course': fagkode})


@login_required
def delegate_course_view(request, fagkode=''):
    current_user = request.user
    if current_user.groups.filter(name='Lecturer').exists():
        return lecturer_course_view(request, fagkode)
    else:
        return student_course_view(request, fagkode)


def lecturer_course(request):
    return render(request, 'lecturer_course.html')
