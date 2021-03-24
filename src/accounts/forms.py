from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm, fields, forms, Form

from django import forms

from accounts.models import User


class AccountCreateForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
        ]


class AccountUpdateForm(ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'bio',
            'birth_date',
        ]


class ContactUs(Form):
    subject = fields.CharField(max_length=256, empty_value='Message from Testify')
    message = fields.CharField(widget=forms.Textarea)
