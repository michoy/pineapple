from django.test import Client
from django.test import TestCase
import django
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pineapple.settings")
from django.contrib.auth.models import User
# Tester om sidene på serveren og funksjonene der fungerer rett
# Kan kjøre uten at serveren faktisk er på, tester kun serverkode, bruker ikke http
class ServerTestCase(TestCase):

    def setUp(self):
        # Må kjøres, ellers krasj
        django.setup()
        self.client = Client()
        # Create test user
        User.objects.create_user('theMan', 'the@man.no', 'thePa$$word')

    # Test server connectivity

    # Kan homepage nås?
    def test_homepage(self):
        resp = self.client.get('')
        self.assertEqual(200, resp.status_code)

    # Kan about siden nås?
    def test_about(self):
        resp = self.client.get('/about/')
        self.assertEqual(200, resp.status_code)

    # Kan login page nås?
    def test_login(self):
        # Test if login page can be reached
        resp = self.client.get('/login/')
        self.assertEqual(200, resp.status_code)
        # Test if client is redirected correctly after login
        resp = self.client.post('/login/', {'username': 'theMan', 'password': 'thePa$$word'})
        self.assertEqual(302, resp.status_code)
        self.assertEqual('/overview/',resp.url)
        # Test if client is logged in
        self.assertIn('_auth_user_id', self.client.session)
