from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
import polls

urlpatterns = [
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
	url(r'^polls/', include('polls.urls')),
	url(r'^lookup/', include('lookup.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^status/', polls.views.status, name='status'),
    url(r'^rates/', polls.views.rates, name='rates'),
    url(r'^main/', polls.views.main, name='main'),
    url(r'^packagedeets/', polls.views.packagedeets, name='packagedeets'),

    


] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

#Add Django site authentication urls (for login, logout, password management)
urlpatterns += [
    url(r'^accounts/', include('django.contrib.auth.urls')),
]

