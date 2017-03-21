from django import forms

from exercise import Course


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'
