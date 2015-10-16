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
from django.views.static import serve
import clientsideredirect.views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    # url(r'^', include('dashboard.urls')),
    url(r'^api/', include('advising.urls')),
    url(r'^login/', clientsideredirect.views.login, name='login-redirect'),
    url(r'^$', clientsideredirect.views.login, name='login-redirect'),
    # url(r'^$', serve, {
    #     'document_root': 'sespa/app',
    #     'path': 'index.html'
    # }),
    url(r'^bower_components/(?P<path>.*)$', serve, {
        'document_root': 'sespa/bower_components',
    }),
    url(r'^(?P<path>.*)$', serve, {
        'document_root': 'sespa/app',
    }),
]
