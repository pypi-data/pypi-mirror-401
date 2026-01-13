"""Font export module for HOLE Fonts - FontBase integration"""

import logging
import shutil
from pathlib import Path
from typing import Dict, List, Optional
from collections import defaultdict

logger = logging.getLogger(__name__)


class FontExporter:
    """Export converted fonts in FontBase-friendly structure"""

    EXPORT_STRUCTURES = {
        'flat-by-family': 'Family folders with all formats together',
        'format-separated': 'Family folders with format subdirectories',
        'single-flat': 'All fonts in one directory',
    }

    def __init__(self, export_dir: Path, structure: str = 'flat-by-family'):
        """
        Initialize exporter

        Args:
            export_dir: Export directory (watched by font manager)
            structure: Export structure type
        """
        self.export_dir = Path(export_dir)
        self.structure = structure

        if structure not in self.EXPORT_STRUCTURES:
            raise ValueError(f"Invalid structure. Choose from: {list(self.EXPORT_STRUCTURES.keys())}")

    def export_fonts(
        self,
        converted_fonts: Dict[str, Dict[str, Path]],
        family_name: Optional[str] = None
    ) -> Path:
        """
        Export converted fonts to directory

        Args:
            converted_fonts: Dict mapping font base name to {format: path}
            family_name: Optional family name (auto-detected if None)

        Returns:
            Path to exported family directory

        Example:
            converted_fonts = {
                'AgencyFB-Bold': {
                    'ttf': Path('Output/AgencyFB-Bold.ttf'),
                    'otf': Path('Output/AgencyFB-Bold.otf'),
                    'woff2': Path('Output/AgencyFB-Bold.woff2')
                }
            }
        """
        if not converted_fonts:
            raise ValueError("No fonts to export")

        # Auto-detect family if not provided
        if family_name is None:
            family_name = self._detect_family_name(converted_fonts)

        logger.info(f"Exporting {len(converted_fonts)} font(s) from family '{family_name}'")

        # Export based on structure
        if self.structure == 'flat-by-family':
            return self._export_flat_by_family(converted_fonts, family_name)
        elif self.structure == 'format-separated':
            return self._export_format_separated(converted_fonts, family_name)
        elif self.structure == 'single-flat':
            return self._export_single_flat(converted_fonts)

    def _export_flat_by_family(
        self,
        converted_fonts: Dict[str, Dict[str, Path]],
        family_name: str
    ) -> Path:
        """
        Export fonts in flat-by-family structure

        Structure:
            Export/
            └── AgencyFB/
                ├── AgencyFB-Bold.ttf
                ├── AgencyFB-Bold.otf
                ├── AgencyFB-Bold.woff2
                └── ...
        """
        family_dir = self.export_dir / family_name
        family_dir.mkdir(parents=True, exist_ok=True)

        logger.info(f"Exporting to: {family_dir}")

        for font_name, formats in converted_fonts.items():
            for fmt, source_path in formats.items():
                if source_path.exists():
                    dest_path = family_dir / source_path.name
                    self._copy_font(source_path, dest_path)

        logger.info(f"✓ Exported {sum(len(f) for f in converted_fonts.values())} files to {family_dir}")
        return family_dir

    def _export_format_separated(
        self,
        converted_fonts: Dict[str, Dict[str, Path]],
        family_name: str
    ) -> Path:
        """
        Export fonts with format subdirectories

        Structure:
            Export/
            └── AgencyFB/
                ├── OTF/
                │   └── AgencyFB-Bold.otf
                ├── TTF/
                │   └── AgencyFB-Bold.ttf
                └── WOFF2/
                    └── AgencyFB-Bold.woff2
        """
        family_dir = self.export_dir / family_name
        family_dir.mkdir(parents=True, exist_ok=True)

        logger.info(f"Exporting to: {family_dir}")

        # Create format directories
        for fmt in ['TTF', 'OTF', 'WOFF2']:
            fmt_dir = family_dir / fmt
            fmt_dir.mkdir(exist_ok=True)

        for font_name, formats in converted_fonts.items():
            for fmt, source_path in formats.items():
                if source_path.exists():
                    fmt_dir = family_dir / fmt.upper()
                    dest_path = fmt_dir / source_path.name
                    self._copy_font(source_path, dest_path)

        logger.info(f"✓ Exported {sum(len(f) for f in converted_fonts.values())} files to {family_dir}")
        return family_dir

    def _export_single_flat(
        self,
        converted_fonts: Dict[str, Dict[str, Path]]
    ) -> Path:
        """
        Export all fonts to single flat directory

        Structure:
            Export/
            ├── AgencyFB-Bold.ttf
            ├── AgencyFB-Bold.otf
            ├── AgencyFB-Bold.woff2
            └── ...
        """
        self.export_dir.mkdir(parents=True, exist_ok=True)

        logger.info(f"Exporting to: {self.export_dir}")

        for font_name, formats in converted_fonts.items():
            for fmt, source_path in formats.items():
                if source_path.exists():
                    dest_path = self.export_dir / source_path.name
                    self._copy_font(source_path, dest_path)

        logger.info(f"✓ Exported {sum(len(f) for f in converted_fonts.values())} files to {self.export_dir}")
        return self.export_dir

    def _copy_font(self, source: Path, dest: Path) -> None:
        """
        Copy font file to destination

        Args:
            source: Source font file
            dest: Destination path
        """
        try:
            shutil.copy2(source, dest)
            logger.debug(f"Copied: {source.name} → {dest.parent.name}/{dest.name}")
        except Exception as e:
            logger.error(f"Failed to copy {source.name}: {e}")
            raise

    def _detect_family_name(self, converted_fonts: Dict[str, Dict[str, Path]]) -> str:
        """
        Auto-detect family name from font names

        Args:
            converted_fonts: Dictionary of converted fonts

        Returns:
            Detected family name
        """
        if not converted_fonts:
            return "Unknown"

        # Get first font name
        first_font = next(iter(converted_fonts.keys()))

        # Remove common suffixes to get family name
        family = first_font

        # Remove weight/style suffixes
        suffixes = [
            '-Bold', '-Regular', '-Light', '-Medium', '-SemiBold',
            '-ExtraBold', '-Black', '-Thin', '-Italic', '-Oblique',
            '-BoldItalic', '-LightItalic', '-Condensed', '-Extended',
            '-Narrow', '-Wide', '-Compressed', 'Bold', 'Regular',
            'Light', 'Medium', 'Italic'
        ]

        for suffix in suffixes:
            if family.endswith(suffix):
                family = family[:-len(suffix)]
                break

        # Remove number prefixes (like "9866842-")
        if '-' in family:
            parts = family.split('-')
            if parts[0].isdigit():
                family = '-'.join(parts[1:])

        return family.strip('-_') or first_font

    def export_batch(
        self,
        fonts_by_family: Dict[str, Dict[str, Dict[str, Path]]]
    ) -> List[Path]:
        """
        Export multiple font families at once

        Args:
            fonts_by_family: {
                'AgencyFB': {
                    'AgencyFB-Bold': {'ttf': path, 'otf': path, ...},
                    'AgencyFB-Regular': {...}
                },
                'Helvetica': {...}
            }

        Returns:
            List of exported family directories
        """
        exported = []

        for family_name, converted_fonts in fonts_by_family.items():
            try:
                family_dir = self.export_fonts(converted_fonts, family_name)
                exported.append(family_dir)
            except Exception as e:
                logger.error(f"Failed to export family '{family_name}': {e}")
                continue

        logger.info(f"✓ Batch export complete: {len(exported)} families")
        return exported

    def get_export_info(self) -> Dict:
        """Get information about export directory"""
        if not self.export_dir.exists():
            return {
                'exists': False,
                'path': str(self.export_dir),
                'families': 0,
                'total_fonts': 0
            }

        families = [d for d in self.export_dir.iterdir() if d.is_dir()]
        total_fonts = 0

        for family_dir in families:
            if self.structure == 'format-separated':
                for fmt_dir in family_dir.iterdir():
                    if fmt_dir.is_dir():
                        total_fonts += len(list(fmt_dir.glob('*')))
            else:
                total_fonts += len(list(family_dir.glob('*')))

        return {
            'exists': True,
            'path': str(self.export_dir),
            'structure': self.structure,
            'families': len(families),
            'total_fonts': total_fonts,
            'family_names': sorted([f.name for f in families])
        }


def group_fonts_by_family(
    converted_fonts: List[Dict[str, Path]],
    family_names: Optional[List[str]] = None
) -> Dict[str, Dict[str, Dict[str, Path]]]:
    """
    Group converted fonts by family

    Args:
        converted_fonts: List of {format: path} dictionaries
        family_names: Optional list of family names (auto-detect if None)

    Returns:
        Fonts grouped by family
    """
    families = defaultdict(dict)

    for font_dict in converted_fonts:
        # Get font base name (without extension)
        first_path = next(iter(font_dict.values()))
        base_name = first_path.stem

        # Detect family
        exporter = FontExporter(Path('temp'))
        family = exporter._detect_family_name({base_name: font_dict})

        families[family][base_name] = font_dict

    return dict(families)
