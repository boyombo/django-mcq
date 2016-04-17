from django.shortcuts import render, get_object_or_404, redirect
#from django.http import Http404
from question.models import Batch, Question
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


def exam_result(request, exam_id):
    exam = get_object_or_404(Exam, pk=exam_id)
    return render(request, 'exam/result.html', {'exam': exam})


def end(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    if request.method == 'POST':
        exam.end()
        return redirect(exam_result, exam_id=exam_id)
    return render(request, 'exam/end.html', {'exam': exam})


def get_question(request, exam_id, question_id):
    exam = get_object_or_404(Exam, pk=exam_id)
    question = get_object_or_404(Question, pk=question_id)
    if request.method == 'POST':
        form = AnswerForm(request.POST, question=question)
        #import pdb;pdb.set_trace()
        if form.is_valid():
            selected = form.cleaned_data['option']
            answer, _ = Answer.objects.get_or_create(
                exam=exam, question=question)
            answer.selected = selected
            answer.save()

            try:
                next_question = exam.next_question(question_id)
            except LastQuestion:
                return redirect(end, exam_id=exam_id)
            return redirect(
                get_question, exam_id=exam_id, question_id=next_question.id)

    else:
        form = AnswerForm(question=question)
    return render(request, 'exam/question.html',
                  {'question': question, 'form': form})
