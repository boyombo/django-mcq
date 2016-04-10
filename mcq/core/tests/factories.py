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
