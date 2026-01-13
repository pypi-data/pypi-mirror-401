"""Font deduplication and matching system"""

import logging
from pathlib import Path
from typing import List, Dict, Set, Optional, Tuple
from dataclasses import dataclass
from difflib import SequenceMatcher

from .metadata import FontMetadata, FontDatabase


logger = logging.getLogger(__name__)


@dataclass
class DuplicateMatch:
    """A potential duplicate font match"""
    primary_font: FontMetadata
    duplicate_font: FontMetadata
    confidence: float
    reason: str
    can_auto_delete: bool


@dataclass
class DeduplicationReport:
    """Report of duplicate detection results"""
    total_fonts: int
    exact_duplicates: int  # Same file hash
    high_confidence_dupes: int  # >0.85 confidence
    medium_confidence_dupes: int  # 0.60-0.85
    low_confidence_dupes: int  # <0.60
    matches: List[DuplicateMatch]
    potential_savings_mb: float


class DuplicateDetector:
    """Detect duplicate fonts with confidence scoring"""

    def __init__(self, database: FontDatabase):
        self.db = database

    def find_duplicates(self, min_confidence: float = 0.60) -> DeduplicationReport:
        """
        Find duplicate fonts in database

        Args:
            min_confidence: Minimum confidence threshold (0.0-1.0)

        Returns:
            DeduplicationReport with all matches
        """
        logger.info(f"Finding duplicates (min confidence: {min_confidence})")

        matches = []
        seen_hashes = set()
        hash_groups = self._group_by_hash()

        # Step 1: Exact duplicates (same file hash)
        exact_dupes = self._find_exact_duplicates(hash_groups)
        matches.extend(exact_dupes)

        # Mark exact duplicates as seen
        for match in exact_dupes:
            seen_hashes.add(match.duplicate_font.file_hash)

        # Step 2: Smart matching (different files, same font)
        smart_matches = self._find_smart_matches(min_confidence, seen_hashes)
        matches.extend(smart_matches)

        # Calculate statistics
        exact_count = len(exact_dupes)
        high_conf = sum(1 for m in matches if m.confidence >= 0.85)
        medium_conf = sum(1 for m in matches if 0.60 <= m.confidence < 0.85)
        low_conf = sum(1 for m in matches if m.confidence < 0.60)

        # Calculate potential savings
        savings_bytes = sum(m.duplicate_font.file_size for m in matches if m.can_auto_delete)
        savings_mb = savings_bytes / (1024 * 1024)

        report = DeduplicationReport(
            total_fonts=len(self.db.fonts),
            exact_duplicates=exact_count,
            high_confidence_dupes=high_conf,
            medium_confidence_dupes=medium_conf,
            low_confidence_dupes=low_conf,
            matches=matches,
            potential_savings_mb=savings_mb
        )

        logger.info(f"Found {len(matches)} potential duplicates")
        logger.info(f"Exact: {exact_count}, High conf: {high_conf}, Medium: {medium_conf}, Low: {low_conf}")

        return report

    def _group_by_hash(self) -> Dict[str, List[FontMetadata]]:
        """Group fonts by file hash"""
        hash_groups = {}

        for font in self.db.fonts.values():
            if font.file_hash not in hash_groups:
                hash_groups[font.file_hash] = []
            hash_groups[font.file_hash].append(font)

        return hash_groups

    def _find_exact_duplicates(self, hash_groups: Dict[str, List[FontMetadata]]) -> List[DuplicateMatch]:
        """Find exact duplicates (same file hash)"""
        exact_matches = []

        for file_hash, fonts in hash_groups.items():
            if len(fonts) > 1:
                # Sort by filename to pick primary consistently
                fonts_sorted = sorted(fonts, key=lambda f: f.filename)
                primary = fonts_sorted[0]

                # Rest are duplicates
                for duplicate in fonts_sorted[1:]:
                    match = DuplicateMatch(
                        primary_font=primary,
                        duplicate_font=duplicate,
                        confidence=1.0,
                        reason="Exact duplicate (same file hash)",
                        can_auto_delete=True
                    )
                    exact_matches.append(match)

        return exact_matches

    def _find_smart_matches(self, min_confidence: float, seen_hashes: Set[str]) -> List[DuplicateMatch]:
        """Find potential duplicates using smart matching"""
        matches = []
        fonts_list = list(self.db.fonts.values())

        # Group fonts by family for efficiency
        family_groups = self._group_by_family()

        for family_name, fonts in family_groups.items():
            if len(fonts) < 2:
                continue  # No duplicates in single-font families

            # Compare each font with others in same family
            for i, font1 in enumerate(fonts):
                if font1.file_hash in seen_hashes:
                    continue  # Already marked as duplicate

                for font2 in fonts[i + 1:]:
                    if font2.file_hash in seen_hashes:
                        continue  # Already marked as duplicate

                    # Calculate match confidence
                    confidence, reason = self._calculate_match_confidence(font1, font2)

                    if confidence >= min_confidence:
                        # Determine which is primary (prefer smaller file if same format)
                        primary, duplicate = self._select_primary(font1, font2)

                        match = DuplicateMatch(
                            primary_font=primary,
                            duplicate_font=duplicate,
                            confidence=confidence,
                            reason=reason,
                            can_auto_delete=confidence >= 0.85
                        )
                        matches.append(match)

                        # Mark as seen
                        seen_hashes.add(duplicate.file_hash)

        return matches

    def _group_by_family(self) -> Dict[str, List[FontMetadata]]:
        """Group fonts by family name"""
        family_groups = {}

        for font in self.db.fonts.values():
            family = font.family_name or font.postscript_name or "Unknown"

            if family not in family_groups:
                family_groups[family] = []

            family_groups[family].append(font)

        return family_groups

    def _calculate_match_confidence(self, font1: FontMetadata, font2: FontMetadata) -> Tuple[float, str]:
        """
        Calculate match confidence between two fonts

        STRICT RULES:
        - Weight MUST match exactly
        - Italic MUST match exactly
        - Width MUST match exactly
        - Only then check name similarity

        Returns:
            (confidence, reason) tuple
        """
        reasons = []

        # CRITICAL: Metadata must match EXACTLY
        # Different weight/italic/width = NOT duplicates!

        # Check weight
        if font1.weight != font2.weight:
            # Different weights = definitely not duplicates
            return 0.0, "Different weights"

        # Check italic
        if font1.italic != font2.italic:
            # Italic vs Regular = definitely not duplicates
            return 0.0, "Different italic status"

        # Check width
        if font1.width != font2.width:
            # Condensed vs Extended = definitely not duplicates
            return 0.0, "Different width"

        # Extract unique IDs from filenames (Monotype pattern: numbers after hyphen)
        id1 = self._extract_unique_id(font1.filename)
        id2 = self._extract_unique_id(font2.filename)

        if id1 and id2 and id1 != id2:
            # Different unique IDs = definitely not duplicates
            return 0.0, f"Different unique IDs ({id1} vs {id2})"

        # Now metadata matches exactly - check names
        name_sim = self._name_similarity(font1, font2)

        # Only consider duplicates if name is VERY similar
        if name_sim < 0.95:  # Raised from 0.8 - must be nearly identical
            return 0.0, "Name not similar enough"

        # Build confidence and reason
        confidence = name_sim  # Start with name similarity
        reasons.append(f"Name match: {name_sim:.0%}")

        # Metadata matched exactly
        metadata_parts = []
        if font1.weight:
            metadata_parts.append(f"Weight: {font1.weight}")
        if font1.italic:
            metadata_parts.append("Italic: True")
        if font1.width and font1.width != 'normal':
            metadata_parts.append(f"Width: {font1.width}")

        if metadata_parts:
            reasons.append(", ".join(metadata_parts))

        # Glyph count must be very close
        if font1.glyph_count and font2.glyph_count:
            glyph_diff = abs(font1.glyph_count - font2.glyph_count)
            if glyph_diff < 5:  # Must be nearly identical
                confidence += 0.05
                reasons.append(f"Identical glyphs: {font1.glyph_count}")
            elif glyph_diff > 50:  # Too different
                return 0.0, "Glyph count too different"

        reason = "; ".join(reasons)

        return confidence, reason

    def _extract_unique_id(self, filename: str) -> Optional[str]:
        """
        Extract unique identifier from filename

        Patterns:
        - Monotype: FontName-123456.ttf → "123456"
        - Others: May have different patterns
        """
        import re

        # Pattern: hyphen followed by 6+ digits before extension
        match = re.search(r'-(\d{6,})\.', filename)
        if match:
            return match.group(1)

        return None

    def _name_similarity(self, font1: FontMetadata, font2: FontMetadata) -> float:
        """Calculate name similarity using SequenceMatcher"""

        # Use PostScript name or family name
        name1 = (font1.postscript_name or font1.family_name or "").lower()
        name2 = (font2.postscript_name or font2.family_name or "").lower()

        if not name1 or not name2:
            return 0.0

        # Calculate similarity ratio
        return SequenceMatcher(None, name1, name2).ratio()

    def _select_primary(self, font1: FontMetadata, font2: FontMetadata) -> Tuple[FontMetadata, FontMetadata]:
        """
        Select which font should be primary (keep) vs duplicate (can delete)

        Prefers:
        1. Smaller file size (if same format)
        2. TTF over OTF over WOFF2 (more versatile)
        """

        # If same format, prefer smaller file
        if font1.format == font2.format:
            if font1.file_size <= font2.file_size:
                return font1, font2
            else:
                return font2, font1

        # Prefer TTF > OTF > WOFF2
        format_priority = {'ttf': 3, 'otf': 2, 'woff2': 1, 'woff': 1}

        priority1 = format_priority.get(font1.format, 0)
        priority2 = format_priority.get(font2.format, 0)

        if priority1 >= priority2:
            return font1, font2
        else:
            return font2, font1
