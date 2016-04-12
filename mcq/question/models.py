from __future__ import unicode_literals
from datetime import datetime

from django.db import models

QUESTION_NAME = 'QUESTION'
CORRECT_NAME = 'CORRECT'

FIELD_NAMES = [
    QUESTION_NAME,
    'A',
    'B',
    'C',
    'D',
    'E',
    CORRECT_NAME
]


class Category(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = 'Categories'

    def __unicode__(self):
        return self.name


class Batch(models.Model):
    name = models.CharField(max_length=200)
    uploaded_on = models.DateTimeField(default=datetime.now)
    question_file = models.FileField(upload_to='question_dir')
    category = models.ForeignKey(Category)
    duration = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Batches'
        unique_together = ('name', 'category')

    def __unicode__(self):
        return self.name


class Question(models.Model):
    text = models.CharField(max_length=250)
    batch = models.ForeignKey(Batch, related_name='questions')

    def __unicode__(self):
        return self.text


class Option(models.Model):
    label = models.CharField(max_length=50)
    text = models.CharField(max_length=250)
    correct = models.BooleanField()
    question = models.ForeignKey(Question, related_name='answers')

    def __unicode__(self):
        return self.text
