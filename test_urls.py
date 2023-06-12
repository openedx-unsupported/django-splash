""" ROOT_URLCONF for tests """
from django.urls import re_path

from test_utils import views


urlpatterns = [
    re_path(r'^home', views.home, name='home'),
]
