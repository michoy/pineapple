from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from exercise.models import *

@login_required
def student_course_view(request):
    user = request.user
    if request.method == 'GET':
        tempCourseName = 'TDT4140'
        #course = request['course]
        course = tempCourseName
        exercise_name_list = list(Exercise.objects.filter(course__name=course).values_list('title', flat=True))
        return render(request, 'student_course.html', {'exercises':exercise_name_list, 'course':course})
    else:
        pass

@login_required
def lecturer_course_view(request):
    user = request.user
    if request.method == 'GET':
        tempCourseName = 'TDT4140'
        # course = request['course]
        course = tempCourseName
        exercise_name_list = list(Exercise.objects.filter(course__name=course).filter(private=False).values_list('title', flat=True))
        return render(request, 'student_course.html', {'exercises': exercise_name_list, 'course': course})
    else:
        pass

