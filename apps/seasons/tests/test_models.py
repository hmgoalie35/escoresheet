import datetime

from django.core.exceptions import ValidationError
from django.urls import reverse
from django.db import IntegrityError

from divisions.tests import DivisionFactory
from escoresheet.utils.testing_utils import BaseTestCase
from leagues.tests import LeagueFactory
from seasons.models import Season, HockeySeasonRoster
from teams.tests import TeamFactory
from . import SeasonFactory, HockeySeasonRosterFactory


class SeasonModelTests(BaseTestCase):
    def test_to_string(self):
        season = SeasonFactory()
        self.assertEqual(str(season), '{start_year}-{end_year} Season'.format(start_year=season.start_date.year,
                                                                              end_year=season.end_date.year))

    def test_end_date_before_start_date(self):
        start_date = datetime.date(2016, 8, 15)
        end_date = start_date + datetime.timedelta(days=-365)
        with self.assertRaisesMessage(ValidationError, "The season's end date must be after the season's start date."):
            SeasonFactory(start_date=start_date, end_date=end_date).full_clean()

    def test_end_date_equal_to_start_date(self):
        start_date = datetime.date(2016, 8, 15)
        end_date = start_date
        with self.assertRaisesMessage(ValidationError, "The season's end date must be after the season's start date."):
            SeasonFactory(start_date=start_date, end_date=end_date).full_clean()

    def test_unique_together_start_date_league(self):
        league = LeagueFactory(full_name='Long Island Amateur Hockey League')
        start_date = datetime.date(2016, 8, 15)
        SeasonFactory(start_date=start_date, end_date=start_date + datetime.timedelta(days=365), league=league)
        with self.assertRaises(IntegrityError):
            SeasonFactory(start_date=start_date, end_date=start_date + datetime.timedelta(days=360), league=league)

    def test_unique_together_end_date_league(self):
        league = LeagueFactory(full_name='Long Island Amateur Hockey League')
        end_date = datetime.date(2016, 8, 15)
        SeasonFactory(start_date=datetime.date(2016, 8, 15), end_date=end_date, league=league)
        with self.assertRaises(IntegrityError):
            SeasonFactory(start_date=datetime.date(2016, 9, 23), end_date=end_date, league=league)

    def test_unique_for_year(self):
        start_date = datetime.date(2016, 8, 15)
        league = LeagueFactory(full_name='Long Island Amateur Hockey League')
        SeasonFactory(start_date=start_date, league=league)
        with self.assertRaisesMessage(ValidationError,
                                      "{'league': ['League must be unique for Start Date year.']}"):
            SeasonFactory(start_date=start_date + datetime.timedelta(days=30), league=league).full_clean()

    def test_default_ordering(self):
        start_date = datetime.date(2014, 8, 15)
        end_date = datetime.date(2015, 8, 15)
        league = LeagueFactory(full_name='Long Island Amateur Hockey League')
        seasons = []
        for i in range(3):
            start = start_date + datetime.timedelta(days=i * 365)
            end = end_date + datetime.timedelta(days=i * 365)
            season = SeasonFactory(start_date=start, end_date=end, league=league)
            seasons.append(season)
        self.assertListEqual(list(reversed(seasons)), list(Season.objects.all()))


