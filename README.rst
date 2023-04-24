django-splash
=============

|pypi-badge| |ci-badge| |codecov-badge| |pyversions-badge|
|license-badge|

Splash screen middleware for Django apps

Overview
--------

Checks incoming requests, to redirect users to a configured splash screen URL
if they don't have the proper cookie set. This can be used to display a small
marketing landing page, protect an alpha website from the public eye, make an
announcement, etc.

Meant to be used with https://github.com/openedx/edx-platform/ -- or you will need
to import the config_models application to your Django application:
https://github.com/openedx/django-config-models

Installation
------------

Add the application to the `INSTALLED_APPS`:

::

    python
    INSTALLED_APPS = (
        ...
        # Splash screen
        'splash',
    )

Add the middleware to the configuration:

::

    python
    MIDDLEWARE_CLASSES = (
        ...
        'splash.middleware.SplashMiddleware',
    )

Run the migrations:

``$ ./manage.py migrate splash``

Then go to your Django admin, in http://yourserver/admin/splash/splashconfig/add/
and configure the following variables:

* `enabled`: To activate the feature
* `cookie_name`: The name of the cookie
* `cookie_allowed_values`: The user cookie value must match one of the values to not be redirected to the splash screen URL
* `unaffected_users`: Users which should never be redirected (usernames)
* `redirect_url`: The URL the users should be redirected to when they don't have the right cookie

License
-------

The code in this repository is licensed under the Apache Software License 2.0 unless
otherwise noted.

Please see ``LICENSE.txt`` for details.

How To Contribute
-----------------

Contributions are very welcome.

Please read `How To Contribute <https://github.com/openedx/.github/blob/master/CONTRIBUTING.md>`_ for details.


Reporting Security Issues
-------------------------

Please do not report security issues in public. Please email security@edx.org.

Getting Help
------------

Have a question about this repository, or about Open edX in general?  Please
refer to this `list of resources`_ if you need any assistance.

.. _list of resources: https://open.edx.org/getting-help


.. |pypi-badge| image:: https://img.shields.io/pypi/v/django-splash.svg
    :target: https://pypi.python.org/pypi/django-splash/
    :alt: PyPI

.. |ci-badge| image:: https://github.com/openedx/django-splash/workflows/Python%20CI/badge.svg?branch=master
    :target: https://github.com/openedx/django-splash/actions?query=workflow%3A%22Python+CI%22
    :alt: CI

.. |codecov-badge| image:: http://codecov.io/github/edx/django-splash/coverage.svg?branch=master
    :target: http://codecov.io/github/edx/django-splash?branch=master
    :alt: Codecov

.. |pyversions-badge| image:: https://img.shields.io/pypi/pyversions/django-splash.svg
    :target: https://pypi.python.org/pypi/django-splash/
    :alt: Supported Python versions

.. |license-badge| image:: https://img.shields.io/github/license/edx/django-splash.svg
    :target: https://github.com/openedx/django-splash/blob/master/LICENSE.txt
    :alt: License
