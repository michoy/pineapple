from django.test import Client
from django.test import TestCase
import django
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pineapple.settings")
from django.contrib.auth.models import User
from exercise import populate
# Tester om sidene på serveren og funksjonene der fungerer rett
# Kan kjøre uten at serveren faktisk er på, tester kun serverkode, bruker ikke http
class ServerTestCase(TestCase):

    def setUp(self):
        # Må kjøres, ellers krasj
        django.setup()
        self.client = Client()
        # Create test lecturer and the corresponding lecturer group.
        u = populate.add_user(
            username='theTeach',
            email='teach@me.com',
            password='schooled',
            course_list=[],
            pers_exercise_list=[],
            result_pk_list=[]
        )
        g = populate.add_user_group('Lecturer')
        u.groups.add(g)
        # Create test course to select later
        populate.add_course(
            name='TDTT3st',
            admin_list=['theTeach'],
            material_list=[],
            description='For testing purposes'
        )
        # Create test student
        u = populate.add_user(
            username='theMan',
            email='the@man.no',
            password='thePa$$word',
            course_list=[],
            pers_exercise_list=[],
            result_pk_list=[]
        )
        g = populate.add_user_group('Student')
        u.groups.add(g)
        populate.add_question(
            title='test Q',
            question='Will this humble test bless us by working as intended?',
            alternative_list=['hell yeah!', 'over my dead body', 'Never!', 'define "working"'],
            correct_num=4,
            tag_list=[],
            belongs_to='TDTT3st',
            is_worth=1000000,
        )
        populate.add_exercise(title='test E',question_list=['test Q'], course='TDTT3st')

    def test_stud_exercise_sel(self):
        # Login and start with the a course page
        self.client.login(username='theMan', password='thePa$$word')
        resp = self.client.get('/course/TDTT3st/')
        self.assertEqual(200, resp.status_code)
        # Select an exercise
        resp = self.client.post('/course/TDTT3st/', {'exercise-select':'testE'})
        self.assertEqual(302, resp.status_code)
        self.assertEqual('/exercise/testE/', resp.url)

    def test_lect_exercise_sel(self):
        # Login and start with the a course page
        self.client.login(username='theTeach', password='schooled')
        resp = self.client.get('/course/TDTT3st/')
        self.assertEqual(200, resp.status_code)
        # Select an exercise
        resp = self.client.post('/course/TDTT3st/', {'exercise-select':'testE'})
        self.assertEqual(302, resp.status_code)
        self.assertEqual('/exercise/testE/', resp.url)