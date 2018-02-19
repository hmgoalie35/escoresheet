import datetime

import pytz
from django.utils import timezone

from common.tests import GenericChoiceFactory
from divisions.tests import DivisionFactory
from ayrabo.utils.testing import BaseTestCase
from games.forms import HockeyGameCreateForm
from leagues.tests import LeagueFactory
from seasons.tests import SeasonFactory
from sports.tests import SportFactory
from teams.tests import TeamFactory


# Tests for the .clean method can be found in test_views
class AbstractGameCreateFormTests(BaseTestCase):
    """
    Testing the abstract class via `HockeyGameCreateForm`.
    """

    def setUp(self):
        self.form_cls = HockeyGameCreateForm

        self.ice_hockey = SportFactory(name='Ice Hockey')
        self.liahl = LeagueFactory(full_name='Long Island Amateur Hockey League', sport=self.ice_hockey)
        self.mm_aa = DivisionFactory(name='Midget Minor AA', league=self.liahl)
        self.t1 = TeamFactory(id=1, division=self.mm_aa)
        self.t2 = TeamFactory(id=2, division=self.mm_aa)
        self.t3 = TeamFactory(id=3, division=self.mm_aa)
        self.t4 = TeamFactory(id=4, name='Green Machine IceCats', division=self.mm_aa)

        self.squirt = DivisionFactory(name='Squirt', league=self.liahl)
        self.squirt_teams = TeamFactory.create_batch(3, division=self.squirt)

        GenericChoiceFactory(id=1, short_value='exhibition', long_value='Exhibition', type='game_type',
                             content_object=self.ice_hockey)
        GenericChoiceFactory(id=2, short_value='2', long_value='2', type='game_point_value',
                             content_object=self.ice_hockey)

    def test_teams_filtered_by_division(self):
        form = self.form_cls(team=self.t4)
        home_team_qs = form.fields['home_team'].queryset
        away_team_qs = form.fields['away_team'].queryset
        self.assertListEqual(sorted(list(home_team_qs.values_list('id', flat=True))), [1, 2, 3, 4])
        self.assertListEqual(sorted(list(away_team_qs.values_list('id', flat=True))), [1, 2, 3, 4])

    def test_generic_choice_filtered_by_game_type(self):
        form = self.form_cls(team=self.t4)
        game_type_qs = form.fields['type'].queryset
        self.assertListEqual(list(game_type_qs.values_list('id', flat=True)), [1])

    def test_generic_choice_filtered_by_game_point_value(self):
        form = self.form_cls(team=self.t4)
        point_value_qs = form.fields['point_value'].queryset
        self.assertListEqual(list(point_value_qs.values_list('id', flat=True)), [2])

    def test_season_filtered_by_league(self):
        SeasonFactory(id=1, league=self.liahl)
        SeasonFactory(id=2, league=self.liahl, start_date=datetime.date(month=12, day=26, year=2000))
        SeasonFactory(id=3)
        form = self.form_cls(team=self.t4)
        season_qs = form.fields['season'].queryset
        self.assertListEqual(list(season_qs.values_list('id', flat=True)), [1, 2])

    def test_initial_timezone(self):
        timezone.activate(pytz.timezone('US/Eastern'))
        form = self.form_cls(team=self.t4)
        self.assertEqual(form.fields['timezone'].initial, 'US/Eastern')