from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet, ModelForm, modelformset_factory
from django import forms
from quiz.models import Choice


class QuestionsInlineFormSet(BaseInlineFormSet):

    def clean(self):
        if not (self.instance.QUESTION_MIN_LIMIT <= len(self.forms) <= self.instance.QUESTION_MAX_LIMIT):
            raise ValidationError('Quantity of questions is out of range ({}..{})'.format(
                self.instance.QUESTION_MIN_LIMIT, self.instance.QUESTION_MAX_LIMIT
            ))


class ChoiceInlineFormSet(BaseInlineFormSet):

    def clean(self):
        if not (self.instance.ANSWER_MIN_LIMIT <= len(self.forms) <= self.instance.ANSWER_MAX_LIMIT):
            raise ValidationError('Quantity of answers is out of range ({}..{})'.format(
                self.instance.ANSWER_MIN_LIMIT, self.instance.ANSWER_MAX_LIMIT
            ))

        total_number = sum(
            1
            for form in self.forms
            if form.cleaned_data['is_correct']
        )

        if total_number == len(self.forms):
            raise ValidationError('NOT allowed to select all choices')

        if total_number == 0:
            raise ValidationError('At LEAST 1 choice should be selected')


class ChoiceForm(ModelForm):
    is_selected = forms.BooleanField(required=False)

    class Meta:
        model = Choice
        fields = ['text']

ChoiceFormSet = modelformset_factory(
    model=Choice,
    form=ChoiceForm,
    extra=0
)