class SeasonTeamM2MSignalTests(BaseTestCase):
    def setUp(self):
        self.liahl = LeagueFactory(full_name='Long Island Amateur Hockey League')
        self.nhl = LeagueFactory(full_name='National Hockey League')
        self.mites = DivisionFactory(name='Mites', league=self.liahl)
        self.midget_minor_aa = DivisionFactory(name='Midget Minor AA', league=self.liahl)
        self.pacific = DivisionFactory(name='Pacific Division', league=self.nhl)
        self.liahl_season = SeasonFactory(league=self.liahl)

    def test_add_teams_same_leagues_to_season_obj(self):
        """
        Not reverse, i.e. season_obj.teams.add(team_obj), so pk_set contains pks for team objects
        """
        # self.mites are a part of the same league...
        icecats = TeamFactory(division=self.mites, name='IceCats')
        sharks = TeamFactory(division=self.mites, name='San Jose Sharks')
        self.assertListEqual([], list(self.liahl_season.teams.all()))
        self.liahl_season.teams.add(icecats, sharks)
        self.assertListEqual([icecats, sharks], list(self.liahl_season.teams.all()))

    def test_add_teams_diff_leagues_to_season_obj(self):
        """
        Not reverse, i.e. season_obj.teams.add(team_obj), so pk_set contains pks for team objects
        """
        # Different divisions and leagues will be created by factory boy.
        icecats = TeamFactory(name='IceCats')
        sharks = TeamFactory(name='San Jose Sharks')
        self.assertListEqual([], list(self.liahl_season.teams.all()))
        self.liahl_season.teams.add(icecats, sharks)
        self.assertListEqual([], list(self.liahl_season.teams.all()))

    def test_add_season_diff_league_to_team_obj(self):
        """
        reverse, i.e. team_obj.season_set.add(season_obj), so pk_set contains pks for season objects
        """
        team = TeamFactory(division=self.mites, name='IceCats')
        s1 = SeasonFactory()
        s2 = SeasonFactory(league=self.nhl)
        self.assertListEqual([], list(team.season_set.all()))
        team.season_set.add(s1, s2)
        self.assertListEqual([], list(team.season_set.all()))

    def test_add_season_same_league_to_team_obj(self):
        """
        reverse, i.e. team_obj.season_set.add(season_obj), so pk_set contains pks for season objects
        """
        start_date = datetime.date(2016, 8, 15)
        end_date = start_date + datetime.timedelta(days=365)
        team = TeamFactory(division=self.mites, name='IceCats')
        s1 = SeasonFactory(league=self.liahl, start_date=start_date, end_date=end_date)
        s2 = SeasonFactory(league=self.liahl, start_date=start_date - datetime.timedelta(days=365),
                           end_date=end_date - datetime.timedelta(days=365))
        self.assertListEqual([], list(team.season_set.all()))
        team.season_set.add(s1, s2)
        self.assertListEqual([s1, s2], list(team.season_set.all()))

    def test_invalid_pks(self):
        self.liahl_season.teams.add(88)
        self.assertListEqual([], list(self.liahl_season.teams.all()))


class AbstractSeasonRosterModelTests(BaseTestCase):
    """
    We can't create an instance of AbstractSeasonRosterFactory so just default to the hockey factory
    """

    def test_to_string(self):
        season_roster = HockeySeasonRosterFactory()
        self.assertEqual(str(season_roster), '{team}-{division}: {season}'.format(team=season_roster.team,
                                                                                  division=season_roster.team.division,
                                                                                  season=season_roster.season))

    def test_roster_default_false(self):
        season_roster = HockeySeasonRosterFactory()
        self.assertFalse(season_roster.default)

    def test_default_ordering(self):
        rosters = []
        start_time = datetime.datetime.now()
        for i in range(5):
            rosters.append(HockeySeasonRosterFactory(created=start_time + datetime.timedelta(hours=i * 10)))

        self.assertListEqual(rosters, list(HockeySeasonRoster.objects.all()))

    def test_get_latest(self):
        rosters = []
        start_time = datetime.datetime.now()
        for i in range(5):
            rosters.append(HockeySeasonRosterFactory(created=start_time + datetime.timedelta(hours=i * 10)))

        latest_obj = rosters[len(rosters) - 1]
        self.assertEqual(latest_obj.pk, HockeySeasonRoster.objects.latest().pk)

    def test_get_absolute_url(self):
        season_roster = HockeySeasonRosterFactory()
        self.assertEqual(season_roster.get_absolute_url(), reverse('teams:season_rosters:update',
                                                                   kwargs={'team_pk': season_roster.team.pk,
                                                                           'pk': season_roster.pk}))


class HockeySeasonRosterModelTests(BaseTestCase):
    """
    Currently don't need any unit tests for this model
    """
    pass
