from django import forms
from exercise.models import Course, Exercise, Question


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'


class PartialExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercise
        exclude = ['course', 'private']
        widgets = {'contains': forms.CheckboxSelectMultiple}


class PartialQuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        exclude = ['belongsTo', 'is_worth']
        widgets = {'themeTags': forms.CheckboxSelectMultiple}
