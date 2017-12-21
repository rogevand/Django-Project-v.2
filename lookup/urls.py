from django.conf.urls import *

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^polls/lookup$', views.lookup, name='lookup'),
]
