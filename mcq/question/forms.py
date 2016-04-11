from django import forms
from models import Batch, FIELD_NAMES

from csv import DictReader


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
                raise forms.ValidationError("Some file headers are missing")
            #headers = fd.
            return list(data)
