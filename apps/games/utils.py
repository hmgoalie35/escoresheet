from managers.models import Manager
from scorekeepers.models import Scorekeeper


def get_game_list_context(user, sport):
    """
    Computes the manager objects for the given user and what teams the user is a manager. These values will be used
    for any view/template listing games.

    :param user: User to get managers for
    :param sport: Only include managers for this sport
    :return: managers for the given user and teams the user is a manager for
    """
    manager_objects_for_user = Manager.objects.active().filter(user=user)
    # It's more efficient to compute this once and use `in` rather than query to see if a manager exists for the user
    # and some team.
    team_ids_managed_by_user = manager_objects_for_user.filter(team__division__league__sport=sport).values_list(
        'team_id', flat=True)
    is_scorekeeper = Scorekeeper.objects.active().filter(user=user, sport=sport).exists()
    return {
        'team_ids_managed_by_user': team_ids_managed_by_user,
        'is_scorekeeper': is_scorekeeper,
        'sport': sport
    }


def optimize_games_query(qs):
    """
    Applies query optimizations to the QuerySet.

    In the future, we will need to selectively choose what fields to select related, prefetch related on because qs
    can be for HockeyGames, BaseballGames, etc and the fields may not be common among those model classes.

    :param qs: QuerySet of games
    :return: The QuerySet with any query optimizations applied
    """
    return qs.select_related(
        'home_team',
        'home_team__division',
        'away_team',
        'away_team__division',
        'type',
        'location',
        'team'
    )
