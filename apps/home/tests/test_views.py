from ayrabo.utils.testing import BaseTestCase
from sports.tests import SportRegistrationFactory
from users.tests import UserFactory


class HomeViewTests(BaseTestCase):
    url = 'home'

    def setUp(self):
        self.email = 'user@ayrabo.com'
        self.password = 'myweakpassword'

    def test_unauthenticated(self):
        response = self.client.get(self.format_url())
        self.assert_200(response)
        self.assertTemplateUsed(response, 'home/anonymous_home.html')

    def test_authenticated_no_user_profile(self):
        user = UserFactory(email=self.email, password=self.password)
        SportRegistrationFactory(user=user)
        self.login(email=self.email, password=self.password)

        response = self.client.get(self.format_url())

        self.assert_200(response)
        self.assertTemplateUsed(response, 'home/authenticated_home.html')


class AboutUsViewTests(BaseTestCase):
    url = 'about_us'

    def test_get(self):
        response = self.client.get(self.format_url())

        self.assert_200(response)
        self.assertTemplateUsed(response, 'home/about_us.html')


class ContactUsViewTests(BaseTestCase):
    url = 'contact_us'

    def test_get(self):
        response = self.client.get(self.format_url())

        self.assert_200(response)
        self.assertTemplateUsed(response, 'home/contact_us.html')

        context = response.context

        self.assertDictEqual(context.get('support_contact'), {
            'name': 'Harris Pittinsky',
            'email': 'support@ayrabo.com'
        })
