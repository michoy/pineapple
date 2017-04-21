from course.views import *


def get_course_list(username):
    # Get a list of the user's courses
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
    # Allow the user to select a course-page
    current_user = request.user
    if request.method == 'POST':
        if request.POST.get('course_name', False):  # add new course to student
            course_name = request.POST['course_name']
            if Course.objects.filter(name=course_name).exists():
                new_course = Course.objects.get(name=course_name)
                current_user.coursecollection.courses.add(new_course)
        elif request.POST.get('course-select', False):   # navigate to selected course
            selected_course = request.POST['course-select']
            if current_user.groups.filter(name='Lecturer').exists():
                return HttpResponseRedirect('/course/' + selected_course + '/')
            else:
                return HttpResponseRedirect('/course/' + selected_course + '/')
    course_list = get_course_list(current_user.username)
    return render(request, 'overview.html', {'courseList': course_list, 'username': current_user})
