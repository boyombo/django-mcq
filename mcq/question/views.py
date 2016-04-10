from django.shortcuts import render


def new_batch(request):
    return render(request, 'question/batch.html', {})
