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
        question_list=selected_pks
    )
    col.exercises.add(new_e)
    return new_e


def make_rec(username, course):
    # Creates a distribution which can be fed to the gen_* methods
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


def main():
    rec = make_rec('Pål', 'TDT4140')
    gen_exercise(2, rec, 'Pål', 'TDT4140')
    gen_reading_rec(3, rec)

if __name__ == '__main__':
    main()
