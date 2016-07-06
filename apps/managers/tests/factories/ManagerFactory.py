import factory
from factory import django

from accounts.tests.factories.UserFactory import UserFactory
from managers.models import Manager
from teams.tests.factories.TeamFactory import TeamFactory


class ManagerFactory(django.DjangoModelFactory):
    class Meta:
        model = Manager

    user = factory.SubFactory(UserFactory)
    team = factory.SubFactory(TeamFactory)
