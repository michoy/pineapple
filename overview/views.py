from course.forms import CourseForm
from course.views import *
from .forms import StudentAddCourseForm


def get_course_list(username):
    user = User.objects.get(username=username)
    user_groups = list(user.groups.all().values_list('name', flat=True))
    course_list = []
    if 'Student' in user_groups:
        for each in user.coursecollection.courses.all():
            course_list.append((each.name, each.description))
    if 'Lecturer' in user_groups:
        for each in user.coursecollection.courses.all():
            course_list.append((each.name, each.description))
        for each in Course.objects.all():
            if list(each.administrators.all().values_list('username', flat=True)):
                course_list.append((each.name, each.description))
    return course_list


@login_required()
def courses(request):
    current_user = request.user
    if request.method == 'POST':
        if request.POST['course-select']:
            selected_course = request.POST['course-select']
            if current_user.groups.filter(name='Lecturer').exists():
                return HttpResponseRedirect('/course/' + selected_course + '/')
            else:
                return HttpResponseRedirect('/course/' + selected_course + '/')

    else:
        if current_user.groups.filter(name='Lecturer').exists():
            form = CourseForm()
        else:
            form = StudentAddCourseForm()
    course_list = get_course_list(request.user.username)
    return render(request, 'overview.html', {'courseList': course_list, 'form': form})
