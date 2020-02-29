from django.forms import ModelForm
from django import forms
from django.core.exceptions import ValidationError

from . import models

class SignUpForm(ModelForm):
    password = forms.CharField(max_length=20, min_length=8, widget=forms.PasswordInput)
    verify_password = forms.CharField(max_length=20, min_length=8, widget=forms.PasswordInput)

    class Meta:
        model = models.User
        fields = ('username', 'password')

    def clean(self):
        # verify the password matches the verified password
        if self.cleaned_data['password'] != self.cleaned_data['verify_password']:
            raise ValidationError('The password does not match the verified password!')

        return super(SignUpForm, self).clean()