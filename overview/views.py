from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render

from course.forms import CourseForm


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
    if request.method == 'POST':     # and request.user.has_perm('exercise.add_course'):
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()  # uncertain part
            form = CourseForm()
    else:
        form = CourseForm()
    course_list = get_course_list(request.user.username)
    return render(request, 'overview.html', {'courseList': course_list, 'form': form})
