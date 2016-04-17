from django.contrib import admin

from exam.models import Exam, Answer


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ['batch', 'start_at', 'ended_at', 'status']


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['exam', 'question', 'selected', 'is_correct']
