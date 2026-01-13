"""Font metadata extraction and analysis module"""

import hashlib
import logging
from pathlib import Path
from typing import Optional, List, Dict, Any
from dataclasses import dataclass, asdict
from fontTools.ttLib import TTFont


logger = logging.getLogger(__name__)


@dataclass
class VariableAxis:
    """Information about a variable font axis"""
    tag: str
    name: str
    min_value: float
    default_value: float
    max_value: float


@dataclass
class FontMetadata:
    """Complete metadata for a font file"""

    # File information
    filename: str
    file_path: str
    file_size: int
    file_hash: str
    format: str  # ttf, otf, woff2

    # Font names
    postscript_name: Optional[str]
    family_name: Optional[str]
    full_name: Optional[str]

    # Style attributes
    weight: Optional[int]  # 100-900
    width: Optional[str]  # normal, condensed, extended
    italic: bool

    # Variable font data
    is_variable: bool
    axes: Optional[List[VariableAxis]]

    # Font metrics
    glyph_count: Optional[int]
    character_set_size: Optional[int]

    # Design metrics
    units_per_em: Optional[int]
    ascender: Optional[int]
    descender: Optional[int]
    cap_height: Optional[int]
    x_height: Optional[int]

    # Designer/Foundry metadata (from name table)
    designer: Optional[str]
    foundry: Optional[str]
    copyright: Optional[str]
    description: Optional[str]
    vendor_url: Optional[str]
    designer_url: Optional[str]

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        data = asdict(self)
        # Convert VariableAxis dataclasses to dicts
        if self.axes:
            data['axes'] = [asdict(axis) for axis in self.axes]
        return data


class FontAnalyzer:
    """Extract metadata from font files"""

    def __init__(self):
        self.cache = {}

    def analyze_font(self, font_path: Path) -> Optional[FontMetadata]:
        """
        Extract complete metadata from a font file

        Args:
            font_path: Path to font file

        Returns:
            FontMetadata object or None if analysis fails
        """
        try:
            # Check cache
            cache_key = str(font_path)
            if cache_key in self.cache:
                return self.cache[cache_key]

            logger.info(f"Analyzing: {font_path.name}")

            # Load font
            font = TTFont(font_path)

            # Extract metadata
            metadata = FontMetadata(
                filename=font_path.name,
                file_path=str(font_path),
                file_size=font_path.stat().st_size,
                file_hash=self._calculate_file_hash(font_path),
                format=self._detect_format(font_path),

                postscript_name=self._get_postscript_name(font),
                family_name=self._get_family_name(font),
                full_name=self._get_full_name(font),

                weight=self._detect_weight(font),
                width=self._detect_width(font),
                italic=self._detect_italic(font),

                is_variable='fvar' in font,
                axes=self._extract_axes(font) if 'fvar' in font else None,

                glyph_count=len(font.getGlyphOrder()) if hasattr(font, 'getGlyphOrder') else None,
                character_set_size=self._get_character_set_size(font),

                units_per_em=font['head'].unitsPerEm if 'head' in font else None,
                ascender=font['hhea'].ascent if 'hhea' in font else None,
                descender=font['hhea'].descent if 'hhea' in font else None,
                cap_height=self._get_cap_height(font),
                x_height=self._get_x_height(font),

                # Designer/Foundry metadata from name table
                designer=self._get_designer(font),
                foundry=self._get_foundry(font),
                copyright=self._get_copyright(font),
                description=self._get_description(font),
                vendor_url=self._get_vendor_url(font),
                designer_url=self._get_designer_url(font),
            )

            font.close()

            # Cache result
            self.cache[cache_key] = metadata

            return metadata

        except Exception as e:
            logger.error(f"Failed to analyze {font_path.name}: {e}")
            return None

    def _calculate_file_hash(self, file_path: Path) -> str:
        """Calculate SHA256 hash of file for duplicate detection"""
        sha256 = hashlib.sha256()

        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(8192), b''):
                sha256.update(chunk)

        return sha256.hexdigest()

    def _detect_format(self, file_path: Path) -> str:
        """Detect font format from extension"""
        ext = file_path.suffix.lower()
        return ext.lstrip('.')

    def _get_postscript_name(self, font: TTFont) -> Optional[str]:
        """Extract PostScript name (name ID 6)"""
        try:
            if 'name' in font:
                return font['name'].getDebugName(6)
        except:
            pass
        return None

    def _get_family_name(self, font: TTFont) -> Optional[str]:
        """Extract family name (name ID 1)"""
        try:
            if 'name' in font:
                return font['name'].getDebugName(1)
        except:
            pass
        return None

    def _get_full_name(self, font: TTFont) -> Optional[str]:
        """Extract full font name (name ID 4)"""
        try:
            if 'name' in font:
                return font['name'].getDebugName(4)
        except:
            pass
        return None

    def _detect_weight(self, font: TTFont) -> Optional[int]:
        """Detect font weight (100-900)"""
        try:
            if 'OS/2' in font:
                return font['OS/2'].usWeightClass
        except:
            pass
        return None

    def _detect_width(self, font: TTFont) -> Optional[str]:
        """Detect font width (normal, condensed, extended)"""
        try:
            if 'OS/2' in font:
                width_class = font['OS/2'].usWidthClass
                width_map = {
                    1: 'ultra-condensed',
                    2: 'extra-condensed',
                    3: 'condensed',
                    4: 'semi-condensed',
                    5: 'normal',
                    6: 'semi-expanded',
                    7: 'expanded',
                    8: 'extra-expanded',
                    9: 'ultra-expanded'
                }
                return width_map.get(width_class, 'normal')
        except:
            pass
        return 'normal'

    def _detect_italic(self, font: TTFont) -> bool:
        """Detect if font is italic"""
        try:
            if 'post' in font:
                return font['post'].italicAngle != 0
        except:
            pass
        return False

    def _extract_axes(self, font: TTFont) -> List[VariableAxis]:
        """Extract variable font axes"""
        axes = []

        try:
            if 'fvar' not in font:
                return axes

            for axis in font['fvar'].axes:
                axis_name = 'name' in font and font['name'].getDebugName(axis.axisNameID) or axis.axisTag

                axes.append(VariableAxis(
                    tag=axis.axisTag,
                    name=axis_name,
                    min_value=axis.minValue,
                    default_value=axis.defaultValue,
                    max_value=axis.maxValue
                ))
        except Exception as e:
            logger.warning(f"Error extracting axes: {e}")

        return axes

    def _get_character_set_size(self, font: TTFont) -> Optional[int]:
        """Get approximate character set size"""
        try:
            if 'cmap' in font:
                # Get best cmap table
                cmap = font.getBestCmap()
                if cmap:
                    return len(cmap)
        except:
            pass
        return None

    def _get_cap_height(self, font: TTFont) -> Optional[int]:
        """Get cap height from OS/2 table"""
        try:
            if 'OS/2' in font:
                return font['OS/2'].sCapHeight
        except:
            pass
        return None

    def _get_x_height(self, font: TTFont) -> Optional[int]:
        """Get x-height from OS/2 table"""
        try:
            if 'OS/2' in font:
                return font['OS/2'].sxHeight
        except:
            pass
        return None

    def _get_designer(self, font: TTFont) -> Optional[str]:
        """Extract designer name from name table (name ID 9)"""
        try:
            if 'name' in font:
                for record in font['name'].names:
                    if record.nameID == 9:
                        value = record.toUnicode().strip()
                        if value:
                            return value
        except:
            pass
        return None

    def _get_foundry(self, font: TTFont) -> Optional[str]:
        """Extract foundry/manufacturer name from name table (name ID 8)"""
        try:
            if 'name' in font:
                for record in font['name'].names:
                    if record.nameID == 8:
                        value = record.toUnicode().strip()
                        if value:
                            return value
        except:
            pass
        return None

    def _get_copyright(self, font: TTFont) -> Optional[str]:
        """Extract copyright notice from name table (name ID 0)"""
        try:
            if 'name' in font:
                for record in font['name'].names:
                    if record.nameID == 0:
                        value = record.toUnicode().strip()
                        if value:
                            return value
        except:
            pass
        return None

    def _get_description(self, font: TTFont) -> Optional[str]:
        """Extract font description from name table (name ID 10)"""
        try:
            if 'name' in font:
                for record in font['name'].names:
                    if record.nameID == 10:
                        value = record.toUnicode().strip()
                        if value:
                            return value
        except:
            pass
        return None

    def _get_vendor_url(self, font: TTFont) -> Optional[str]:
        """Extract vendor URL from name table (name ID 11)"""
        try:
            if 'name' in font:
                for record in font['name'].names:
                    if record.nameID == 11:
                        value = record.toUnicode().strip()
                        if value:
                            return value
        except:
            pass
        return None

    def _get_designer_url(self, font: TTFont) -> Optional[str]:
        """Extract designer URL from name table (name ID 12)"""
        try:
            if 'name' in font:
                for record in font['name'].names:
                    if record.nameID == 12:
                        value = record.toUnicode().strip()
                        if value:
                            return value
        except:
            pass
        return None


