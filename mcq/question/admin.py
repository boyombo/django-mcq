from django.contrib import admin

from question.models import Category, Batch, Question, Option


@admin.register(Category, Question, Option)
class QuestionAdmin(admin.ModelAdmin):
    pass


@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    exclude = ['uploaded_on']


#class CategoryAdmin(admin.ModelAdmin):
#    list_display = ['name']
#
#
#class QuestionAdmin(admin.ModelAdmin):
#    list_display = ['text', 'batch']
#
#
#class OptionAdmin(admin.ModelAdmin):
#    list_display = ['label', 'text', 'correct', 'question']
#
#
#admin.site.register(Category, CategoryAdmin)
#admin.site.register(Batch, BatchAdmin)
#admin.site.register(Question, QuestionAdmin)
#admin.site.register(Option, OptionAdmin)
