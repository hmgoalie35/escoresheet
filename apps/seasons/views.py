from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views import generic
from django.views.generic import DetailView

from ayrabo.utils import chunk
from ayrabo.utils.exceptions import SportNotConfiguredException
from ayrabo.utils.mixins import HandleSportNotConfiguredMixin, HasPermissionMixin
from divisions.models import Division
from games.mappings import get_game_model_cls
from games.utils import get_game_list_context, optimize_games_query
from leagues.models import League
from managers.models import Manager
from seasons.models import Season
from teams.models import Team
from .forms import HockeySeasonRosterCreateUpdateForm
from .models import HockeySeasonRoster


SPORT_FORM_MAPPINGS = {
    'Ice Hockey': HockeySeasonRosterCreateUpdateForm
}

SPORT_MODEL_MAPPINGS = {
    'Ice Hockey': HockeySeasonRoster
}


class SeasonRosterCreateView(LoginRequiredMixin,
                             HandleSportNotConfiguredMixin,
                             HasPermissionMixin,
                             SuccessMessageMixin,
                             generic.CreateView):
    template_name = 'seasons/season_roster_create.html'
    success_message = 'Your season roster has been created.'

    def _get_team(self):
        if hasattr(self, 'team'):
            return self.team
        self.team = get_object_or_404(
            Team.objects.select_related('division', 'division__league', 'division__league__sport'),
            pk=self.kwargs.get('team_pk')
        )
        self.sport = self.team.division.league.sport
        return self.team

    def has_permission_func(self):
        user = self.request.user
        team = self._get_team()
        return Manager.objects.active().filter(user=user, team=team).exists()

    def get_form_class(self):
        form_cls = SPORT_FORM_MAPPINGS.get(self.sport.name)
        if form_cls is None:
            raise SportNotConfiguredException(self.sport)
        return form_cls

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        instance = self.get_form_class().Meta.model(team=self.team, created_by=self.request.user)

        form_kwargs['team'] = self.team
        form_kwargs['instance'] = instance
        return form_kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['team'] = self.team
        return context

    def get_success_url(self):
        return reverse('sports:dashboard', kwargs={'slug': self.sport.slug})

    def get(self, request, *args, **kwargs):
        self._get_team()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self._get_team()
        return super().post(request, *args, **kwargs)


class SeasonRosterListView(LoginRequiredMixin, HandleSportNotConfiguredMixin, HasPermissionMixin, generic.ListView):
    template_name = 'seasons/season_roster_list.html'
    context_object_name = 'season_rosters'

    def _get_team(self):
        if hasattr(self, 'team'):
            return self.team
        self.team = get_object_or_404(
            Team.objects.select_related('division', 'division__league', 'division__league__sport'),
            pk=self.kwargs.get('team_pk')
        )
        self.sport = self.team.division.league.sport
        return self.team

    def _get_players(self, season_roster):
        return season_roster.players.active().order_by('jersey_number').select_related('user')

    def has_permission_func(self):
        user = self.request.user
        team = self._get_team()
        return Manager.objects.active().filter(user=user, team=team).exists()

    def get_queryset(self):
        season_roster_cls = SPORT_MODEL_MAPPINGS.get(self.sport.name)
        if season_roster_cls is None:
            raise SportNotConfiguredException(self.sport)
        # Datatables is ordering by season, desc. It seems to be doing a lexicographical sort so it works, but isn't
        # the best way to sort season rosters.
        return season_roster_cls.objects.filter(team=self.team).select_related(
            'season', 'team', 'team__division', 'created_by')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        season_rosters = context.pop(self.context_object_name)
        context['season_rosters'] = {roster: self._get_players(roster) for roster in season_rosters}
        context['team'] = self.team
        return context

    def get(self, request, *args, **kwargs):
        self._get_team()
        return super().get(request, *args, **kwargs)


