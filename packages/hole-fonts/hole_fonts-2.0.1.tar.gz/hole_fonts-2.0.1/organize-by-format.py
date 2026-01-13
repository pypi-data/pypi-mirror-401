#!/usr/bin/env python3
"""
Organize flat font directory into folders by file type

Usage:
    python organize-by-format.py <source-directory> [output-directory]

Example:
    python organize-by-format.py hole-fonts-output/ organized-fonts/
"""

import sys
import shutil
from pathlib import Path
from collections import defaultdict


def organize_by_format(source_dir: Path, output_dir: Path = None):
    """
    Organize fonts from flat directory into format-based folders

    Creates:
        output/
        ├── TTF/
        ├── OTF/
        └── WOFF2/
    """
    source_dir = Path(source_dir)

    if output_dir is None:
        output_dir = source_dir.parent / f"{source_dir.name}-organized"
    else:
        output_dir = Path(output_dir)

    if not source_dir.exists():
        print(f"❌ Error: Source directory not found: {source_dir}")
        sys.exit(1)

    print(f"📁 Organizing fonts from: {source_dir}")
    print(f"📁 Output to: {output_dir}")
    print()

    # Create format directories
    format_dirs = {
        'ttf': output_dir / 'TTF',
        'otf': output_dir / 'OTF',
        'woff2': output_dir / 'WOFF2',
        'woff': output_dir / 'WOFF'
    }

    for format_dir in format_dirs.values():
        format_dir.mkdir(parents=True, exist_ok=True)

    # Collect files by format
    stats = defaultdict(int)
    errors = []

    print("🔄 Organizing files...")

    for font_file in source_dir.iterdir():
        if not font_file.is_file():
            continue

        # Get file extension
        ext = font_file.suffix.lower().lstrip('.')

        if ext not in format_dirs:
            continue

        # Destination
        dest_dir = format_dirs[ext]
        dest_path = dest_dir / font_file.name

        try:
            # Copy file
            shutil.copy2(font_file, dest_path)
            stats[ext.upper()] += 1

            # Progress indicator
            if stats[ext.upper()] % 100 == 0:
                print(f"  {ext.upper()}: {stats[ext.upper()]} files...", end='\r')

        except Exception as e:
            errors.append(f"{font_file.name}: {e}")

    # Summary
    print("\n")
    print("✅ Organization Complete!")
    print()
    print("📊 Summary:")
    for fmt in ['TTF', 'OTF', 'WOFF2', 'WOFF']:
        if fmt in stats:
            print(f"  {fmt}: {stats[fmt]:,} files")

    print()
    print(f"📁 Output: {output_dir}")

    if errors:
        print(f"\n⚠️  {len(errors)} errors occurred:")
        for error in errors[:10]:  # Show first 10
            print(f"  - {error}")
        if len(errors) > 10:
            print(f"  ... and {len(errors) - 10} more")

    return output_dir


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python organize-by-format.py <source-directory> [output-directory]")
        print()
        print("Example:")
        print("  python organize-by-format.py hole-fonts-output/")
        print("  python organize-by-format.py hole-fonts-output/ organized-fonts/")
        sys.exit(1)

    source = sys.argv[1]
    output = sys.argv[2] if len(sys.argv) > 2 else None

    organize_by_format(source, output)
