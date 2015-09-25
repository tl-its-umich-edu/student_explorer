from django.conf.urls import patterns, url

urlpatterns = patterns('dashboard.views',
                       url(r'^$', 'dashboard', name='dashboard'),
                       url(r'^student/(?P<student>[a-zA-Z]+)/$', 'studentPage', name='studentPage'),
                       url(r'^advisors/$', 'advisorDashboard', name='advisorDashboard'),
                       url(r'^advisors/(?P<advisor>[a-zA-Z]+)/students/$', 'dashboard', name='dashboard'),
                       )
