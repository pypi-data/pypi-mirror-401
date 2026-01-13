"""Adobe Typekit API client for font metadata enrichment"""

import logging
import time
from typing import Optional, List, Dict, Any
from dataclasses import dataclass
import requests
from functools import lru_cache


logger = logging.getLogger(__name__)


@dataclass
class TypekitFont:
    """Font information from Typekit API"""
    id: str
    name: str
    family: str
    slug: str
    foundry: Optional[str]
    designer: Optional[str]
    classifications: List[str]
    variations: List[Dict[str, Any]]


class TypekitClient:
    """Client for Adobe Typekit API"""

    BASE_URL = "https://typekit.com/api/v1/json"

    def __init__(self, api_key: str):
        """
        Initialize Typekit client

        Args:
            api_key: Adobe Typekit API key
        """
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            'X-Typekit-Token': api_key
        })
        self.rate_limit_delay = 0.5  # Delay between requests (seconds)
        self.last_request_time = 0

    def _rate_limit(self):
        """Implement rate limiting"""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.rate_limit_delay:
            time.sleep(self.rate_limit_delay - elapsed)
        self.last_request_time = time.time()

    @lru_cache(maxsize=1000)
    def search_family(self, query: str) -> List[TypekitFont]:
        """
        Search for font family by name

        Args:
            query: Font family name to search for

        Returns:
            List of matching TypekitFont objects
        """
        self._rate_limit()

        try:
            # Search in the full library
            url = f"{self.BASE_URL}/libraries/full"

            response = self.session.get(url, timeout=30)
            response.raise_for_status()

            data = response.json()

            # Search for matching families
            matches = []
            query_lower = query.lower()

            for family in data.get('library', {}).get('families', []):
                family_name = family.get('name', '').lower()

                # Check if query matches family name
                if query_lower in family_name or family_name in query_lower:
                    matches.append(self._parse_family(family))

            logger.info(f"Found {len(matches)} Typekit matches for '{query}'")
            return matches

        except requests.RequestException as e:
            logger.error(f"Typekit API error searching for '{query}': {e}")
            return []

    @lru_cache(maxsize=500)
    def get_family_details(self, family_id: str) -> Optional[TypekitFont]:
        """
        Get detailed information about a font family

        Args:
            family_id: Typekit family ID

        Returns:
            TypekitFont with complete information
        """
        self._rate_limit()

        try:
            url = f"{self.BASE_URL}/families/{family_id}"

            response = self.session.get(url, timeout=30)
            response.raise_for_status()

            data = response.json()
            family = data.get('family', {})

            return self._parse_family(family)

        except requests.RequestException as e:
            logger.error(f"Typekit API error getting family '{family_id}': {e}")
            return None

    def _parse_family(self, family_data: Dict) -> TypekitFont:
        """Parse Typekit family data into TypekitFont object"""

        # Extract classifications
        classifications = []
        if 'classifications' in family_data:
            for classification in family_data['classifications']:
                if isinstance(classification, dict):
                    classifications.append(classification.get('name', ''))
                else:
                    classifications.append(str(classification))

        # Extract variations
        variations = family_data.get('variations', [])

        return TypekitFont(
            id=family_data.get('id', ''),
            name=family_data.get('name', ''),
            family=family_data.get('name', ''),
            slug=family_data.get('slug', ''),
            foundry=family_data.get('foundry', {}).get('name') if isinstance(family_data.get('foundry'), dict) else None,
            designer=family_data.get('designer', {}).get('name') if isinstance(family_data.get('designer'), dict) else None,
            classifications=classifications,
            variations=variations
        )

    def enrich_metadata(self, font_name: str) -> Optional[Dict[str, Any]]:
        """
        Enrich font metadata with Typekit information

        Args:
            font_name: Font family name to search for

        Returns:
            Dictionary with enriched metadata or None
        """
        # Search for font
        matches = self.search_family(font_name)

        if not matches:
            return None

        # Take best match (first result)
        best_match = matches[0]

        return {
            'typekit_id': best_match.id,
            'foundry': best_match.foundry,
            'designer': best_match.designer,
            'classifications': best_match.classifications,
            'typekit_slug': best_match.slug,
            'variations': best_match.variations
        }

    def normalize_font_name(self, name: str) -> str:
        """
        Normalize font name for better Typekit matching

        Args:
            name: Font name to normalize

        Returns:
            Normalized font name
        """
        # Remove common prefixes
        prefixes = [
            'Adobe', 'Monotype', 'Linotype', 'URW', 'ITC', 'FF',
            'Bitstream', 'Letraset', 'Emigre'
        ]

        normalized = name
        for prefix in prefixes:
            if normalized.startswith(prefix):
                normalized = normalized[len(prefix):].strip()

        # Remove file extensions
        for ext in ['.ttf', '.otf', '.woff', '.woff2']:
            if normalized.lower().endswith(ext):
                normalized = normalized[:-len(ext)]

        # Remove weight/style suffixes for family search
        # (but keep for variation matching)
        # This is handled by the matching logic

        return normalized.strip()


class TypekitEnricher:
    """Enrich font metadata with Typekit data"""

    def __init__(self, typekit_client: TypekitClient):
        self.client = typekit_client
        self.cache = {}

    def enrich_font(self, metadata: 'FontMetadata') -> Dict[str, Any]:
        """
        Enrich font metadata with Typekit information

        Args:
            metadata: FontMetadata object

        Returns:
            Dictionary with Typekit enrichments
        """
        # Try family name first
        family_name = metadata.family_name or metadata.postscript_name

        if not family_name:
            return {}

        # Normalize name for better matching
        normalized = self.client.normalize_font_name(family_name)

        # Check cache
        if normalized in self.cache:
            return self.cache[normalized]

        # Query Typekit
        enrichment = self.client.enrich_metadata(normalized)

        # Cache result
        if enrichment:
            self.cache[normalized] = enrichment

        return enrichment or {}

    def batch_enrich(self, fonts: List['FontMetadata'], progress_callback=None) -> Dict[str, Dict[str, Any]]:
        """
        Enrich multiple fonts with Typekit data

        Args:
            fonts: List of FontMetadata objects
            progress_callback: Optional callback for progress updates

        Returns:
            Dictionary mapping file_hash to enrichment data
        """
        enrichments = {}

        for i, font_meta in enumerate(fonts):
            enrichment = self.enrich_font(font_meta)

            if enrichment:
                enrichments[font_meta.file_hash] = enrichment

            if progress_callback and (i + 1) % 10 == 0:
                progress_callback(i + 1, len(fonts))

        return enrichments
