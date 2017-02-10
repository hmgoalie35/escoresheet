import factory
import factory.fuzzy
from factory import django, post_generation

from leagues.models import League
from sports.tests import SportFactory


class LeagueFactory(django.DjangoModelFactory):
    class Meta:
        model = League

    full_name = factory.sequence(lambda x: 'National Sport_{x} League'.format(x=x))
    # abbreviated named is autogenerated via overridden .clean method on the model.
    sport = factory.SubFactory(SportFactory)

    @post_generation
    def full_clean(self, obj, extracted, **kwargs):
        self.full_clean(exclude=['slug', 'abbreviated_name'])
