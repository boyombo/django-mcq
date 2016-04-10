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
    class Meta:
        model = Batch
        exclude = ['uploaded_on']
