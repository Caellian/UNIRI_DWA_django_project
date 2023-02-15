from django.contrib import admin, auth
from .models import *

model_list = [Project, Issue, Comment, Team, User]

admin.site.register(model_list)
