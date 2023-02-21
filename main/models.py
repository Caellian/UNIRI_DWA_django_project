from django.db import models
from django.db.models import Model
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _
import uuid


class User(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def get_teams(self):
        return Team.objects.filter(members=self)

    def get_projects(self):
        teams = self.get_teams()

        projects = []
        for team in teams:
            projects += list(Project.objects.filter(team=team))

        return projects

    def __str__(self):
        return f"{self.username} ({self.first_name} {self.last_name})"


class Team(Model):
    namespace = models.CharField(primary_key=True, max_length=32)
    name = models.CharField(max_length=255)
    members = models.ManyToManyField(User)

    def get_projects(self):
        return Project.objects.filter(team=self.namespace)

    def __str__(self):
        return self.name


class ProjectSchedule(Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)


class Project(Model):
    class Meta:
        unique_together = (('team', 'namespace'),)

    namespace = models.CharField(primary_key=True, max_length=32)
    name = models.CharField(max_length=64)
    description = models.TextField()

    team = models.ForeignKey(Team, null=True, on_delete=models.CASCADE)
    schedule = models.OneToOneField(
        ProjectSchedule, null=True, on_delete=models.SET_NULL)

    def get_issues(self):
        return Issue.objects.filter(project=self)

    def __str__(self):
        return self.name


class IssueStatus(models.TextChoices):
    SOLVED = "SO", _("Solved")
    CLOSED = "CL", _("Closed")
    OPEN = "OP", _("Open")
    PLANNED = "PL", _("Planned")

    @classmethod
    def values(cls):
        return map(lambda choice: choice[0], cls.choices)


class IssuePriority(models.TextChoices):
    URGENT = "UR", _("Urgent")
    HIGH = "HI", _("High")
    IMPORTANT = "IM", _("Important")
    NORMAL = "NO", _("Normal")
    ENHANCMENT = "EN", _("Enhancment")
    LOW = "LO", _("Low")

    @classmethod
    def values(cls):
        return map(lambda choice: choice[0], cls.choices)


class Issue(Model):
    class Meta:
        unique_together = (('project', 'id'),)

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    status = models.CharField(max_length=2)
    priority = models.CharField(max_length=2)

    author = models.ForeignKey(
        User, null=True, on_delete=models.SET_NULL, related_name="issue_author")
    assigned = models.ForeignKey(
        User, null=True, on_delete=models.SET_NULL, related_name="issue_assigned")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_comments(self):
        return Comment.objects.filter(issue=self)

    def __str__(self):
        return self.title


class Comment(Model):
    class Meta:
        unique_together = (('issue', 'id'),)

    id = models.AutoField()
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text
