from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^status/', views.status, name='status'),
    url(r'^rates/', views.rates, name='rates'),
    url(r'^packagedeets/', views.packagedeets, name='packagedeets'),
    
]

