from django.urls import path
from tracking import views

urlpatterns = [
    path('record-event/', views.record_event, name="record-event"),
]