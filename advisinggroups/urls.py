from django.conf.urls import url
from views import ExcelFormview


urlpatterns = [
    url(r'^$', ExcelFormview.as_view(), name='index'),
]
