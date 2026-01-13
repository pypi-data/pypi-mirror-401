"""Font search and filtering system"""

import logging
from pathlib import Path
from typing import List, Optional, Dict, Any
from dataclasses import dataclass

from .metadata import FontMetadata, FontDatabase


logger = logging.getLogger(__name__)


@dataclass
class SearchCriteria:
    """Criteria for searching fonts"""
    classification: Optional[str] = None  # sans-serif, serif, display, etc.
    family: Optional[str] = None
    weight_min: Optional[int] = None
    weight_max: Optional[int] = None
    italic: Optional[bool] = None
    variable: Optional[bool] = None
    has_axis: Optional[str] = None  # wght, wdth, slnt, etc.
    designer: Optional[str] = None
    foundry: Optional[str] = None
    format: Optional[str] = None  # ttf, otf, woff2


class FontSearch:
    """Search fonts by criteria"""

    def __init__(self, database: FontDatabase, enrichments: Optional[Dict[str, Dict]] = None):
        """
        Initialize search system

        Args:
            database: FontDatabase to search
            enrichments: Optional Typekit enrichment data
        """
        self.db = database
        self.enrichments = enrichments or {}

    def search(self, criteria: SearchCriteria) -> List[FontMetadata]:
        """
        Search fonts matching criteria

        Args:
            criteria: SearchCriteria object

        Returns:
            List of matching FontMetadata objects
        """
        results = []

        for font in self.db.fonts.values():
            if self._matches_criteria(font, criteria):
                results.append(font)

        logger.info(f"Found {len(results)} fonts matching criteria")
        return results

    def _matches_criteria(self, font: FontMetadata, criteria: SearchCriteria) -> bool:
        """Check if font matches all criteria"""

        # Family name filter
        if criteria.family:
            if not font.family_name:
                return False
            if criteria.family.lower() not in font.family_name.lower():
                return False

        # Weight range filter
        if criteria.weight_min is not None or criteria.weight_max is not None:
            if not font.weight:
                return False

            if criteria.weight_min and font.weight < criteria.weight_min:
                return False

            if criteria.weight_max and font.weight > criteria.weight_max:
                return False

        # Italic filter
        if criteria.italic is not None:
            if font.italic != criteria.italic:
                return False

        # Variable font filter
        if criteria.variable is not None:
            if font.is_variable != criteria.variable:
                return False

        # Has specific axis filter
        if criteria.has_axis:
            if not font.is_variable or not font.axes:
                return False

            axis_tags = [axis.tag for axis in font.axes]
            if criteria.has_axis not in axis_tags:
                return False

        # Format filter
        if criteria.format:
            if font.format != criteria.format.lower():
                return False

        # Classification filter (requires Typekit enrichment)
        if criteria.classification:
            enrichment = self.enrichments.get(font.file_hash, {})
            classifications = enrichment.get('classifications', [])

            # Convert to lowercase for matching
            classifications_lower = [c.lower() for c in classifications]

            if criteria.classification.lower() not in classifications_lower:
                # Also check family name for common classifications
                if not self._infer_classification(font, criteria.classification):
                    return False

        # Designer filter (from font metadata)
        if criteria.designer:
            designer = font.designer or ''

            if not designer:
                return False

            if criteria.designer.lower() not in designer.lower():
                return False

        # Foundry filter (from font metadata)
        if criteria.foundry:
            foundry = font.foundry or ''

            if not foundry:
                return False

            if criteria.foundry.lower() not in foundry.lower():
                return False

        return True

    def _infer_classification(self, font: FontMetadata, classification: str) -> bool:
        """
        Infer classification from font name if no Typekit data

        Args:
            font: FontMetadata
            classification: Classification to check for

        Returns:
            True if classification likely matches
        """
        family_name = (font.family_name or font.postscript_name or "").lower()

        # Sans serif indicators
        sans_indicators = ['sans', 'gothic', 'grotesk', 'helvetica', 'arial', 'univers']

        # Serif indicators
        serif_indicators = ['serif', 'garamond', 'times', 'baskerville', 'bodoni']

        # Display indicators
        display_indicators = ['display', 'headline', 'poster', 'titling']

        # Monospace indicators
        mono_indicators = ['mono', 'code', 'typewriter', 'courier']

        classification_lower = classification.lower()

        if 'sans' in classification_lower:
            return any(indicator in family_name for indicator in sans_indicators)

        if 'serif' in classification_lower and 'sans' not in classification_lower:
            return any(indicator in family_name for indicator in serif_indicators)

        if 'display' in classification_lower:
            return any(indicator in family_name for indicator in display_indicators)

        if 'mono' in classification_lower:
            return any(indicator in family_name for indicator in mono_indicators)

        return False

    def group_by_family(self, fonts: List[FontMetadata]) -> Dict[str, List[FontMetadata]]:
        """
        Group fonts by family name

        Args:
            fonts: List of fonts to group

        Returns:
            Dictionary mapping family name to list of fonts
        """
        groups = {}

        for font in fonts:
            family = font.family_name or "Unknown"

            if family not in groups:
                groups[family] = []

            groups[family].append(font)

        return groups

    def group_by_format(self, fonts: List[FontMetadata]) -> Dict[str, List[FontMetadata]]:
        """Group fonts by format"""
        groups = {}

        for font in fonts:
            if font.format not in groups:
                groups[font.format] = []

            groups[font.format].append(font)

        return groups

    def filter_variable_fonts(self, fonts: Optional[List[FontMetadata]] = None) -> List[FontMetadata]:
        """
        Get all variable fonts

        Args:
            fonts: Optional list to filter, or use entire database

        Returns:
            List of variable fonts
        """
        source = fonts if fonts else self.db.fonts.values()
        return [f for f in source if f.is_variable]

    def find_by_designer(self, designer: str) -> List[FontMetadata]:
        """Find all fonts by a specific designer (requires Typekit enrichment)"""
        results = []

        for font in self.db.fonts.values():
            enrichment = self.enrichments.get(font.file_hash, {})

            font_designer = enrichment.get('designer', '')

            if designer.lower() in font_designer.lower():
                results.append(font)

        return results

    def find_by_foundry(self, foundry: str) -> List[FontMetadata]:
        """Find all fonts by a specific foundry (requires Typekit enrichment)"""
        results = []

        for font in self.db.fonts.values():
            enrichment = self.enrichments.get(font.file_hash, {})

            font_foundry = enrichment.get('foundry', '')

            if foundry.lower() in font_foundry.lower():
                results.append(font)

        return results
