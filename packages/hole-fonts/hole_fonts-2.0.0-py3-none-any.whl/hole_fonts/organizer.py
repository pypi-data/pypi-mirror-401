"""Font library organization module for HOLE Fonts"""

import logging
import shutil
from pathlib import Path
from typing import Dict, List, Optional
import re


logger = logging.getLogger(__name__)


class FontOrganizer:
    """Organize fonts into structured library"""

    def __init__(self, library_path: Path):
        """
        Initialize organizer

        Args:
            library_path: Root path of font library
        """
        self.library_path = Path(library_path)
        self.library_path.mkdir(parents=True, exist_ok=True)

    def organize_font(
        self,
        font_files: Dict[str, Path],
        family_name: Optional[str] = None,
        skip_existing: bool = True
    ) -> Path:
        """
        Organize font files into library structure

        Creates structure: library/FamilyName/format/filename.ext

        Args:
            font_files: Dictionary mapping format to file path
            family_name: Font family name (auto-detected if None)
            skip_existing: Skip if font already exists

        Returns:
            Path to font family directory

        Raises:
            ValueError: If no font files provided
        """
        if not font_files:
            raise ValueError("No font files provided")

        # Auto-detect family name from first file if not provided
        if family_name is None:
            first_file = next(iter(font_files.values()))
            family_name = self._extract_family_name(first_file)

        # Normalize family name for directory
        family_dir_name = self._normalize_name(family_name)
        family_path = self.library_path / family_dir_name

        logger.info(f"Organizing font family: {family_name}")

        # Create family directory
        family_path.mkdir(parents=True, exist_ok=True)

        # Organize each format
        for fmt, source_path in font_files.items():
            self._organize_format(family_path, fmt, source_path, skip_existing)

        logger.info(f"Font organized to: {family_path}")
        return family_path

    def _organize_format(
        self,
        family_path: Path,
        fmt: str,
        source_path: Path,
        skip_existing: bool
    ) -> None:
        """
        Organize a single format file

        Args:
            family_path: Path to font family directory
            fmt: Format name (ttf, otf, woff2)
            source_path: Source file path
            skip_existing: Skip if file already exists
        """
        # Create format subdirectory
        format_dir = family_path / fmt
        format_dir.mkdir(exist_ok=True)

        # Destination path
        dest_path = format_dir / source_path.name

        # Check if exists
        if dest_path.exists() and skip_existing:
            logger.info(f"Skipping existing file: {dest_path.name}")
            return

        # Copy file to library
        try:
            shutil.copy2(source_path, dest_path)
            logger.debug(f"Copied {source_path.name} to {format_dir}")
        except Exception as e:
            logger.error(f"Failed to copy {source_path.name}: {e}")
            raise

    def _extract_family_name(self, font_path: Path) -> str:
        """
        Extract font family name from filename

        Examples:
            AgencyFB-Bold.ttf -> AgencyFB
            Helvetica-BoldItalic.otf -> Helvetica
            Arial.ttf -> Arial

        Args:
            font_path: Path to font file

        Returns:
            Extracted family name
        """
        # Get filename without extension
        name = font_path.stem

        # Remove common weight/style suffixes
        patterns = [
            r'-?(Bold|Regular|Light|Medium|SemiBold|ExtraBold|Black|Thin|Ultra)',
            r'-?(Italic|Oblique|Inclined)',
            r'-?(Condensed|Extended|Narrow|Wide)',
            r'-?\d+',  # Remove numbers
        ]

        for pattern in patterns:
            name = re.sub(pattern, '', name, flags=re.IGNORECASE)

        # Clean up any trailing hyphens or underscores
        name = name.rstrip('-_')

        return name or font_path.stem  # Fallback to original if empty

    def _normalize_name(self, name: str) -> str:
        """
        Normalize name for directory usage

        Args:
            name: Font family name

        Returns:
            Normalized directory name
        """
        # Remove special characters except hyphens and underscores
        normalized = re.sub(r'[^\w\s-]', '', name)

        # Replace spaces with hyphens
        normalized = re.sub(r'\s+', '-', normalized)

        # Remove consecutive hyphens
        normalized = re.sub(r'-+', '-', normalized)

        return normalized.strip('-_')

    def get_family_path(self, family_name: str) -> Optional[Path]:
        """
        Get path to font family directory if it exists

        Args:
            family_name: Font family name

        Returns:
            Path to family directory, or None if doesn't exist
        """
        family_dir_name = self._normalize_name(family_name)
        family_path = self.library_path / family_dir_name

        if family_path.exists() and family_path.is_dir():
            return family_path
        return None

    def list_families(self) -> List[str]:
        """
        List all font families in library

        Returns:
            List of font family names
        """
        if not self.library_path.exists():
            return []

        families = []
        for item in self.library_path.iterdir():
            if item.is_dir() and not item.name.startswith('.'):
                families.append(item.name)

        return sorted(families)

    def get_family_info(self, family_name: str) -> Dict[str, List[str]]:
        """
        Get information about a font family

        Args:
            family_name: Font family name

        Returns:
            Dictionary mapping format to list of font files
        """
        family_path = self.get_family_path(family_name)
        if not family_path:
            return {}

        info = {}
        for fmt in ['ttf', 'otf', 'woff2']:
            format_dir = family_path / fmt
            if format_dir.exists():
                files = [f.name for f in format_dir.glob(f'*.{fmt}')]
                if files:
                    info[fmt] = sorted(files)

        return info

    def validate_structure(self) -> Dict[str, List[str]]:
        """
        Validate library structure and report issues

        Returns:
            Dictionary of issues found
        """
        issues = {
            'missing_formats': [],
            'empty_directories': [],
            'invalid_files': []
        }

        for family in self.list_families():
            family_path = self.library_path / family
            formats_found = []

            for fmt in ['ttf', 'otf', 'woff2']:
                format_dir = family_path / fmt
                if format_dir.exists():
                    files = list(format_dir.glob(f'*.{fmt}'))
                    if files:
                        formats_found.append(fmt)
                    else:
                        issues['empty_directories'].append(str(format_dir))

            # Check if any formats are missing
            if len(formats_found) < 3:
                missing = set(['ttf', 'otf', 'woff2']) - set(formats_found)
                issues['missing_formats'].append({
                    'family': family,
                    'missing': list(missing)
                })

        return issues
