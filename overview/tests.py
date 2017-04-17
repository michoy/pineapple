from django.test import Client
from django.test import TestCase
import django
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pineapple.settings")
from django.contrib.auth.models import User
from exercise import populate


class ServerTestCase(TestCase):

    def setUp(self):
        # Must be run, else crash
        django.setup()
        self.client = Client()
        # Create test lecturer and the corresponding lecturer group.
        u = User.objects.create_user(username='theTeach', email='teach@me.com', password='schooled')
        g = populate.add_user_group('Lecturer')
        u.groups.add(g)
        populate.add_coursecollection(student='theTeach', course_list=[])
        # Create test course to select later
        populate.add_course(
            name='TDTT3st',
            full_name='L33t3st C0urse',
            admin_list=['theTeach'],
            material_list=[],
            description='For testing purposes'
        )
        # Create test student
        u = User.objects.create_user(username='theMan', email='the@man.no', password='thePa$$word')
        g = populate.add_user_group('Student')
        u.groups.add(g)
        populate.add_coursecollection(student='theMan', course_list=['TDTT3st'])

    def test_overview_student(self):
        # Log in
        self.client.login(username='theMan', password='thePa$$word')
        # Can overview be reached?
        resp = self.client.get('/overview/')
        self.assertEqual(200, resp.status_code)
        # Does the redirect work when the course is selected?
        resp = self.client.post('/overview/', {'course-select': 'TDTT3st'})
        self.assertEqual(302, resp.status_code)
        self.assertEqual('/course/TDTT3st/', resp.url)

    def test_overview_lecturer(self):
        # Log in
        self.client.login(username='theTeach', password='schooled')
        # Can overview be reached?
        resp = self.client.get('/overview/')
        self.assertEqual(200, resp.status_code)
        # Does redirect work when the course is selected?
        resp = self.client.post('/overview/', {'course-select': 'TDTT3st'})
        self.assertEqual(302, resp.status_code)
        self.assertEqual('/course/TDTT3st/', resp.url)

    def test_overview_redirect(self):
        # If user is not logged in, is he redirected correctly?
        resp = self.client.get('/overview/')
        self.assertEqual(302, resp.status_code)
        self.assertEqual('/login/?next=/overview/', resp.url)
