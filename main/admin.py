from django.contrib import admin, auth
from .models import *

# Register your models here.

admin.site.register([Project, Issue, Comment, Team, User])