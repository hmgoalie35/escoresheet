from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView

from ayrabo.utils.mixins import HandleSportNotConfiguredMixin
from games.mappings import get_game_model_cls
from games.utils import get_game_list_context
from leagues.models import League
from seasons.models import Season


class LeagueDetailView(LoginRequiredMixin, HandleSportNotConfiguredMixin, DetailView):
    """
    League detail view that defaults to displaying the league's schedule for the current season
    """
    template_name = 'leagues/league_detail_schedule.html'
    context_object_name = 'league'
    queryset = League.objects.select_related('sport')

    def _get_games(self, sport, season):
        model_cls = get_game_model_cls(sport)
        return model_cls.objects.select_related(
            'home_team', 'home_team__division', 'away_team', 'away_team__division', 'type', 'location', 'season', 'team'
        ).filter(season=season)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        league = self.object
        sport = league.sport
        current_season = Season.objects.get_current(league=league)
        game_list_context = get_game_list_context(user, sport)
        games = self._get_games(sport, current_season)
        context.update({
            'active_tab': 'schedule',
            'season': current_season,
            'games': games,
        })
        context.update(game_list_context)
        return context
