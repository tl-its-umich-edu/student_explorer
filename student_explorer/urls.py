"""
student_explorer URL Configuration

This file was originally created to work with Django 1.8. It has since been updated to use Django 2.2.
Refer to the Django documentation at the following link for proper usage:
https://docs.djangoproject.com/en/2.2/ref/urls/

"""
from django.urls import include, path
from django.views.generic import TemplateView
from django.contrib import admin
from django.conf import settings
from . import views

urlpatterns = [
    path(
        'robots.txt',
        TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
        name="robots_file"
    ),
    path('', include('seumich.urls', namespace='seumich')),
    path('about', views.about, name='about'),
    path('admin/', admin.site.urls),
    path('manage/', include('management.urls')),
    path('feedback/', include('feedback.urls', namespace='feedback')),
    path('usage/', include('usage.urls', namespace='usage')),
    path('status/', include('watchman.urls')),
    path('pages/', include('django.contrib.flatpages.urls')),
]

# Override auth_logout from djangosaml2 and registration for consistent behavior
urlpatterns.append(path('accounts/logout/', views.logout, name='auth_logout'))

if 'djangosaml2' in settings.INSTALLED_APPS:
    from djangosaml2.views import EchoAttributesView
    urlpatterns += [
        path('accounts/', include('djangosaml2.urls')),
        path('accounts/echo_attributes/', EchoAttributesView.as_view()),
    ]
elif 'registration' in settings.INSTALLED_APPS:
    urlpatterns += [
        path('accounts/', include('registration.backends.default.urls')),
    ]

# Configure Django Debug Toolbar
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
