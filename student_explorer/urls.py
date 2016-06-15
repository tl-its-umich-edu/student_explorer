"""student_explorer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('seumich.urls')),
    url(r'^status/', include('watchman.urls')),
    url(r'^advising_groups/', include('advisinggroups.urls')),
]

if 'djangosaml2' in settings.INSTALLED_APPS:
    urlpatterns += (
        url(r'^accounts/', include('djangosaml2.urls')),
    )

if 'registration' in settings.INSTALLED_APPS:
    urlpatterns += (
        url(r'^accounts/', include('registration.backends.default.urls')),
    )

# Override auth_logout from djangosaml2 and registration for consistant
# behavior
urlpatterns.append(url(r'^accounts/logout', views.logout, name='auth_logout'))
urlpatterns.append(url(r'^about', views.about, name='about'))
