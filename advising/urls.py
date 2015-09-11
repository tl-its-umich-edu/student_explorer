from django.conf.urls import patterns, url

urlpatterns = patterns('advising.views',
                       url(r'^$', 'advisor_list', name='advisor_list'),
                       )
