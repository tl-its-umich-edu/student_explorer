from django.conf.urls import url, include
from rest_framework import routers
from advising import views

router = routers.DefaultRouter()
router.register(r'advisors', views.AdvisorViewSet)
router.register(r'students', views.StudentViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^advisors/', include('rest_framework.urls',
        namespace='rest_framework'))
]
