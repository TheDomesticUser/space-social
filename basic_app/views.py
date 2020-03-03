from django.shortcuts import render, redirect

from . import models
from . import forms

# http responses
from django.http import HttpResponseRedirect

# display functionality
from django.views.generic.base import TemplateView

# signup and login functionality
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.hashers import make_password

# display views
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

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

class UserLogout(LoginRequiredMixin, LogoutView):
    template_name = reverse_lazy('basic_app:user_logout')

class CreateGroup(LoginRequiredMixin, CreateView):
    template_name = 'create_group.html'

    model = models.Group
    fields = ['name']

    def form_valid(self, form):
        user = self.request.user
        group = models.Group(name=form.cleaned_data['name'])

        # save the group
        group.save()

        # set the user group relation
        assocation = models.Association(is_leader=True, group=group, member=user)
        assocation.save()

        return HttpResponseRedirect(reverse('basic_app:groups_list'))

class ListGroups(ListView):
    template_name = 'list_groups.html'
    
    model = models.Group

