from django.shortcuts import render, redirect

from . import models
from . import forms

# http responses
from django.http import HttpResponse, HttpResponseRedirect

# display functionality
from django.views.generic.base import TemplateView

# signup and login functionality
from django.views.generic.edit import CreateView, UpdateView, DeleteView, View
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
        group = models.Group(name=form.cleaned_data['name'], leader=user)

        # save the group
        group.save()

        # set the user group relation
        assocation = models.Association(group=group, member=user)
        assocation.save()

        return HttpResponseRedirect(reverse('basic_app:groups_list'))

class ListGroups(ListView):
    template_name = 'list_groups.html'
    
    model = models.Group

class GroupDetailView(DetailView):
    template_name = 'group_detail.html'

    model = models.Group

    def get_context_data(self, **kwargs):
        # call the base implementation first to be able to set key values
        context = super().get_context_data(**kwargs)

        # get the user and group
        user = self.request.user
        group = self.get_object()

        # verify if the user is not in the group. If not, display join group btn
        assocation = models.Association.objects.filter(
            member=user,
            group=group
        ).first()

        if assocation:
            context['already_joined'] = True

            return context
        return context

class DeleteGroup(LoginRequiredMixin, DeleteView):
    template_name = 'group_confirm_delete.html'

    model = models.Group
    success_url = reverse_lazy('basic_app:groups_list')

    def get(self, request, *args, **kwargs):
        # confirm the get request was sent by the leader
        groupLeader = self.get_object().leader

        if groupLeader != request.user:
            # show a standard 401 access denied page
            return HttpResponse('<h1>Access Denied.</h1>', status=401)

        # continue everything as usual if correct authentication
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # confirm the post request was sent by the leader
        groupLeader = self.get_object().leader
        
        if groupLeader != request.user:
            # show a standard 401 unauthorized access page
            return HttpResponse('<h1>Something went wrong.</h1>', status=401)
        
        # continue everything as usual if correct authentication
        return super().post(request, *args, **kwargs)

class JoinGroup(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        # set the group to user assocation
        user = request.user
        group = models.Group.objects.get(pk=kwargs['pk'])

        # verify the association already exists to avoid duplicates
        assnCheck = models.Association.objects.filter(member=user, group=group)
        
        if not assnCheck.exists():
            # save the instance
            assn = models.Association(member=user, group=group)
            assn.save()

        # redirect the user to the group he/she joined
        return redirect(reverse('basic_app:group_detail', kwargs={ 'pk': group.pk }))