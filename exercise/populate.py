import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pineapple.settings")
django.setup()  # Don't mess with this, unless you know what you're doing
from django.contrib.auth.models import Group
from exercise.models import *


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


def add_course(name, full_name, admin_list, material_list, description):
    course = Course(name=name, full_name=full_name, description=description)
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


def add_exercise(title, course, question_list, private=False):
    exercise = Exercise(
        title=title,
        course=Course.objects.get(name=course),
        private=private)
    exercise.save()
    for each in question_list:
        exercise.contains.add(Question.objects.get(title=each))
    exercise.save()
    return exercise


def add_result(val, question, student, exercise):
    result = Result(
        resultVal=val,
        question=Question.objects.get(title=question),
        exercise=Exercise.objects.get(pk=exercise)
    )
    result.save()
    user = User.objects.get(username=student)
    try:
        col = User.objects.get(username=user.get_username()).resultcollection.results.add(result)
    except:
        col = add_resultcollection(user.get_username(), [result.pk])
    return result


def add_coursecollection(student, course_list):
    user = User.objects.get(username=student)
    try:
        course_col = user.coursecollection
        for each in course_list:
            course_col.courses.add(Course.objects.get(name=each))
        course_col.save()
    except:
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
        exercise_col.exercises.add(Exercise.objects.get(id=each))
    exercise_col.save()
    return exercise_col


def add_resultcollection(student, result_pk_list):
    result_col = ResultCollection(student=User.objects.get(username=student))
    result_col.save()
    for each in result_pk_list:
        result_col.results.add(Result.objects.get(pk=each))
    result_col.save()
    return result_col


def add_user_group(name):
    new_group = Group()
    new_group.name = name
    new_group.save()
    return new_group


def add_user(username, email, password, course_list, result_pk_list, pers_exercise_list, group_name_list):
    user = User.objects.create_user(username=username, email=email, password=password)
    add_exercisecollection(student=username, exercise_list=pers_exercise_list)
    add_coursecollection(student=username, course_list=course_list)
    add_resultcollection(student=username, result_pk_list=result_pk_list)
    for each in group_name_list:
        user.groups.add(Group.objects.get(name=each))
    return user

