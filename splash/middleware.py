"""
Splash screen - Middleware
"""
import logging

from django.shortcuts import redirect

from models import SplashConfig

log = logging.getLogger(__name__)


class SplashMiddleware(object):
    """
    Checks incoming requests, to redirect users to a configured splash screen URL
    if they don't have the proper cookie set

    This can be used to display a small marketing landing page, protect an
    alpha website from the public eye, make an announcement, etc.
    """

    def process_request(self, request):
        """
        Determine if the user needs to be redirected
        """
        config = SplashConfig.current()
        if not config.enabled:
            return

        # Some users should never be redirected
        if request.user.username in config.unaffected_usernames_list:
            return

        cookie_value = request.COOKIES.get(config.cookie_name)
        if (cookie_value not in config.cookie_allowed_values_list and
                request.build_absolute_uri() != config.redirect_url):
            return redirect(config.redirect_url)
