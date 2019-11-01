# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SplashConfig',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('change_date', models.DateTimeField(auto_now_add=True, verbose_name='Change date')),
                ('enabled', models.BooleanField(default=False, verbose_name='Enabled')),
                ('cookie_name', models.TextField(default=u'edx_splash_screen', help_text=u'The name of the cookie to check when assessing if the user needs to be redirected')),
                ('cookie_allowed_values', models.TextField(default=u'seen', help_text=u'Comma-separated list of values accepted as cookie values to prevent the redirect')),
                ('unaffected_usernames', models.TextField(default=u'', help_text=u'Comma-separated list of users which should never be redirected (usernames)', blank=True)),
                ('unaffected_url_paths', models.TextField(default=u'', help_text=u'Comma-separated list of URL paths (not including the hostname) which should not be redirected. Paths may include wildcards denoted by * (example: /*/student_view)', blank=True)),
                ('redirect_url', models.URLField(default=u'http://edx.org', help_text=u"The URL the users should be redirected to when they don't have the right cookie")),
                ('changed_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, editable=False, to=settings.AUTH_USER_MODEL, null=True, verbose_name='Changed by')),
            ],
            options={
                'ordering': ('-change_date',),
                'abstract': False,
            },
        ),
    ]

