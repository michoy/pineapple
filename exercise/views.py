from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from exercise.forms import AnswerForm, make_question_form
from exercise.models import Question, ResultCollection, Result
from exercise import populate


def base(request):
    return render(request, 'base.html')


@login_required()
def do_exercise(request, exer_id):
    """ 1. Sends form with alternatives through context. Receives answer alternative.
     2. Evaluates it and saves the result. Sends context with correct value and empty form.
     3. recieves request without post. Send context with new alternatives (1.) """
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
        return render(request, 'exercise.html', {'form': form, 'correct': correct, 'wrong': wrong,'que_pk': que.title, 'que_que': que.question,})
    else:
        # todo: retrieve a valid question
        questions = ResultCollection.objects.raw(
            'SELECT DISTINCT R.id, R.question_id '
            'FROM exercise_resultcollection AS Rc '
            'JOIN exercise_resultcollection_results AS RcR ON Rc.id = RcR.resultcollection_id '
            'JOIN exercise_result AS R ON RcR.result_id = R.id '
            'JOIN exercise_exercise_contains AS EC ON R.question_id = EC.question_id '
            'WHERE EC.exercise_id = %s AND Rc.student_id = %s', [exer_id, current_user.id]
        )
        '''
        cursor = connection.cursor()
        cursor.execute(
            'SELECT DISTINCT EC.question_id '
            'FROM exercise_resultcollection AS Rc '
            'JOIN exercise_resultcollection_results AS RcR ON Rc.id = RcR.resultcollection_id '
            'JOIN exercise_result AS R ON RcR.result_id = R.id '
            'JOIN exercise_exercise_contains AS EC ON R.question_id = EC.question_id '
            'WHERE EC.exercise_id = %s', [exer_id]
        )
        stuff = cursor.fetchall()
        '''
        stuff = questions.columns
        que = Question.objects.first()
        choices = (
            ('1', que.alternative_1),
            ('2', que.alternative_2),
            ('3', que.alternative_3),
            ('4', que.alternative_4),
        )
        que_form = make_question_form(choices)
        context = {
            'form': que_form,
            'que_pk': que.title,
            'que_que': que.question,
        }
        return render(request, 'exercise.html', context)
