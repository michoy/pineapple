from django.test import Client
from django.test import TestCase
import django
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pineapple.settings")
from exercise import populate
from exercise.models import *
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate


class ServerTestCase(TestCase):

    def setUp(self):
        # Must be run, crashes otherwise
        django.setup()
        self.client = Client()
        # Attempt to add entries to database, using methods from populate.py
        populate.add_reading_material('NewMaterial', 'www.google.com')  # Reading material
        populate.add_tag('TestTag', ['NewMaterial'])  # Theme Tag
        populate.add_course('NewCourse', 'This course is an example', [], [], '')
        populate.add_user_group('Lecturer')  # Group
        populate.add_user_group('Student')
        populate.add_user(
            username='Pekka',
            email='the@man.com',
            password='kanban',
            course_list=['NewCourse'],
            group_name_list=['Lecturer', 'Student'],
            pers_exercise_list=[],
            result_pk_list=[],
        )
        populate.add_course(
            name='TDT4140',
            full_name='Programvareutvikling',
            admin_list=['Pekka'],
            material_list=['NewMaterial'],
            description='Beware the 27.4',
        )
        populate.add_question(
            'Q1',
            'My car says',
            ['dingdong', 'clingcling', 'boom', 'poof'],
            2,
            ['TestTag'],
            'NewCourse',
            11
        )
        populate.add_question(
            'Q2',
            'My car really says',
            ['dingdong', 'clingcling', 'boom', 'poof'],
            2,
            ['TestTag'],
            'NewCourse',
            11
        )
        ex = populate.add_exercise('Quiz 1', 'NewCourse', ['Q1', 'Q2'])
        populate.add_result(True, 'Q1', 'Pekka', ex.pk)

    # Test if database entries can be found and if their values are correct
    def test_add_reading_material(self):
        self.assertEqual('NewMaterial', ReadingMaterial.objects.all().__getitem__(0).title)
        self.assertEqual('www.google.com', ReadingMaterial.objects.get(title='NewMaterial').link)

    def test_add_tag(self):
        self.assertEqual('TestTag', ThemeTag.objects.all().__getitem__(0).name)
        self.assertEqual('www.google.com', ThemeTag.objects.get(name='TestTag').material.get(title='NewMaterial').link)

    def test_add_user_group(self):
        self.assertEqual('Lecturer', Group.objects.get(name='Lecturer').name)

    def test_create_user(self):
        self.assertEqual('Pekka', User.objects.all().__getitem__(0).username)
        self.assertEqual('the@man.com', User.objects.get(username='Pekka').email)
        self.assertTrue(authenticate(username='Pekka', password='kanban'))
        self.assertTrue(User.objects.all().__getitem__(0).groups.filter(name='Lecturer').exists())

    def test_add_course(self):
        self.assertEqual('NewCourse', Course.objects.all().__getitem__(0).name)
        self.assertEqual('TDT4140', Course.objects.all().__getitem__(1).name)
        self.assertEqual(Course.objects.get(name='TDT4140').administrators.all().__getitem__(0),
                         User.objects.get(username='Pekka'))
        self.assertEqual(Course.objects.get(name='TDT4140').content.all().__getitem__(0).title, 'NewMaterial')
        self.assertEqual(Course.objects.get(name='TDT4140').description, 'Beware the 27.4')

    def test_add_coursecollection(self):
        self.assertEqual('NewCourse', User.objects.get(username='Pekka').coursecollection.courses.all()
                         .__getitem__(0).name)

    def test_add_question(self):
        q = Question.objects.all().__getitem__(0)
        self.assertEqual('Q1', q.title)
        self.assertEqual('My car says', q.question)
        self.assertEqual('dingdong', q.alternative_1)
        self.assertEqual('clingcling', q.alternative_2)
        self.assertEqual('boom', q.alternative_3)
        self.assertEqual('poof', q.alternative_4)
        self.assertEqual(2, q.correct_alternative)
        self.assertEqual(ThemeTag.objects.all().__getitem__(0), q.themeTags.all().__getitem__(0))
        self.assertEqual(11, q.is_worth)
        self.assertEqual('NewCourse', q.belongsTo.name)

    def test_add_exercise(self):
        e = Exercise.objects.all().__getitem__(0)
        self.assertEqual('Quiz 1', e.title)
        self.assertEqual('NewCourse', e.course.name)
        self.assertFalse(e.private)
        self.assertEqual('Q1', e.contains.all().values_list('title', flat=True)[0])

    def test_add_result(self):
        r = Result.objects.all().__getitem__(0)
        self.assertTrue(r.resultVal)
        self.assertEqual('Q1', r.question.title)
        self.assertEqual(r, User.objects.get(username='Pekka').resultcollection.results.all().__getitem__(0))

    def test_populate(self):
        # Tests if populate.py populates the database without errors
        try:
            populate.main()
        except:
            self.fail("Populate.py is broken, you can't populate database properly!")

    # Test server connectivity
    def test_do_quiz(self):
        self.client.login(username='Pekka', password='kanban')
        resp = self.client.get('/exercise/' + str(Exercise.objects.all().__getitem__(0).pk) + '/')
        self.assertEqual(200, resp.status_code)

