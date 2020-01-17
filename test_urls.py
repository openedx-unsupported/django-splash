""" ROOT_URLCONF for tests """
from django.conf.urls import url

from test_utils import views


urlpatterns = [
    url(r'^home', views.home, name='home'),
]