class SeasonRosterUpdateView(LoginRequiredMixin,
                             HandleSportNotConfiguredMixin,
                             HasPermissionMixin,
                             SuccessMessageMixin,
                             generic.UpdateView):
    template_name = 'seasons/season_roster_update.html'
    context_object_name = 'season_roster'
    success_message = 'Your season roster has been updated.'

    def _get_team(self):
        if hasattr(self, 'team'):
            return self.team
        self.team = get_object_or_404(
            Team.objects.select_related('division', 'division__league', 'division__league__sport'),
            pk=self.kwargs.get('team_pk')
        )
        self.sport = self.team.division.league.sport
        return self.team

    def has_permission_func(self):
        user = self.request.user
        team = self._get_team()
        season_roster = self.get_object()
        return team.id == season_roster.team_id and Manager.objects.active().filter(user=user, team=team).exists()

    def get_form_class(self):
        form_cls = SPORT_FORM_MAPPINGS.get(self.sport.name)
        if form_cls is None:
            raise SportNotConfiguredException(self.sport)
        return form_cls

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        form_kwargs['disable'] = ['season']
        return form_kwargs

    def get_object(self, queryset=None):
        model_cls = SPORT_MODEL_MAPPINGS.get(self.sport.name)
        if model_cls is None:
            raise SportNotConfiguredException(self.sport)
        pk = self.kwargs.get(self.pk_url_kwarg, None)
        return get_object_or_404(model_cls.objects.select_related('season', 'team'), pk=pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['team'] = self.team
        return context

    def form_valid(self, form):
        if form.has_changed():
            return super().form_valid(form)
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse('teams:season_rosters:list', kwargs={'team_pk': self.team.pk})

    def get(self, request, *args, **kwargs):
        self._get_team()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self._get_team()
        return super().post(request, *args, **kwargs)


class AbstractSeasonDetailView(LoginRequiredMixin, HandleSportNotConfiguredMixin, DetailView):
    context_object_name = 'season'
    pk_url_kwarg = 'season_pk'

    def _get_league(self):
        """
        We can prevent the need for a select_related call (and therefore an extra query) in get_queryset by using
        `self.league` over `season.league`.
        """
        if hasattr(self, 'league'):
            return self.league
        self.league = get_object_or_404(League, slug=self.kwargs.get('slug'))
        return self.league

    def get_queryset(self):
        league = self._get_league()
        # Make sure the season belongs to the league taken from the slug in the url.
        return Season.objects.filter(league=league)

    def get_object(self, queryset=None):
        if hasattr(self, 'object'):
            return self.object
        self.object = super().get_object(queryset)
        return self.object

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        past_seasons = Season.objects.get_past(league=self.league)
        context.update({
            'past_seasons': past_seasons,
            'league': self.league,
        })
        return context


class SeasonScheduleDetailView(AbstractSeasonDetailView):
    template_name = 'seasons/season_detail_schedule.html'

    def _get_games(self, sport, season):
        model_cls = get_game_model_cls(sport)
        # Seasons are tied to leagues so we don't need to exclude games for other leagues
        qs = model_cls.objects.filter(season=season)
        return optimize_games_query(qs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        league = context.get('league')
        season = context.get('season')
        user = self.request.user
        sport = league.sport
        game_list_context = get_game_list_context(user, sport)
        games = self._get_games(sport, season)
        context.update({
            'active_tab': 'schedule',
            'season': season,
            'games': games,
        })
        context.update(game_list_context)
        return context


class SeasonDivisionsDetailView(AbstractSeasonDetailView):
    template_name = 'seasons/season_detail_divisions.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        season = context.get('season')
        teams = season.teams.all()
        division_ids = teams.values_list('division', flat=True)
        divisions = Division.objects.prefetch_related('teams').filter(id__in=division_ids)
        per_row = 4
        # The generator gets exhausted after the template loops over the chunked divisions so using it anywhere else
        # resulted in an empty array. Convert to a list here to prevent this problem.
        chunked_divisions = list(chunk(divisions, per_row))
        context.update({
            'active_tab': 'divisions',
            'chunked_divisions': chunked_divisions,
        })
        return context
