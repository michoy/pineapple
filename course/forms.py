from django import forms
from exercise.models import Course, Exercise, Question, ReadingMaterial, ThemeTag


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'


class PartialExerciseForm(forms.ModelForm):
    def __init__(self, course_pk, *args, **kwargs):
        super (PartialExerciseForm,self ).__init__(*args, **kwargs) # populates the post
        self.fields['contains'].queryset = Question.objects.filter(belongsTo__pk=course_pk)

    class Meta:
        model = Exercise
        exclude = ['course', 'private']
        widgets = {'contains': forms.CheckboxSelectMultiple}


class PartialQuestionForm(forms.ModelForm):
    def __init__(self, course_pk, *args, **kwargs):
        super (PartialQuestionForm,self ).__init__(*args, **kwargs) # populates the post
        # Lordhavemercy, sqlite limitation workaround
        reading_mats = list(Course.objects.get(pk=course_pk).content.values_list('pk',flat=True))
        tags = ThemeTag.objects.filter(material__pk__in=reading_mats).values_list('pk', flat=True).distinct()
        self.fields['themeTags'].queryset = ThemeTag.objects.filter(pk__in=tags)

    class Meta:
        model = Question
        exclude = ['belongsTo']
        widgets = {'themeTags': forms.CheckboxSelectMultiple}


class ReadingMatForm(forms.ModelForm):
    class Meta:
        model = ReadingMaterial
        exclude = []


class ThemeTagForm(forms.ModelForm):
    def __init__(self, course_pk, *args, **kwargs):
        super (ThemeTagForm,self ).__init__(*args, **kwargs) # populates the post
        self.fields['material'].queryset = Course.objects.get(pk=course_pk).content

    class Meta:
        model = ThemeTag
        exclude = []
        widgets = {'readingMaterial': forms.CheckboxSelectMultiple}
