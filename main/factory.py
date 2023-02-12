import factory
from factory.django import DjangoModelFactory

from main.models import *


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Faker('email')
    username = factory.Faker('first_name').lower() + \
        "_" + factory.Faker('last_name').lower()
    password = factory.PostGenerationMethodCall('set_password', 'f4keuse3r')
    bio = factory.Faker("sentence", nb_words=120)

    is_superuser = False
    is_staff = False
    is_active = True

    name = factory.Faker("first_name")
    address = factory.Faker("address")
    city = factory.Faker("city")
    country = factory.Faker("country")


class TeamFactory(DjangoModelFactory):
    class Meta:
        model = Team

    name = factory.Faker('company')
    members = factory.SubFactory(UserFactory)


class ProjectFactory(DjangoModelFactory):
    class Meta:
        model = Project

    name = factory.Faker('word')
    description = factory.Faker('text')

    team = factory.SubFactory(TeamFactory)
    start_date = factory.Faker('date_this_decade')
    end_date = factory.Faker('date_this_decade', end_date='+30d')
    is_active = True


class IssueFactory(DjangoModelFactory):
    class Meta:
        model = Issue

    title = factory.Faker('sentence')
    description = factory.Faker('text')
    project = factory.SubFactory(ProjectFactory)
    status = factory.Faker('word')
    priority = factory.Faker('word')


class CommentFactory(DjangoModelFactory):
    class Meta:
        model = Comment

    issue = factory.SubFactory(IssueFactory)
    text = factory.Faker('text')
    created_at = factory.Faker('date_time_this_decade', tzinfo=None)
