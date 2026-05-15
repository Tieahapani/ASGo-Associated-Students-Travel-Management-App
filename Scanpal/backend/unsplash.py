import os
import re
import logging
import requests
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

GOOGLE_PLACES_API_KEY = os.getenv("GOOGLE_PLACES_API_KEY")

# US state abbreviations to strip from destination strings
_STATE_ABBREVS = {
    "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA",
    "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
    "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
    "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
    "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY",
}


def _clean_destination(raw: str) -> str:
    """Extract a clean city/place name from messy destination strings."""
    text = raw.strip()
    text = re.sub(r'\s*trip\s*$', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\b\d{5}(-\d{4})?\b', '', text)
    text = re.sub(r'^\d+\s+\w+\s*(,|\.)\s*', '', text)

    parts = [p.strip() for p in text.split(',')]
    cleaned_parts = []
    for part in parts:
        words = part.split()
        filtered = [w for w in words if w.upper() not in _STATE_ABBREVS]
        joined = ' '.join(filtered).strip()
        if joined:
            cleaned_parts.append(joined)
    text = ', '.join(cleaned_parts)

    text = re.sub(
        r',?\s*\b(California|Texas|Florida|New York|Illinois|Ohio|Pennsylvania|Georgia|Michigan|Washington)\b',
        '', text, flags=re.IGNORECASE,
    )
    return text.strip().strip(',').strip()


def _find_place_photo(query: str) -> str | None:
    """Use Google Places API (New) to find a place and return a photo URL."""
    # Step 1: Text Search to find the place with photos
    resp = requests.post(
        "https://places.googleapis.com/v1/places:searchText",
        json={
            "textQuery": query,
            "maxResultCount": 1,
        },
        headers={
            "X-Goog-Api-Key": GOOGLE_PLACES_API_KEY,
            "X-Goog-FieldMask": "places.id,places.photos",
        },
        timeout=10,
    )
    resp.raise_for_status()
    places = resp.json().get("places", [])
    if not places:
        return None

    photos = places[0].get("photos")
    if not photos:
        return None

    # Step 2: Build the photo URI from the photo resource name
    photo_name = photos[0]["name"]
    return (
        f"https://places.googleapis.com/v1/{photo_name}/media"
        f"?maxWidthPx=1200&key={GOOGLE_PLACES_API_KEY}"
    )


def fetch_destination_image(destination: str) -> str | None:
    """Fetch a photo URL from Google Places for the given destination.
    Returns the photo URL, or None on failure."""
    if not GOOGLE_PLACES_API_KEY:
        logger.warning("GOOGLE_PLACES_API_KEY not set, skipping image fetch")
        return None

    if not destination or not destination.strip():
        return None

    city = _clean_destination(destination)
    if not city:
        city = destination.strip()

    try:
        url = _find_place_photo(city)
        if url:
            logger.info(f"Google Places hit for '{destination}' (query: '{city}')")
            return url
        logger.info(f"No Google Places photo for '{destination}'")
        return None
    except Exception as e:
        logger.error(f"Google Places fetch failed for '{destination}': {e}")
        return None
