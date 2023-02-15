import random

from django.db import transaction
from django.core.management.base import BaseCommand

from main.models import *
from main.factory import *

NUM_USERS = 25
NUM_PROJECTS = 2
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

        # Create Teams
        self.stdout.write(f"- Creating {NUM_PROJECTS} teams...")
        for _ in range(NUM_PROJECTS):
            team = TeamFactory()

            # Assign Users to Teams
            self.stdout.write(f"\t- Assigning users to {team.name} team...")
            for i in range(NUM_USERS):
                if i % 2 == 0:
                    team.members.add(User.objects.all()[i])

        # Create Projects
        self.stdout.write(f"- Creating {NUM_PROJECTS} projects...")
        for i in range(NUM_PROJECTS):
            team = Team.objects.all()[i]
            project = ProjectFactory(team=team)

            def random_team_member():
                return random.choice(team.members.all())

            # Create Issues for each Project
            self.stdout.write(f"\t- Creating {NUM_ISSUES} issues...")
            for _ in range(NUM_ISSUES):
                issue = IssueFactory(project=project)

                # Create Comments for each Issue
                self.stdout.write(
                    f"\t\t- Creating {NUM_COMMENTS} issue comments...")
                for _ in range(NUM_COMMENTS):
                    CommentFactory(issue=issue, author=random_team_member())

        self.stdout.write("Data creation completed.")
