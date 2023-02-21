from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView

from datetime import datetime
import base64

from .mixins import *
from .models import *
from .forms import *


def today():
    return datetime.now().strftime('%Y-%m-%d')


class Dashboard(generic.View):
    def get(self, request):
        return render(request, 'dashboard.html')


class TeamList(generic.ListView):
    model = Team


class TeamDetail(generic.DetailView):
    model = Team
    pk_url_kwarg = "team_namespace"
    slug_url_kwarg = "team_namespace"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['team_projects'] = context['team'].get_projects()
        return context


class ProjectList(generic.ListView):
    model = Project
    pk_url_kwarg = "project_namespace"
    slug_url_kwarg = "team_namespace"


class ProjectDetail(MultiSlugMixin, generic.DetailView):
    model = Project
    slug_url_kwargs = {"team": "team_namespace",
                       "namespace": "project_namespace"}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project_issues'] = context['project'].get_issues()
        return context


class IssueDetail(generic.DetailView):
    model = Issue
    slug_field = "id"
    slug_url_kwarg = "issue_id"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['issue_comments'] = context['issue'].get_comments()
        return context

    def get_object(self):
        q_team = self.kwargs.get('team_namespace')
        q_project = self.kwargs.get('project_namespace')
        q_id = self.kwargs.get('issue_id')

        project = Project.objects.filter(
            team=q_team, namespace=q_project).first()
        result = Issue.objects.filter(project=project, id=q_id).first()
        if result is None:
            raise HttpResponseNotFound("Issue does not exist")
        return result


class UserList(generic.ListView):
    model = User


class UserDetail(generic.DetailView):
    model = User
    slug_field = 'username'
    slug_url_kwarg = 'username'


def signup_view(request):
    context = {}

    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('main:dashboard')

    context['form'] = SignupForm()

    return render(request, 'accounts/signup.html', context)

def login_view(request):
    context = {}

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('main:dashboard')
        else:
            context['errors'] = ['invalid username or password'];
    
    context['form'] = LoginForm()

    return render(request, 'accounts/login.html', context)

def logout_view(request):
    logout(request)
    return redirect('main:dashboard')
