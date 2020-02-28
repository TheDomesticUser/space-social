from django.shortcuts import render

from . import models

# Signup and login functionality
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.hashers import make_password

class UserSignUp(CreateView):
    model = models.User

    fields = ['username', 'password']

    def post(self, request):
        # hash the password
        password = make_password(request.instance.password)

        request.instance.password = password

        return super(self, UserSignUp).post(self.request)

class UserLogin(LoginView):
    model = models.User

    fields = ['username', 'password']
