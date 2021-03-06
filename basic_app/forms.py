from django.forms import ModelForm
from django import forms
from django.core.exceptions import ValidationError
from django.core import validators

# authentication
from django.contrib.auth.hashers import check_password

from . import models

class SignUpForm(ModelForm):
    username = forms.CharField(
        validators=[
            validators.MinLengthValidator(3),
            validators.MaxLengthValidator(20)
        ]
    )
    password = forms.CharField(
        widget=forms.PasswordInput,
        validators=[
            validators.MinLengthValidator(8),
            validators.MaxLengthValidator(20)
        ]
    )
    verify_password = forms.CharField(widget=forms.PasswordInput)

    # all users can be in a maximum of up to 5 groups

    class Meta:
        model = models.User
        fields = ('username', 'password')

    def clean_verify_password(self):
        cleaned_data = super().clean()
        
        password = cleaned_data.get('password')
        verified_password = cleaned_data.get('verify_password')

        if password != verified_password:
            raise ValidationError('The password does not match the verified password!')

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = models.User
        fields = ('username', 'password')
