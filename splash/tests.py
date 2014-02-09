"""
Splash - Tests
"""

from mock import patch

from django.conf import settings
from django.contrib.auth.models import AnonymousUser, User
from django.test import TestCase
from django.test.client import RequestFactory
from django.test.utils import override_settings

from splash.middleware import SplashMiddleware

import logging
log = logging.getLogger(__name__)

class SplashMiddlewareTestCase(TestCase):
    """
    Tests for the splash screen app middleware
    """

    def setUp(self):
        """
        Init
        """
        self.splash_middleware = SplashMiddleware()
        self.request_factory = RequestFactory()

    def build_request(self, username=None, cookies=None):
        """
        Builds a new request, associated with a user (anonymous by default)
        """
        request = self.request_factory.get('/somewhere')

        if username is None:
            request.user = AnonymousUser()
        else:
            request.user = User.objects.create_user(username, 'test@example.com', username)

        if cookies is not None:
            request.COOKIES = cookies

        return request

    def assert_redirect(self, response, redirect_url):
        """
        Check that the response redirects to `redirect_url`, without requiring client
        interface on the response object
        """
        self.assertTrue(response)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response['Location'], redirect_url)

    def test_feature_disabled(self):
        """
        No redirect when the feature is disabled
        """
        request = self.build_request()
        response = self.splash_middleware.process_request(request)
        self.assertEquals(response, None)

    @patch.dict(settings.FEATURES, {'ENABLE_SPLASH_SCREEN': True})
    def test_no_cookie(self):
        """
        No cookie present should redirect
        """
        request = self.build_request()
        response = self.splash_middleware.process_request(request)
        self.assert_redirect(response, 'http://edx.org')

    @patch.dict(settings.FEATURES, {'ENABLE_SPLASH_SCREEN': True})
    @override_settings(SPLASH_SCREEN_COOKIE_ALLOWED_VALUES=['ok1', 'ok2'])
    @override_settings(SPLASH_SCREEN_REDIRECT_URL='http://example.com')
    def test_wrong_cookie(self):
        """
        A cookie value different from the allowed ones should redirect
        """
        request = self.build_request(cookies={'edx_splash_screen': 'not ok'})
        response = self.splash_middleware.process_request(request)
        self.assert_redirect(response, 'http://example.com')

    @patch.dict(settings.FEATURES, {'ENABLE_SPLASH_SCREEN': True})
    @override_settings(SPLASH_SCREEN_COOKIE_ALLOWED_VALUES=['ok1', 'ok2'])
    @override_settings(SPLASH_SCREEN_REDIRECT_URL='http://example.com')
    def test_right_cookie(self):
        """
        A cookie value corresponding to one of the allowed ones should not redirect
        """
        request = self.build_request(cookies={'edx_splash_screen': 'ok2'})
        response = self.splash_middleware.process_request(request)
        self.assertEquals(response, None)

    @patch.dict(settings.FEATURES, {'ENABLE_SPLASH_SCREEN': True})
    @override_settings(SPLASH_SCREEN_COOKIE_NAME='othername')
    def test_wrong_cookie_different_cookie_name(self):
        """
        Different cookie name
        A cookie value different from the allowed ones should redirect
        """
        request = self.build_request(cookies={'othername': 'not ok'})
        response = self.splash_middleware.process_request(request)
        self.assert_redirect(response, 'http://edx.org')

    @patch.dict(settings.FEATURES, {'ENABLE_SPLASH_SCREEN': True})
    @override_settings(SPLASH_SCREEN_COOKIE_NAME='othername')
    def test_right_cookie_different_cookie_name(self):
        """
        Different cookie name
        A cookie value corresponding to one of the allowed ones should not redirect
        """
        request = self.build_request(cookies={'othername': 'seen'})
        response = self.splash_middleware.process_request(request)
        self.assertEquals(response, None)

    @patch.dict(settings.FEATURES, {'ENABLE_SPLASH_SCREEN': True})
    @override_settings(SPLASH_SCREEN_UNAFFECTED_USERS=['user1'])
    def test_not_unaffected_user(self):
        """
        Setting unaffected users should still redirect other users
        """
        request = self.build_request(username='user2')
        response = self.splash_middleware.process_request(request)
        self.assert_redirect(response, 'http://edx.org')

    @patch.dict(settings.FEATURES, {'ENABLE_SPLASH_SCREEN': True})
    @override_settings(SPLASH_SCREEN_UNAFFECTED_USERS=['user1'])
    def test_unaffected_user(self):
        """
        Unaffected users should never be redirected
        """
        request = self.build_request(username='user1')
        response = self.splash_middleware.process_request(request)
        self.assertEquals(response, None)

    @patch.dict(settings.FEATURES, {'ENABLE_SPLASH_SCREEN': True})
    @override_settings(SPLASH_SCREEN_REDIRECT_URL='http://testserver/somewhere')
    def test_redirect_to_current_url(self):
        """
        When the URL of the redirection is the same as the current URL,
        we shouldn't be redirected
        """
        request = self.build_request()
        response = self.splash_middleware.process_request(request)
        self.assertEquals(response, None)
