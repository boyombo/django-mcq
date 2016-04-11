from csv import DictReader
from django.shortcuts import render, redirect
from django.contrib import messages

from question.forms import BatchForm
from question.models import Batch, Question, Option
from question.models import QUESTION_NAME, CORRECT_NAME


def new_batch(request):
    if request.method == 'POST':
        form = BatchForm(request.POST, request.FILES)
        if form.is_valid():
            #questions = form.cleaned_data['question_file']
            batch = form.save()

            #import pdb;pdb.set_trace()
            data = DictReader(form.cleaned_data['question_file'])
            for line in data:
                q_text = line.pop(QUESTION_NAME)
                q = Question.objects.create(batch=batch, text=q_text)
                correct = line.pop(CORRECT_NAME)

                for k, v in line.items():
                    #import pdb;pdb.set_trace()
                    opt_data = {
                        'label': k,
                        'text': v,
                        'question': q,
                        'correct': False
                    }
                    if k == correct:
                        opt_data.update({'correct': True})
                    opt = Option(**opt_data)
                    opt.save()
            messages.info(request, 'Batch upload completed successfully')
            return redirect('new_batch')
        else:
            pass

    else:
        form = BatchForm()
    return render(request, 'question/batch.html', {'form': form})
