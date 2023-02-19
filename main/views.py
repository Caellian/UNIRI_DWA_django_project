from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.contrib.auth.models import User

from datetime import datetime
import base64

from .models import *
from .forms import *


def today():
    return datetime.now().strftime('%Y-%m-%d')


class Dashboard(generic.View):
    def get(self, request):
        return render(request, 'dashboard.html')


class TeamList(generic.ListView):
    model = Team


class ProjectList(generic.ListView):
    model = Project


class IssueList(generic.ListView):
    model = Issue


class UserList(generic.ListView):
    model = User


class CommentList(generic.ListView):
    model = Comment
