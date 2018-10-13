"""website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.i18n import i18n_patterns
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.i18n import javascript_catalog
from django.contrib.sitemaps.views import sitemap
from cms.sitemaps import CMSSitemap

admin.autodiscover()

urlpatterns = [
    url(r'^sitemap\.xml$', sitemap ,{'sitemaps': {'cmspages': CMSSitemap}}),
    url(r'^jsi18n/$', javascript_catalog, name='javascript-catalog'),
    url(r'^auth/', include('users.urls')),
]

urlpatterns += staticfiles_urlpatterns()

# note the django CMS URLs included via i18n_patterns
urlpatterns += i18n_patterns(
    url(r'^admin/', include(admin.site.urls)),
    url(r'^reserv/', include('reserve_calendar_date.urls', namespace='polls')),
    url(r'^', include('cms.urls')),
    prefix_default_language=False) \
  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
