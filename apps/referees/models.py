from django.db import models

from common import managers
from common.models import TimestampedModel
from leagues.models import League


class Referee(TimestampedModel):
    """
    Represents a referee in the system. A user can have many Referee objects related to them provided each referee
    object is for a different league.
    TLDR; A user can be a referee for multiple leagues and a new referee object is created for each league.
    """
    user = models.ForeignKey('users.User', related_name='referees', on_delete=models.PROTECT)
    league = models.ForeignKey(League, on_delete=models.PROTECT)
    is_active = models.BooleanField(default=True, verbose_name='Is Active')

    objects = managers.ActiveManager()

    class Meta:
        unique_together = (('user', 'league'),)

    def __str__(self):
        return 'Referee {full_name}'.format(full_name=self.user.get_full_name())
