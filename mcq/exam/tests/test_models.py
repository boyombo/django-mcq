import pytest

from core.tests import factories
from exam.models import Exam, Answer, NoQuestion, LastQuestion
from question.models import Question


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


@pytest.mark.django_db
def test_exam_first_question(exam):
    '''We can get first question for an exam.'''
    assert exam.first_question.id == 10


@pytest.mark.django_db
def test_exam_first_question_none():
    '''No question for exam, should throw exception.'''
    batch = factories.Batch()
    exam = factories.Exam(batch=batch)

    with pytest.raises(NoQuestion):
        exam.first_question


@pytest.mark.django_db
def test_exam_next_question_correct_batch():
    '''Exam obj gives question from the correct batch.'''
    batch1 = factories.Batch()
    batch2 = factories.Batch()
    factories.Question(batch=batch1)
    factories.Question(batch=batch1)
    factories.Question(batch=batch2)
    exam = factories.Exam(batch=batch1)
    qtn = exam.next_question()

    assert qtn.batch.id == batch1.id


@pytest.mark.django_db
def test_exam_next_question_first(exam):
    '''First Question for batch is sent in correct order.'''
    qtn1 = exam.next_question()

    assert qtn1.id == 10


@pytest.mark.django_db
def test_exam_next_question_correct(exam):
    '''Next question from batch is sent in correct order.'''
    qtn = exam.next_question(question_id=11)
    assert qtn.id == 12


@pytest.mark.django_db
def test_exam_next_question_none():
    '''No question for exam, should throw exception.'''
    batch = factories.Batch()
    exam = factories.Exam(batch=batch)

    with pytest.raises(NoQuestion):
        exam.next_question()


@pytest.mark.django_db
def test_exam_next_question_last(exam):
    '''Questions finished for exam should throw exception.'''
    q = Question.objects.get(id=12)

    with pytest.raises(LastQuestion):
        exam.next_question(q.id)


@pytest.fixture
def exam():
    batch = factories.Batch()
    exam = factories.Exam(batch=batch)

    factories.Question(id=10, batch=batch)
    factories.Question(id=11, batch=batch)
    factories.Question(id=12, batch=batch)
    return exam
