from unittest.mock import Mock

from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.urls import reverse
from django.utils.text import slugify

from accounts.tests import UserFactory
from coaches.tests import CoachFactory
from divisions.tests import DivisionFactory
from escoresheet.utils.testing import BaseTestCase
from leagues.tests import LeagueFactory
from managers.tests import ManagerFactory
from players.tests import HockeyPlayerFactory
from referees.tests import RefereeFactory
from sports.exceptions import RoleDoesNotExistException, InvalidNumberOfRolesException
from sports.models import Sport, SportRegistration
from teams.tests import TeamFactory
from .factories.SportFactory import SportFactory
from .factories.SportRegistrationFactory import SportRegistrationFactory


class SportModelTests(BaseTestCase):
    # Slugs are auto generated from the name attribute, so the uniqueness of slugs makes sure names are also
    # unique for case insensitive ice Hockey and Ice Hockey will pass the uniqueness of the name field,
    # but won't pass uniqueness of slug field
    def test_unique_names_case_sensitive(self):
        Sport.objects.create(name='Ice Hockey')
        with self.assertRaises(IntegrityError):
            Sport.objects.create(name='Ice Hockey')

    def test_unique_slugs_case_insensitive(self):
        # Note trailing space, this prevents the unique constraint on name from failing this test. We want the slug
        # unique constraint to fail.
        SportFactory.create(name='ice Hockey ')
        with self.assertRaises(IntegrityError):
            SportFactory.create(name='ice hockey')

    def test_unique_names_case_insensitive(self):
        SportFactory.create(name='ice Hockey')
        with self.assertRaises(ValidationError):
            SportFactory.create(name='ice hockey')

    def test_slug_generation(self):
        ice_hockey = SportFactory.create(name='Ice hockey')
        self.assertEqual(ice_hockey.slug, slugify(ice_hockey.name))

    def test_default_ordering(self):
        ice_hockey = SportFactory(name='Ice Hockey')
        soccer = SportFactory(name='Soccer')
        baseball = SportFactory(name='Baseball')
        expected = [baseball, ice_hockey, soccer]
        self.assertListEqual(list(Sport.objects.all()), expected)

    def test_to_string(self):
        sport = SportFactory.build(name='Ice Hockey')
        self.assertEqual(str(sport), 'Ice Hockey')

    def test_name_converted_to_titlecase(self):
        sport = SportFactory.create(name='ice hockey')
        self.assertEqual(sport.name, 'Ice Hockey')


