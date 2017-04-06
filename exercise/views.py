from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render
from exercise.forms import AnswerForm, make_question_form
from exercise.models import Question, ReadingMaterial, Exercise, ResultCollection
from exercise import populate
from botTester.AssistantBot import retrieve_question_material
from django.http import HttpResponseRedirect
from django.db.models import Sum


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
                        val = True,
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
        elif request.POST['next-q']:
            return goto_next_question(request, current_user, exer_id)
        return render(request, 'exercise.html', {'form': form, 'correct': correct, 'wrong': wrong,'que_pk': que.title, 'que_que': que.question,})
    else:
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
        reading_material_ids = retrieve_question_material(que.title, 5)
        read_mats = []
        for rm_id in reading_material_ids:
            read_mats.append(ReadingMaterial.objects.get(title=rm_id))

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
            'prog_num': prog_num,
        }
        return render(request, 'exercise.html', context)
    else:
        course_name = Exercise.objects.get(pk=exer_id).course.name
        # TODO: add something to tell the user that this exercise is done
        return HttpResponseRedirect('/course/' + course_name + '/')