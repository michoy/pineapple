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
        User.objects.get(username=user.get_username()).resultcollection.results.add(result)
    except:
        add_resultcollection(user.get_username(), [result.pk])
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


def add_user(username, email, password, group_name_list=['Student'], course_list=[],
             result_pk_list=[], pers_exercise_list=[]):
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
    # Must begin with https:// if you want to link to external page
    add_reading_material(
        # PU
        title='TDT4140 Assessment Criteria',
        link='https://ntnu.itslearning.com/file/download.aspx?FileID=4682507&FileVersionID=-1&ChildID=-1',
    )
    add_reading_material(
        # PU
        title='TDT4140 Project Milestones',
        link='https://ntnu.itslearning.com/file/download.aspx?FileID=4684192&FileVersionID=-1&ChildID=-1',
    )
    add_reading_material(
        # PU
        title='TDT4140 Project Description',
        link='https://ntnu.itslearning.com/file/download.aspx?FileID=4686464&FileVersionID=-1&ChildID=-1',
    )
    add_reading_material(
        # PU
        title='TDT4140 Poster Layout',
        link='https://ntnu.itslearning.com/file/download.aspx?FileID=4691171&FileVersionID=-1&ChildID=-1',
    )
    add_reading_material(
        # PU
        title='Improving Needed Posters',
        link='https://ntnu.itslearning.com/file/download.aspx?FileID=4735595&FileVersionID=-1&ChildID=-1',
    )
    add_reading_material(
        # PU
        title='Exercise class 1 - exploration phase',
        link='https://ntnu.itslearning.com/file/download.aspx?FileID=4684246&FileVersionID=-1&ChildID=-1',
    )
    add_reading_material(
        # PU
        title='Bot Technologies',
        link='https://ntnu.itslearning.com/file/download.aspx?FileID=4692502&FileVersionID=-1&ChildID=-1',
    )
    add_reading_material(
        # PU
        title='Bot Code Examples',
        link='https://ntnu.itslearning.com/file/download.aspx?FileID=4692504&FileVersionID=-1&ChildID=-1',
    )
    add_reading_material(
        # PU
        title='Git planning',
        link='http://bit.do/tdt4140-git',
    )
    add_reading_material(
        # PU
        title='Sprint planning',
        link='http://bit.do/tdt4140-sprint',
    )
    add_reading_material(
        # PU
        title='Unit Testing',
        link='https://ntnu.itslearning.com/file/download.aspx?FileID=4712822&FileVersionID=-1&ChildID=-1',
    )
    add_reading_material(
        # PU
        title='Unit testing code examples',
        link='https://ntnu.itslearning.com/file/download.aspx?FileID=4713066&FileVersionID=-1&ChildID=-1'
    )
    add_reading_material(
        # PU
        title='Software Architecture',
        link='https://applications.itslearning.com/Resource/Proxy/DownloadRedirect.ashx?LearningObjectId=14824289&'
        'LearningObjectInstanceId=30536736',
    )
    add_reading_material(
        # PU
        title='Software Quality Assurance',
        link='https://ntnu.itslearning.com/file/download.aspx?FileID=4747391&FileVersionID=-1&ChildID=-1',
    )
    add_reading_material(
        # FYS
        title='Newtons Laws of Gravity',
        link='https://www.grc.nasa.gov/www/k-12/airplane/newton.html',
    )
    add_reading_material(
        # FYS
        title='Work, energy, power',
        link='http://hyperphysics.phy-astr.gsu.edu/hbase/work.html',
    )
    add_reading_material(
        # FYS
        title='Newtons Laws',
        link='http://hyperphysics.phy-astr.gsu.edu/hbase/Newt.html',
    )
    add_reading_material(
        # FYS
        title='Thermodynamics Khan Academy',
        link='https://nb.khanacademy.org/science/chemistry/thermodynamics-chemistry',
    )
    # Tags:
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
        'Newtons Laws',
    ]
    add_tag(
        # FYS
        name='Mechanics',
        material_list=physics_reading_material_list,
    )
    add_tag(
        # FYS
        name='Thermodynamics',
        material_list=['Thermodynamics Khan Academy']
    )
    add_tag(
        # PU
        name='PU-prosjekt',
        material_list=pu_prosjekt_list,
    )
    add_tag(
        # PU
        name='Exercise Lecture 1',
        material_list=['Exercise class 1 - exploration phase'],
    )
    add_tag(
        # PU
        name='Exercise Lecture 2',
        material_list=['Bot Technologies', 'Bot Code Examples'],
    )
    add_tag(
        # PU
        name='Exercise Lecture 3',
        material_list=['Git planning', 'Sprint planning'],
    )
    add_tag(
        # PU
        name='Exercise Lecture 4',
        material_list=['Unit Testing', 'Unit testing code examples'],
    )
    add_tag(
        # PU
        name='Exercise LEcture 5',
        material_list=['Software Architecture'],
    )
    add_tag(
        # PU
        name='Exercise Lecture 6',
        material_list=['Software Quality Assurance'],
    )
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
    add_tag(
        # PU
        name='Exercise Lectures',
        material_list=exercise_list,
    )
    # Add user groups
    add_user_group('Lecturer')
    add_user_group('Student')
    # Lecturers
    add_user(
        # PU
        username='Pekka',
        email='the@man.com',
        password='passord',
        course_list=[],
        pers_exercise_list=[],
        result_pk_list=[],
        group_name_list=['Lecturer'],
    )
    add_user(
        # MAT
        username='MortenNome',
        email='too@awesome.com',
        password='passord',
        course_list=[],
        pers_exercise_list=[],
        result_pk_list=[],
        group_name_list=['Lecturer'],
    )
    add_user(
        #FYS
        username='Magnus Borstad Lilledahl',
        email='magnus@ntnu.no',
        password='passord',
        course_list=[],
        pers_exercise_list=[],
        result_pk_list=[],
        group_name_list=['Lecturer']
    )
    add_user(
        username='RandomStudAss',
        email='red@shirt.com',
        password='passord',
        course_list=[],
        pers_exercise_list=[],
        result_pk_list=[],
        group_name_list=['Lecturer', 'Student'],
    )
    # Course:
    add_course(
        name='TDT4140',
        full_name='Programvareutvikling',
        admin_list=['Pekka'],
        material_list=pu_prosjekt_list + exercise_list,
        description='Beware the 27.4',
    )
    add_course(
        name='TMA4100',
        full_name='Matematikk 1',
        admin_list=['MortenNome'],
        material_list=[],
        description='Begynnelsen av matteeventyret',
    )
    add_course(
        name='TFY4125',
        full_name='Fysikk 1',
        admin_list=['Magnus Borstad Lilledahl'],
        material_list=[],
        description='Alt en trenger å vite innen fysikk',
    )
    # Students
    add_user(
        username='Per',
        email='pers@son.no',
        password='passord',
        course_list=['TDT4140'],
        pers_exercise_list=[],
        result_pk_list=[],
        group_name_list=['Student']
    )
    add_user(
        username='Pål',
        email='pål@son.no',
        password='passord',
        course_list=['TDT4140'],
        pers_exercise_list=[],
        result_pk_list=[],
        group_name_list=['Student']
    )
    add_user(
        username='Sofie',
        email='sofie@notstud.ntnu.no',
        password='passord',
        course_list=['TDT4140'],
        pers_exercise_list=[],
        result_pk_list=[],
        group_name_list=['Student']
    )
    add_user(
        username='Andreas',
        email='andreas@stud.ntnu.no',
        password='passord',
        course_list=['TDT4140'],
        pers_exercise_list=[],
        result_pk_list=[],
        group_name_list=['Student']
    )
    add_user(
        username='Jakob',
        email='jakob@stud.ntnu.no',
        password='passord',
        course_list=['TDT4140'],
        pers_exercise_list=[],
        result_pk_list=[],
        group_name_list=['Student']
    )
    add_user(
        username='Michael',
        email='michael@stud.ntnu.no',
        password='passord',
        course_list=['TDT4140'],
        pers_exercise_list=[],
        result_pk_list=[],
        group_name_list=['Student']
    )
    add_user(
        username='Richard',
        email='richard@stud.ntnu.no',
        password='passord',
        course_list=['TDT4140'],
        pers_exercise_list=[],
        result_pk_list=[],
        group_name_list=['Student']
    )
    # Questions:
    add_question(
        title='TFY4125_Innlevering1_Spørsmål_1',
        question="What is Newton's secound law of physics?",
        alternative_list=['E=mc^2', 'B=aD', 'F=ma', 'F=0.5mv^2'],
        correct_num=3,
        tag_list=['Mechanics'],
        belongs_to='TFY4125',
        is_worth=5,
    )
    add_question(
        title='TFY4125_Innlevering1_Spørsmål_2',
        question='What is the speed of light?',
        alternative_list=['300 m/s', '10^8 m/s', '300 000 km/s', '3*10^9 m/s'],
        correct_num=3,
        tag_list=['Mechanics'],
        belongs_to='TFY4125',
        is_worth=7,
    )
    add_question(
        title='TFY4125_Innlevering1_Spørsmål_3',
        question='Work is ...',
        alternative_list=['Displacement times force', 'Hard!', 'Measured in newton', 'invers proportional to force'],
        correct_num=1,
        tag_list=['Mechanics'],
        belongs_to='TFY4125',
        is_worth=2,
    )
    # Exercises:
    ex_1 = add_exercise(
        title='TFY4125_Exercise1',
        course='TFY4125',
        question_list=[
            'TFY4125_Innlevering1_Spørsmål_1',
            'TFY4125_Innlevering1_Spørsmål_2',
            'TFY4125_Innlevering1_Spørsmål_3',
        ]
    )
    # Results:



if __name__ == '__main__':
    main()
