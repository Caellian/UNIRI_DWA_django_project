import random

from django.db import transaction
from django.core.management.base import BaseCommand

from main.models import *
from main.factory import *

NUM_USERS = 25
NUM_TEAMS = 2
NUM_PROJECTS = 7
NUM_ISSUES = 10
NUM_COMMENTS = 25

class Command(BaseCommand):
    help = "Generates test data"

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write("Deleting old data...")
        models = [Project, Issue, Comment, Team, User]
        for m in models:
            m.objects.all().delete()

        self.stdout.write("Creating new data:")

        # Create Users
        self.stdout.write(f"- Creating {NUM_USERS} users...")
        for _ in range(NUM_USERS):
            UserFactory()
        users = User.objects.all()

        # Create Teams
        self.stdout.write(f"- Creating {NUM_TEAMS} teams...")
        for _ in range(NUM_TEAMS):
            team = TeamFactory()
        teams = Team.objects.all()

        self.stdout.write("- Assigning users to teams...")
        for i in range(NUM_USERS):
            self.stdout.write(f"\t{users[i].username} -> {teams[i % NUM_TEAMS].namespace}")
            teams[i % NUM_TEAMS].members.add(users[i])

        # Create Projects
        self.stdout.write(f"- Creating {NUM_PROJECTS} projects...")
        for i in range(NUM_PROJECTS):
            team = teams[i % NUM_TEAMS]
            members = team.members.all()
            project = ProjectFactory(team=team)

            def random_team_member():
                return random.choice(members)

            # Create Issues for each Project
            self.stdout.write(f"\t- Creating {NUM_ISSUES} issues with {NUM_COMMENTS} comments...")
            for _ in range(NUM_ISSUES):
                issue = IssueFactory(project=project)

                # Create Comments for each Issue
                for _ in range(NUM_COMMENTS):
                    CommentFactory(issue=issue, author=random_team_member())

        self.stdout.write("Data creation completed.")
