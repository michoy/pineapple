from django.shortcuts import render

# Create your views here.
def lecturer_course(request):
    return render(request, 'lecturer_course.html')
