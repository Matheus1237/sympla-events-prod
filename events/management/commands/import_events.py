import logging

from django.conf import settings
from django.core.management.base import BaseCommand

from events.services.import_service import EventImportService

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Import events from Sympla API"

    def handle(self, *args, **options):
        try:
            self.stdout.write("Starting event import...")
            
            # Log the API key value from settings
            api_key = settings.SYMPLA_API_KEY
            logger.info(f"API Key from settings: {api_key}")
            
            import_service = EventImportService(api_key)
            import_log = import_service.import_events()
            
            self.stdout.write(
                self.style.SUCCESS(
                    f"Successfully imported {import_log.imported_count} events "
                    f"(version {import_log.version})"
                )
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"Error importing events: {str(e)}")
            )
            raise 