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
from django.conf.urls import url
from seumich import views
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie

from django.conf import settings

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

urlpatterns = [
    url(
        r'^$',
        vary_on_cookie(cache_page(CACHE_TTL)(views.IndexView.as_view())),
        name='index'),

    url(
        r'^advisors/$',
        vary_on_cookie(cache_page(CACHE_TTL)(views.AdvisorsListView.as_view())),
        name='advisors_list'),
    url(
        r'^cohorts/$',
        vary_on_cookie(cache_page(CACHE_TTL)(views.CohortsListView.as_view())),
        name='cohorts_list'),
    url(
        r'^advisors/(?P<advisor>[\s\w-]+)/$',
        vary_on_cookie(cache_page(CACHE_TTL)(views.AdvisorView.as_view())),
        name='advisor'),
    url(
        r'^cohorts/(?P<code>[\s\w-]+)/$',
        vary_on_cookie(cache_page(CACHE_TTL)(views.CohortView.as_view())),
        name='cohort'),
    url(
        r'^classes/(?P<class_site_id>\d+)/$',
        vary_on_cookie(cache_page(CACHE_TTL)(views.ClassSiteView.as_view())),
        name='class_site'),
    url(r'^students/$',
        vary_on_cookie(cache_page(CACHE_TTL)(views.StudentsListView.as_view())),
        name='students_list'),
    url(r'^students/(?P<student>\w+)/$',
        vary_on_cookie(cache_page(CACHE_TTL)(views.StudentView.as_view())),
        name='student'),
    url(r'^students/(?P<student>\w+)/class_sites/(?P<classcode>[\w-]+)/$',
        vary_on_cookie(cache_page(CACHE_TTL)(views.StudentClassSiteView.as_view())),
        name='student_class'),
]
