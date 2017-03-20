from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from quiz.forms import CourseForm


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
    """OBS: lecture frot end må bruke CourseFrom fra quiz.forms"""
    if request.method == 'POST':     # and request.user.has_perm('quiz.add_course'):
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()  # uncertain part
            form = CourseForm()
    else:
        form = CourseForm()
    course_list = get_course_list(request.user.username)
    return render(request, 'courses.html', {'courseList': course_list, 'form': form})
