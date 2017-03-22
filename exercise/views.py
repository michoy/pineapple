from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.shortcuts import render
from exercise.models import Question, Exercise, ResultCollection, Result
from exercise.forms import AnswerForm, make_question_form
from django.db import connection


def base(request):
    return render(request, 'base.html')


@login_required()
def do_exercise(request):
    """ 1. Sends form with alternatives through context. Receives answer alternative.
     2. Evaluates it and saves the result. Sends context with correct value and empty form.
     3. recieves request without post. Send context with new alternatives (1.) """
    current_user = request.user
    if request.method == 'POST':
        correct = False
        form = AnswerForm(request.POST)
        if form.is_valid():
            que = 'the question obj'    # todo: keep question object in process
            data = form.cleaned_data    # gives an alt_#
            if True:       # data == righ alternative
                res = Result(True, que)
                res.save()
                rc = ResultCollection(current_user, res)        # todo: save result properly
                rc.save()
                correct = True
            else:
                res = Result(False, que)
                # osv..
            form = []
        return render(request, 'exercise.html', {'form': form, 'correct': correct})
    else:
        # todo: retrieve a valid question
        cursor = connection.cursor()
        cursor.execute(
            'SELECT question '
            'FROM auth_user  JOIN (exercise_resultcollection, exercise_resultcollection_results,exercise_result, exercise_question) '
            'ON (auth_user.id = exercise_resultcollection.student_id) AND '
            '(exercise_resultcollection.id = exercise_resultcollection_results.resultcollection_id) AND '
            '(exercise_resultcollection_results.result_id = exercise_result.id) AND '
            'exercise_result.question_id = exercise_question.title '
            'WHERE result.id = NULL'
            '')
        choices = cursor.fetchall()
        correct_ans = 'alt_1'
        que_form = make_question_form(choices, correct_ans)
        context = {
            'form': que_form,
            #'question': title,
            #'stuff': stuff,
        }
        return render(request, 'exercise.html', context)
