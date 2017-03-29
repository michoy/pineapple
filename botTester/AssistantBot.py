import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pineapple.settings")
django.setup()  # Don't mess with this, unless you know what you're doing
from exercise.populate import add_exercisecollection
from exercise.populate import add_exercise
from exercise.models import *
import random
from django.db.models import Sum


def gen_exercise(num, dist_dict, username, course):
    """ 
    Generates a new exercise for a student 
    
    Args:
        :param num: number of questions
        :param dist_dict: dictt containing themetags and a num describing importance for student. Retreive from make_rec
        
    Return:
        New exercise
    """
    # Test that percentages add up to 100
    total = 0
    for key in dist_dict:
        total += dist_dict[key]
    if int(total) != 1:     # Kan være round må brukes her
        raise ValueError('Distribution does not add up to 100!')
    # Make sure user has an exercise collector
    user = User.objects.get(username=username)
    try:
        col = user.pecollector
    except:
        col = add_exercisecollection(user.get_username(), [])
    # Find questions
    selected_pks = []
    for key in dist_dict:
        x = int(round((dist_dict[key]*num)))
        question_pks = list(Question.objects.filter(themeTags__name=key).values_list('pk', flat=True).distinct())
        selected_pks.extend(random.sample(question_pks, min(x, len(question_pks))))
    # Create new exercise and give to user
    new_e = add_exercise(
        title=user.username+"'s tailored Exercise "+(str(col.exercises.all().count()+1)),
        course=course,
        question_list=selected_pks,
        private=True,
    )
    col.exercises.add(new_e)
    return new_e


def make_rec(username, course):
    """ 
    Creates a distribution which can be fed to the gen_* methods
    Args:
        :param username: 
        :param course: 
    Return:
        dict: containing themetags and their importance to the user 
    """
    # Figure out how many percent to dedicate to topic
    user = User.objects.get(username=username)
    tag_list = list(user.resultcollection.results.filter(question__belongsTo=course).
                    values_list('question__themeTags', flat=True).distinct())  # Kan sikkert optimaliseres
    out_dict = {}
    work_sum = 0
    for each in tag_list:
        correct = int(user.resultcollection.results.filter(question__themeTags__name=each).filter(resultVal=True).
                      aggregate(Sum('question__is_worth'))['question__is_worth__sum'] or 0)
        possible = int(user.resultcollection.results.filter(question__themeTags__name=each).
                       aggregate(Sum('question__is_worth'))['question__is_worth__sum'] or 0)
        new_val = (1-(correct/possible))
        work_sum += new_val
        out_dict[each] = new_val
    for each in out_dict:
        out_dict[each] = out_dict[each]/work_sum
    return out_dict


def gen_reading_rec(num, dist_dict):
    # Test that percentages add up to 100
    total = 0
    for key in dist_dict:
        total += dist_dict[key]
    if int(total) != 1:
        raise ValueError('Distribution does not add up to 100!')
    # Find reading material
    selected_pks = []
    for key in dist_dict:
        x = int(round((dist_dict[key] * num)))
        tag_pks = list(ThemeTag.objects.get(name=key).material.all().values_list('pk', flat=True))
        selected_pks.extend(random.sample(tag_pks, min(x, len(tag_pks))))
    return selected_pks


def gen_graph_data(mode, username):
    # Delegate to other methods
    pass


def gen_lecturer_exercise(course_name):
    exercise_list = list(Exercise.objects.filter(course__name=course_name)
                         .filter(private=False).values_list('title', flat=True))
    data_points = []
    for ex_name in exercise_list:
        q_list = list(Exercise.objects.get(title=ex_name).contains.all().values_list('title', flat=True))
        correct = int(Result.objects.filter(question__title__in=q_list).filter(resultVal=True)
                      .aggregate(Sum('question__is_worth'))['question__is_worth__sum'] or 0)
        possible = int(Result.objects.filter(question__title__in=q_list)
                       .aggregate(Sum('question__is_worth'))['question__is_worth__sum'] or 0)
        if possible != 0:
            data_points.append(int((correct/possible)*100))
        else:
            data_points.append(0)
    return exercise_list, data_points


