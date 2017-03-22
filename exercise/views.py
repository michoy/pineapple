from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.shortcuts import render
from exercise.models import Question, Exercise, ResultCollection, Result
from exercise.forms import QuestionForm, make_answer_form
from django.db.models import Q


def base(request):
    return render(request, 'base.html')


@login_required()
def do_exercise(request):
    """ Displayes the question in the answer-question site """
    current_user = request.user
    if request.method == 'POST':
        pass
    else:
        result_cols = ResultCollection.results
        exercise = Exercise.objects.first()
        #question = exercise.contains.exclude.first()
        stuff = result_cols
        choices = (
            ('alt_1', 'Blue'),
            ('alt_2', 'Green'),
            ('alt_3', 'Black'),
        )
        que_form = make_answer_form(choices)
        context = {
            'form': que_form,
            'stuff': stuff,
        }
        return render(request, 'exercise.html', context)
