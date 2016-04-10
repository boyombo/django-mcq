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

    def clean_question_file(self):
        if 'question_file' in self.cleaned_data:
            fd = self.cleaned_data['question_file']
            #import pdb;pdb.set_trace()
            data = DictReader(fd)
            field_names = data.fieldnames
            if set(FIELD_NAMES).difference(field_names):
                raise forms.ValidationError("Some field names are missing")
            #headers = fd.
            return list(data)
