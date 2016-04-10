from django import forms
from models import Batch

from csv import DictReader

FIELD_NAMES = [
    'QUESTION',
    'OPTION_A',
    'OPTION_B',
    'OPTION_C',
    'OPTION_D',
    'OPTION_E',
    'CORRECT'
]


class BatchForm(forms.ModelForm):
    model = Batch
    exclude = ['uploaded_on']

    def clean_question_file(self):
        if 'question_file' in self.cleaned_data:
            questions = DictReader(self.cleaned_data['question_file'])
        raise forms.ValidationError('no data')
