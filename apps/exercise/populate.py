import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pineapple.settings")
django.setup()  # Don't mess with this, unless you know what you're doing
from django.contrib.auth.models import User
from django.contrib.auth.models import Group


# Simple script to populate the database with objects for testing and demonstration

def add_reading_material(title, link):
    material = ReadingMaterial(title=title, link=link)
    material.save()
    return material


def add_tag(name, material_list):
    tag = ThemeTag(name=name)
    tag.save()
    for each in material_list:
        tag.material.add(ReadingMaterial.objects.get(title=each))
    tag.save()
    return tag

def add_course(name, admin_list, material_list, description):
    course = Course(name=name, description=description)
    course.save()
    for each in admin_list:
        course.administrators.add(User.objects.get(username=each))
    for each in material_list:
        course.content.add(ReadingMaterial.objects.get(title=each))
    course.save()
    return course


def add_question(title, question, alternative_list, correct_num, tag_list, belongs_to, is_worth):
    new_q = Question(
        title=title,
        question=question,
        alternative_1=alternative_list[0],
        alternative_2=alternative_list[1],
        alternative_3=alternative_list[2],
        alternative_4=alternative_list[3],
        correct_alternative=correct_num,
        belongsTo=Course.objects.get(name=belongs_to),
        is_worth=is_worth
    )
    new_q.save()
    for each in tag_list:
        new_q.themeTags.add(ThemeTag.objects.get(name=each))
    new_q.save()
    return new_q

    # TODO: Rewrite question to allow arbitrary amount of alternatives?


def add_exercise(title, course, question_list):
    exercise = Exercise(title=title, course=Course.objects.get(name=course))
    exercise.save()
    for each in question_list:
        exercise.contains.add(Question.objects.get(title=each))
    exercise.save()
    return exercise


def add_result(val, question, student):
    result = Result(
        resultVal=val,
        question=Question.objects.get(title=question)
    )
    result.save()
    user = User.objects.get(username=student)
    try:
        col = User.objects.get(username=user.get_username()).resultcollection.results.add(result)
    except:
        col = add_resultcollection(user.get_username(), [result.pk])
    return result

def add_coursecollection(student, course_list):
    course_col = CourseCollection(student=User.objects.get(username=student))
    course_col.save()
    for each in course_list:
        course_col.courses.add(Course.objects.get(name=each))
    course_col.save()
    return course_col

def add_exercisecollection(student, exercise_list):
    exercise_col = PECollector(student=User.objects.get(username=student))
    exercise_col.save()
    for each in exercise_list:
        exercise_col.exercises.add(Exercise.objects.get(name=each))
    exercise_col.save()
    return exercise_col

def add_resultcollection(student, result_pk_list):
    result_col = ResultCollection(student=User.objects.get(username=student))
    result_col.save()
    for each in result_pk_list:
        result_col.results.add(Result.objects.get(pk=each))
    result_col.save()
    return result_col

