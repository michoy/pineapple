from django import forms
from apps.exercise.models import Course


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'
