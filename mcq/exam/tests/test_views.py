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
