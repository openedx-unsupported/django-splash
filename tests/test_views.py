"""
Tests for views which will trigger the middleware automatically.
"""
from http import cookies

from django.contrib.auth import get_user_model
from django.test.testcases import TestCase
from django.urls import reverse

from splash.models import SplashConfig

PASSWORD = '1234'
User = get_user_model()


class ViewsTestCase(TestCase):
    """
    Test a views.
    """
    def setUp(self):
        super().setUp()
        self.home_url = reverse('home')

    def test_no_cookie(self):
        """
        No cookie present should redirect
        """
        SplashConfig(
            enabled=True,
        ).save()

        response = self.client.get(self.home_url)
        self.assert_redirect(response, 'http://edx.org')

    def test_right_cookie(self):
        """
        A cookie value corresponding to one of the allowed ones should not redirect
        """
        SplashConfig(
            enabled=True,
            cookie_allowed_values='ok1,ok2',
            redirect_url='http://example.com'
        ).save()

        self.client.cookies = cookies.SimpleCookie({'edx_splash_screen': 'ok1'})
        self.assert_no_redirect()

    def test_wrong_cookie_different_cookie_name(self):
        SplashConfig(
            enabled=True,
            cookie_name='othername',
            cookie_allowed_values='ok1,ok2',
        ).save()

        self.client.cookies = cookies.SimpleCookie({'othername': 'not'})
        response = self.client.get(self.home_url)
        self.assert_redirect(response, 'http://edx.org')

    def test_not_unaffected_user(self):
        """
        Setting unaffected users should still redirect other users
        """
        SplashConfig(
            enabled=True,
            unaffected_usernames='user1',
        ).save()

        user = User.objects.create_user('user2', 'test@example.com', PASSWORD)
        self.client.login(username=user.username, password=PASSWORD)
        response = self.client.get(self.home_url)
        self.assert_redirect(response, 'http://edx.org')

    def test_unaffected_user(self):
        """
        Unaffected users should never be redirected
        """
        SplashConfig(
            enabled=True,
            unaffected_usernames='user1',
        ).save()

        user = User.objects.create_user('user1', 'test@example.com', PASSWORD)
        self.client.login(username=user.username, password=PASSWORD)
        self.assert_no_redirect()

    def test_path_not_equal(self):
        """
        When the URL of the redirection not equal it will redirect.
        """
        SplashConfig(
            enabled=True,
            redirect_url='http://edx.org'
        ).save()

        response = self.client.get(self.home_url)
        self.assert_redirect(response, 'http://edx.org')

    def test_redirect_with_different_current_url(self):
        """
         When the URL of the redirection is the different from current URL,
         redirect it.
        """
        # to avoid the direct call and replace with test server doing this in two steps.
        SplashConfig(
            enabled=True,
            redirect_url='http://edx.org'
        ).save()

        response = self.client.get('http://testserver/home')
        self.assert_redirect(response, 'http://edx.org')

    def test_redirect_to_current_url(self):
        """
          When the URL of the redirection is the same as the current URL,
          we shouldn't be redirected
        """
        # to avoid the direct call and replace with test server doing this in two steps.
        SplashConfig(
            enabled=True,
            redirect_url='http://edx.org'
        ).save()

        # Above save method url triggers the validation error http://testserver/home
        # update this url to match the testserver url.

        SplashConfig.objects.filter(id=1).update(redirect_url='http://testserver/home')
        self.assert_no_redirect()

    def test_affected_path(self):
        """
        Affected paths should never be redirected - custom value
        """
        SplashConfig(
            enabled=True,
            unaffected_url_paths='/home,/my/url/',
        ).save()

        self.assert_no_redirect()

    def test_unaffected_wildcard_path(self):
        """
        Unaffected wildcard will be redirected
        """
        SplashConfig(
            enabled=True,
            unaffected_url_paths='/test1/*, /test2/*/after, /test3/*/before/*/after',
        ).save()

        # These paths match and should NOT redirect.
        response = self.client.get(self.home_url)
        self.assert_redirect(response, 'http://edx.org')

    def test_affected_wildcard_path(self):
        """
        Unaffected wildcard paths should never be redirected - custom value
        """
        SplashConfig(
            enabled=True,
            unaffected_url_paths='/test1/*, /test2/*/after, /test3/*/before/*/after',
        ).save()

        # These paths match and should NOT redirect.
        response = self.client.get(self.home_url)
        self.assert_redirect(response, 'http://edx.org')

    def assert_no_redirect(self):
        """
        Check that the response redirects to `redirect_url`, without requiring client
        interface on the response object
        """
        response = self.client.get(self.home_url)
        assert response.status_code == 200
        assert response.content.decode('utf-8') == 'ok'

    def assert_redirect(self, response, redirect_url):
        """
        Check that the response redirects to `redirect_url`, without requiring client
        interface on the response object
        """
        assert response
        assert response.status_code == 302
        assert response['Location'] == redirect_url
