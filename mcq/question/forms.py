from django import forms
from models import Batch, FIELD_NAMES, CORRECT_NAME

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
            try:
                field_names = data.fieldnames
            except:
                raise forms.ValidationError(
                    "The file is not in the correct format")
            if set(FIELD_NAMES).difference(field_names):
                raise forms.ValidationError("Some file headers are missing")

            options = [i[CORRECT_NAME].strip() for i in data]
            if set(options).difference(FIELD_NAMES):
                raise forms.ValidationError(
                    "Questions must have a valid option")
            return self.cleaned_data['question_file']
