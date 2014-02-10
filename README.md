Splash screen middleware for Django apps
========================================

Checks incoming requests, to redirect users to a configured splash screen URL
if they don't have the proper cookie set. This can be used to display a small
marketing landing page, protect an alpha website from the public eye, make an
announcement, etc.

Meant to be used with https://github.com/edx/edx-platform/

### Installation

Add the following configuration variables:

```python
############################### Splash screen ####################################

SPLASH_SCREEN_COOKIE_NAME = 'edx_splash_screen'

# The user cookie value must match one of the values to not be redirected to the
# splash screen URL
SPLASH_SCREEN_COOKIE_ALLOWED_VALUES = ['seen']

# Users which should never be redirected (usernames)
SPLASH_SCREEN_UNAFFECTED_USERS = []

# The URL the users should be redirected to when they don't have the right cookie
SPLASH_SCREEN_REDIRECT_URL = 'http://edx.org'
```

Add the middleware to the configuration:

```python
MIDDLEWARE_CLASSES = (
    ...
    'splash.middleware.SplashMiddleware',
)
```

And to the `INSTALLED_APPS`:

```python
INSTALLED_APPS = (
    ...
    # Splash screen
    'splash',
)
```

