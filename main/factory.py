import random
from datetime import timedelta

import factory
from factory.django import DjangoModelFactory

from main.models import *


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Faker('email')
    password = factory.PostGenerationMethodCall('set_password', 'f4k3use3r')
    bio = factory.Faker("sentence", nb_words=120)

    is_superuser = False
    is_staff = False
    is_active = True

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")

    username = factory.LazyAttribute(
        lambda obj: f"{obj.first_name.lower()}_{obj.last_name.lower()}"
    )


class TeamFactory(DjangoModelFactory):
    class Meta:
        model = Team

    namespace = factory.Faker('word')
    name = factory.LazyAttribute(
        lambda team: team.namespace)

    @factory.post_generation
    def members(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of members were passed in, use them.
            for member in extracted:
                self.members.add(member)
        else:
            # No members were passed in, create some.
            num_members = random.randint(1, 10)
            for _ in range(num_members):
                member = UserFactory()
                self.members.add(member)


class ProjectScheduleFactory(DjangoModelFactory):
    class Meta:
        model = ProjectSchedule

    start_date = factory.Faker('date_this_decade')
    end_date = factory.LazyAttribute(
        lambda project: project.start_date + timedelta(days=random.randint(1, 4) * 30))
    is_active = True


class ProjectFactory(DjangoModelFactory):
    class Meta:
        model = Project

    namespace = factory.Faker('word')
    name = factory.LazyAttribute(
        lambda project: project.namespace)
    description = factory.Faker('text')

    team = factory.SubFactory(TeamFactory)
    schedule = factory.SubFactory(ProjectScheduleFactory)


class IssueFactory(DjangoModelFactory):
    class Meta:
        model = Issue

    title = factory.Faker('sentence')
    description = factory.Faker('text')
    project = factory.SubFactory(ProjectFactory)
    author = factory.LazyAttribute(
        lambda issue: random.choice(issue.project.team.members.all()))
    assigned = factory.LazyAttribute(
        lambda issue: random.choice(issue.project.team.members.all()))
    status = factory.Iterator(IssueStatus.values)
    priority = factory.Iterator(IssuePriority.values)


class CommentFactory(DjangoModelFactory):
    class Meta:
        model = Comment

    issue = factory.SubFactory(IssueFactory)
    author = factory.Iterator(User.objects.all())
    text = factory.Faker('text')
    created_at = factory.Faker('date_time', tzinfo=None)
