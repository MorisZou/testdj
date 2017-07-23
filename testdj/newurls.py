from django.conf.urls.defaults import *
from . import view


   
urlpartterns = [
    url(r'^$', view.search),
]
