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
import unittest

# Tester om sidene på serveren og funksjonene der fungerer rett
# Kan kjøre uten at serveren faktisk er på, tester kun serverkode, bruker ikke http
class ServerTestCase(TestCase):

    def setUp(self):
        # Må kjøres, ellers krasj
        django.setup()
        self.client = Client()
        #Attempt to add entries
        populate.add_reading_material('NewMaterial', 'www.google.com')  # Reading material
        populate.add_tag('TestTag', ['NewMaterial'])  # Theme Tag
        populate.add_user_group('Lecturer')  # Group
        User.objects.create_user(username='Pekka', email='the@man.com', password='kanban')
        populate.add_course('TDT4140', ['Pekka'], ['NewMaterial'], 'Beware the 27.4')

    #Test if database entries can be found and if their values are correct
    def test_add_reading_material(self):
        self.assertEqual('NewMaterial', ReadingMaterial.objects.all().__getitem__(0).title)
        self.assertEqual('www.google.com', ReadingMaterial.objects.get(title='NewMaterial').link)

    def test_add_tag(self):
        self.assertEqual('TestTag', ThemeTag.objects.all().__getitem__(0).name)
        self.assertEqual('www.google.com', ThemeTag.objects.get(name='TestTag').material.get(title='NewMaterial').link)

    def test_add_user_group(self):
        self.assertEqual('Lecturer', Group.objects.get(name='Lecturer').name)
        #TODO check permissions

    def test_create_user(self):
        self.assertEqual('Pekka', User.objects.all().__getitem__(0).username)
        self.assertEqual('the@man.com', User.objects.get(username='Pekka').email)
        self.assertTrue(authenticate(username='Pekka', password='kanban'))

    def test_add_course(self):
        self.assertEqual(Course.objects.get(name='TDT4140').administrators.all().__getitem__(0), User.objects.get(username='Pekka'))

    # Test server connectivity
    #def testAdd_question(self):
    #    resp = self.client.get('/add_question/')
    #    # Kan quizsiden nås?
    #    self.assertEqual(200, resp.status_code)

def main():
    unittest.main()

if __name__ == '__main__':
    main()