import datetime

from django import forms
from django.contrib.admin import widgets
from django.core.exceptions import ValidationError

from escoresheet.utils import set_fields_disabled
from escoresheet.utils.form_fields import SeasonModelChoiceField, TeamModelChoiceField
from players.models import HockeyPlayer
from teams.models import Team
from .models import Season, HockeySeasonRoster


class SeasonAdminForm(forms.ModelForm):
    class Meta:
        model = Season
        fields = ['league', 'start_date', 'end_date', 'teams']

    def clean(self):
        super().clean()
        league = self.cleaned_data.get('league', None)
        teams = self.cleaned_data.get('teams', [])
        errors = {'teams': []}
        if league and teams:
            for team in teams:
                if team.division.league_id != league.id:
                    errors['teams'].append(
                            'The team specified ({team_name}) does not belong to {league}'.format(
                                    team_name=team.name, league=league.full_name))

            if errors['teams']:
                raise ValidationError(errors)


class HockeySeasonRosterAdminForm(forms.ModelForm):
    """
    Custom admin form that optimizes db access for certain model fields.
    """

    sport_name = 'Hockey'

    season = SeasonModelChoiceField(
            queryset=Season.objects.filter(league__sport__name__icontains=sport_name).select_related(
                    'league'))
    team = TeamModelChoiceField(
            queryset=Team.objects.filter(division__league__sport__name__icontains=sport_name).select_related(
                    'division'))

    players = forms.ModelMultipleChoiceField(queryset=HockeyPlayer.objects.active().select_related('user'),
                                             widget=widgets.FilteredSelectMultiple(verbose_name='Players',
                                                                                   is_stacked=False))

    class Meta:
        model = HockeySeasonRoster
        fields = '__all__'


class HockeySeasonRosterCreateForm(forms.ModelForm):
    """
    Form for creating a hockey season roster that optimizes db access through select_related and excludes any
    seasons, teams, players that belong to different leagues or divisions
    """

    def __init__(self, *args, **kwargs):
        league = kwargs.pop('league', None)
        read_only_fields = kwargs.pop('read_only_fields', None)
        team = kwargs.pop('team', None)

        super(HockeySeasonRosterCreateForm, self).__init__(*args, **kwargs)

        if read_only_fields:
            set_fields_disabled(read_only_fields, self.fields)

        if league:
            today = datetime.date.today()
            self.fields['season'].queryset = Season.objects.filter(
                    league__full_name=league).exclude(end_date__lt=today).select_related('league')
            self.fields['team'].queryset = Team.objects.filter(
                    division__league__full_name=league).select_related('division')

        if team:
            self.fields['players'].queryset = HockeyPlayer.objects.active().filter(team=team).select_related('user')

    season = SeasonModelChoiceField(queryset=Season.objects.all().select_related('league'))
    players = forms.ModelMultipleChoiceField(queryset=HockeyPlayer.objects.active().select_related('user'))

    class Meta:
        model = HockeySeasonRoster
        fields = ['team', 'season', 'players', 'name', 'default']


class HockeySeasonRosterUpdateForm(forms.ModelForm):
    """
    Form for updating a hockey season roster that optimizes db access and excludes any players belonging to different
    teams
    """

    def __init__(self, *args, **kwargs):
        team = kwargs.pop('team', None)
        super(HockeySeasonRosterUpdateForm, self).__init__(*args, **kwargs)
        set_fields_disabled(['season'], self.fields)
        if team:
            self.fields['players'].queryset = HockeyPlayer.objects.active().filter(team=team).select_related('user')

    players = forms.ModelMultipleChoiceField(queryset=HockeyPlayer.objects.active().select_related('user'))

    class Meta:
        model = HockeySeasonRoster
        fields = ['season', 'players', 'name', 'default']