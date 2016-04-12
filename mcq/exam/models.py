from __future__ import unicode_literals
from datetime import datetime

from django.db import models
from question.models import Batch, Question, Option


class Exam(models.Model):
    PENDING = 0
    STARTED = 1
    COMPLETED = 2
    EXAM_STATUS = enumerate((PENDING, STARTED, COMPLETED))
    batch = models.ForeignKey(Batch)
    start_at = models.DateTimeField(default=datetime.now)
    ended_at = models.DateTimeField(default=datetime.now)
    status = models.PositiveIntegerField(choices=EXAM_STATUS, default=PENDING)

    def __unicode__(self):
        return unicode(self.batch)


class Answer(models.Model):
    exam = models.ForeignKey(Exam, related_name='answers')
    question = models.ForeignKey(Question)
    selected = models.ForeignKey(Option, null=True, blank=True)

    def __unicode__(self):
        return unicode(self.exam)
