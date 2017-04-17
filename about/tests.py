from django.test import Client
from django.test import TestCase
import django
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pineapple.settings")
from django.contrib.auth.models import User


class ServerTestCase(TestCase):

    def setUp(self):
        # Must be run, else crash
        django.setup()
        self.client = Client()
        # Create test user
        User.objects.create_user('theMan', 'the@man.no', 'thePa$$word')

    # Test server connectivity

    # Can homepage be reached?
    def test_homepage(self):
        resp = self.client.get('')
        self.assertEqual(200, resp.status_code)

    # Can the about page be reached?
    def test_about(self):
        resp = self.client.get('/about/')
        self.assertEqual(200, resp.status_code)

    # Can the user log in?
    def test_login(self):
        # Test wether login page can be reached
        resp = self.client.get('/login/')
        self.assertEqual(200, resp.status_code)
        # Test wether client is redirected correctly after login
        resp = self.client.post('/login/', {'username': 'theMan', 'password': 'thePa$$word'})
        self.assertEqual(302, resp.status_code)
        self.assertEqual('/overview/', resp.url)
        # Test wether client is logged in
        self.assertIn('_auth_user_id', self.client.session)

    # Can the user register?
    def test_register(self):
        # Test wether register page can be reached
        resp = self.client.get('/register/')
        self.assertEqual(200, resp.status_code)
        # Test wether new account is successfully created
        resp = self.client.post(
            '/register/',
            {'username': 'newMan', 'password': 'datPWord', 'email': 'newMan@mailmail.com'}
        )
        self.assertEqual(200, resp.status_code)
        self.assertTrue('newMan', User.objects.all().__getitem__(1).username)