def gen_lecturer_theme(course_name):
    data_points = []
    # TODO: Optimaliser
    # Finn spørsmål som hører til faget
    q_list = list(Question.objects.filter(belongsTo__name=course_name).values_list('title', flat=True))
    # Finn tags som hører til disse spørsmålene
    tag_list = []
    for q in q_list:
        tag_list.extend(Question.objects.get(title=q).themeTags.exclude(name__in=tag_list)
                        .values_list('name', flat=True))
    # Finn performance for hver av disse tag-ene
    for tag in tag_list:
        correct = int(Result.objects.filter(question__belongsTo__name=course_name)
                      .filter(question__themeTags__name__contains=tag).filter(resultVal=True)
                      .aggregate(Sum('question__is_worth'))['question__is_worth__sum'] or 0)
        possible = int(Result.objects.filter(question__belongsTo__name=course_name)
                       .filter(question__themeTags__name=tag)
                       .aggregate(Sum('question__is_worth'))['question__is_worth__sum'] or 0)
        if possible != 0:
            data_points.append(int((correct/possible)*100))
        else:
            data_points.append(0)
    return tag_list, data_points

# def gen_lecturer_time(course_name):
#    pass


def gen_student_exercise(course_name, username):
    user = User.objects.get(username=username)
    exercise_list = list(Exercise.objects.filter(course__name=course_name)
                         .filter(private=False).values_list('title', flat=True))
    data_points_class = []
    data_points_student = []
    for ex_name in exercise_list:
        q_list = list(Exercise.objects.get(title=ex_name).contains.all().values_list('title', flat=True))
        correct_class = int(Result.objects.filter(question__title__in=q_list).filter(resultVal=True)
                            .aggregate(Sum('question__is_worth'))['question__is_worth__sum'] or 0)
        possible_class = int(Result.objects.filter(question__title__in=q_list)
                             .aggregate(Sum('question__is_worth'))['question__is_worth__sum'] or 0)
        if possible_class != 0:
            data_points_class.append(int((correct_class/possible_class)*100))
        else:
            data_points_class.append(0)
        correct_student = int(user.resultcollection.results.filter(question__title__in=q_list).filter(resultVal=True)
                              .aggregate(Sum('question__is_worth'))['question__is_worth__sum'] or 0)
        possible_student = int(user.resultcollection.results.filter(question__title__in=q_list)
                               .aggregate(Sum('question__is_worth'))['question__is_worth__sum'] or 0)
        if possible_student != 0:
            data_points_student.append(int((correct_student/possible_student)*100))
        else:
            data_points_student.append(0)
    return exercise_list, data_points_class, data_points_student


def gen_student_theme(course_name, username):
    user = User.objects.get(username=username)
    data_points_stud = []
    data_points_class = []
    # TODO: Optimaliser
    # Finn spørsmål som hører til faget
    q_list = list(Question.objects.filter(belongsTo__name=course_name).values_list('title', flat=True))
    # Finn tags som hører til disse spørsmålene
    tag_list = []
    for q in q_list:
        tag_list.extend(Question.objects.get(title=q).themeTags.exclude(name__in=tag_list)
                        .values_list('name', flat=True))
    # Finn performance for hver av disse tag-ene
    print(tag_list)
    for tag in tag_list:
        print(tag)
        correct_class = int(Result.objects.filter(question__belongsTo__name=course_name)
                            .filter(question__themeTags__name__contains=tag).filter(resultVal=True)
                            .aggregate(Sum('question__is_worth'))['question__is_worth__sum'] or 0)
        possible_class = int(Result.objects.filter(question__belongsTo__name=course_name)
                             .filter(question__themeTags__name=tag)
                             .aggregate(Sum('question__is_worth'))['question__is_worth__sum'] or 0)
        if possible_class != 0:
            data_points_class.append(int((correct_class / possible_class) * 100))
        else:
            data_points_class.append(0)
        correct_stud = int(user.resultcollection.results.filter(question__belongsTo__name=course_name)
                           .filter(question__themeTags__name__contains=tag).filter(resultVal=True)
                           .aggregate(Sum('question__is_worth'))['question__is_worth__sum'] or 0)
        possible_stud = int(user.resultcollection.results.filter(question__belongsTo__name=course_name)
                            .filter(question__themeTags__name=tag)
                            .aggregate(Sum('question__is_worth'))['question__is_worth__sum'] or 0)
        if possible_stud != 0:
            data_points_stud.append(int((correct_stud / possible_stud) * 100))
        else:
            data_points_stud.append(0)
    return tag_list, data_points_class, data_points_stud


# def gen_student_time(course_name):
#    pass

def main():
    rec = make_rec('Pål', 'TDT4140')
    gen_exercise(2, rec, 'Pål', 'TDT4140')
    gen_reading_rec(3, rec)
    print(gen_student_theme('TDT4140', 'Pål'))


if __name__ == '__main__':
    main()
