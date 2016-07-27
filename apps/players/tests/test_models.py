from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.test import TestCase

from accounts.tests.factories.UserFactory import UserFactory
from .factories.PlayerFactory import HockeyPlayerFactory


class PlayerModelTests(TestCase):
    """
    The tests in this class are testing the shared functionality the abstract Player class provides to subclasses.
    Subclasses shouldn't need to test the fields, properties, etc of the Player class as all of that is handled by this
    class

    NOTE: We can't create instances of PlayerFactory so just use any factory that is a subclass. In this case it is
    HockeyPlayerFactory. Nothing specific to HockeyPlayerFactory is being tested in this class.
    """

    def setUp(self):
        self.player = HockeyPlayerFactory()

    def test_league_property(self):
        self.assertEqual(self.player.league, self.player.team.division.league.full_name)

    def test_division_property(self):
        self.assertEqual(self.player.division, self.player.team.division.name)

    def test_max_jersey_number(self):
        with self.assertRaises(ValidationError, msg='Ensure this value is less than or equal to 99.'):
            HockeyPlayerFactory(jersey_number=100).full_clean()

    def test_min_jersey_number(self):
        with self.assertRaises(ValidationError, msg='Ensure this value is greater than or equal to 0.'):
            HockeyPlayerFactory(jersey_number=-1).full_clean()

    def test_to_string(self):
        self.assertEqual(str(self.player), self.player.user.get_full_name())

    def test_unique_with_sport(self):
        with self.assertRaises(IntegrityError,
                               msg='UNIQUE constraint failed: players_hockeyplayer.user_id, players_hockeyplayer.sport_id'):
            HockeyPlayerFactory(user=self.player.user, sport=self.player.sport)

    def test_unique_with_team(self):
        with self.assertRaises(IntegrityError,
                               msg='UNIQUE constraint failed: players_hockeyplayer.user_id, players_hockeyplayer.team_id'):
            HockeyPlayerFactory(user=self.player.user, team=self.player.team)

    def test_create_player_user_missing_player_role(self):
        user = UserFactory()
        user.userprofile.set_roles(['Referee'])
        player = HockeyPlayerFactory(user=user, league=self.player.team)
        with self.assertRaises(ValidationError,
                               msg='{full_name} does not have the player role assigned, please update their userprofile to include it'.format(
                                       full_name=user.get_full_name())):
            player.clean()


class HockeyPlayerModelTests(TestCase):
    def setUp(self):
        self.jersey_number = 35
        self.hockey_player = HockeyPlayerFactory(jersey_number=self.jersey_number)

    def test_duplicate_jersey_number(self):
        validation_msg = 'Please choose another number, {jersey_number} is currently unavailable for {team}'.format(
                jersey_number=self.jersey_number, team=self.hockey_player.team)
        with self.assertRaises(ValidationError, msg=validation_msg):
            HockeyPlayerFactory(team=self.hockey_player.team, jersey_number=self.jersey_number).full_clean()

    def test_different_jersey_numbers(self):
        jersey_number = 23
        another_hockey_player = HockeyPlayerFactory(team=self.hockey_player.team, jersey_number=jersey_number)
        self.assertEqual(another_hockey_player.jersey_number, jersey_number)

    def test_create_player_user_missing_player_role(self):
        user = UserFactory()
        user.userprofile.set_roles(['Referee'])
        player = HockeyPlayerFactory(user=user, league=self.hockey_player.team)
        with self.assertRaises(ValidationError,
                               msg='{full_name} does not have the player role assigned, please update their userprofile to include it'.format(
                                       full_name=user.get_full_name())):
            player.clean()
