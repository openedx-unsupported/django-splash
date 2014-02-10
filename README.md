Splash screen middleware for Django apps
========================================

Checks incoming requests, to redirect users to a configured splash screen URL
if they don't have the proper cookie set. This can be used to display a small
marketing landing page, protect an alpha website from the public eye, make an
announcement, etc.

Meant to be used with https://github.com/edx/edx-platform/ -- or you will need 
to import the config_models application to your Django application:
https://github.com/edx/edx-platform/tree/master/common/djangoapps/config_models

### Installation

Add the application to the `INSTALLED_APPS`:

```python
INSTALLED_APPS = (
    ...
    # Splash screen
    'splash',
)
```

Add the middleware to the configuration:

```python
MIDDLEWARE_CLASSES = (
    ...
    'splash.middleware.SplashMiddleware',
)
```

Run the migrations:

```
$ ./manage.py migrate splash
```

Then go to your Django admin, in http://yourserver/admin/splash/splashconfig/add/
and configure the following variables:

* `enabled`: To activate the feature
* `cookie_name`: The name of the cookie
* `cookie_allowed_values`: The user cookie value must match one of the values to not be redirected to the splash screen URL
* `unaffected_users`: Users which should never be redirected (usernames)
* `redirect_url`: The URL the users should be redirected to when they don't have the right cookie

