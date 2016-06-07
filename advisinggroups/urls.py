from django.conf.urls import url
from views import ExcelFormView, ConfirmImport, UndoImport


urlpatterns = [
    url(r'^$', ExcelFormView.as_view(), name='index'),
    url(r'^confirm/$', ConfirmImport.as_view(), name='confirm'),
    url(r'^undo/$', UndoImport.as_view(), name='undo'),
]
