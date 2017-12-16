import datetime

import pytz

from common.tests import GenericChoiceFactory
from escoresheet.utils.testing import BaseTestCase
from games.tests import HockeyGameFactory
from sports.tests import SportFactory
from teams.tests import TeamFactory


class AbstractGameModelTests(BaseTestCase):
    """
    Testing this model via `HockeyGame`
    """

    def setUp(self):
        self.sport = SportFactory()
        self.point_value = GenericChoiceFactory(content_object=self.sport,
                                                short_value='1',
                                                long_value='1',
                                                type='game_point_value')
        self.game_type = GenericChoiceFactory(content_object=self.sport,
                                              short_value='exhibition',
                                              long_value='Exhibition',
                                              type='game_type')
        self.tz_name = 'America/New_York'
        home_team = TeamFactory(name='New York Islanders')
        away_team = TeamFactory(name='New York Rangers', division=home_team.division)
        # 12/16/2017 @ 07:00PM
        self.start = pytz.timezone('UTC').localize(datetime.datetime(year=2017, month=12, day=16, hour=19))
        self.game = HockeyGameFactory(type=self.game_type, point_value=self.point_value, start=self.start,
                                      timezone=self.tz_name, home_team=home_team, away_team=away_team)

    def test_to_string(self):
        self.assertEqual(str(self.game), '12/16/2017 02:00 PM EST New York Islanders vs. New York Rangers')

    def test_datetime_localized(self):
        # 12/16/2017 @ 02:00PM
        expected = pytz.timezone(self.tz_name).localize(datetime.datetime(year=2017, month=12, day=16, hour=14))
        self.assertEqual(self.game.datetime_localized(self.game.start), expected)

    def test_datetime_formatted(self):
        self.assertEqual(self.game.datetime_formatted(self.game.start), '12/16/2017 02:00 PM EST')
