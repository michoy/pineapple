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
        #TFY
        title='Newton Mechanics Wikipedia',
        link='https://en.wikipedia.org/wiki/Classical_mechanics'
    )
    add_reading_material(
        #TFY
        title='Newton Mechanics: p. 100',
    )
    add_reading_material(
        #TFY
        title='Mechanical Energy Wikipedia',
        link='https://en.wikipedia.org/wiki/Mechanical_energy'
    )
    add_reading_material(
        #TFY
        title='Mechanical Energy: p. 125'
    )
    add_reading_material(
        #TFY
        title='Rotation Wikipedia',
        link='https://en.wikipedia.org/wiki/Rotation'
    )
    add_reading_material(
        #TFY
        title='Rotation: p. 137'
    )
    add_reading_material(
        #TFY
        title='Electrostatics Wikipedia',
        link='https://en.wikipedia.org/wiki/Electrostatics'
    )
    add_reading_material(
        #TFY
        title='Electrostatics: p. 213'
    )
    add_reading_material(
        #TFY
        title='Dielectric Wikipedia',
        link='https://en.wikipedia.org/wiki/Dielectric'
    )
    add_reading_material(
        #TFY
        title='Dielectric: p. 231'
    )
    add_reading_material(
        #TFY
        title='Magnetic Field Wikipedia',
        link='https://en.wikipedia.org/wiki/Magnetic_field'
    )
    add_reading_material(
        #TFY
        title='Magnetic Field: p. 245'
    )
    add_reading_material(
        #TFY
        title='Temperature Wikipedia',
        link='https://en.wikipedia.org/wiki/Temperature'
    )
    add_reading_material(
        #TFY
        title='Temperature: p. 270'
    )
    add_reading_material(
        #TFY
        title='Carnot Cycle Wikipedia',
        link='https://en.wikipedia.org/wiki/Carnot_cycle'
    )
    add_reading_material(
        #TFY
        title='Carnot Cycle: p. 292'
    )
    add_reading_material(
        #TFY
        title='Ideal Gas Wikipedia',
        link='https://en.wikipedia.org/wiki/Ideal_gas'
    )
    add_reading_material(
        #TFY
        title='Ideal Gas: p. 302'
    )

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
<<<<<<< HEAD

    # Tags:
=======
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
    add_reading_material(
        # KTN
        title='SMTP protocol - Computer Networking ATDA s.123-130',
        link='',
    )
    add_reading_material(
        # KTN
        title='SMTP example - Computer Networking ATDA s.127-128',
        link='',
    )
    add_reading_material(
        # KTN
        title='SMTP - Slide 38',
        link='https://ntnu.itslearning.com/file/download.aspx?FileID=4681008&FileVersionID=-1&ChildID=-1'
    )
    add_reading_material(
        # KTN
        title='POP3 - Computer Networking ATDA s.131',
        link='',
    )
    add_reading_material(
        # KTN
        title='POP3 example - Slide 44',
        link='https://ntnu.itslearning.com/file/download.aspx?FileID=4681008&FileVersionID=-1&ChildID=-1'
    )
    add_reading_material(
        # KTN
        title='IMAP - Computer Networking ATDA s.132',
        link='',
    )
    add_reading_material(
        # KTN
        title='DNS - Computer Networking ATDA s.150-153',
        link=''
    )
    add_reading_material(
        # KTN
        title='CDN - Computer Networking ATDA s.154-157',
        link=''
    )
    add_reading_material(
        # KTN
        title='TCP  - Computer Networking ATDA s.177-187',
        link='',
    )
    add_reading_material(
        # KTN
        title='UDP - Computer Networking ATDA s.170-177',
        link='',
    )
    add_reading_material(
        # KTN
        title='HTTP - Computer Networking ATDA s.89-94',
        link=''
    )
    add_reading_material(
        # KTN
        title='HTTP message types - Slide 19-29',
        link='https://ntnu.itslearning.com/file/download.aspx?FileID=4681008&FileVersionID=-1&ChildID=-1'
    )
>>>>>>> refs/remotes/origin/master
    pu_prosjekt_list = [
        'TDT4140 Assessment Criteria',
        'TDT4140 Project Milestones',
        'TDT4140 Project Description',
        'TDT4140 Poster Layout',
        'Improving Needed Posters'
    ]
