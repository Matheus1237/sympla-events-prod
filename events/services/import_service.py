import logging
from typing import Dict, List

from django.db import transaction
from django.db.models import Max

from events.models import Category, Event, ImportLog, Venue
from events.services.sympla_api import SymplaAPIClient

logger = logging.getLogger(__name__)


class EventImportService:
    def __init__(self, api_key: str):
        self.api_client = SymplaAPIClient(api_key)

    def _get_next_version(self) -> int:
        """
        Get the next version number for import logging.
        """
        current_max = ImportLog.objects.aggregate(Max("version"))["version__max"]
        return 1 if current_max is None else current_max + 1

    def _create_or_update_venue(self, venue_data: Dict) -> Venue:
        """
        Create or update a venue based on the Sympla ID.
        """
        venue, _ = Venue.objects.update_or_create(
            sympla_id=venue_data["sympla_id"],
            defaults={
                "name": venue_data["name"],
                "city": venue_data["city"],
            }
        )
        return venue

    def _create_or_update_category(self, category_data: Dict) -> Category:
        """
        Create or update a category based on the name.
        """
        category, _ = Category.objects.update_or_create(
            name=category_data["name"]
        )
        return category

    @transaction.atomic
    def import_events(self) -> ImportLog:
        """
        Import events from Sympla API and persist them in the database.
        """
        version = self._get_next_version()
        import_log = ImportLog.objects.create(
            version=version,
            status=ImportLog.Status.SUCCESS,
            imported_count=0
        )

        try:
            events_data = self.api_client.fetch_all_events()
            
            for event_data in events_data:
                try:
                    # Create or update related entities
                    venue = self._create_or_update_venue(event_data["venue"])
                    category = self._create_or_update_category(event_data["category"])

                    # Create or update event
                    Event.objects.update_or_create(
                        sympla_id=event_data["sympla_id"],
                        defaults={
                            "name": event_data["name"],
                            "start_date": event_data["start_date"],
                            "venue": venue,
                            "category": category,
                            "import_version": import_log,
                            "raw_data": event_data["raw_data"],
                        }
                    )
                    import_log.imported_count += 1
                    
                except Exception as e:
                    logger.error(f"Error processing event {event_data.get('sympla_id')}: {str(e)}")
                    continue

            import_log.save()
            logger.info(f"Successfully imported {import_log.imported_count} events")
            
        except Exception as e:
            error_message = f"Failed to import events: {str(e)}"
            logger.error(error_message)
            import_log.status = ImportLog.Status.ERROR
            import_log.error_message = error_message
            import_log.save()
            raise

        return import_log 