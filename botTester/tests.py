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
from botTester import AssistantBot
# Tester om sidene på serveren og funksjonene der fungerer rett
# Kan kjøre uten at serveren faktisk er på, tester kun serverkode, bruker ikke http


class ServerTestCase(TestCase):

    def setUp(self):
        # Må kjøres, ellers krasj
        django.setup()
        self.client = Client()
        populate.add_reading_material(title='Robot toes', link='http://wikipedia.com/robotstoes')
        populate.add_reading_material(title='Cakes', link='http://wikipedia.com/cakes')
        populate.add_reading_material(title='TheThingNobodyReads', link='http://studemail.no')
        populate.add_tag(name='Robot-things', material_list=['Robot toes'])
        populate.add_tag(name='Not robot-things', material_list=['Cakes'])
        populate.add_tag(name='Nobody gets this', material_list=['TheThingNobodyReads'])
        populate.add_course(
            name='TDT0001',
            full_name='This is a test course!',
            admin_list=[],
            material_list=['Robot toes', 'Cakes'],
            description='For bot-testing purposes'
        )
        populate.add_question(
            title='RoboToes',
            question='Do board-wiping robots need toes?',
            alternative_list=[
                'Absolutely!',
                'Only if board is 1m+ high',
                'Add 50, just in case',
                'Yes, so that they can stub them!',
            ],
            correct_num=3,
            tag_list=['Robot-things'],
            belongs_to='TDT0001',
            is_worth=10,
        )
        populate.add_question(
            title='Cupcakecakes',
            question='How many cups of cupcake-cakebatter per cup of cupcake?',
            alternative_list=[
                10,
                15,
                0.2,
                0.73,
            ],
            correct_num=4,
            tag_list=['Not robot-things', 'Robot-things'],
            belongs_to='TDT0001',
            is_worth=15,
        )
        populate.add_question(
            title='DoNotAnswerThis',
            question="Please don't answer, maybe",
            alternative_list=[
                "you don't know me!",
                'yeah, that will show him',
                "can't find back button, sorry",
                "ok.. waitNoooooo",
            ],
            correct_num=4,
            tag_list=['Nobody gets this'],
            belongs_to='TDT0001',
            is_worth=0,
        )
        ex = populate.add_exercise(
            title='OopsAlmostForgotTheExercise',
            course='TDT0001',
            question_list=['RoboToes', 'Cupcakecakes', 'DoNotAnswerThis']
        )
        populate.add_user_group('Student')
        populate.add_user(
            username='YoungAndNaive',
            email='xXx69xXx@yahoo.com',
            password=123,
            course_list=['TDT0001'],
            result_pk_list=[],
            pers_exercise_list=[],
            group_name_list=['Student'],
        )
        populate.add_result(
            val=False,
            question='RoboToes',
            student='YoungAndNaive',
            exercise=ex.pk,
        )
        populate.add_result(
            val=True,
            question='Cupcakecakes',
            student='YoungAndNaive',
            exercise=ex.pk,
        )
        populate.add_result(
            val=True,
            question='DoNotAnswerThis',
            student='YoungAndNaive',
            exercise=ex.pk,
        )

    def test_make_rec(self):
        result = AssistantBot.make_rec('YoungAndNaive', 'TDT0001')
        self.assertEqual({'Robot-things': 1.0, 'Not robot-things': 0.0, 'Nobody gets this': 0.0}, result)

    def test_gen_reading_rec(self):
        rec = AssistantBot.make_rec('YoungAndNaive', 'TDT0001')
        result = AssistantBot.gen_reading_rec(5, rec)
        self.assertEqual([('Robot toes', 'http://wikipedia.com/robotstoes')],result)
        self.assertRaises(ValueError, AssistantBot.gen_reading_rec, 5, {'test': 0.5})

    def test_gen_exercise(self):
        rec = AssistantBot.make_rec('YoungAndNaive', 'TDT0001')
        result = AssistantBot.gen_exercise(2,rec, 'YoungAndNaive', 'TDT0001')
        self.assertEqual("YoungAndNaive's tailored Exercise 1", result.title)
        self.assertEqual(
            result.pk,
            User.objects.get(username='YoungAndNaive').pecollector.exercises.all().__getitem__(0).pk
        )
        self.assertEqual(['Cupcakecakes', 'RoboToes'], sorted(list(result.contains.all().values_list('title',flat=True))))
        self.assertEqual(2, len(list(result.contains.all().values_list('title',flat=True))))
        self.assertTrue('Cupcakecakes' in list(result.contains.all().values_list('title',flat=True)))
        self.assertTrue('RoboToes' in list(result.contains.all().values_list('title', flat=True)))
        self.assertRaises(ValueError, AssistantBot.gen_exercise, 5,{},'YoungAndNaive','TDT0001')
        self.assertRaises(ValueError, AssistantBot.gen_exercise, 5, {'test':0.5}, 'YoungAndNaive', 'TDT0001')

    def test_gen_student_exercise(self):
        result = AssistantBot.gen_student_exercise('TDT0001', 'YoungAndNaive')
        self.assertEqual((['OopsAlmostForgotTheExercise'], [60], [60]), result)

    def test_gen_student_theme(self):
        result = AssistantBot.gen_student_theme('TDT0001', 'YoungAndNaive')
        self.assertEqual(
            (['Robot-things', 'Not robot-things', 'Nobody gets this'], [60, 100, 100], [60, 100, 100]),
            result
        )

    def test_gen_lecturer_exercise(self):
        result = AssistantBot.gen_lecturer_exercise('TDT0001')
        self.assertEqual((['OopsAlmostForgotTheExercise'], [60]), result)

    def test_gen_lecturer_theme(self):
        result = AssistantBot.gen_lecturer_theme('TDT0001')
        self.assertEqual((['Robot-things', 'Not robot-things', 'Nobody gets this'], [60, 100, 100]), result)

    def test_retrieve_question_material(self):
        result_1 = AssistantBot.retrieve_question_material('RoboToes', 5)
        result_2 = AssistantBot.retrieve_question_material('Cupcakecakes', 5)
        result_3 = AssistantBot.retrieve_question_material('DoNotAnswerThis', 5)
        self.assertEqual(['Robot toes'], result_1)
        self.assertEqual(['Cakes', 'Robot toes'], sorted(result_2))
        self.assertEqual(['TheThingNobodyReads'], result_3)