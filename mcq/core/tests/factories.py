import factory
import factory.django
import factory.fuzzy

from question import models as question


class Category(factory.django.DjangoModelFactory):
    class Meta:
        model = question.Category

    name = factory.fuzzy.FuzzyText()


class Batch(factory.django.DjangoModelFactory):
    class Meta:
        model = question.Batch

    name = factory.fuzzy.FuzzyText()
    question_file = factory.django.FileField()
    category = factory.SubFactory('core.tests.factories.Category')


class Question(factory.django.DjangoModelFactory):
    class Meta:
        model = question.Question

    text = factory.fuzzy.FuzzyText()
    batch = factory.SubFactory('core.tests.factories.Batch')
