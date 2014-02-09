"""
Splash screen - Middleware
"""
import logging

from django.conf import settings
from django.shortcuts import redirect

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
        if not settings.FEATURES.get('ENABLE_SPLASH_SCREEN'):
            return

        # Some users should never be redirected
        if request.user.username in settings.SPLASH_SCREEN_UNAFFECTED_USERS:
            return

        cookie_value = request.COOKIES.get(settings.SPLASH_SCREEN_COOKIE_NAME)
        if cookie_value not in settings.SPLASH_SCREEN_COOKIE_ALLOWED_VALUES \
                and request.build_absolute_uri() != settings.SPLASH_SCREEN_REDIRECT_URL:
            return redirect(settings.SPLASH_SCREEN_REDIRECT_URL)
