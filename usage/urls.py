from django.conf.urls import url
from usage import views

urlpatterns = [
    url(r'^$', views.UsageView.as_view(), name='usage_index'),
    url(r'^download/$', views.DownloadCsvView.as_view(),
        name='usage_download'),
]
