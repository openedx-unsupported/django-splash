"""
Admin site bindings for splash screen
"""


from django.contrib import admin

from config_models.admin import ConfigurationModelAdmin

from splash.models import SplashConfig

admin.site.register(SplashConfig, ConfigurationModelAdmin)
