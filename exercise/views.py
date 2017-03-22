from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.shortcuts import render
from exercise.models import Question, Exercise, ResultCollection, Result
from exercise.forms import QuestionForm, make_answer_form


def base(request):
    return render(request, 'base.html')


def do_exercise(request):
    """ Displayes the question in the answer-question site """
    current_user = request.user
    if request.method == 'POST':
        pass
    else:
        #exercise = Exercise.objects.get(id=1)
        result_cols = ResultCollection.objects.filter(student=current_user)
        done_que = result_cols.results.question
        #question = exercise.contains.exclude(done_que).first()
        stuff = done_que
        choices = (
            ('alt_1', 'Blue'),
            ('alt_2', 'Green'),
            ('alt_3', 'Black'),
            ('alt_4', )
        )
        que_form = make_answer_form(choices)
        context = {
            'form': que_form,
            'stuff': stuff,
        }
        return render(request, 'exercise.html', context)
