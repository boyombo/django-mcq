from django import forms

#from question.models import Option


class AnswerForm(forms.Form):

    def __init__(self, *args, **kwargs):
        self.question = kwargs.pop('question')
        super(AnswerForm, self).__init__(*args, **kwargs)

        self.fields['option'] = forms.ModelChoiceField(
            self.question.answers.all(),
            widget=forms.RadioSelect(),
            empty_label=None,
            required=False)
