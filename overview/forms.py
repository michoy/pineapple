from django import forms
from exercise.models import Course


class StudentAddCourseForm(forms.Form):
    course_name = forms.CharField(max_length=20)


class CourseForm(forms.Form):
    course_name = forms.CharField(max_length=20)
