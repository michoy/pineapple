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
    Generates a new exercise for a student.
    Args:
        :param course:      [str] The pk of the course which this exercise will belong to
        :param username:    [str] The username of the student who generates the exercise
        :param num:         [int] The number of questions to add to the new exercise
        :param dist_dict:   [dict] Dictionary containing themetags and a num describing priority for student.
                                Retreive from make_rec
        
    Return:
        [exercise] A new personal exercise
    """
    if len(dist_dict) == 0:
        raise ValueError('Distribution dictionary is empty, no exercise can be generated.')
    # Test that percentages add up to 100
    total = 0
    for key in dist_dict:
        total += dist_dict[key]
    if round(total, 2) != 1.00:
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
    selected_pks = list(set(selected_pks))
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
    Creates a distribution which can be fed to the gen_exercise and gen_reading_rec methods.
    The distribution indicates topic priority.
    Args:
        :param username:    [str] The username of the student
        :param course:      [str] The pk of the course for which this recommendation is valid
    Return:
        [dict] A distribution with themeTag-pk as key and a float percentage as value
    """
    # Figure out how many percent to dedicate to topic
    last_x = 5  # Bot only considers the last X of the results, so that the calculated performance can reach 100%
    user = User.objects.get(username=username)
    q_list = list(Question.objects.filter(belongsTo__pk=course).values_list('pk', flat=True))
    tag_list = []
    for each in q_list:
        tag_list.extend(list(Question.objects.get(pk=each).themeTags.values_list('pk', flat=True)))
    tag_list = list(set(tag_list))
    out_dict = {}
    work_sum = 0
    for each in tag_list:
        # How many points the user has in a topic
        correct = int(
            user.resultcollection.results.filter(question__themeTags__name=each).filter(resultVal=True).order_by('pk').
            reverse()[:last_x].aggregate(Sum('question__is_worth'))['question__is_worth__sum'] or 0
        )
        # How many points the user could have got
        possible = int(
            user.resultcollection.results.filter(question__themeTags__name=each).order_by('pk').
            reverse()[:last_x].aggregate(Sum('question__is_worth'))['question__is_worth__sum'] or 0
        )
        if possible == 0:
            new_val = 1
        else:
            new_val = (1-(correct/possible))
        work_sum += new_val
        out_dict[each] = new_val
    if work_sum == 0:
        for each in out_dict:
            out_dict[each] = 1/len(out_dict)
        return out_dict
    else:
        for each in out_dict:
            out_dict[each] = out_dict[each]/work_sum
        return out_dict


def gen_reading_rec(num, dist_dict):
    """
    Find suitable ReadingMaterial.
    Args:
        :param num:         [int] The number of recommendations to be made
        :param dist_dict:   [dict] A distribution, made by gen_rec
    :return:
        [list] A list of tuples in the format (title, link)
    """
    # Test that percentages add up to 100
    total = 0
    for key in dist_dict:
        total += dist_dict[key]
    if len(dist_dict) != 0 and round(total, 2) != 1.00:
        raise ValueError('Distribution does not add up to 1! Rather: ' + str(total))
    # Find reading material
    selected_pks = []
    for key in dist_dict:
        x = int(round((dist_dict[key] * num)))
        tag_pks = list(ThemeTag.objects.get(name=key).material.all().values_list('pk', flat=True))
        selected_pks.extend(random.sample(tag_pks, min(x, len(tag_pks))))
    selected_materials = []
    for pk in selected_pks:
        selected_materials.append((pk, ReadingMaterial.objects.get(pk=pk).link))
    return selected_materials


def gen_lecturer_exercise(course_name):
    """
    Creates data points for the lecturers exercise graph.
    Args:
        :param course_name: [str] Pk of the course in which this graph is generated
    :return:
        [tuple] The list of Exercise pks, and a list of class success percentages
    """
    exercise_list = list(Exercise.objects.filter(course__name=course_name)
                         .filter(private=False).values_list('pk', flat=True))
    data_points = []
    for ex_id in exercise_list:
        q_list = list(Exercise.objects.get(pk=ex_id).contains.all().values_list('pk', flat=True))
        correct = int(Result.objects.filter(question__title__in=q_list).filter(resultVal=True)
                      .aggregate(Sum('question__is_worth'))['question__is_worth__sum'] or 0)
        possible = int(Result.objects.filter(question__title__in=q_list)
                       .aggregate(Sum('question__is_worth'))['question__is_worth__sum'] or 0)
        if possible != 0:
            data_points.append(int((correct/possible)*100))
        else:
            data_points.append(0)
    exercise_out_list = list(Exercise.objects.filter(course__name=course_name)
                             .filter(private=False).values_list('title', flat=True))
    return exercise_out_list, data_points