<<<<<<< HEAD
=======
    physics_reading_material_list = [
        'Newtons Laws of Gravity',
        'Work, energy, power',
        'Newtons Laws',
    ]
    # Tags:
>>>>>>> refs/remotes/origin/master

    add_tag(
        #TFY
        name='Mechanics',
        material_list=[
            'Newton Mechanics Wikipedia',
            'Newtons Mechanics: p. 100',
            'Mechanical Energy Wikipedia',
            'Mechanical Energy: p. 125',
            'Rotation Wikipedia',
            'Rotation: p. 137'
        ]
    )
    add_tag(
        #TFY
        name='Mechanical Energy',
        material_list=[
            'Mechanical Energy Wikipedia',
            'Mechanical Energy: p. 125'
        ]
    )
    add_tag(
        # TFY
        name='Newton',
        material_list=[
            'Newton Mechanics Wikipedia',
            'Newton Mechanics: p. 100'
        ]
    )
    add_tag(
        # TFY
        name='Rotation',
        material_list=[
            'Rotation Wikipedia',
            'Rotation: p. 137'
        ]
    )
    add_tag(
        #TFY
        name='Electromagnetism',
        material_list=[
            'Electrostatics Wikipedia',
            'Electrostatics: p. 213',
            'Dielectric Wikipedia',
            'Dielectric: p. 231',
            'Magnetic Field Wikipedia',
            'Magnetic Field: p. 245',
        ]
    )
    add_tag(
        #TFY
        name='Electrostatics',
        material_list=[
            'Electrostatics Wikipedia',
            'Electrostatics: p. 213'
        ]
    )
    add_tag(
        # TFY
        name='Dielectrics',
        material_list=[
            'Dielectrics Wikipedia',
            'Dielectrics: p. 231'
        ]
    )
    add_tag(
        # TFY
        name='Magnetic Field',
        material_list=[
            'Magnetic Field Wikipedia',
            'Magnetic Field: p. 245'
        ]
    )
    add_tag(
        #TFY
        name='Thermodynamics',
        material_list=[
            'Temperature Wikipedia',
            'Temperature: p. 270',
            'Carnot Cycle Wikipedia',
            'Carnot Cycle: p. 292',
            'Ideal Gas Wikipedia',
            'Ideal Gas: p. 302'
        ]
    )
    add_tag(
        #TFY
        name='Temperature',
        material_list=[
            'Temperature Wikipedia',
            'Temperature: p. 270'
        ]
    )
    add_tag(
        #TFY
        name='Carnot Cycle',
        material_list=[
            'Carnot Cycle Wikipedia',
            'Carnot Cycle: p. 292'
        ]
    )
    add_tag(
        #TFY
        name='Ideal Gas',
        material_list=[
            'Ideal Gas Wikipedia',
            'Ideal Gas: p.302'
        ]
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
    add_tag(
        # KTN
        name='SMTP',
        material_list=[
            'SMTP protocol - Computer Networking ATDA s.123-130',
            'SMTP example - Computer Networking ATDA s.127-128',
            'SMTP - Slide 38',
        ]
    )
    add_tag(
        # KTN
        name='Email protocols',
        material_list=[
            'SMTP protocol - Computer Networking ATDA s.123-130',
            'SMTP example - Computer Networking ATDA s.127-128',
            'SMTP - Slide 38',
            'POP3 - Computer Networking ATDA s.131',
            'POP3 example - Slide 44',
            'IMAP - Computer Networking ATDA s.132',
        ]
    )
    add_tag(
        # KTN
        name='DNS',
        material_list=[
            'DNS - Computer Networking ATDA s.150-153',
        ]
    )
    add_tag(
        # KTN
        name='Content Distribution',
        material_list=[
            'CDN - Computer Networking ATDA s.154-157',
        ]
    )
    add_tag(
        # KTN
        name='Transport Layer',
        material_list=[
            'TCP  - Computer Networking ATDA s.177-187',
            'UDP - Computer Networking ATDA s.170-177',
        ]
    )
    add_tag(
        # KTN
        name='HTTP',
        material_list=[
            'HTTP - Computer Networking ATDA s.89-94',
            'HTTP message types - Slide 19-29',
        ]
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
        # FYS
        username='MagnusBorstadLilledahl',
        email='magnus@ntnu.no',
        password='passord',
        course_list=[],
        pers_exercise_list=[],
        result_pk_list=[],
        group_name_list=['Lecturer']
    )
    add_user(
<<<<<<< HEAD
        #TFY
        username='Magnus Borstad Lilledahl',
        email='magnus@ntnu.no',
=======
        # KTN
        username='KjerstiMoldeklev',
        email='kjersti@ntnu.no',
>>>>>>> refs/remotes/origin/master
        password='passord',
        course_list=[],
        pers_exercise_list=[],
        result_pk_list=[],
        group_name_list=['Lecturer'],
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
        # PU
        name='TDT4140',
        full_name='Programvareutvikling',
        admin_list=['Pekka'],
        material_list=pu_prosjekt_list + exercise_list,
        description='Beware the 27.4',
    )
    add_course(
        # FYS
        name='TFY4125',
        full_name='Physics',
        admin_list=['MagnusBorstadLilledahl'],
        material_list=[],
        description='Everything one needs to know about physics.',
    )
    add_course(
        # KTN
        name='TTM4100',
        full_name='Communication - Services and Networks',
        admin_list=['KjerstiMoldeklev'],
        material_list=[
            'SMTP protocol - Computer Networking ATDA s.123-130',
            'SMTP example - Computer Networking ATDA s.127-128',
            'SMTP - Slide 38',
            'POP3 - Computer Networking ATDA s.131',
            'POP3 example - Slide 44',
            'IMAP - Computer Networking ATDA s.132',
            'DNS - Computer Networking ATDA s.150-153',
            'CDN - Computer Networking ATDA s.154-157',
            'TCP  - Computer Networking ATDA s.177-187',
            'UDP - Computer Networking ATDA s.170-177',
            'HTTP - Computer Networking ATDA s.89-94',
            'HTTP message types - Slide 19-29',
        ],
        description='All there is to know about networks and the internet.'
    )
    # Students
    add_user(
        username='Per',
        email='pers@son.no',
        password='passord',
        course_list=['TTM4100'],
        pers_exercise_list=[],
        result_pk_list=[],
        group_name_list=['Student']
    )
    add_user(
        username='Pål',
        email='pål@son.no',
        password='passord',
        course_list=['TTM4100'],
        pers_exercise_list=[],
        result_pk_list=[],
        group_name_list=['Student']
    )
    add_user(
        username='Sofie',
        email='sofie@notstud.ntnu.no',
        password='passord',
        course_list=['TTM4100'],
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
<<<<<<< HEAD
        #TFY
        title='TFY_E1_Q1',
        question='What is newtons second law of physics?',
        alternative_list=['F = 0.5*mv^2','F = ma','Carrots', 'F = m*ln(x)'],
        correct_num=2,
        tag_list=['Newton'],
        belongs_to='TFY4125',
        is_worth=3
    )
    add_question(
        #TFY
        title='TFY_E1_Q2',
        question='Rotational force is directed:',
        alternative_list=['Upwards', 'In the direction of motion', 'Towards the center of the rotation', 'Allways towards Earts center'],
=======
        # FYS
        title='TFY4125_Innlevering1_Spørsmål_1',
        question="What is Newton's secound law of physics?",
        alternative_list=['E=mc^2', 'B=aD', 'F=ma', 'F=0.5mv^2'],
>>>>>>> refs/remotes/origin/master
        correct_num=3,
        tag_list=['Rotation'],
        belongs_to='TFY4125',
        is_worth=5
    )
    add_question(
<<<<<<< HEAD
        # TFY
        title='TFY_E1_Q3',
        question='Work is:',
        alternative_list=['Hard', 'Mass times acceleration', 'Force times distance', 'Equal force'],
=======
        # FYS
        title='TFY4125_Innlevering1_Spørsmål_2',
        question='What is the speed of light?',
        alternative_list=['300 m/s', '10^8 m/s', '300 000 km/s', '3*10^9 m/s'],
>>>>>>> refs/remotes/origin/master
        correct_num=3,
        tag_list=['Mechanical Energy'],
        belongs_to='TFY4125',
        is_worth=5
    )
    add_question(
        # TFY
        title='TFY_E2_Q1',
        question='The formula for electrostatic force is:',
        alternative_list=['F = E/q', 'F = k*qQ/r^2', 'F = (q/r)^2', 'Too complicated to remember'],
        correct_num=2,
        tag_list=['Electrostatics'],
        belongs_to='TFY4125',
        is_worth=5
    )
    add_question(
        # TFY
        title='TFY_E2_Q1',
        question='The formula for electrostatic force is:',
        alternative_list=['F = E/q', 'F = k*qQ/r^2', 'F = (q/r)^2', 'Too complicated to remember'],
        correct_num=2,
        tag_list=['Electrostatics'],
        belongs_to='TFY4125',
        is_worth=5
    )
    add_question(
<<<<<<< HEAD
        # TFY
        title='TFY_E2_Q2',
        question='Capacitance is:',
        alternative_list=['invers proportional to voltage', 'not dependent on material type', 'Q = F*E', 'Monty Python'],
=======
        # FYS
        title='TFY4125_Innlevering1_Spørsmål_3',
        question='Work is ...',
        alternative_list=['Displacement times force', 'Hard!', 'Measured in newton', 'invers proportional to force'],
>>>>>>> refs/remotes/origin/master
        correct_num=1,
        tag_list=['Dielectric'],
        belongs_to='TFY4125',
        is_worth=5
    )
    add_question(
        # TFY
        title='TFY_E2_Q3',
        question='How can we fugure out the direction of a electromagnetic force?',
        alternative_list=['Look at the electrons', 'I do not know', 'Hand Rule', 'Right Hand Rule'],
        correct_num=4,
        tag_list=['Electro Magnetism'],
        belongs_to='TFY4125',
        is_worth=5
    )
    add_question(
        # TFY
        title='TFY_E3_Q1',
        question='What is temperature?',
        alternative_list=['Comparative measuer of heat', 'Thermometer', 'Cold', 'Balls'],
        correct_num=1,
        tag_list=['Temperature'],
        belongs_to='TFY4125',
        is_worth=5
    )
    add_question(
        # TFY
        title='TFY_E3_Q2',
        question='Which is true?',
        alternative_list=['T1*T2=C1*C2', 'T1*Q2=T2*Q1', 'T1=T2', 'Q^2=T1*T2'],
        correct_num=2,
        tag_list=['Carnot Cycle'],
        belongs_to='TFY4125',
        is_worth=5
    )
    add_question(
        # TFY
        title='TFY_E3_Q3',
        question='Which is true?',
        alternative_list=['nR=N', 'RV=P/nT', 'PV=T', 'PV=nRT'],
        correct_num=4,
        tag_list=['Ideal Gas'],
        belongs_to='TFY4125',
        is_worth=5
    )
    add_question(
        # KTN
        title='Exercise 1: Email, Q1',
        question='SMTP stands for:',
        alternative_list=[
            'Simple Mail Transfer Protocol',
            'Strict Mail Threading Plan',
            'Strong Multi-Translated Port',
            'Severe Markup Transfer Protection',
        ],
        correct_num=1,
        tag_list=['SMTP'],
        belongs_to='TTM4100',
        is_worth=5,
    )
    add_question(
        # KTN
        title='Exercise 1: Email, Q2',
        question='The main difference between POP3 and IMAP is:',
        alternative_list=[
            'POP3 is push-oriented, while IMAP is pull-oriented',
            'POP3 is a simple protocol, IMAP is more feature rich',
            'POP3 is designed for human interaction, IMAP for server-server communication',
            'POP3 is deprecated, IMAP should be used instead as of 2008'
        ],
        correct_num=2,
        tag_list=['Email protocols'],
        belongs_to='TTM4100',
        is_worth=3,
    )
    add_question(
        # KTN
        title='Exercise 1: Email, Q3',
        question='SMTP is usually used when:',
        alternative_list=[
            'Downloading email from server to client',
            'Retrieving email from the server when using a browser as client',
            'Uploading to email server and transferring between servers',
            'POP3 is downloading encoded files, such as pictures (jpg, png) or movies',
        ],
        correct_num=3,
        tag_list=['SMTP', 'Email protocols'],
        belongs_to='TTM4100',
        is_worth=4,
    )
    add_question(
        # KTN
        title='Exercise 2: HTTP and content distribution, Q1',
        question='When looking for an IP-adress, DNS generally accesses these three servers:',
        alternative_list=[
            'Root, TLD and Authoritative',
            'Base, SSL and Denominative',
            'Core, TQR and Relative',
            'Central, SQC and Root',
        ],
        correct_num=1,
        tag_list=['DNS'],
        belongs_to='TTM4100',
        is_worth=3,
    )
    add_question(
        # KTN
        title='Exercise 2: HTTP and content distribution, Q2',
        question='"The "method"-field in an HTTP/1.1 request can contain one of these strings:',
        alternative_list=[
            'GET, POST, HEAD',
            'GET, POST, HEAD, PUT, DELETE',
            'GET, POST, HEAD, PUT, DELETE, SELECT',
            'GET, POST, HEAD, ACK'
        ],
        correct_num=2,
        tag_list=['HTTP'],
        belongs_to='TTM4100',
        is_worth=5,
    )
    add_question(
        # KTN
        title='Exercise 2: HTTP and content distribution, Q3',
        question='TCP guarantees several features which UDP does not, these include:',
        alternative_list=[
            'End-to-end encryption and pipelining',
            'Increased bitrate and version control',
            'Congestion control and reliable data transfer',
            'Error correction and signal backups'
        ],
        correct_num=3,
        tag_list=['Transport Layer'],
        belongs_to='TTM4100',
        is_worth=6,
    )
    add_question(
        # KTN
        title='Exercise 2: HTTP and content distribution, Q4',
        question='Usually CDNs use one these two server placement methods. Pick the right one:',
        alternative_list=[
            'Reach far, Short Reroute',
            'Explore, Expand',
            'Exploit Exterminate',
            'Bring Home, Enter Deep',
        ],
        correct_num=4,
        tag_list=['Content Distribution'],
        belongs_to='TTM4100',
        is_worth=10,
    )
    # Exercises:
<<<<<<< HEAD
    add_exercise(
        title='TFY_E1',
        course='TFY4125',
        question_list=['TFY_E1_Q1','TFY_E1_Q2','TFY_E1_Q3']
    )
    add_exercise(
        title='TFY_E2',
        course='TFY4125',
        question_list=['TFY_E2_Q1', 'TFY_E2_Q2', 'TFY_E2_Q3']
    )
    add_exercise(
        title='TFY_E3',
        course='TFY4125',
        question_list=['TFY_E3_Q1', 'TFY_E3_Q2', 'TFY_E3_Q3']
=======
    ex_1 = add_exercise(
        # FYS
        title='TFY4125_Exercise1',
        course='TFY4125',
        question_list=[
            'TFY4125_Innlevering1_Spørsmål_1',
            'TFY4125_Innlevering1_Spørsmål_2',
            'TFY4125_Innlevering1_Spørsmål_3',
        ],
    )
    ex_2 = add_exercise(
        # KTN
        title='Exercise 1: Email',
        course='TTM4100',
        question_list=[
            'Exercise 1: Email, Q1',
            'Exercise 1: Email, Q2',
            'Exercise 1: Email, Q3',
        ],
    )
    ex_3 = add_exercise(
        # KTN
        title='Exercise 2: HTTP and content distribution',
        course='TTM4100',
        question_list=[
            'Exercise 2: HTTP and content distribution, Q1',
            'Exercise 2: HTTP and content distribution, Q2',
            'Exercise 2: HTTP and content distribution, Q3',
            'Exercise 2: HTTP and content distribution, Q4'
        ],
    )
    ex_4 = add_exercise(
        # KTN
        title='Exercise3: Repetition',
        course='TTM4100',
        question_list=[
            'Exercise 2: HTTP and content distribution, Q1',
            'Exercise 2: HTTP and content distribution, Q2',
            'Exercise 1: Email, Q2',
            'Exercise 1: Email, Q3',
        ]
>>>>>>> refs/remotes/origin/master
    )
    # Results:
    # Per
    add_result(
        # KTN
        val=False,
        question='Exercise 1: Email, Q1',
        student='Per',
        exercise=ex_2.pk,
    )
    add_result(
        # KTN
        val=False,
        question='Exercise 1: Email, Q2',
        student='Per',
        exercise=ex_2.pk,
    )
    add_result(
        # KTN
        val=False,
        question='Exercise 1: Email, Q3',
        student='Per',
        exercise=ex_2.pk,
    )
    add_result(
        # KTN
        val=False,
        question='Exercise 2: HTTP and content distribution, Q1',
        student='Per',
        exercise=ex_3.pk,
    )
    add_result(
        # KTN
        val=True,
        question='Exercise 2: HTTP and content distribution, Q2',
        student='Per',
        exercise=ex_3.pk,
    )
    add_result(
        # KTN
        val=False,
        question='Exercise 2: HTTP and content distribution, Q3',
        student='Per',
        exercise=ex_3.pk,
    )
    add_result(
        # KTN
        val=True,
        question='Exercise 2: HTTP and content distribution, Q4',
        student='Per',
        exercise=ex_3.pk,
    )
    add_result(
        # KTN
        val=False,
        question='Exercise 2: HTTP and content distribution, Q1',
        student='Per',
        exercise=ex_4.pk,
    )
    add_result(
        # KTN
        val=False,
        question='Exercise 2: HTTP and content distribution, Q2',
        student='Per',
        exercise=ex_4.pk,
    )
    add_result(
        # KTN
        val=False,
        question='Exercise 1: Email, Q2',
        student='Per',
        exercise=ex_4.pk,
    )
    add_result(
        # KTN
        val=False,
        question='Exercise 1: Email, Q3',
        student='Per',
        exercise=ex_4.pk,
    )
    # Pål
    add_result(
        # KTN
        val=False,
        question='Exercise 1: Email, Q1',
        student='Pål',
        exercise=ex_2.pk
    )
    add_result(
        # KTN
        val=False,
        question='Exercise 1: Email, Q2',
        student='Pål',
        exercise=ex_2.pk,
    )
    add_result(
        # KTN
        val=False,
        question='Exercise 1: Email, Q3',
        student='Pål',
        exercise=ex_2.pk,
    )
    add_result(
        # KTN
        val=False,
        question='Exercise 2: HTTP and content distribution, Q1',
        student='Pål',
        exercise=ex_3.pk
    )
    add_result(
        # KTN
        val=True,
        question='Exercise 2: HTTP and content distribution, Q2',
        student='Pål',
        exercise=ex_3.pk
    )
    add_result(
        # KTN
        val=False,
        question='Exercise 2: HTTP and content distribution, Q3',
        student='Pål',
        exercise=ex_3.pk
    )
    add_result(
        # KTN
        val=True,
        question='Exercise 2: HTTP and content distribution, Q4',
        student='Pål',
        exercise=ex_3.pk
    )
    # Sofie
    add_result(
        # KTN
        val=True,
        question='Exercise 1: Email, Q1',
        student='Sofie',
        exercise=ex_2.pk
    )
    add_result(
        # KTN
        val=False,
        question='Exercise 1: Email, Q2',
        student='Sofie',
        exercise=ex_2.pk,
    )
    add_result(
        # KTN
        val=True,
        question='Exercise 1: Email, Q3',
        student='Sofie',
        exercise=ex_2.pk,
    )
    add_result(
        # KTN
        val=False,
        question='Exercise 2: HTTP and content distribution, Q1',
        student='Sofie',
        exercise=ex_3.pk
    )
    add_result(
        # KTN
        val=True,
        question='Exercise 2: HTTP and content distribution, Q2',
        student='Pål',
        exercise=ex_3.pk
    )
    add_result(
        # KTN
        val=True,
        question='Exercise 2: HTTP and content distribution, Q3',
        student='Pål',
        exercise=ex_3.pk
    )
    add_result(
        # KTN
        val=True,
        question='Exercise 2: HTTP and content distribution, Q4',
        student='Pål',
        exercise=ex_3.pk
    )

if __name__ == '__main__':
    main()
