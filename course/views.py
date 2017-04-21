from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from botTester import AssistantBot
from exercise.models import *
from course.forms import PartialExerciseForm, PartialQuestionForm, ReadingMatForm, ThemeTagForm
from django.db.models import Sum


@login_required
def student_course_view(request, fagkode, done_exercise=False):
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
            return HttpResponseRedirect('/course/' + fagkode + '/' + '#exercises')
    exercise_name_list = list(Exercise.objects.filter(course__name=fagkode).filter(private=False))
    user = User.objects.get(username=request.user)
    # Collect data
    exercise_name_list.extend(user.pecollector.exercises.filter(course=fagkode))
    ex_out_list = []
    for each in exercise_name_list:     # Calculate how many points the exercise is worth
        ex_out_list.append((
            each,
            int(each.contains.aggregate(Sum('is_worth'))['is_worth__sum'] or 0)
        ))
    recommendations_list = AssistantBot.gen_reading_rec(
        num=10,
        dist_dict=AssistantBot.make_rec(username=user.username, course=fagkode)
    )
    ex_graph_data = AssistantBot.gen_student_exercise(course_name=fagkode, username=request.user)
    tag_graph_data = AssistantBot.gen_student_theme(course_name=fagkode, username=request.user)
    course_full = Course.objects.get(name=fagkode).full_name
    context = {
        'exercises': ex_out_list,
        'rec_list': recommendations_list,
        'course': fagkode,
        'course_full': course_full,
        'ex_graph_data': ex_graph_data,
        'tag_graph_data': tag_graph_data,
        'exercise_done': done_exercise,
    }
    return render(request, 'student_course.html', context)


@login_required
def lecturer_course_view(request, fagkode=''):
    added_exercise = False
    added_question = False
    added_reading_mat = False
    added_theme_tag = False
    target_pos = ''
    if fagkode == '':
        return HttpResponseRedirect('/overview')  # Redirect if no course-code has been selected
    if request.method == 'POST':
        if request.POST.get('exercise_select', False):
            selected_ex = request.POST.get('exercise_select', False)
            return HttpResponseRedirect('/exercise/' + selected_ex + '/')
        elif request.POST.get('new_exercise', False):
            form = PartialExerciseForm(fagkode, request.POST)
            target_pos = 'lect_new_q_or_e'
            if form.is_valid():
                new_exercise = form.save(commit=False)
                # Prevent name duplicates
                if new_exercise.title not in list(
                        Exercise.objects.filter(course=fagkode).values_list('title', flat=True)):
                    new_exercise.course = Course.objects.get(name=fagkode)
                    new_exercise.private = False
                    new_exercise.save()
                    added_exercise = True
        elif request.POST.get('new_question', False):
            form = PartialQuestionForm(fagkode, request.POST)
            target_pos = 'lect_new_q_or_e'
            if form.is_valid():
                new_question = form.save(commit=False)
                new_question.belongsTo = Course.objects.get(name=fagkode)
                new_question.save()
                added_question = True
        elif request.POST.get('new_reading_mat', False):
            form = ReadingMatForm(request.POST)
            target_pos = 'lect_new_r_or_t'
            if form.is_valid():
                new_reading_mat = form.save()
                current_course = Course.objects.get(pk=fagkode)
                current_course.content.add(new_reading_mat)
                added_reading_mat = True
        elif request.POST.get('new_theme_tag', False):
            form = ThemeTagForm(fagkode, request.POST)
            target_pos = 'lect_new_r_or_t'
            if form.is_valid():
                new_theme_tag = form.save()
                added_theme_tag = True
    exercise_name_list = list(Exercise.objects.filter(course__name=fagkode).filter(private=False))
    user = User.objects.get(username=request.user)
    # Collect data for graphs
    exercise_name_list.extend(user.pecollector.exercises.filter(course=fagkode))
    ex_graph_data = AssistantBot.gen_lecturer_exercise(course_name=fagkode)
    tag_graph_data = AssistantBot.gen_lecturer_theme(course_name=fagkode)
    course_full = Course.objects.get(name=fagkode).full_name
    # Add new exercise
    exercise_form = PartialExerciseForm(fagkode)
    # Add new question
    question_form = PartialQuestionForm(fagkode)
    # Add new reading material
    reading_mat_form = ReadingMatForm()
    # Add new theme tag
    theme_tag_form = ThemeTagForm(fagkode)
    context = {
        'exercises': exercise_name_list,
        'course': fagkode,
        'course_full': course_full,
        'ex_graph_data': ex_graph_data,
        'tag_graph_data': tag_graph_data,
        'exercise_form': exercise_form,
        'question_form': question_form,
        'reading_mat_form': reading_mat_form,
        'theme_tag_form': theme_tag_form,
        'added_exercise': added_exercise,
        'added_question': added_question,
        'added_reading_mat': added_reading_mat,
        'added_theme_tag': added_theme_tag,
        'target_pos': target_pos
    }
    return render(request, 'lecturer_course.html', context)


@login_required
def delegate_course_view(request, fagkode=''):
    current_user = request.user
    # Redirect lecturers
    lecturer_list = list(Course.objects.get(pk=fagkode).administrators.values_list('username', flat=True))
    if current_user.username in lecturer_list:
        return lecturer_course_view(request, fagkode)
    else:
        return student_course_view(request, fagkode)
