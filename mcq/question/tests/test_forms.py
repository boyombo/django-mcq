import pytest
from django.core.files.uploadedfile import SimpleUploadedFile

from question.forms import BatchForm
from core.tests import factories


@pytest.mark.django_db
def test_upload(suf, form_data):
    form = BatchForm(form_data, {'question_file': suf})
    assert form.is_valid()


@pytest.mark.django_db
def test_duration_negative(suf, form_data):
    form_data.update({'duration': -2})
    form = BatchForm(form_data, {'question_file': suf})

    assert not form.is_valid()
    err_text = 'Ensure this value is greater than or equal to 0.'
    assert err_text in form.errors['duration']


#@pytest.mark.django_db
#def test_upload_question_correct(suf, form_data):
#    '''Validate that the content of cleaned_data is same as sent in file.'''
#    form = BatchForm(form_data, {'question_file': suf})
#    form.is_valid()
#    file_content = form.cleaned_data['question_file']
#    assert len(file_content) == 2
#    assert file_content[0]['QUESTION'] == 'question1'
#    assert file_content[1]['QUESTION'] == 'question2'


@pytest.mark.django_db
def test_batch_file_header(form_data):
    '''Validate that file contains all the required headers for the file'''
    data = 'QUESTION,OPTION_A,OPTION_B,OPTION_C,OPTION_D,OPTION_F,CORRECT\n'\
           'question1,one,two,three,four,five,A\n'
    suf = SimpleUploadedFile('questions.csv', data, content_type='text/csv')

    form = BatchForm(form_data, {'question_file': suf})

    assert not form.is_valid()
    assert 'Some file headers are missing' in form.errors['question_file']


@pytest.fixture(scope='module')
def suf():
    data = 'QUESTION,A,B,C,D,E,CORRECT\n'\
           'question1,one,two,three,four,five,A\n'\
           'question2,aone,atwo,athree,afour,afive,C'

    suf = SimpleUploadedFile('questions.csv', data, content_type='text/csv')
    return suf


@pytest.fixture()
def form_data():
    category = factories.Category()
    return {'name': 'test', 'category': str(category.id)}
