from django.shortcuts import render, get_object_or_404
from django.http import Http404
from question.models import Batch
from exam.models import Exam, Answer, NoQuestion, LastQuestion
from exam.forms import AnswerForm


def start(request, id):
    batch = get_object_or_404(Batch, pk=id)
    exam = Exam.objects.create(batch=batch)
    try:
        first_question = exam.first_question
    except NoQuestion:
        first_question = None
    return render(
        request,
        'exam/start.html',
        {'exam': exam, 'first_question': first_question})


def get_question(request, exam_id, question_id=None):
    # For the first Question 0 is passed as question_id
    #import pdb;pdb.set_trace()
    exam = get_object_or_404(Exam, pk=exam_id)
    try:
        question = exam.next_question(question_id)
    except (NoQuestion, LastQuestion):
        raise Http404
    if request.method == 'POST':
        form = AnswerForm(request.POST, question=question)
        #import pdb;pdb.set_trace()
        if form.is_valid():
            selected = form.cleaned_data['option']
            answer, _ = Answer.objects.get_or_create(
                exam=exam, question=question)
            answer.selected = selected
            answer.save()
    else:
        form = AnswerForm(question=question)
    return render(request, 'exam/question.html',
                  {'question': question, 'form': form})
