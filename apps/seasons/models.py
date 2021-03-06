import logging

from django.core.validators import ValidationError
from django.db import models
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone

from common.models import TimestampedModel
from seasons.managers import SeasonManager
from teams.models import Team
from users.models import User


logger = logging.getLogger()


class Season(TimestampedModel):
    """
    Represents a season which is used to organize games, etc. under. A league has many seasons. A season has many teams
    and a team has many seasons.
    """
    league = models.ForeignKey('leagues.League', unique_for_year='start_date', related_name='seasons',
                               on_delete=models.PROTECT)
    teams = models.ManyToManyField(Team, related_name='seasons')
    start_date = models.DateField(verbose_name='Start Date')
    end_date = models.DateField(verbose_name='End Date')

    objects = SeasonManager()

    def clean(self):
        if self.end_date and self.start_date and self.end_date <= self.start_date:
            raise ValidationError({
                'end_date': "The season's end date must be after the season's start date."
            })

    @property
    def is_past(self):
        return timezone.now().date() > self.end_date

    @property
    def is_current(self):
        return self.start_date <= timezone.now().date() <= self.end_date

    @property
    def is_future(self):
        return timezone.now().date() < self.start_date

    @property
    def league_detail_schedule_url(self):
        kwargs = {'slug': self.league.slug}
        if self.is_current:
            return reverse('leagues:schedule', kwargs=kwargs)
        kwargs.update({'season_pk': self.pk})
        return reverse('leagues:seasons:schedule', kwargs=kwargs)

    @property
    def league_detail_divisions_url(self):
        kwargs = {'slug': self.league.slug}
        if self.is_current:
            return reverse('leagues:divisions', kwargs=kwargs)
        kwargs.update({'season_pk': self.pk})
        return reverse('leagues:seasons:divisions', kwargs=kwargs)

    def __str__(self):
        return f'{self.start_date.year}-{self.end_date.year} Season'

    class Meta:
        ordering = ['-end_date', '-start_date']
        unique_together = (
            ('start_date', 'league'),
            ('end_date', 'league'),
        )


@receiver(m2m_changed, sender=Season.teams.through)
def validate_leagues(action, instance, pk_set, reverse, **kwargs):
    """
    This function validates that teams/seasons being added to the manytomany relationship between the two
    are in the same league, which also means they are in the same sport.
    This function does not raise a validation error, it simply removes the pks from pk_set if the pks aren't in the
    same league as instance so those pks are never added to the relationship by the RelatedManager
    A validation error is not raised because it would have to be caught, which is possible in the views, but the admin
    would break.

    This function is meant to work in conjunction with a model form, i.e. SeasonAdminForm that will actually display
    form errors if a user ever needs to manually add teams to a season.

    :param action: The type of m2m action that has occurred.
    :param instance: The object being acted upon (being updated). Can be of class Team or Season depending on reverse.
    :param pk_set: List of pks for objects being added
    :param reverse: True if team_obj.seasons was used, False if season_obj.teams was used
    :param kwargs: Other kwargs sent by the signal
    """
    if action == 'pre_add':
        if reverse:
            # i.e. team_obj.season_set.add(season_obj), so pk_set contains pks for season objects
            cls = Season
            error_msg = 'The {0} specified ({1} - pk={2}) is not configured for {3}'
        else:
            # i.e. season_obj.teams.add(team_obj), so pk_set contains pks for team objects
            cls = Team
            error_msg = 'The {0} specified ({1} - pk={2}) does not belong to {3}'

        errors = []
        pks = pk_set.copy()
        for pk in pks:
            qs = cls.objects.filter(pk=pk)
            if qs.exists():
                obj = qs.first()
                if reverse and obj.league_id != instance.division.league_id:
                    # Remove the pk from the set so it is not added
                    pk_set.remove(pk)
                    errors.append(
                        error_msg.format(cls.__name__.lower(), str(obj), obj.pk,
                                         instance.division.league.name))
                elif not reverse and obj.division.league_id != instance.league_id:
                    # Remove the pk from the set so it is not added
                    pk_set.remove(pk)
                    errors.append(error_msg.format(cls.__name__.lower(), str(obj), obj.pk, instance.league.name))
            else:
                logger.error('{cls} with pk {pk} does not exist'.format(cls=cls.__name__, pk=pk))
        if errors:
            logger.error('. '.join(errors))
            # raise ValidationError(errors)


class AbstractSeasonRoster(TimestampedModel):
    """
    Abstract base class used to represent a season roster. A season roster keeps tabs on all players for a team. This is
    different from a game roster because a game roster may not include all players in the season roster due to players
    being scratched, hurt, etc.
    Multiple season rosters can be created for a season/team.
    """
    name = models.CharField(verbose_name='Name', max_length=255)
    season = models.ForeignKey(Season, on_delete=models.PROTECT)
    team = models.ForeignKey(Team, related_name='season_rosters', on_delete=models.PROTECT)
    default = models.BooleanField(default=False, verbose_name='Default Season Roster')
    created_by = models.ForeignKey(User, null=True, related_name='season_rosters', verbose_name='Created By',
                                   on_delete=models.PROTECT)

    def can_update(self):
        return not self.season.is_past

    def clean(self):
        if hasattr(self, 'name') and hasattr(self, 'team') and hasattr(self, 'season'):
            model_cls = self.__class__
            qs = model_cls.objects.filter(name=self.name, team=self.team, season=self.season).exclude(pk=self.pk)
            if qs.exists():
                raise ValidationError({'name': 'Name must be unique for this team and season.'})

    def get_absolute_url(self):
        return reverse('teams:season_rosters:update', kwargs={'team_pk': self.team.pk, 'pk': self.pk})

    def __str__(self):
        return '{team}-{division}: {season}'.format(team=self.team, division=self.team.division, season=self.season)

    class Meta:
        abstract = True
        ordering = ['created']
        get_latest_by = 'created'


class HockeySeasonRoster(AbstractSeasonRoster):
    """
    Season roster for hockey
    """
    players = models.ManyToManyField('players.HockeyPlayer')

    def get_players(self):
        """
        Grab active players tied to this season roster.

        NOTE: Since this function is using .filter (via .active) it can't reuse objects prefetched
        through .prefetch_related. If we were using .all the prefetched objects would be used. There is probably a way
        around this...

        :return: Active players for this season roster, sorted by jersey number ascending.
        """
        return self.players.active().order_by('jersey_number').select_related('user')

    def clean(self):
        super().clean()
        if hasattr(self, 'team') and hasattr(self, 'season'):
            qs = HockeySeasonRoster.objects.filter(team=self.team,
                                                   season=self.season,
                                                   default=True).exclude(pk=self.pk)
            if self.default and qs.exists():
                raise ValidationError(
                    {'default': 'A default season roster for this team and season already exists.'})
