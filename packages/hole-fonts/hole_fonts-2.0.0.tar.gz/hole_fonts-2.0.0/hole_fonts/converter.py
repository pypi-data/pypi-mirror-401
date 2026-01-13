"""Font conversion module for HOLE Fonts"""

import logging
from pathlib import Path
from typing import Dict, Optional, List
from fontTools.ttLib import TTFont
from fontTools.ttLib.ttFont import TTLibError


logger = logging.getLogger(__name__)


class VariableFontInfo:
    """Information about a variable font"""

    def __init__(self, axes: List[Dict], instances: List[str]):
        self.axes = axes
        self.instances = instances
        self.is_variable = True

    def __repr__(self):
        axis_names = [f"{ax['tag']} ({ax['min']}-{ax['max']})" for ax in self.axes]
        return f"Variable Font: {', '.join(axis_names)}"


class FontConverter:
    """Handle font format conversions"""

    VALID_INPUT_FORMATS = {'.ttf', '.otf', '.woff', '.woff2'}
    OUTPUT_FORMATS = {'ttf', 'otf', 'woff2'}

    def __init__(self, output_dir: Optional[Path] = None):
        """
        Initialize converter

        Args:
            output_dir: Directory for temporary conversion output
        """
        self.output_dir = output_dir or Path('Output')
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def convert(self, input_path: Path, output_formats: Optional[list] = None) -> Dict[str, Path]:
        """
        Convert font to multiple formats

        Args:
            input_path: Path to input font file
            output_formats: List of formats to generate (default: ['ttf', 'otf', 'woff2'])

        Returns:
            Dictionary mapping format to output path

        Raises:
            FileNotFoundError: If input file doesn't exist
            ValueError: If input format is not supported
            TTLibError: If font conversion fails
        """
        if not input_path.exists():
            raise FileNotFoundError(f"Font file not found: {input_path}")

        if input_path.suffix.lower() not in self.VALID_INPUT_FORMATS:
            raise ValueError(f"Unsupported input format: {input_path.suffix}")

        output_formats = output_formats or list(self.OUTPUT_FORMATS)
        results = {}

        logger.info(f"Converting {input_path.name} to formats: {output_formats}")

        try:
            # Load the font
            font = TTFont(input_path)

            # Check if variable font
            var_font_info = self._detect_variable_font(font)
            if var_font_info:
                logger.info(f"🎨 Variable font detected: {var_font_info}")
                results['variable_font_info'] = var_font_info

            # Get base name without extension
            base_name = input_path.stem

            # Convert to each requested format
            for fmt in output_formats:
                if fmt not in self.OUTPUT_FORMATS:
                    logger.warning(f"Skipping unsupported format: {fmt}")
                    continue

                output_path = self._convert_to_format(font, base_name, fmt)
                if output_path:
                    results[fmt] = output_path
                    logger.info(f"Created {fmt.upper()}: {output_path.name}")

            font.close()

        except TTLibError as e:
            logger.error(f"Failed to convert {input_path.name}: {e}")
            raise

        return results

    def _detect_variable_font(self, font: TTFont) -> Optional[VariableFontInfo]:
        """
        Detect if font is a variable font and extract axis information

        Args:
            font: Loaded TTFont instance

        Returns:
            VariableFontInfo if variable font, None otherwise
        """
        # Check for fvar table (font variations)
        if 'fvar' not in font:
            return None

        try:
            fvar = font['fvar']
            axes = []
            instances = []

            # Extract axis information
            for axis in fvar.axes:
                axes.append({
                    'tag': axis.axisTag,
                    'name': font['name'].getDebugName(axis.axisNameID) if 'name' in font else axis.axisTag,
                    'min': axis.minValue,
                    'default': axis.defaultValue,
                    'max': axis.maxValue
                })

            # Extract named instances
            for instance in fvar.instances:
                instance_name = font['name'].getDebugName(instance.subfamilyNameID) if 'name' in font else f"Instance {instance.subfamilyNameID}"
                instances.append(instance_name)

            return VariableFontInfo(axes=axes, instances=instances)

        except Exception as e:
            logger.warning(f"Error extracting variable font info: {e}")
            return None

    def _convert_to_format(self, font: TTFont, base_name: str, fmt: str) -> Optional[Path]:
        """
        Convert font to specific format

        Args:
            font: Loaded TTFont instance
            base_name: Base filename without extension
            fmt: Target format ('ttf', 'otf', or 'woff2')

        Returns:
            Path to converted file, or None if conversion failed
        """
        output_path = self.output_dir / f"{base_name}.{fmt}"

        try:
            if fmt == 'woff2':
                # Save as WOFF2
                font.flavor = 'woff2'
                font.save(output_path)
                font.flavor = None  # Reset flavor
            elif fmt == 'ttf':
                # Save as TrueType
                # Note: If source is OTF (CFF), this may need cu2qu for curve conversion
                # For now, we'll save as-is and handle conversion issues later
                if output_path.exists():
                    output_path.unlink()
                font.save(output_path)
            elif fmt == 'otf':
                # Save as OpenType
                if output_path.exists():
                    output_path.unlink()
                font.save(output_path)

            return output_path

        except Exception as e:
            logger.error(f"Failed to convert to {fmt.upper()}: {e}")
            return None

    def convert_to_ttf(self, input_path: Path) -> Path:
        """Convert font to TTF format"""
        results = self.convert(input_path, ['ttf'])
        return results['ttf']

    def convert_to_otf(self, input_path: Path) -> Path:
        """Convert font to OTF format"""
        results = self.convert(input_path, ['otf'])
        return results['otf']

    def convert_to_woff2(self, input_path: Path) -> Path:
        """Convert font to WOFF2 format"""
        results = self.convert(input_path, ['woff2'])
        return results['woff2']

    @staticmethod
    def validate_font(font_path: Path) -> bool:
        """
        Validate that a font file can be loaded

        Args:
            font_path: Path to font file

        Returns:
            True if font is valid, False otherwise
        """
        try:
            font = TTFont(font_path)
            font.close()
            return True
        except Exception as e:
            logger.warning(f"Font validation failed for {font_path.name}: {e}")
            return False

    @staticmethod
    def is_variable_font(font_path: Path) -> bool:
        """
        Quick check if font is a variable font

        Args:
            font_path: Path to font file

        Returns:
            True if variable font, False otherwise
        """
        try:
            font = TTFont(font_path)
            is_var = 'fvar' in font
            font.close()
            return is_var
        except Exception:
            return False
