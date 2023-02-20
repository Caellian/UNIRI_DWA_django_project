from django.contrib import admin, auth
from .models import *

model_list = [Project, ProjectSchedule, Issue, Comment, Team, User]

admin.site.register(model_list)