class SportRegistrationModelTests(BaseTestCase):
    def test_to_string(self):
        sr = SportRegistrationFactory()
        self.assertEqual(str(sr), '{email} - {sport}'.format(email=sr.user.email, sport=sr.sport.name))

    def test_absolute_url(self):
        ice_hockey = SportRegistrationFactory(sport__name='Ice Hockey')
        self.assertEqual(ice_hockey.get_absolute_url(),
                         reverse('sportregistrations:detail', kwargs={'pk': ice_hockey.pk}))

    def test_current_available_roles(self):
        self.assertListEqual(SportRegistration.ROLES, ['Player', 'Coach', 'Referee', 'Manager'])

    def test_set_roles_param_not_a_list(self):
        sr = SportRegistrationFactory()
        with self.assertRaises(AssertionError):
            sr.set_roles(('Player', 'Manager'))

    def test_set_roles_no_append(self):
        sr = SportRegistrationFactory()
        sr.set_roles(['Player', 'Manager'])
        self.assertEqual(sr.roles_mask, 9)

    def test_set_roles_append(self):
        sr = SportRegistrationFactory()
        sr.set_roles(['Player', 'Manager'])
        sr.set_roles(['Coach'], append=True)
        self.assertEqual(sr.roles_mask, 11)

    def test_set_roles_invalid_role(self):
        sr = SportRegistrationFactory()
        sr.set_roles(['Referee', 'Invalid'])
        self.assertEqual(sr.roles, ['Referee'])

    def test_set_roles_empty_list(self):
        sr = SportRegistrationFactory()
        sr.set_roles([])
        self.assertEqual(sr.roles_mask, 0)

    def test_roles_property(self):
        roles = ['Player', 'Manager']
        sr = SportRegistrationFactory()
        sr.set_roles(roles)
        self.assertEqual(sr.roles, roles)

    def test_has_role_true(self):
        roles = ['Player', 'Manager']
        sr = SportRegistrationFactory()
        sr.set_roles(roles)
        self.assertTrue(sr.has_role('Player'))
        self.assertTrue(sr.has_role('manager'))

    def test_has_role_false(self):
        roles = ['Coach', 'Manager']
        sr = SportRegistrationFactory()
        sr.set_roles(roles)
        self.assertFalse(sr.has_role('Player'))
        self.assertFalse(sr.has_role('InvalidRole'))

    def test_user_unique_with_sport(self):
        user = UserFactory(email='testing@example.com')
        sport = SportFactory(name='Ice Hockey')
        SportRegistrationFactory(user=user, sport=sport)
        with self.assertRaises(IntegrityError):
            SportRegistrationFactory(user=user, sport=sport)

    def test_get_related_role_objects_all_roles(self):
        user = UserFactory(email='testing@example.com')
        sport = SportFactory(name='Ice Hockey')
        league = LeagueFactory(full_name='Long Island Amateur Hockey League', sport=sport)
        division = DivisionFactory(name='Midget Minor AA', league=league)
        team = TeamFactory(name='Green Machine Icecats', division=division)
        sr = SportRegistrationFactory(user=user, sport=sport)
        sr.set_roles(SportRegistration.ROLES)

        m = ManagerFactory(user=user, team__division__league__sport=sport, is_active=False)
        p = HockeyPlayerFactory(user=user, sport=sport, is_active=False)
        c = CoachFactory(user=user, team__division__league__sport=sport, is_active=False)
        r = RefereeFactory(user=user, league__sport=sport, is_active=False)

        manager = [ManagerFactory(user=user, team=team)]
        player = [HockeyPlayerFactory(user=user, team=team, sport=sport)]
        coach = [CoachFactory(user=user, team=team)]
        referee = [RefereeFactory(user=user, league=league)]

        result = sr.get_related_role_objects()

        players = list(result.get('Player'))
        coaches = list(result.get('Coach'))
        referees = list(result.get('Referee'))
        managers = list(result.get('Manager'))

        self.assertListEqual(player, players)
        self.assertListEqual(coach, coaches)
        self.assertListEqual(referee, referees)
        self.assertListEqual(manager, managers)

        self.assertNotIn(m, managers)
        self.assertNotIn(p, players)
        self.assertNotIn(c, coaches)
        self.assertNotIn(r, referees)

    def test_get_related_role_objects_3_roles(self):
        user = UserFactory(email='testing@example.com')
        sport = SportFactory(name='Ice Hockey')
        league = LeagueFactory(full_name='Long Island Amateur Hockey League', sport=sport)
        division = DivisionFactory(name='Midget Minor AA', league=league)
        team = TeamFactory(name='Green Machine Icecats', division=division)
        sr = SportRegistrationFactory(user=user, sport=sport)
        sr.set_roles(['Player', 'Coach', 'Referee'])
        player = [HockeyPlayerFactory(user=user, team=team, sport=sport)]
        coach = [CoachFactory(user=user, team=team)]
        referee = [RefereeFactory(user=user, league=league)]
        result = sr.get_related_role_objects()

        self.assertListEqual(player, list(result.get('Player')))
        self.assertListEqual(coach, list(result.get('Coach')))
        self.assertListEqual(referee, list(result.get('Referee')))

    def test_get_related_role_objects_2_roles(self):
        user = UserFactory(email='testing@example.com')
        sport = SportFactory(name='Ice Hockey')
        league = LeagueFactory(full_name='Long Island Amateur Hockey League', sport=sport)
        division = DivisionFactory(name='Midget Minor AA', league=league)
        team = TeamFactory(name='Green Machine Icecats', division=division)
        sr = SportRegistrationFactory(user=user, sport=sport)
        sr.set_roles(['Player', 'Coach'])
        player = [HockeyPlayerFactory(user=user, team=team, sport=sport)]
        coach = [CoachFactory(user=user, team=team)]
        result = sr.get_related_role_objects()
        self.assertListEqual(player, list(result.get('Player')))
        self.assertListEqual(coach, list(result.get('Coach')))

    def test_get_related_role_objects_1_role(self):
        user = UserFactory(email='testing@example.com')
        sport = SportFactory(name='Ice Hockey')
        league = LeagueFactory(full_name='Long Island Amateur Hockey League', sport=sport)
        division = DivisionFactory(name='Midget Minor AA', league=league)
        team = TeamFactory(name='Green Machine Icecats', division=division)
        sr = SportRegistrationFactory(user=user, sport=sport)
        sr.set_roles(['Manager'])
        manager = [ManagerFactory(user=user, team=team)]
        result = sr.get_related_role_objects()
        self.assertListEqual(manager, list(result.get('Manager')))

    def test_get_related_role_objects_no_roles(self):
        user = UserFactory(email='testing@example.com')
        sport = SportFactory(name='Ice Hockey')
        sr = SportRegistrationFactory(user=user, sport=sport)
        sr.set_roles([])
        result = sr.get_related_role_objects()
        self.assertDictEqual({}, result)

    def test_remove_role_when_role_dne(self):
        user = UserFactory(email='testing@example.com')
        sport = SportFactory(name='Ice Hockey')
        sr = SportRegistrationFactory(user=user, sport=sport)
        sr.set_roles(['Player', 'Coach'])
        with self.assertRaises(RoleDoesNotExistException):
            sr.remove_role('Manager')
            sr.remove_role('Referee')

    def test_remove_role_when_last_role(self):
        user = UserFactory(email='testing@example.com')
        sport = SportFactory(name='Ice Hockey')
        sr = SportRegistrationFactory(user=user, sport=sport)
        sr.set_roles(['Player'])
        with self.assertRaises(InvalidNumberOfRolesException):
            sr.remove_role('Player')

    def test_remove_role_valid(self):
        user = UserFactory(email='testing@example.com')
        sport = SportFactory(name='Ice Hockey')
        sr = SportRegistrationFactory(user=user, sport=sport)
        roles = ['Player', 'Coach', 'Referee', 'Manager']
        sr.set_roles(roles)
        sr.remove_role('Coach')
        self.assertEqual(sorted(sr.roles), sorted(list(set(roles) - {'Coach'})))

    def test_remove_role_case_insensitive(self):
        user = UserFactory(email='testing@example.com')
        sport = SportFactory(name='Ice Hockey')
        sr = SportRegistrationFactory(user=user, sport=sport)
        roles = ['Player', 'Coach', 'Referee', 'Manager']
        sr.set_roles(roles)
        sr.remove_role('coach')
        self.assertEqual(sorted(sr.roles), sorted(list(set(roles) - {'Coach'})))

    def test_get_next_namespace_for_registration_no_roles_complete(self):
        sr = SportRegistrationFactory()
        sr.set_roles(['Player', 'Coach', 'Referee', 'Manager'])
        sr.save()
        self.assertEqual(sr.get_next_namespace_for_registration(), 'players')

    def test_get_next_namespace_for_registration_player_role_complete(self):
        sr = SportRegistrationFactory()
        sr.set_roles(['Player', 'Coach', 'Referee', 'Manager'])
        sr.save()
        sr.get_related_role_objects = Mock(return_value={'Player': Mock()})
        self.assertEqual(sr.get_next_namespace_for_registration(), 'coaches')

    def test_get_next_namespace_for_registration_player_coach_roles_complete(self):
        sr = SportRegistrationFactory()
        sr.set_roles(['Player', 'Coach', 'Referee', 'Manager'])
        sr.save()
        sr.get_related_role_objects = Mock(return_value={'Player': Mock(), 'Coach': Mock()})
        self.assertEqual(sr.get_next_namespace_for_registration(), 'referees')

    def test_get_next_namespace_for_registration_player_coach_referee_roles_complete(self):
        sr = SportRegistrationFactory()
        sr.set_roles(['Player', 'Coach', 'Referee', 'Manager'])
        sr.save()
        sr.get_related_role_objects = Mock(return_value={'Player': Mock(), 'Coach': Mock(), 'Referee': Mock()})
        self.assertEqual(sr.get_next_namespace_for_registration(), 'managers')

    def test_get_next_namespace_for_registration_all_roles_complete(self):
        sr = SportRegistrationFactory()
        sr.set_roles(['Player', 'Coach', 'Referee', 'Manager'])
        sr.save()
        sr.get_related_role_objects = Mock(
                return_value={'Player': Mock(), 'Coach': Mock(), 'Referee': Mock(), 'Manager': Mock()})
        self.assertIsNone(sr.get_next_namespace_for_registration())