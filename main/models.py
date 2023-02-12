from django.db import models
from django.db.models import Model
from django.contrib.auth.models import AbstractUser
import uuid


class User(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.username} ({self.first_name} {self.last_name})"


class Team(Model):
    name = models.CharField(max_length=255)
    members = models.ManyToManyField(User)

    def __str__(self):
        return self.name


class Project(Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=64)
    description = models.TextField()

    team = models.ForeignKey(Team, null=True, on_delete=models.SET_NULL)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Issue(Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    status = models.CharField(max_length=255)
    priority = models.CharField(max_length=255)

    author = models.OneToOneField(
        User, null=True, on_delete=models.SET_NULL, related_name="issue_author")
    assigned = models.OneToOneField(
        User, null=True, on_delete=models.SET_NULL, related_name="issue_assigned")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Comment(Model):
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text