def gen_lecturer_theme(course_name):
    """
    Creates data points for the lecturer ThemeTag graph.
    Args:
        :param course_name: [str] Pk of the course in which this graph is generated
    :return:
        [tuple] The list of ThemeTag pks, and a list of class success percentages
    """
    data_points = []
    # Find questions belonging to the course
    q_list = list(Question.objects.filter(belongsTo__name=course_name).values_list('title', flat=True))
    # Find tags belonging to those questions
    tag_list = []
    for q in q_list:
        tag_list.extend(Question.objects.get(title=q).themeTags.exclude(name__in=tag_list)
                        .values_list('name', flat=True))
    # Find performance for each of those tags
    for tag in tag_list:
        correct = int(Result.objects.filter(question__belongsTo__name=course_name)
                      .filter(question__themeTags__name=tag).filter(resultVal=True)
                      .aggregate(Sum('question__is_worth'))['question__is_worth__sum'] or 0)
        possible = int(Result.objects.filter(question__belongsTo__name=course_name)
                       .filter(question__themeTags__name=tag)
                       .aggregate(Sum('question__is_worth'))['question__is_worth__sum'] or 0)
        if possible != 0:
            data_points.append(int((correct/possible)*100))
        else:
            data_points.append(0)
    return tag_list, data_points


def gen_student_exercise(course_name, username):
    """
    Creates data points for the student Exercise graph.
    Args:
        :param course_name: [str] Pk of the course in which this graph is generated
        :param username:    [str] Username of the student
    :return:
        [tuple] The list of Exercise pks, list of class success percentages, list of user success percentages
    """
    user = User.objects.get(username=username)
    exercise_list = list(Exercise.objects.filter(course__name=course_name)
                         .filter(private=False).values_list('pk', flat=True))
    data_points_class = []
    data_points_student = []
    for ex_id in exercise_list:
        q_list = list(Exercise.objects.get(pk=ex_id).contains.all().values_list('pk', flat=True))
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
    exercise_out_list = list(Exercise.objects.filter(course__name=course_name)
                             .filter(private=False).values_list('title', flat=True))
    return exercise_out_list, data_points_class, data_points_student


def gen_student_theme(course_name, username):
    """
    Creates data points for the student ThemeTag graph.
    Args:
        :param course_name: [str] Pk of the course in which this graph is generated
        :param username:    [str] Username of the student
    :return:
        [tuple] The list of ThemeTag pks, list of class success percentages, list of user success percentages
    """
    user = User.objects.get(username=username)
    data_points_stud = []
    data_points_class = []
    # Find questions belonging to the course
    q_list = list(Question.objects.filter(belongsTo__name=course_name).values_list('pk', flat=True))
    # Find tags that belong to those questions
    tag_list = []
    for q in q_list:
        tag_list.extend(Question.objects.get(pk=q).themeTags.exclude(name__in=tag_list)
                        .values_list('name', flat=True))
    # Find performance for each of those tags
    for tag in tag_list:
        correct_class = int(Result.objects.filter(question__belongsTo__name=course_name)
                            .filter(question__themeTags__name=tag).filter(resultVal=True)
                            .aggregate(Sum('question__is_worth'))['question__is_worth__sum'] or 0)
        possible_class = int(Result.objects.filter(question__belongsTo__name=course_name)
                             .filter(question__themeTags__name=tag)
                             .aggregate(Sum('question__is_worth'))['question__is_worth__sum'] or 0)
        if possible_class != 0:
            data_points_class.append(int((correct_class / possible_class) * 100))
        else:
            data_points_class.append(0)
        correct_stud = int(user.resultcollection.results.filter(question__belongsTo__name=course_name)
                           .filter(question__themeTags__name=tag).filter(resultVal=True)
                           .aggregate(Sum('question__is_worth'))['question__is_worth__sum'] or 0)
        possible_stud = int(user.resultcollection.results.filter(question__belongsTo__name=course_name)
                            .filter(question__themeTags__name=tag)
                            .aggregate(Sum('question__is_worth'))['question__is_worth__sum'] or 0)
        if possible_stud != 0:
            data_points_stud.append(int((correct_stud / possible_stud) * 100))
        else:
            data_points_stud.append(0)
    return tag_list, data_points_class, data_points_stud


def retrieve_question_material(question_title, num):
    """
    Generates recommended reading material, for when the student solves a quiz
    Some hacks
    :return
        [list] of reading material pk's
    """
    tag_list = Question.objects.get(title=question_title).themeTags.all()
    material_list = []
    for each in tag_list:
        material_list.extend(each.material.all().values_list('title', flat=True))
    out_list = random.sample(material_list, min(num, len(material_list)))
    return out_list
