from __future__ import unicode_literals
from datetime import datetime

from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = 'Categories'

    def __unicode__(self):
        return self.name


class Batch(models.Model):
    name = models.CharField(max_length=200)
    uploaded_on = models.DateTimeField(default=datetime.now)
    category = models.ForeignKey(Category)

    class Meta:
        verbose_name_plural = 'Batches'

    def __unicode__(self):
        return self.name


class Question(models.Model):
    text = models.CharField(max_length=250)
    batch = models.ForeignKey(Batch)

    def __unicode__(self):
        return self.text


class Option(models.Model):
    label = models.PositiveIntegerField()
    text = models.CharField(max_length=250)
    correct = models.BooleanField()
    question = models.ForeignKey(Question, related_name='answers')

    def __unicode__(self):
        return self.text
