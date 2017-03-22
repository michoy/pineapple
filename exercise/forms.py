# coding=utf-8
""" This is where forms for the exercise module are stored """
from django import forms

from exercise.models import Question


class TestForm(forms.Form):
    """ Can be used get data from user """
    name = forms.CharField()
    num = forms.IntegerField()


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = '__all__'


def make_answer_form(choices):
    class AnswerForm(forms.Form):
        Answer = forms.ChoiceField(choices=choices, widget=forms.RadioSelect)
    return AnswerForm
