from django.shortcuts import render

from . import models
from . import forms

# signup and login functionality
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.hashers import make_password

# url searching through their names
from django.urls import reverse, reverse_lazy

class UserSignUp(CreateView):
    template_name = 'signup.html'

    model = models.User
    form_class = forms.SignUpForm

    def form_valid(self, form):
        # hash the password. argon2 by default
        password = make_password(form.instance.password)
        form.instance.password = password

        # save the form data
        form.save()

        # display the success message on the same signup page
        return render(self.request, self.template_name, context={
            'signup_success': True,
            'form': form
        })

class UserLogin(LoginView):
    model = models.User

    fields = ['username', 'password']
