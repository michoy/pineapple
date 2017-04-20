from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render
from exercise.forms import AnswerForm, make_question_form
from exercise.models import Question, ReadingMaterial, Exercise, Course, Result
from exercise import populate
from botTester.AssistantBot import retrieve_question_material
from django.http import HttpResponseRedirect
from course.views import student_course_view


def base(request):
    return render(request, 'base.html')


@login_required()
def do_exercise(request, exer_id):
    """
    1. Sends form with alternatives through context. Receives answer alternative.
    2. Evaluates it and saves the result. Sends context with correct value and empty form.
    3. recieves request without post. Send context with new alternatives (1.)
    """
    current_user = request.user
    if request.method == 'POST':
        correct = False
        wrong = False
        form = AnswerForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data  # gives an alt_#
            if request.POST['submit']:
                que_pk = request.POST['submit']
                que = Question.objects.get(title=que_pk)
                if int(data['Answer']) == que.correct_alternative:
                    correct = True
                    populate.add_result(
                        val=True,
                        question=que_pk,
                        student=current_user,
                        exercise=exer_id,
                    )
                else:
                    wrong = True
                    populate.add_result(
                        val=False,
                        question=que_pk,
                        student=current_user,
                        exercise=exer_id,
                    )
                form = []
                # Hint
                read_mats = get_hints(que_pk)
                # headline
                exercise_name = Exercise.objects.get(pk=exer_id).title
                return render(
                    request,
                    'exercise.html',
                    {'form': form,
                     'correct': correct,
                     'wrong': wrong,
                     'que_pk': que.title,
                     'que_que': que.question,
                     'exercise_name': exercise_name,
                     'read_mats': read_mats,
                     }
                )
        elif request.POST.get('next-q', False):
            return goto_next_question(request, current_user, exer_id)
    elif request.method == 'GET':
        # Redirect lecturers
        lecturer_list = list(
        Course.objects.get(pk=Exercise.objects.get(pk=exer_id).course.pk)
        .administrators.values_list('username', flat=True)
        )
        # TODO: work in progress
        if current_user.username in lecturer_list:
            return HttpResponseRedirect('/examine_exercise/' + exer_id + '/')
            return goto_next_question(request, current_user, exer_id)
    return goto_next_question(request, current_user, exer_id)


def find_next_question(student_name, exercise_pk):
    re = User.objects.get(username=student_name).resultcollection.results.all()
    ex = Exercise.objects.get(pk=exercise_pk)
    q_list = list(ex.contains.values_list('pk', flat=True))
    for q in q_list:
        res_list = re.filter(question__pk=q).filter(exercise__pk=exercise_pk)
        if res_list.count() == 0:
            return q
    return False


def goto_next_question(request, username, exer_id):
    next_pk = find_next_question(username, exer_id)
    if next_pk:
        que = Question.objects.get(pk=find_next_question(username, exer_id))
        choices = (
            ('1', que.alternative_1),
            ('2', que.alternative_2),
            ('3', que.alternative_3),
            ('4', que.alternative_4),
        )
        que_form = make_question_form(choices)

        # reading material
        read_mats = get_hints(que.pk)
        # headline
        exercise_name = Exercise.objects.get(pk=exer_id).title
        # progress number
        done_questions = len(username.resultcollection.results.filter(exercise_id=exer_id))
        q_list = len(list(Exercise.objects.get(pk=exer_id).contains.all().values_list('pk', flat=True)))
        if q_list:
            prog_num = (done_questions / q_list) * 100
        else:
            prog_num = 0
        context = {
            'form': que_form,
            'que_pk': que.title,
            'que_que': que.question,
            'read_mats': read_mats,
            'exercise_name': exercise_name,
            'prog_num': prog_num,
        }
        return render(request, 'exercise.html', context)
    course_name = Exercise.objects.get(pk=exer_id).course.name
    return student_course_view(request, course_name, True)


def get_hints(question_pk):
    # reading material
    reading_material_ids = retrieve_question_material(question_pk, 5)
    read_mats = []
    for rm_id in reading_material_ids:
        read_mats.append(ReadingMaterial.objects.get(title=rm_id))
    return read_mats


def examine_exercise(request, exer_id):
    ex = Exercise.objects.get(pk=exer_id)
    questions = []
    q_list = list(ex.contains.values_list('pk', flat=True))
    for each in q_list:
        questions.append((Question.objects.get(pk=each), Result.objects.filter(question__pk=each).count()))
    context = {
        'exercise': ex,
        'questions': questions,
    }
    return render(request, 'exercise_overview.html', context)
