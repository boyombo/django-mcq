from django import forms
from models import Batch, FIELD_NAMES

from csv import DictReader


class BatchForm(forms.ModelForm):
    #name = forms.CharField(
    #    widget=forms.TextInput(attrs={'class': 'form-control'}))
    #category = forms.ModelChoiceField(
    #    widget=forms.ChoiceInput(attr={'css': 'form-control'}))

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
            #headers = fd.
            #return list(data)
            return self.cleaned_data['question_file']
