""" Views used only for test setup """
from django.http import HttpResponse


def home(request):
    """ Placeholder test view """
    return HttpResponse("ok")
