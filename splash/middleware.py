"""
Splash screen - Middleware
"""
import logging
import re

from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin

from .models import SplashConfig

log = logging.getLogger(__name__)


class SplashMiddleware(MiddlewareMixin):
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
            return None

        # Some URLs should never be redirected
        path_info = request.path_info
        for unaffected_path in config.unaffected_url_paths_list:
            if self.path_matches(path_info, unaffected_path):
                return None

        # Some users should never be redirected
        if request.user.username in config.unaffected_usernames_list:
            return None

        cookie_value = request.COOKIES.get(config.cookie_name)
        if (cookie_value not in config.cookie_allowed_values_list and
                request.build_absolute_uri() != config.redirect_url):
            return redirect(config.redirect_url)
        return None

    def path_matches(self, path, pattern):
        """
        Determine whether `path` matches the `pattern`.

        `pattern` may include wildcards (*) which represent a sequence of
        zero or more arbitrary characters.
        """
        matches = False

        if path == pattern:
            matches = True
        elif '*' in pattern:
            pattern = re.escape(pattern).replace('\\*', '.*')
            if re.match(pattern + '$', path):
                matches = True

        return matches


    def __call__(self, request):
        """
        This adds compatibility for django 2.2
        for more details check
        https://docs.djangoproject.com/en/2.0/topics/http/middleware/#upgrading-middleware
        """
        response = self.process_request(request)
        return response
