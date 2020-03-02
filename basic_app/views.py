from django.shortcuts import render, redirect

from . import models
from . import forms

# display functionality
from django.views.generic.base import TemplateView

# signup and login functionality
from django.views.generic.edit import CreateView, View
from django.contrib.auth.views import LoginView
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate, login

# url searching through their names
from django.urls import reverse, reverse_lazy

class HomePageView(TemplateView):
    template_name = 'index.html'

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
    template_name = 'login.html'