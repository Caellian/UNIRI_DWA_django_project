from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.contrib.auth.models import User

from datetime import datetime
import base64

from .models import *
from .forms import *

def today():
    return datetime.now().strftime('%Y-%m-%d')

class DashboardView(generic.View):
    def get(self, request):
        projects = Project.objects.filter(is_active=True)
        users = User.objects.all().order_by('-last_login')[:10]
        return render(request, 'dashboard.html', {'projects': projects, 'users': users})

class ProjectListView(generic.View):
    def get(self, request):
        projects = Project.objects.all()
        return render(request, 'info/project_list.html', {'projects': projects})

    def post(self, request):
        if 'delete' in request.POST:
            Project.objects.get(id=request.POST['project_id']).delete()
            return redirect('main:project_list')

class ProjectDetailView(generic.View):
    def get(self, request, project_id):
        project = get_object_or_404(Project, pk=project_id)
        issues = Issue.objects.filter(project=project)
        return render(request, 'info/project_detail.html', {'project': project, 'issues': issues})

class ProjectFormCreateView(generic.View):
    def get(self, request):
        form = ProjectCreateForm(initial={'start_date': today()})
        return render(request, 'forms/create_project.html', {'form': form})

    def post(self, request):
        form = ProjectCreateForm(request.POST)
    
        if form.is_valid():
            name = form.cleaned_data['name']
            
            if Project.objects.filter(name=name).exists():
                return render(request, 'forms/create_project.html', {'form': form, 'error': 'A project with the same name already exists.'})
            else:
                form.save()
                return redirect('main:project_list')

class IssueFormCreateView(generic.View):
    def get(self, request):
        form = ProjectCreateForm(initial={'start_date': today()})
        return render(request, 'forms/create_project.html', {'form': form})

    def post(self, request):
        form = ProjectCreateForm(request.POST)
    
        if form.is_valid():
            name = form.cleaned_data['name']
            
            if Project.objects.filter(name=name).exists():
                return render(request, 'forms/create_project.html', {'form': form, 'error': 'A project with the same name already exists.'})
            else:
                form.save()
                return redirect('main:project_list')
