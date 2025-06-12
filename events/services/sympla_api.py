import logging
from datetime import datetime
from typing import Dict, List, Optional

import requests
from dateutil.parser import parse
from django.conf import settings
from django.utils import timezone
from requests.exceptions import RequestException

logger = logging.getLogger(__name__)


class SymplaAPIClient:
    BASE_URL = "https://api.sympla.com.br/public/v3"
    
    def __init__(self, api_key: str):
        logger.info(f"Initializing SymplaAPIClient with API key: {api_key}")
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            "s_token": self.api_key,
            "Content-Type": "application/json",
            "Accept": "application/json"
        })
        logger.info(f"Session headers after initialization: {self.session.headers}")

    def _make_request(self, endpoint: str, params: Optional[Dict] = None) -> Dict:
        """
        Make a request to the Sympla API with error handling and retries.
        """
        try:
            logger.info(f"Current API key before request: {self.api_key}")
            logger.info(f"Current headers before request: {self.session.headers}")
            response = self.session.get(
                f"{self.BASE_URL}/{endpoint}",
                params=params,
                timeout=10
            )
            logger.info(f"Request URL: {response.url}")
            logger.info(f"Request headers sent: {response.request.headers}")
            logger.info(f"Response status: {response.status_code}")
            logger.info(f"Response body: {response.text}")
            
            response.raise_for_status()
            return response.json()
        except RequestException as e:
            logger.error(f"Error making request to Sympla API: {str(e)}")
            raise

    def get_events(self, page: int = 1, published: bool = True) -> Dict:
        """
        Get events from Sympla API with pagination.
        """
        params = {
            "page": page,
            "published": published
        }
        
        try:
            response = self._make_request("events", params)
            logger.info(f"Response data: {response}")
            return response  # Return the full response
        except Exception as e:
            logger.error(f"Failed to fetch events from Sympla API: {str(e)}")
            raise

    @staticmethod
    def normalize_event_data(event_data: Dict) -> Dict:
        """
        Normalize and validate event data from the API.
        """
        try:
            # Extract and normalize basic event information
            start_date = parse(event_data.get("start_date", ""))
            if timezone.is_naive(start_date):
                start_date = timezone.make_aware(start_date)
                
            event = {
                "sympla_id": str(event_data.get("id")),
                "name": event_data.get("name", "").strip(),
                "start_date": start_date,
                "raw_data": event_data,
            }

            # Extract and normalize venue information
            venue_data = event_data.get("address", {})
            event["venue"] = {
                "sympla_id": str(venue_data.get("id")),
                "name": venue_data.get("name", "").strip(),
                "city": venue_data.get("city", "").strip(),
            }

            # Extract and normalize category information
            category_data = event_data.get("category_prim", {})
            event["category"] = {
                "name": category_data.get("name", "Outros").strip(),
            }

            return event
        except Exception as e:
            logger.error(f"Error normalizing event data: {str(e)}")
            raise ValueError(f"Invalid event data format: {str(e)}")

    def fetch_all_events(self) -> List[Dict]:
        """
        Fetch all events from the API using pagination.
        """
        all_events = []
        page = 1
        
        while True:
            try:
                logger.info(f"Fetching page {page}")
                response = self.get_events(page=page)
                events = response.get("data", [])
                pagination = response.get("pagination", {})
                
                if not events:
                    logger.info("No events found on this page")
                    break
                
                logger.info(f"Found {len(events)} events on page {page}")
                normalized_events = [
                    self.normalize_event_data(event)
                    for event in events
                ]
                all_events.extend(normalized_events)
                
                # Check if there are more pages
                if not pagination.get("has_next", False):
                    logger.info("No more pages available")
                    break
                    
                page += 1
                
            except Exception as e:
                logger.error(f"Error fetching events on page {page}: {str(e)}")
                raise

        logger.info(f"Total events found: {len(all_events)}")
        return all_events 