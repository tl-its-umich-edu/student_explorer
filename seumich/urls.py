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
from django.conf.urls import include, url, handler400, handler403, handler404, handler500
from seumich import views
from django.views.generic.base import TemplateView

urlpatterns = [
    url(r'^$', views.StudentsListView.as_view(), name='index'),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^advisors/(?P<advisor>\w+)/$',
        views.AdvisorView.as_view(), name='advisor'),
    url(r'^advisors/', views.AdvisorsListView.as_view(), name='advisors_list'),
    url(r'^students/(?P<student>\w+)/class_sites/(?P<classcode>\d+)/$',
        views.StudentClassSiteView.as_view(), name='student_class'),
    url(r'^students/(?P<student>\w+)/$',
        views.StudentView.as_view(), name='student'),
    url(r'^students/', views.StudentsListView.as_view(), name='students_list'),
]

handler400 = TemplateView.as_view(template_name="404.html")
handler403 = TemplateView.as_view(template_name="403.html")
handler404 = TemplateView.as_view(template_name="400.html")
handler500 = TemplateView.as_view(template_name="500.html")
