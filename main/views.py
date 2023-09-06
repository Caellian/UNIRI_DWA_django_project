from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse, reverse_lazy
from django.conf import settings
from django.db.models import Q


from datetime import datetime

from .mixins import *
from .models import *
from .forms import *
from .util import next_or_dashboard, get_next


def today():
    return datetime.now().strftime('%Y-%m-%d')


def dashboard(request):
    return render(request, 'dashboard.html')


class TeamList(generic.ListView):
    model = Team

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["create_form"] = TeamForm()
        return context


class TeamDetail(TeamRequiredMixin, generic.DetailView):
    model = Team
    pk_url_kwarg = "team_namespace"
    slug_url_kwarg = "team_namespace"


class TeamDelete(TeamRequiredMixin, generic.edit.DeleteView):
    model = Team
    pk_url_kwarg = "team_namespace"
    slug_url_kwarg = "team_namespace"
    template_name = 'forms/team_delete.html'
    success_url = reverse_lazy('main:team_list')


class ProjectList(TeamRequiredMixin, generic.ListView):
    model = Project
    pk_url_kwarg = "project_namespace"
    slug_url_kwarg = "team_namespace"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'team_namespace' in self.kwargs:
            context['team_namespace'] = self.kwargs['team_namespace']
        return context


class ProjectDetail(TeamRequiredMixin, MultiSlugMixin, generic.DetailView):
    model = Project
    slug_url_kwargs = {"team": "team_namespace",
                       "namespace": "project_namespace"}


class ProjectDelete(TeamRequiredMixin, MultiSlugMixin, generic.edit.DeleteView):
    model = Project
    slug_url_kwargs = {"team": "team_namespace",
                       "namespace": "project_namespace"}
    template_name = 'forms/project_delete.html'

    def get_success_url(self):
        team_namespace = self.kwargs['team_namespace']
        return reverse('main:team_detail', args=[team_namespace])


class ProjectEdit(TeamRequiredMixin, MultiSlugMixin, generic.edit.UpdateView):
    model = Project
    template_name = 'forms/project_edit.html'
    slug_url_kwargs = {"team__namespace": "team_namespace",
                       "namespace": "project_namespace"}
    form_class = ProjectForm

    def get_success_url(self):
        return reverse('main:project_detail', team_namespace=self.kwargs["team_namespace"], project_namespace=self.kwargs["project_namespace"])


class IssueDetail(TeamRequiredMixin, generic.DetailView):
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


class IssueDelete(TeamRequiredMixin, MultiSlugMixin, generic.edit.DeleteView):
    model = Issue
    slug_url_kwargs = {"project__team__namespace": "team_namespace",
                       "project__namespace": "project_namespace",
                       "id": "issue_id"}
    template_name = 'forms/issue_delete.html'
            
    def get_success_url(self):
        team_namespace = self.kwargs['team_namespace']
        project_namespace = self.kwargs['project_namespace']
        return reverse('main:project_detail', args=[team_namespace, project_namespace])


class IssueEdit(TeamRequiredMixin, MultiSlugMixin, generic.edit.UpdateView):
    model = Issue
    fields = ['title', 'description', 'status', 'priority', 'assigned']
    template_name = 'forms/issue_edit.html'
    slug_url_kwargs = {"project__team__namespace": "team_namespace",
                       "project__namespace": "project_namespace",
                       "id": "issue_id"}

    def get_success_url(self):
        return reverse('main:issue_detail', team_namespace=self.kwargs["team_namespace"], project_namespace=self.kwargs["project_namespace"], issue_id=self.kwargs["issue_id"])


class UserList(generic.ListView):
    model = User


class UserDetail(TeamRequiredMixin, generic.DetailView):
    model = User
    slug_field = 'username'
    slug_url_kwarg = 'username'


class TeamFormView(TeamRequiredMixin, generic.edit.CreateView):
    model = Team
    fields = ['namespace', 'name']
    template_name = "forms/team_form.html"
    success_url = reverse_lazy('main:team_list')


class ProjectFormView(TeamRequiredMixin, generic.edit.CreateView):
    model = Project
    fields = ['namespace', 'team', 'name', 'description']
    template_name = "forms/project_form.html"
    success_url = reverse_lazy('main:project_list')

    def get_initial(self):
        initial = super(ProjectFormView, self).get_initial()
        if "team_namespace" in self.kwargs:
            initial.update({'team': self.kwargs['team_namespace']})
        return initial

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if "team_namespace" in self.kwargs:
            form.fields['team'].widget = forms.HiddenInput()
            form.fields['team'].widget.attrs.update(
                {'value': self.kwargs['team_namespace']})
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if "team_namespace" in self.kwargs:
            context['team_namespace'] = self.kwargs['team_namespace']
        return context


class IssueFormView(TeamRequiredMixin, generic.edit.FormView):
    template_name = 'forms/issue_form.html'
    form_class = IssueForm

    def get_initial(self):
        initial = super(IssueFormView, self).get_initial()
        if 'team_namespace' in self.kwargs and 'project_namespace' in self.kwargs:
            initial.update({'team': self.kwargs['team_namespace'],
                            'project': self.kwargs['project_namespace']})
        return initial

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if 'team_namespace' in self.kwargs and 'project_namespace' in self.kwargs:
            form.fields['team'].widget = forms.HiddenInput()
            form.fields['team'].widget.attrs.update(
                {'value': self.kwargs['team_namespace']})
            form.fields['project'].widget = forms.HiddenInput()
            form.fields['project'].widget.attrs.update(
                {'value': self.kwargs['project_namespace']})
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'team_namespace' in self.kwargs and 'project_namespace' in self.kwargs:
            context['team_namespace'] = self.kwargs['team_namespace']
            context['project_namespace'] = self.kwargs['project_namespace']
        return context

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        team_namespace = self.form.cleaned_data['team']
        project_namespace = self.form.cleaned_data['project']
        issue_id = self.form.cleaned_data['id']
        return reverse('main:issue_detail', team_namespace=team_namespace, project_namespace=project_namespace, id=issue_id)


def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            user = authenticate(request, username=username, password=password)
            login(request, user)
            return redirect('main:dashboard')
    else:
        form = SignupForm()

    context = {
        'form': form
    }

    return render(request, 'accounts/signup.html', context)


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return next_or_dashboard(request)
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = AuthenticationForm()

    context = {
        'form': form,
        'next': get_next(request)
    }

    return render(request, 'accounts/login.html', context)


def logout_view(request):
    logout(request)
    return next_or_dashboard(request)

def search(request):
    q = request.GET.get('q') if request.GET.get('q') is not None else ''
    users = User.objects.filter(
        Q(username__icontains=q) |
        Q(email__icontains=q) |
        Q(first_name__icontains=q) |
        Q(last_name__icontains=q)
    ) if request.user.is_authenticated else []

    teams = Team.objects.filter(
        Q(name__icontains=q) |
        Q(namespace__icontains=q)
    )

    projects = Project.objects.filter(
        Q(name__icontains=q) |
        Q(namespace__icontains=q) |
        Q(description__icontains=q)
    ) if request.user.is_authenticated else []
    
    issues = Issue.objects.filter(
        Q(title__icontains=q) |
        Q(description__icontains=q)
    ) if request.user.is_authenticated else []

    context = {
        "users": users,
        "teams": teams,
        "projects": projects,
        "issues": issues
    }
    return render(request, 'main/search.html', context)