def main():
    # Delete existing entries
    ReadingMaterial.objects.all().delete()
    ThemeTag.objects.all().delete()
    User.objects.filter(is_superuser=0).delete()
    Course.objects.all().delete()
    Question.objects.all().delete()
    Exercise.objects.all().delete()
    Result.objects.all().delete()
    # Reading material:
    add_reading_material('google', 'www.google.com')
    add_reading_material('wikipedia', 'www.wikipedia.com')
    add_reading_material('its', 'www.itslearning.com')
    add_reading_material(
        'TDT4140 Assessment Criteria',
        'https://ntnu.itslearning.com/file/download.aspx?FileID=4682507&FileVersionID=-1&ChildID=-1'
    )
    add_reading_material(
        'TDT4140 Project Milestones',
        'https://ntnu.itslearning.com/file/download.aspx?FileID=4684192&FileVersionID=-1&ChildID=-1'
    )
    add_reading_material(
        'TDT4140 Project Description',
        'https://ntnu.itslearning.com/file/download.aspx?FileID=4686464&FileVersionID=-1&ChildID=-1'
    )
    add_reading_material(
        'TDT4140 Poster Layout',
        'https://ntnu.itslearning.com/file/download.aspx?FileID=4691171&FileVersionID=-1&ChildID=-1'
    )
    add_reading_material(
        'Improving Needed Posters',
        'https://ntnu.itslearning.com/file/download.aspx?FileID=4735595&FileVersionID=-1&ChildID=-1'
    )
    add_reading_material(
        'Exercise class 1 - exploration phase',
        'https://ntnu.itslearning.com/file/download.aspx?FileID=4684246&FileVersionID=-1&ChildID=-1'
    )
    add_reading_material(
        'Bot Technologies',
        'https://ntnu.itslearning.com/file/download.aspx?FileID=4692502&FileVersionID=-1&ChildID=-1'
    )
    add_reading_material(
        'Bot Code Examples',
        'https://ntnu.itslearning.com/file/download.aspx?FileID=4692504&FileVersionID=-1&ChildID=-1'
    )
    add_reading_material(
        'Git planning',
        'http://bit.do/tdt4140-git'
    )
    add_reading_material(
        'Sprint planning',
        'http://bit.do/tdt4140-sprint'
    )
    add_reading_material(
        'Unit Testing',
        'https://ntnu.itslearning.com/file/download.aspx?FileID=4712822&FileVersionID=-1&ChildID=-1'
    )
    add_reading_material(
        'Unit testing code examples',
        'https://ntnu.itslearning.com/file/download.aspx?FileID=4713066&FileVersionID=-1&ChildID=-1'
    )
    add_reading_material(
        'Software Architecture',
        'https://applications.itslearning.com/Resource/Proxy/DownloadRedirect.ashx?LearningObjectId=14824289&'
        'LearningObjectInstanceId=30536736'
    )
    add_reading_material(
        'Software Quality Assurance',
        'https://ntnu.itslearning.com/file/download.aspx?FileID=4747391&FileVersionID=-1&ChildID=-1'
    )
    # Tags:
    add_tag('basicStuff', ['google', 'wikipedia', 'its'])
    pu_prosjekt_list = [
        'TDT4140 Assessment Criteria',
        'TDT4140 Project Milestones',
        'TDT4140 Project Description',
        'TDT4140 Poster Layout',
        'Improving Needed Posters'
        ]
    add_tag('PU-prosjekt', pu_prosjekt_list)
    add_tag('Exercise Lecture 1', ['Exercise class 1 - exploration phase'])
    add_tag('Exercise Lecture 2', ['Bot Technologies', 'Bot Code Examples'])
    add_tag('Exercise Lecture 3', ['Git planning', 'Sprint planning'])
    add_tag('Exercise Lecture 4', ['Unit Testing', 'Unit testing code examples'])
    add_tag('Exercise LEcture 5', ['Software Architecture'])
    add_tag('Exercise Lecture 6', ['Software Quality Assurance'])
    exercise_list = [
        'Exercise class 1 - exploration phase',
        'Bot Technologies',
        'Bot Code Examples',
        'Git planning',
        'Sprint planning',
        'Unit Testing',
        'Unit testing code examples',
        'Software Architecture',
        'Software Quality Assurance'
         ]
    add_tag('Exercise Lectures', exercise_list)
    # Lecturers
    group = Group.objects.get(name='Lecturer')
    lect = User.objects.create_user(username='Pekka', email='the@man.com', password='kanban')
    lect.groups.add(group)
    lect = User.objects.create_user(username='RandomStudAss', email='red@shirt.com', password='ctrlCctrlV')
    lect.groups.add(group)

    # Students
    group = Group.objects.get(name='Student')
    stud = User.objects.create_user(username='Per', email='pers@son.no', password='personifikasjon')
    stud.groups.add(group)
    stud = User.objects.create_user(username='Pål', email='pål@son.no', password='ape')
    stud.groups.add(group)
    stud = User.objects.create_user(username='Sofie', email='sofie@notstud.ntnu.no', password='apple')
    stud.groups.add(group)
    # Course:
    add_course('TDT4140', ['Pekka'], pu_prosjekt_list + exercise_list, 'Beware the 27.4')
    add_course('NyttFag',['Pekka'],[], 'Someone forgot to add a description')

    #Course collections:
    add_coursecollection('Per', ['TDT4140'])
    add_coursecollection('Pål', ['TDT4140', 'NyttFag'])
    add_coursecollection('Sofie', ['TDT4140'])
    add_coursecollection('Pekka', ['TDT4140'])
    add_coursecollection('RandomStudAss', ['NyttFag'])

    # Question:
    add_question(
        'Q1',
        'My car says',
        ['dingdong', 'clingcling', 'boom', 'poof'],
        2,
        ['basicStuff'],
        'TDT4140',
        11
    )
    add_question(
        'Q2',
        'What day is it?',
        ['monday', 'april 27', 'payday', 'taco-friday'],
        4,
        ['basicStuff', 'PU-prosjekt'],
        'TDT4140',
        2
    )
    add_question(
        'Q3',
        'You should use:',
        ['GitHub', 'Common Sense', 'Itslearning', 'All of the above'],
        4,
        ['Exercise Lectures', 'Exercise Lecture 3'],
        'TDT4140',
        5
    )

    # Exercises:
    add_exercise('Quiz 1', 'TDT4140', ['Q1', 'Q2', 'Q3'])
    add_exercise('New and empty', 'TDT4140', [])
    # Results:
    add_result(True, 'Q1', 'Per')
    add_result(True, 'Q1', 'Pål')
    add_result(True, 'Q1', 'Sofie')
    add_result(False, 'Q2', 'Per')
    add_result(False, 'Q2', 'Pål')
    add_result(True, 'Q2', 'Sofie')
    add_result(True, 'Q3', 'Per')
    add_result(True, 'Q3', 'Pål')


if __name__ == '__main__':
    main()
