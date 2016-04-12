import pytest

from core.tests import factories
from exam.models import Exam, Answer


@pytest.mark.django_db
def test_exam_model():
    batch = factories.Batch()
    exam = Exam.objects.create(batch=batch)

    assert str(exam) == batch.name

    # default status
    assert exam.status == Exam.PENDING


@pytest.mark.django_db
def test_answer_model_repr():
    batch = factories.Batch()
    exam = Exam.objects.create(batch=batch)
    question = factories.Question()
    answer = Answer.objects.create(exam=exam, question=question)

    assert str(answer) == batch.name
