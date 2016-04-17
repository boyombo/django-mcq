from __future__ import unicode_literals
from datetime import datetime

from django.db import models
from question.models import Batch, Question, Option


class NoQuestion(Exception):
    pass


class LastQuestion(Exception):
    pass


class Exam(models.Model):
    PENDING = 0
    STARTED = 1
    COMPLETED = 2
    EXAM_STATUS = enumerate((PENDING, STARTED, COMPLETED))
    batch = models.ForeignKey(Batch)
    start_at = models.DateTimeField(default=datetime.now)
    ended_at = models.DateTimeField(null=True, blank=True)
    status = models.PositiveIntegerField(choices=EXAM_STATUS, default=PENDING)

    def __unicode__(self):
        return unicode(self.batch)

    def end(self):
        self.ended_at = datetime.now()
        self.status = self.COMPLETED
        super(Exam, self).save()

    @property
    def num_questions(self):
        return self.batch.questions.count()

    @property
    def first_question(self):
        questions = Question.objects.filter(batch=self.batch).order_by('id')
        if not questions:
            raise NoQuestion
        return questions[0]

    def next_question(self, question_id=None):
        '''Return the next question from the batch.'''
        questions = Question.objects.filter(batch=self.batch).order_by('id')
        if not questions:
            raise NoQuestion
        if question_id:
            greater = [qtn for qtn in questions if qtn.id > int(question_id)]
            if greater:
                return greater[0]
            else:
                raise LastQuestion
        return questions[0]


class Answer(models.Model):
    exam = models.ForeignKey(Exam, related_name='answers')
    question = models.ForeignKey(Question)
    selected = models.ForeignKey(Option, null=True, blank=True)

    def __unicode__(self):
        return unicode(self.exam)

    @property
    def is_correct(self):
        return self.selected.correct
