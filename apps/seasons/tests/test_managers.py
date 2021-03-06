from datetime import datetime, timedelta
from unittest import mock

from ayrabo.utils.testing import BaseTestCase
from leagues.tests import LeagueFactory
from seasons.models import Season
from seasons.tests import SeasonFactory
from sports.tests import SportFactory


class SeasonManagerTests(BaseTestCase):
    def setUp(self):
        self.ice_hockey = SportFactory(name='Ice Hockey')
        self.liahl = LeagueFactory(sport=self.ice_hockey, name='Long Island Amateur Hockey League')
        self.past_past_start_date = datetime(2015, 9, 4)
        self.past_start_date = datetime(2016, 9, 4)
        self.start_date = datetime(2017, 9, 4)
        self.end_date = datetime(2018, 9, 4)
        self.future_end_date = datetime(2019, 9, 4)
        # 2015-2016 season
        self.past_past_season = SeasonFactory(
            league=self.liahl, start_date=self.past_past_start_date, end_date=self.past_start_date
        )
        # 2016-2017 season
        self.past_season = SeasonFactory(league=self.liahl, start_date=self.past_start_date, end_date=self.start_date)
        # 2017-2018 season
        self.current_season = SeasonFactory(league=self.liahl, start_date=self.start_date, end_date=self.end_date)
        # 2018-2019 season
        self.future_season = SeasonFactory(league=self.liahl, start_date=self.end_date, end_date=self.future_end_date)

    def _get_current_season(self):
        return Season.objects.get_current(league=self.liahl)

    def _assert_current_season(self):
        season = self._get_current_season()
        self.assertEqual(season.id, self.current_season.id)

    def test_get_for_league(self):
        nhl = LeagueFactory(sport=self.ice_hockey, name='National Hockey League')
        SeasonFactory(league=nhl)

        seasons = Season.objects.get_for_league(league=self.liahl)
        self.assertListEqual(
            list(seasons),
            [self.future_season, self.current_season, self.past_season, self.past_past_season]
        )

    @mock.patch('django.utils.timezone.now')
    def test_get_current_today_before_season_start(self, mock_now):
        mock_now.return_value = self.start_date - timedelta(days=60)
        self.assertEqual(self._get_current_season().id, self.past_season.id)

    @mock.patch('django.utils.timezone.now')
    def test_get_current_today_same_as_season_start(self, mock_now):
        mock_now.return_value = self.start_date
        self._assert_current_season()

    @mock.patch('django.utils.timezone.now')
    def test_get_current_today_after_season_start(self, mock_now):
        mock_now.return_value = self.start_date + timedelta(days=60)
        self._assert_current_season()

    @mock.patch('django.utils.timezone.now')
    def test_get_current_today_past_new_year(self, mock_now):
        mock_now.return_value = datetime(2018, 1, 1)
        self._assert_current_season()

    @mock.patch('django.utils.timezone.now')
    def test_get_current_today_same_as_season_end(self, mock_now):
        mock_now.return_value = self.end_date
        self.assertEqual(self._get_current_season().id, self.future_season.id)

    @mock.patch('django.utils.timezone.now')
    def test_get_current_today_after_season_end(self, mock_now):
        mock_now.return_value = self.end_date + timedelta(days=60)
        self.assertEqual(self._get_current_season().id, self.future_season.id)

    @mock.patch('django.utils.timezone.now')
    def test_get_past(self, mock_now):
        mock_now.return_value = self.end_date
        past_seasons = Season.objects.get_past(league=self.liahl)
        self.assertListEqual(list(past_seasons), [self.past_season, self.past_past_season])
