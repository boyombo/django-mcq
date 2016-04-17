from django.contrib import admin

from question.models import Category, Batch, Question, Option


@admin.register(Category, Batch, Question)
class QuestionAdmin(admin.ModelAdmin):
    pass


@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ['label', 'text', 'correct', 'question']
    list_filter = ['question__batch']


#@admin.register(Batch)
#class BatchAdmin(admin.ModelAdmin):
#    exclude = ['uploaded_on']
#    form = BatchForm
#
#    def save_model(self, request, obj, form, change):
#        questions = DictReader(obj.question_file)
#        self.message_user(
#            request, "File format is wrong", level=messages.ERROR)


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
