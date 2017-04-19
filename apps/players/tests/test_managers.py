from escoresheet.utils.testing_utils import BaseTestCase
from players.models import HockeyPlayer, BaseballPlayer, BasketballPlayer
from players.tests import HockeyPlayerFactory, BaseballPlayerFactory, BasketballPlayerFactory


class IsActiveManagerTests(BaseTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.p1 = HockeyPlayerFactory()
        cls.p2 = HockeyPlayerFactory(is_active=False)

        cls.b1 = BasketballPlayerFactory()
        cls.b2 = BasketballPlayerFactory(is_active=False)

        cls.o1 = BaseballPlayerFactory()
        cls.o2 = BaseballPlayerFactory(is_active=False)

    def test_excludes_inactive_hockey(self):
        self.assertNotIn(self.p2, HockeyPlayer.objects.all())

    def test_excludes_inactive_basketball(self):
        self.assertNotIn(self.b2, BasketballPlayer.objects.all())

    def test_excludes_inactive_baseball(self):
        self.assertNotIn(self.o2, BaseballPlayer.objects.all())
