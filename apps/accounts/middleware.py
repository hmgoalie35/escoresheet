from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.utils.deprecation import  MiddlewareMixin

from sports.models import SportRegistration
from userprofiles.models import UserProfile


class AccountAndSportRegistrationCompleteMiddleware(MiddlewareMixin):
    """
    This middleware makes sure the user has a profile, has at least one sport registration and has no sport registrations
    that are not complete. Any requests to the urls in whitelisted_urls are allowed to pass through because a redirect
    loop would occur otherwise. It is the job of the view for the whitelisted_urls to make sure user's can't go from
    create_profile_url to create_sport_registration_url, etc.
    """

    def process_request(self, request):
        create_profile_url = reverse('profile:create')
        create_sport_registration_url = reverse('sport:create_sport_registration')
        finish_sport_registration_url = reverse('sport:finish_sport_registration')
        whitelisted_urls = [reverse('account_logout'), create_profile_url, create_sport_registration_url,
                            finish_sport_registration_url]

        # debug_toolbar wasn't working properly because of my custom middleware so let all debug_toolbar
        # requests through
        if '__debug__' in request.path:  # pragma: no cover
            return None

        # Do not apply this middleware to anonymous users, or for any request to a whitelisted url. A redirect
        # loop would occur if we didn't whitelist certain urls.
        if request.user.is_authenticated() and request.path not in whitelisted_urls:

            up = UserProfile.objects.filter(user=request.user)
            if not up.exists():
                request.session['is_user_currently_registering'] = True
                return redirect(create_profile_url)

            sport_registrations = SportRegistration.objects.filter(user=request.user)
            if not sport_registrations.exists():
                request.session['is_user_currently_registering'] = True
                return redirect(create_sport_registration_url)

            incomplete_sport_registrations = sport_registrations.filter(is_complete=False)
            if incomplete_sport_registrations.exists():
                request.session['is_user_currently_registering'] = True
                return redirect(finish_sport_registration_url)

            # At this point the user's account is "complete" and all sport registrations are complete
            request.session['is_user_currently_registering'] = False

            complete_sport_registrations = sport_registrations.filter(is_complete=True)
            user_roles = []
            for sport_reg in complete_sport_registrations:
                for role in sport_reg.roles:
                    user_roles.append(role) if role not in user_roles else None
            request.session['user_roles'] = user_roles
            return None

        return None
