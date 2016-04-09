from django.contrib import admin

from question.models import Category, Batch, Question, Option


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']


class BatchAdmin(admin.ModelAdmin):
    list_display = ['name', 'uploaded_on', 'category']


class QuestionAdmin(admin.ModelAdmin):
    list_display = ['text', 'batch']


class OptionAdmin(admin.ModelAdmin):
    list_display = ['label', 'text', 'correct', 'question']


admin.site.register(Category, CategoryAdmin)
admin.site.register(Batch, BatchAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Option, OptionAdmin)
