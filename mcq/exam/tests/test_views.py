import pytest

from core.tests import factories
from exam.models import Exam


@pytest.mark.django_db
def test_exam_start_status(client):
    '''GET request status is 200.'''
    batch = factories.Batch(id=2)
    response = client.get('/exam/start/{}/'.format(batch.id))
    #import pdb;pdb.set_trace()

    assert response.status_code == 200


@pytest.mark.django_db
def test_exam_start_exam_obj(client):
    '''Exam object created is for the correct batch.'''
    batch = factories.Batch(id=2)
    client.get('/exam/start/{}/'.format(batch.id))
    #import pdb;pdb.set_trace()
    # make sure exam object is produced
    assert Exam.objects.count() == 1
    # make sure it is the right one
    assert Exam.objects.all()[0].batch.id == batch.id


@pytest.mark.django_db
def test_exam_start_correct_template(client):
    '''Correct template is rendered.'''
    batch = factories.Batch()
    response = client.get('/exam/start/{}/'.format(batch.id))
    template_names = [i.name for i in response.templates]

    assert 'exam/start.html' in template_names


@pytest.mark.django_db
def test_exam_start_exam_context(client):
    '''Correct exam and first_question contexts contained in response.'''
    batch = factories.Batch()
    response = client.get('/exam/start/{}/'.format(batch.id))

    assert response.context[0]['exam'].batch.id == batch.id
    assert 'first_question' in response.context[0]


@pytest.mark.django_db
def test_exam_start_question_context(client, btch):
    '''Correct first question is in context.'''
    response = client.get('/exam/start/{}/'.format(btch.id))

    assert response.context[0]['first_question'].id == 17


@pytest.mark.django_db
def test_exam_start_question_context_no_question(client):
    '''None is sent as first_question if no question in batch.'''
    batch = factories.Batch()
    response = client.get('/exam/start/{}/'.format(batch.id))

    assert not response.context[0]['first_question']


@pytest.mark.django_db
def test_exam_question_template(client):
    '''Correct template is rendered for /exam/question/.'''
    b = factories.Batch()
    factories.Question(batch=b)
    x = factories.Exam(batch=b)
    response = client.get('/exam/question/{}/0/'.format(x.id))

    assert 'exam/question.html' in [i.name for i in response.templates]


@pytest.mark.django_db
def test_exam_get_question_first(client, btch):
    '''get_question view with 1 param gives first question'''
    x = factories.Exam(batch=btch)

    response = client.get('/exam/question/{}/0/'.format(x.id))
    #import pdb;pdb.set_trace()
    assert response.context['question'].id == 17


@pytest.mark.django_db
def test_exam_get_question_next(client, btch):
    '''get_question view with 2 params gives question after question_id'''
    x = factories.Exam(batch=btch)

    context = {'exam': x.id, 'question': 23}
    response = client.get(
        '/exam/question/{exam}/{question}/'.format(**context))
    #import pdb;pdb.set_trace()
    assert response.context['question'].id == 35


@pytest.fixture
def btch():
    b = factories.Batch()
    factories.Question(batch=b, id=23)
    factories.Question(batch=b, id=35)
    factories.Question(batch=b, id=17)
    return b
