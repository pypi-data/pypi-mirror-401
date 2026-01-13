#!/bin/bash

# Process all font families in Input/Organized-Folders
# Each subdirectory becomes a separate font family

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

INPUT_DIR="Input/Organized-Folders"
TOTAL=0
SUCCESS=0
FAILED=0
VARIABLE=0

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║          HOLE Fonts - Batch Font Conversion                   ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Count total families
TOTAL=$(find "$INPUT_DIR" -mindepth 1 -maxdepth 1 -type d | wc -l | tr -d ' ')
echo "Found $TOTAL font families to process"
echo ""

CURRENT=0

# Process each subdirectory
for family_dir in "$INPUT_DIR"/*/; do
    if [ -d "$family_dir" ]; then
        CURRENT=$((CURRENT + 1))
        family_name=$(basename "$family_dir")

        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo "[$CURRENT/$TOTAL] Processing: $family_name"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

        # Count fonts in this family
        font_count=$(find "$family_dir" \( -name "*.ttf" -o -name "*.otf" -o -name "*.woff" -o -name "*.woff2" \) | wc -l | tr -d ' ')
        echo "  Fonts in family: $font_count"

        # Process the family
        if uv run python -m hole_fonts.cli convert "$family_dir" 2>&1 | grep -q "Variable"; then
            VARIABLE=$((VARIABLE + 1))
            echo "  🎨 Variable font detected!"
        fi

        # Check if successful
        if [ ${PIPESTATUS[0]} -eq 0 ]; then
            SUCCESS=$((SUCCESS + 1))
            echo "  ✓ Success"
        else
            FAILED=$((FAILED + 1))
            echo "  ✗ Failed"
        fi

        echo ""
    fi
done

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                    Batch Conversion Complete                  ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
echo "Summary:"
echo "  Total families processed: $TOTAL"
echo "  Successful: $SUCCESS"
echo "  Failed: $FAILED"
echo "  Variable fonts found: $VARIABLE"
echo ""
echo "View library: uv run python -m hole_fonts.cli list"
echo ""