def main():
    # Delete existing entries
    ReadingMaterial.objects.all().delete()
    ThemeTag.objects.all().delete()
    User.objects.filter(is_superuser=0).delete()
    Group.objects.all().delete()
    Course.objects.all().delete()
    Question.objects.all().delete()
    Exercise.objects.all().delete()
    Result.objects.all().delete()
    # Reading material:
    add_reading_material('google', 'http://www.google.com')
    add_reading_material('wikipedia', 'http://www.wikipedia.com')
    add_reading_material('its', 'http://www.itslearning.com')
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
    add_reading_material(
        'Newtons Laws of Gravity',
        'https://www.grc.nasa.gov/www/k-12/airplane/newton.html'
    )
    add_reading_material(
        'Work, energy, power',
        'http://hyperphysics.phy-astr.gsu.edu/hbase/work.html'
    )
    add_reading_material(
        'Newtons Laws',
        'http://hyperphysics.phy-astr.gsu.edu/hbase/Newt.html'
    )
    add_reading_material(
        'Thermodynamics Khan Academy',
        'https://nb.khanacademy.org/science/chemistry/thermodynamics-chemistry'
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
    physics_reading_material_list = [
        'Newtons Laws of Gravity',
        'Work, energy, power',
        'Newtons Laws'
    ]
    add_tag('Mechanics', physics_reading_material_list)
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

    # Add groups (needed for unit testing)
    # TODO add permissions
    lecturergroup = add_user_group('Lecturer')
    studentgroup = add_user_group('Student')

    # Lecturers
    add_user(
        username='Pekka',
        email='the@man.com',
        password='kanban',
        course_list=[],
        pers_exercise_list=[],
        result_pk_list=[],
        group_name_list=['Lecturer'],
    )
    add_user(
        username='RandomStudAss',
        email='red@shirt.com',
        password='ctrlCctrlV',
        course_list=[],
        pers_exercise_list=[],
        result_pk_list=[],
        group_name_list=['Lecturer', 'Student'],
    )

    add_user(
        username='Magnus',
        email='red@shirt.com',
        password='ctrlCctrlV',
        course_list=[],
        pers_exercise_list=[],
        result_pk_list=[],
        group_name_list=['Lecturer', 'Student'],
    )

    add_user(
        username='Bovim',
        email='red@shirt.com',
        password='ctrlCctrlV',
        course_list=[],
        pers_exercise_list=[],
        result_pk_list=[],
        group_name_list=['Lecturer', 'Student'],
    )

    # Course:
    add_course('TDT4140','Programvareutvikling' , ['Pekka'], pu_prosjekt_list + exercise_list, 'Beware the 27.4')
    add_course('TMA4100', 'Matematikk 1', ['Pekka'], [], 'Matte 1')
    add_course('TFY4125', 'Fysikk', ['Magnus'], physics_reading_material_list, 'Exam will consist of multiple choice questions')
    add_course('TDT4145', 'Datamodellering og databasesystemer', ['Bovim'], [], 'Databaser for n00bs')
    
    # Students
    add_user(
        username='Per',
        email='pers@son.no',
        password='personifikasjon',
        course_list=['TDT4140'],
        pers_exercise_list=[],
        result_pk_list=[],
        group_name_list=['Student']
    )
    add_user(
        username='Pål',
        email='pål@son.no',
        password='ape',
        course_list=['TDT4140'],
        pers_exercise_list=[],
        result_pk_list=[],
        group_name_list=['Student']
    )
    add_user(
        username='Sofie',
        email='sofie@notstud.ntnu.no',
        password='apple',
        course_list=['TDT4140'],
        pers_exercise_list=[],
        result_pk_list=[],
        group_name_list=['Student']
    )


    # Question:
    add_question(
        'Q1',
        'What day is it?',
        ['monday', 'april 27', 'payday', 'taco-friday'],
        4,
        ['basicStuff', 'PU-prosjekt'],
        'TDT4140',
        2
    )
    add_question(
        'Q2',
        'My car says',
        ['dingdong', 'clingcling', 'boom', 'poof'],
        2,
        ['basicStuff'],
        'TDT4140',
        11
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

    add_question(
        'TFY4125_Q1',
        'What is Newtons secound law of physics?',
        ['E=mc^2','B=aD','F=ma','F=0.5mv^2'],
        3,
        ['Mechanics'],
        'TFY4125',
        5
    )
    add_question(
        'TFY4125_Q2',
        'What is the speed of light?',
        ['300 m/s','10^8 m/s','300 000 km/s', '3*10^9 m/s'],
        3,
        ['Mechanics'],
        'TFY4125',
        5
    )
    add_question(
        'TFY4125_Q3',
        'Work is ...',
        ['Displacement times force', 'Hard!','Measured in newton', 'invers proportional to force'],
        1,
        ['Mechanics'],
        'TFY4125',
        5
    )

    # Exercises:
    ex_1 = add_exercise('Quiz 1', 'TDT4140', ['Q1', 'Q2', 'Q3'])
    ex_2 = add_exercise('New and empty', 'TDT4140', [])
    ex_3 = add_exercise('TFY4125_Exercise1', 'TFY4125', ['TFY4125_Q1', 'TFY4125_Q2', 'TFY4125_Q3'])

    # Results:
    add_result(True, 'Q1', 'Per', ex_1.pk)
    #add_result(True, 'Q1', 'Pål', ex_1.pk)
    add_result(True, 'Q1', 'Sofie', ex_1.pk)
    add_result(False, 'Q2', 'Per', ex_1.pk)
    #add_result(False, 'Q2', 'Pål', ex_1.pk)
    add_result(True, 'Q2', 'Sofie', ex_1.pk)
    add_result(True, 'Q3', 'Per', ex_1.pk)
    #add_result(True, 'Q3', 'Pål', ex_1.pk)


if __name__ == '__main__':
    main()
