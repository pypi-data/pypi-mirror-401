#!/bin/bash

# HOLE Fonts - Convert Font Library to Webfont Library
# Source: /Users/jth/Documents/HOLE-Fonttools-Project/HOLE-Font-Library
# Destination: iCloud/HOLE-Foundation-Stuff/Brand/Fonts/Webfont-Library

SOURCE="/Users/jth/Documents/HOLE-Fonttools-Project/HOLE-Font-Library"
DEST="/Volumes/80F9F6D9-7BEF-4B9D-BE79-A7E2F900F1ED/Library/Daemon Containers/85C492CA-B246-4619-9E1D-E222C06C5FC9/Data/Library/Mobile Documents/com~apple~CloudDocs/HOLE-Foundation-Stuff/Brand/Fonts/Webfont-Library"

echo "╭─────────────── HOLE Fonts Webfont Export ───────────────╮"
echo "│ Converting fonts to TTF, OTF, WOFF2                      │"
echo "│                                                          │"
echo "│ Source: HOLE-Font-Library/                              │"
echo "│ Destination: Webfont-Library/                           │"
echo "╰──────────────────────────────────────────────────────────╯"
echo ""

cd /Users/jth/Documents/HOLE-Fonttools-Project

# Run the export command
uv run python -m hole_fonts.cli export "$SOURCE" --to "$DEST"

echo ""
echo "✓ Conversion complete!"
echo "→ Webfonts exported to: $DEST"
