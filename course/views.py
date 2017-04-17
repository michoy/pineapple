from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from botTester import AssistantBot
from exercise.models import *
from course.forms import PartialExerciseForm, PartialQuestionForm


@login_required
def student_course_view(request, fagkode):
    current_user = request.user
    if fagkode == '':
        return HttpResponseRedirect('/overview')  # Redirect if no course-code has been selected
    if request.method == 'POST':
        if request.POST.get('exercise_select', False):
            selected_ex = request.POST['exercise_select']
            return HttpResponseRedirect('/exercise/' + selected_ex + '/')
        elif request.POST.get('generate_exercise', False):
            reccomendation = AssistantBot.make_rec(current_user.username, fagkode)
            new_exercise = AssistantBot.gen_exercise(10, reccomendation, current_user.username, fagkode)
            current_user.pecollector.exercises.add(new_exercise)
            return HttpResponseRedirect('/course/' + fagkode + '/')
    else:
        exercise_name_list = list(Exercise.objects.filter(course__name=fagkode).filter(private=False))
        user = User.objects.get(username=request.user)
        # Collect data
        exercise_name_list.extend(user.pecollector.exercises.filter(course=fagkode))
        recommendations_list = AssistantBot.gen_reading_rec(
            num=5,
            dist_dict=AssistantBot.make_rec(username=user.username, course=fagkode)
        )
        ex_graph_data = AssistantBot.gen_student_exercise(course_name=fagkode, username=request.user)
        tag_graph_data = AssistantBot.gen_student_theme(course_name=fagkode, username=request.user)
        course_full = Course.objects.get(name=fagkode).full_name
        return render(
            request,
            'student_course.html',
            {'exercises': exercise_name_list,
             'rec_list': recommendations_list,
             'course': fagkode,
             'course_full': course_full,
             'ex_graph_data': ex_graph_data,
             'tag_graph_data': tag_graph_data}
        )


@login_required
def lecturer_course_view(request, fagkode=''):
    added_exercise = False
    added_question = False
    if fagkode == '':
        return HttpResponseRedirect('/overview')  # Redirect if no course-code has been selected
    if request.method == 'POST':
        if request.POST.get('exercise_select', False):
            selected_ex = request.POST.get('exercise_select', False)
            return HttpResponseRedirect('/exercise/' + selected_ex + '/')
        elif request.POST.get('new_exercise', False):
            form = PartialExerciseForm(request.POST)
            print(form.is_valid())
            if form.is_valid():
                new_exercise = form.save(commit=False)
                new_exercise.course = Course.objects.get(name=fagkode)
                new_exercise.private = False
                new_exercise.save()
                added_exercise = True
        elif request.POST.get('new_question', False):
            form = PartialQuestionForm(request.POST)
            if form.is_valid():
                new_question = form.save(commit=False)
                new_question.belongsTo = Course.objects.get(name=fagkode)
                new_question.is_worth = 10
                new_question.save()
                added_question = True
    exercise_name_list = list(Exercise.objects.filter(course__name=fagkode).filter(private=False)
                              .values_list('id', flat=True))
    user = User.objects.get(username=request.user)
    # Collect data for graphs
    exercise_name_list.extend(user.pecollector.exercises.filter(course=fagkode))
    ex_graph_data = AssistantBot.gen_lecturer_exercise(course_name=fagkode)
    tag_graph_data = AssistantBot.gen_lecturer_theme(course_name=fagkode)
    course_full = Course.objects.get(name=fagkode).full_name
    # Add new exercise
    exercise_form = PartialExerciseForm()
    # Add new question
    question_form = PartialQuestionForm()
    context = {
        'exercises': exercise_name_list,
        'course': fagkode,
        'course_full': course_full,
        'ex_graph_data': ex_graph_data,
        'tag_graph_data': tag_graph_data,
        'exercise_form': exercise_form,
        'question_form': question_form,
        'added_exercise': added_exercise,
        'added_question': added_question,
    }
    return render(request, 'lecturer_course.html', context)


@login_required
def delegate_course_view(request, fagkode=''):
    current_user = request.user
    if current_user.groups.filter(name='Lecturer').exists():
        return lecturer_course_view(request, fagkode)
    else:
        return student_course_view(request, fagkode)
