from django.test import Client
from django.test import TestCase
import django, os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pineapple.settings")


# Tester om sidene på serveren og funksjonene der fungerer rett
# Kan kjøre uten at serveren faktisk er på, tester kun serverkode, bruker ikke http
class ServerTestCase(TestCase):

    def setUp(self):
        # Må kjøres, ellers krasj
        django.setup()
        self.client = Client()

    def testHomepage(self):
        resp = self.client.get('')
        # Kan homepage nås?
        self.assertEqual(200, resp.status_code)

    def testAdd_question(self):
        resp = self.client.get('/add_question/')
        # Kan quizsiden nås?
        self.assertEqual(200, resp.status_code)

