from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render
from .forms import StudentAddCourseForm
from exercise.models import Course, CourseCollection
from course.forms import CourseForm
from exercise import populate


def get_course_list(username):
    user = User.objects.get(username=username)
    course_list = []
    if hasattr(user, 'coursestudent'):
        for each in user.coursestudent.courses.all():
            course_list.append((each.name, each.description))
    if hasattr(user, 'courseadmin'):
        for each in user.courseadmin.courses.all():
            course_list.append((each.name, each.description))
    return course_list


@login_required()
def courses(request):
    current_user = request.user
    if request.method == 'POST':
        if current_user.groups.filter(name='Lecturer').exists():
            form = CourseForm(request.POST)
            if form.is_valid():
                form.save()
                form = CourseForm()
        else:
            form = StudentAddCourseForm(request.POST)
            if form.is_valid():
                course_name = form.cleaned_data.get('course_name')
                if Course.objects.filter(course_name).exists():
                    course = Course.objects.get(course_name)
                    populate.add_coursecollection(current_user, course)

    else:
        if current_user.groups.filter(name='Lecturer').exists():
            form = CourseForm()
        else:
            form = StudentAddCourseForm()
    course_list = get_course_list(request.user.username)
    return render(request, 'overview.html', {'courseList': course_list, 'form': form})