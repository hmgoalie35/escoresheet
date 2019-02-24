from django.core.management import BaseCommand
from waffle.models import Switch

from common.management.commands.utils import create_object, get_object, print_status


class Command(BaseCommand):
    help = 'Seeds waffle flags, switches, samples'

    def make_waffles(self, cls, waffles):
        for waffle in waffles:
            created = False
            # We are going to use `name` as the unique identifier to make sure duplicates aren't created.
            obj = get_object(cls, name=waffle.get('name'))
            if obj is None:
                obj = create_object(cls, **waffle)
                created = True
            print_status(self.stdout, obj, created)

    def handle(self, *args, **options):
        switches = [
            {
                'name': 'sport_registrations',
                'active': False,
                'note': 'Specifies if the user should be prompted to create sport registrations.'
            },
            {
                'name': 'player_update',
                'active': False,
                'note': 'Specifies if the user can update the players associated with their account.'
            },
            {
                'name': 'coach_update',
                'active': False,
                'note': 'Specifies if the user can update the coaches associated with their account.'
            }
        ]

        self.make_waffles(Switch, switches)