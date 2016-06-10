from django.conf.urls import url, include
from tracking import views

urlpatterns = [url(r'^record-event/$', views.record_event, name="record-event"),]