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
from django.urls import path
from seumich import views

app_name = 'seumich'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('advisors/', views.AdvisorsListView.as_view(), name='advisors_list'),
    path('cohorts/', views.CohortsListView.as_view(), name='cohorts_list'),
    path('advisors/<advisor>/', views.AdvisorView.as_view(), name='advisor'),
    path('cohorts/<code>/', views.CohortView.as_view(), name='cohort'),
    path('classes/<class_site_id>/', views.ClassSiteView.as_view(), name='class_site'),
    path('students/', views.StudentsListView.as_view(), name='students_list'),
    path('students/<student>/', views.StudentView.as_view(), name='student'),
    path('students/<student>/class_sites/<classcode>/', views.StudentClassSiteView.as_view(), name='student_class'),
]
