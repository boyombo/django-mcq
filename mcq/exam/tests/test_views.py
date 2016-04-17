import pytest
from django.core.urlresolvers import reverse

from core.tests import factories
from exam.models import Exam, Answer


@pytest.fixture
def batch():
    b = factories.Batch()
    factories.Question(batch=b, id=23)
    factories.Question(batch=b, id=35)
    factories.Question(batch=b, id=17)
    return b


@pytest.fixture
def exam():
    b = factories.Batch()
    q1 = factories.Question(batch=b, id=23)
    q2 = factories.Question(batch=b, id=35)
    factories.Question(batch=b, id=17)
    factories.Option(question=q1, correct=False, id=1)
    factories.Option(question=q1, correct=False, id=2)
    factories.Option(question=q1, id=3, correct=True)
    factories.Option(question=q2, correct=False, id=5)
    factories.Option(question=q2, correct=True, id=6)
    x = factories.Exam(batch=b)
    return x


@pytest.mark.django_db
def test_exam_start_status(client):
    '''GET request status is 200.'''
    batch = factories.Batch(id=2)
    response = client.get(reverse('exam_start', args=[batch.id]))

    assert response.status_code == 200


@pytest.mark.django_db
def test_exam_start_exam_obj(client):
    '''Exam object created is for the correct batch.'''
    batch = factories.Batch(id=2)
    client.get(reverse('exam_start', args=[batch.id]))
    # make sure exam object is produced
    assert Exam.objects.count() == 1
    # make sure it is the right one
    assert Exam.objects.all()[0].batch.id == batch.id


@pytest.mark.django_db
def test_exam_start_correct_template(client):
    '''Correct template is rendered.'''
    batch = factories.Batch()
    response = client.get(reverse('exam_start', args=[batch.id]))
    template_names = [i.name for i in response.templates]

    assert 'exam/start.html' in template_names


@pytest.mark.django_db
def test_exam_start_exam_context(client):
    '''Correct exam and first_question contexts contained in response.'''
    batch = factories.Batch()
    response = client.get(reverse('exam_start', args=[batch.id]))

    assert response.context[0]['exam'].batch.id == batch.id
    assert 'first_question' in response.context[0]


@pytest.mark.django_db
def test_exam_start_question_context(client, batch):
    '''Correct first question is in context.'''
    response = client.get(reverse('exam_start', args=[batch.id]))

    assert response.context[0]['first_question'].id == 17


@pytest.mark.django_db
def test_exam_start_question_context_no_question(client):
    '''None is sent as first_question if no question in batch.'''
    batch = factories.Batch()
    response = client.get(reverse('exam_start', args=[batch.id]))

    assert not response.context[0]['first_question']


@pytest.mark.django_db
def test_exam_question_template(client):
    '''Correct template is rendered for /exam/question/.'''
    b = factories.Batch()
    q = factories.Question(batch=b)
    x = factories.Exam(batch=b)
    response = client.get(reverse('exam_question', args=[x.id, q.id]))

    assert 'exam/question.html' in [i.name for i in response.templates]


#@pytest.mark.django_db
#def test_exam_get_question_first(client, btch):
#    '''get_question view with 1 param gives first question'''
#    x = factories.Exam(batch=btch)
#
#    response = client.get('/exam/question/{}/0/'.format(x.id))
#    #import pdb;pdb.set_trace()
#    assert response.context['question'].id == 17


@pytest.mark.django_db
def test_exam_get_question(client, batch):
    '''get_question context should contain question with id=question_id'''
    x = factories.Exam(batch=batch)

    response = client.get(reverse('exam_question', args=[x.id, 23]))
    assert response.context['question'].id == 23


@pytest.mark.django_db
def test_get_question_post_invalid_no_redirect(client, exam):
    '''If answer is invalid stay in same view.'''
    data = {'option': '5'}  # no option with id == 5
    url = reverse('exam_question', args=[exam.id, 23])
    response = client.post(url, data)

    #import pdb;pdb.set_trace()
    assert not response.context[0]['form'].is_valid()
    assert response.status_code == 200


@pytest.mark.django_db
def test_exam_get_question_post_redirect(client, exam):
    '''After POST to get_question, view redirects to next one.'''
    data = {'option': '3'}
    url = reverse('exam_question', args=[exam.id, 23])
    response = client.post(url, data)

    assert response.status_code == 302
    assert response.url == reverse('exam_question', args=[exam.id, 35])
    #import pdb;pdb.set_trace()


#@pytest.mark.django_db
#def test_get_question_post_context(client, exam):
#    '''Context of response contains required data.'''
#    data = {'option': '3'}
#    url = reverse('exam_question', args=[exam.id, 23])
#    response = client.post(url, data)
#
#    import pdb;pdb.set_trace()
#    assert response.context[0]['question_id'] == 23


@pytest.mark.django_db
def test_correct_answer_recorded(client, exam):
    '''Correct answer recorded properly.'''
    data = {'option': '3'}
    url = reverse('exam_question', args=[exam.id, 23])
    client.post(url, data)
    answer = Answer.objects.get(exam=exam, question__id=23)

    assert answer.is_correct


@pytest.mark.django_db
def test_wrong_answer_recorded(client, exam):
    '''Wrong answer recorded properly.'''
    data = {'option': '2'}
    url = reverse('exam_question', args=[exam.id, 23])
    client.post(url, data)
    answer = Answer.objects.get(exam=exam, question__id=23)

    assert not answer.is_correct


@pytest.mark.django_db
def test_last_get_question_redirect(client, exam):
    '''After POST of last question, view redirects to end view.'''
    data = {'option': '6'}
    url = reverse('exam_question', args=[exam.id, 35])
    response = client.post(url, data)

    assert response.status_code == 302
    assert response.url == reverse('exam_end', args=[exam.id])


@pytest.mark.django_db
def test_end_view_template(client, exam):
    '''Correct template is used for end view.'''
    response = client.get(reverse('exam_end', args=[exam.id]))

    assert 'exam/end.html' in [i.name for i in response.templates]


@pytest.mark.django_db
def test_end_view_context(client, exam):
    '''Correct context in response of end view.'''
    response = client.get(reverse('exam_end', args=[exam.id]))

    assert response.context[0]['exam'].id == exam.id


@pytest.mark.django_db
def test_end_view_post_ends_exam(client, batch):
    '''Exam is marked as completed when end_exam is posted.'''
    exam = factories.Exam(batch=batch)
    #import pdb;pdb.set_trace()
    client.post(reverse('exam_end', args=[exam.id]))

    assert Exam.objects.get(pk=exam.id).status == Exam.COMPLETED


@pytest.mark.django_db
def test_end_view_post_redirect(client, batch):
    '''End view posted redirects to exam_result view.'''
    exam = factories.Exam(batch=batch)
    response = client.post(reverse('exam_end', args=[exam.id]))

    assert response.status_code == 302
    assert response.url == reverse('exam_result', args=[exam.id])


@pytest.mark.django_db
def test_exam_result_template(client, exam):
    response = client.get(reverse('exam_result', args=[exam.id]))

    assert response.status_code == 200
    assert 'exam/result.html' in [i.name for i in response.templates]
