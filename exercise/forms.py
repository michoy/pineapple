# coding=utf-8
""" This is where forms for the exercise module are stored """
from django import forms


class TestForm(forms.Form):
    """ Can be used get data from user """
    name = forms.CharField()
    num = forms.IntegerField()


def make_question_form(choices):
    """ used to display questions. Needs to be identical to AnswerForm """

    class QuestionForm(forms.Form):
        Answer = forms.ChoiceField(choices=choices, widget=forms.RadioSelect)

    return QuestionForm


class AnswerForm(forms.Form):
    Answer = forms.CharField()
