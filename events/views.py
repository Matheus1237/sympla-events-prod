from django.shortcuts import render
from django.conf import settings
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from events.models import Event, ImportLog
from events.serializers import EventSerializer, ImportLogSerializer
from events.services.import_service import EventImportService


class EventViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for listing and retrieving events.
    """
    queryset = Event.objects.select_related("venue", "category", "import_version").all()
    serializer_class = EventSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "venue__name", "venue__city", "category__name"]
    ordering_fields = ["start_date", "name", "created_at"]
    ordering = ["-start_date"]

    @action(detail=False, methods=["post"])
    def import_events(self, request):
        """
        Trigger a new event import from Sympla API.
        """
        try:
            import_service = EventImportService(settings.SYMPLA_API_KEY)
            import_log = import_service.import_events()
            serializer = ImportLogSerializer(import_log)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ImportLogViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for listing and retrieving import logs.
    """
    queryset = ImportLog.objects.all()
    serializer_class = ImportLogSerializer
    ordering = ["-created_at"]
