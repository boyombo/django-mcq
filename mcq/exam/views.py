from django.shortcuts import render, get_object_or_404
from question.models import Batch
from exam.models import Exam


def start(request, id):
    batch = get_object_or_404(Batch, pk=id)
    exam = Exam.objects.create(batch=batch)
    return render(request, 'exam/start.html', {'exam': exam})
