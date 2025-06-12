from django.urls import include, path
from rest_framework.routers import DefaultRouter

from events.views import EventViewSet, ImportLogViewSet

router = DefaultRouter()
router.register(r"events", EventViewSet)
router.register(r"import-logs", ImportLogViewSet)

urlpatterns = [
    path("", include(router.urls)),
] 