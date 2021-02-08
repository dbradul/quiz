from django.contrib import admin

from quiz.forms import QuestionsInlineFormSet, ChoiceInlineFormSet
from quiz.models import Choice, Question, Test, Result


class ChoiceInline(admin.TabularInline):
    model = Choice
    fields = ('text', 'is_correct')
    show_change_link = True
    formset = ChoiceInlineFormSet
    extra = 0


class QuestionAdmin(admin.ModelAdmin):
    inlines = (ChoiceInline,)


class QuestionsInline(admin.TabularInline):
    model = Question
    fields = ('text', 'order_number')
    show_change_link = True
    extra = 0
    formset = QuestionsInlineFormSet
    ordering = ('order_number',)


class TestAdmin(admin.ModelAdmin):
    inlines = (QuestionsInline,)
    readonly_fields = ['uuid']


admin.site.register(Test, TestAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Result)