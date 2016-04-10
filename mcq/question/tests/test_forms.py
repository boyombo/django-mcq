from question.forms import BatchForm
from core.tests import factories
import pytest
from django.core.files.uploadedfile import SimpleUploadedFile


@pytest.mark.django_db
def test_upload(tmpdir):
    data = 'QUESTION,OPTION_A,OPTION_B,OPTION_C,OPTION_D,OPTION_E,CORRECT\n'\
           'question1,one,two,three,four,five,A\n'\
           'question2,aone,atwo,athree,afour,afive,C'

    suf = SimpleUploadedFile('questions.csv', data, content_type='text/csv')

    category = factories.Category()
    form_data = {'name': 'test', 'category': str(category.id)}

    form = BatchForm(form_data, {'question_file': suf})
    assert form.is_valid()
