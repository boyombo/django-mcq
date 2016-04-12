import pytest
from django.core.files.uploadedfile import SimpleUploadedFile

from core.tests import factories
from question.models import Question, Batch, Option


@pytest.mark.django_db
def test_batch_get_status(client):
    '''GET request status is 200.'''
    response = client.get('/question/batch/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_batch_template(client):
    '''The correct template is rendered.'''
    response = client.get('/question/batch/')
    template_names = [i.name for i in response.templates]

    assert 'question/batch.html' in template_names
    assert 'base.html' in template_names


@pytest.mark.django_db
def test_batchlist_template(client):
    '''The correct template renders batchlist.'''
    response = client.get('/question/batchlist/')
    template_names = [i.name for i in response.templates]

    assert 'question/batch_list.html' in template_names
    assert 'base.html' in template_names


@pytest.mark.django_db
def test_batch_redirects_good_file_data(client, suf):
    '''The view redirects if data is good'''
    category = factories.Category()
    d = {'category': str(category.id), 'name': 'test', 'question_file': suf}
    response = client.post('/question/batch/', d)

    assert response.status_code == 302


@pytest.mark.django_db
def test_batch_no_redirect_bad_file_data(client):
    '''The view redirects if data is good'''
    cntnt = 'QQUESTION,A,B,C,D,E,CORRECT\n'\
            'question1,one,two,three,four,five,A\n'\
            'question2,aone,atwo,athree,afour,afive,C'

    suf = SimpleUploadedFile('questions.csv', cntnt, content_type='text/csv')

    category = factories.Category()
    d = {'category': str(category.id), 'name': 'test', 'question_file': suf}
    response = client.post('/question/batch/', d)

    assert response.status_code == 200


@pytest.mark.django_db
def test_batch_saves_data(client, suf):
    '''The Batchform is in the template.'''

    category = factories.Category()
    d = {'category': str(category.id), 'name': 'test', 'question_file': suf}
    client.post('/question/batch/', d)

    assert Batch.objects.count() == 1


@pytest.mark.django_db
def test_batch_saves_questions(client, suf):
    '''The view should save questions.'''
    category = factories.Category()
    d = {'category': str(category.id), 'name': 'test', 'question_file': suf}
    client.post('/question/batch/', d)
    #import pdb;pdb.set_trace()

    assert Question.objects.count() == 2


@pytest.mark.django_db
def test_batch_saves_options(client, suf):
    '''The view should save options and the correct one too.'''
    category = factories.Category()
    d = {'category': str(category.id), 'name': 'test', 'question_file': suf}
    client.post('/question/batch/', d)
    #import pdb;pdb.set_trace()

    assert Option.objects.count() == 10
    correct_option1 = Option.objects.get(question__text='question1', label='A')
    correct_option2 = Option.objects.get(question__text='question2', label='C')
    assert correct_option1.correct
    assert correct_option2.correct
    assert Option.objects.filter(correct=True).count() == 2


@pytest.fixture
def suf():
    cntnt = 'QUESTION,A,B,C,D,E,CORRECT\n'\
            'question1,one,two,three,four,five,A\n'\
            'question2,aone,atwo,athree,afour,afive,C'

    return SimpleUploadedFile('questions.csv', cntnt, content_type='text/csv')
