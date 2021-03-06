from divisions.tests import DivisionFactory
from ayrabo.utils.testing import BaseTestCase
from leagues.tests import LeagueFactory
from managers.forms import ManagerForm
from sports.tests import SportFactory
from teams.tests import TeamFactory
from users.tests import UserFactory
from managers.tests import ManagerFactory


class ManagerFormTests(BaseTestCase):
    def setUp(self):
        self.sport = SportFactory(name='Ice Hockey')
        self.league = LeagueFactory(sport=self.sport, name='Long Island Amateur Hockey League')
        self.division = DivisionFactory(league=self.league, name='Midget Minor AA')
        self.form_cls = ManagerForm

    def test_teams_filtered_by_sport(self):
        TeamFactory.create_batch(5, division=self.division)
        team_different_sport = TeamFactory()

        form = self.form_cls(sport=self.sport)
        team_field = form.fields['team']
        self.assertNotIn(team_different_sport, team_field.queryset)

    def test_no_sport_kwarg(self):
        teams = TeamFactory.create_batch(2, division=self.division)
        team_different_sport = TeamFactory()
        teams.append(team_different_sport)

        form = self.form_cls()
        team_field = form.fields['team']
        self.assertTrue(set(teams).issubset(set(team_field.queryset)))

    def test_sets_fields_disabled(self):
        form = self.form_cls(read_only_fields=['team'])
        self.assertTrue(form.fields['team'].disabled)

    def test_teams_already_registered_for(self):
        """
        Teams already registered for should be excluded
        """
        user = UserFactory()
        teams = TeamFactory.create_batch(5)
        ManagerFactory(user=user, team=teams[0])
        form = self.form_cls(already_registered_for=[teams[0].id])
        team_field = form.fields['team']
        self.assertNotIn(teams[0], team_field.queryset)