class FontDatabase:
    """Manage font metadata database"""

    def __init__(self, db_path: Path):
        self.db_path = db_path
        self.fonts: Dict[str, FontMetadata] = {}

    def scan_directory(self, directory: Path) -> int:
        """
        Scan directory and extract metadata for all fonts

        Args:
            directory: Directory to scan (can have subdirs TTF/, OTF/, WOFF2/)

        Returns:
            Number of fonts scanned
        """
        analyzer = FontAnalyzer()
        count = 0

        # Scan for font files
        patterns = ['**/*.ttf', '**/*.otf', '**/*.woff', '**/*.woff2']

        for pattern in patterns:
            for font_path in directory.glob(pattern):
                metadata = analyzer.analyze_font(font_path)

                if metadata:
                    # Use file hash as key (unique per file)
                    self.fonts[metadata.file_hash] = metadata
                    count += 1

                    if count % 100 == 0:
                        logger.info(f"Scanned {count} fonts...")

        return count

    def save(self) -> None:
        """Save database to JSON file"""
        import json

        data = {
            'version': '0.2.0',
            'total_fonts': len(self.fonts),
            'fonts': [meta.to_dict() for meta in self.fonts.values()]
        }

        with open(self.db_path, 'w') as f:
            json.dump(data, f, indent=2)

        logger.info(f"Saved {len(self.fonts)} fonts to {self.db_path}")

    def load(self) -> None:
        """Load database from JSON file"""
        import json

        if not self.db_path.exists():
            return

        with open(self.db_path, 'r') as f:
            data = json.load(f)

        # Reconstruct FontMetadata objects
        for font_dict in data['fonts']:
            # Convert axes back to VariableAxis objects
            if font_dict.get('axes'):
                font_dict['axes'] = [
                    VariableAxis(**axis) for axis in font_dict['axes']
                ]

            metadata = FontMetadata(**font_dict)
            self.fonts[metadata.file_hash] = metadata

        logger.info(f"Loaded {len(self.fonts)} fonts from {self.db_path}")
