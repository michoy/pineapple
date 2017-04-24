from django.db import models
from django.contrib.auth.models import User


class ReadingMaterial(models.Model):
    title = models.CharField(max_length=100, primary_key=True)
    link = models.CharField(max_length=300)  # Langt felt, kan jo være komplisert link

    def __str__(self):
        return self.title


class ThemeTag(models.Model):
    name = models.CharField(max_length=20, primary_key=True)
    # Relationships:
    material = models.ManyToManyField(ReadingMaterial)

    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=20, primary_key=True)
    full_name = models.CharField(max_length=40)
    description = models.CharField(max_length=300)
    # Relationships:
    administrators = models.ManyToManyField(User)  # Antar dette er greit,
    content = models.ManyToManyField(ReadingMaterial)  # Lesestoff som faget inneholder

    def __str__(self):
        return self.name


class CourseCollection(models.Model):
    student = models.OneToOneField(User)
    courses = models.ManyToManyField(Course)


class Question(models.Model):
    """ OBS: If atributes are changed, QuestionForm in forms must be updateted """
    answer_choices = (
        (1, 'Alternative 1'),
        (2, 'Alternative 2'),
        (3, 'Alternative 3'),
        (4, 'Alternative 4'),
    )
    title = models.CharField(max_length=70, primary_key=True)
    question = models.CharField(max_length=300)
    alternative_1 = models.CharField(max_length=200)
    alternative_2 = models.CharField(max_length=200)
    alternative_3 = models.CharField(max_length=200)
    alternative_4 = models.CharField(max_length=200)
    correct_alternative = models.IntegerField(default=1, choices=answer_choices)
    is_worth = models.IntegerField()
    # Relationships:
    themeTags = models.ManyToManyField(ThemeTag)  # Relaterte temaer
    belongsTo = models.ForeignKey(Course)  # Faget spørsmålet hører til

    def __str__(self):
        return self.question


class Exercise(models.Model):
    title = models.CharField(max_length=70)
    private = models.BooleanField(default=False)
    # Relationships:
    course = models.ForeignKey(Course)
    contains = models.ManyToManyField(Question)  # Spørsmålet oppgaven vil tilby

    def __str__(self):
        return self.title


class Result(models.Model):
    resultVal = models.BooleanField()
    # Relationships:
    question = models.ForeignKey(Question)
    exercise = models.ForeignKey(Exercise)

    def __str__(self):
        return str(self.resultVal)


class PECollector(models.Model):
    student = models.OneToOneField(User)
    exercises = models.ManyToManyField(Exercise)


class ResultCollection(models.Model):
    student = models.OneToOneField(User)
    results = models.ManyToManyField(Result)
