import factory
from factory import django, Faker

from accounts.tests import UserFactory
from players import models
from sports.tests import SportFactory
from teams.tests import TeamFactory


class PlayerFactory(django.DjangoModelFactory):
    class Meta:
        model = models.AbstractPlayer
        abstract = True

    user = factory.SubFactory(UserFactory)
    sport = factory.SubFactory(SportFactory)
    team = factory.SubFactory(TeamFactory)
    jersey_number = Faker('random_int', min=0, max=99)
    is_active = True


class HockeyPlayerFactory(PlayerFactory):
    class Meta:
        model = models.HockeyPlayer

    sport = factory.SubFactory(SportFactory)
    position = Faker('random_element', elements=[position[0] for position in models.HockeyPlayer.POSITIONS])
    handedness = Faker('random_element', elements=[handedness[0] for handedness in models.HockeyPlayer.HANDEDNESS])


class BaseballPlayerFactory(PlayerFactory):
    class Meta:
        model = models.BaseballPlayer

    sport = factory.SubFactory(SportFactory)
    position = Faker('random_element', elements=[position[0] for position in models.BaseballPlayer.POSITIONS])
    catches = Faker('random_element', elements=[catches[0] for catches in models.BaseballPlayer.CATCHES])
    bats = Faker('random_element', elements=[bats[0] for bats in models.BaseballPlayer.BATS])


class BasketballPlayerFactory(PlayerFactory):
    class Meta:
        model = models.BasketballPlayer

    sport = factory.SubFactory(SportFactory)
    position = Faker('random_element', elements=[position[0] for position in models.BasketballPlayer.POSITIONS])
    shoots = Faker('random_element', elements=[shoots[0] for shoots in models.BasketballPlayer.SHOOTS])