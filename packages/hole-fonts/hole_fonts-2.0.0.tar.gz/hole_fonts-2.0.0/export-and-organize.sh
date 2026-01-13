#!/bin/bash
# HOLE Fonts - Export and Organize by Format
# Converts fonts and organizes them into TTF/, OTF/, WOFF2/ folders

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║       HOLE Fonts - Export & Organize by Format                ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Check arguments
if [ "$#" -lt 2 ]; then
    echo -e "${RED}Usage: $0 <input-directory> <output-directory>${NC}"
    echo ""
    echo "Example:"
    echo "  $0 Input/Organized-Folders/ /Volumes/RAID/HOLE-Fonts/"
    echo ""
    exit 1
fi

INPUT_DIR="$1"
OUTPUT_DIR="$2"
TEMP_DIR="${OUTPUT_DIR}-temp"

echo -e "${BLUE}Input:${NC}  $INPUT_DIR"
echo -e "${BLUE}Output:${NC} $OUTPUT_DIR"
echo ""

# Step 1: Export fonts to temp directory
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}Step 1: Converting fonts...${NC}"
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

uv run python -m hole_fonts.cli export "$INPUT_DIR" --to "$TEMP_DIR" --structure single-flat

if [ $? -ne 0 ]; then
    echo -e "${RED}✗ Export failed${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}✓ Conversion complete${NC}"
echo ""

# Step 2: Organize by format
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}Step 2: Organizing by format...${NC}"
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

python3 organize-by-format.py "$TEMP_DIR" "$OUTPUT_DIR"

if [ $? -ne 0 ]; then
    echo -e "${RED}✗ Organization failed${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}✓ Organization complete${NC}"
echo ""

# Step 3: Cleanup temp directory
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}Step 3: Cleaning up...${NC}"
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

echo "Removing temporary directory: $TEMP_DIR"
rm -rf "$TEMP_DIR"

echo ""
echo -e "${GREEN}✓ Cleanup complete${NC}"
echo ""

# Step 4: Verify structure
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}Verification${NC}"
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

echo "Directory structure:"
ls -lh "$OUTPUT_DIR"
echo ""

echo "File counts:"
for dir in TTF OTF WOFF2; do
    if [ -d "$OUTPUT_DIR/$dir" ]; then
        count=$(ls "$OUTPUT_DIR/$dir" | wc -l | tr -d ' ')
        size=$(du -sh "$OUTPUT_DIR/$dir" | cut -f1)
        echo "  $dir: $count files ($size)"
    fi
done

echo ""
echo -e "${GREEN}╔════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║                    Export Complete!                            ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${BLUE}📁 Library Location:${NC} $OUTPUT_DIR"
echo ""
echo -e "${BLUE}Usage:${NC}"
echo "  Web fonts:     $OUTPUT_DIR/WOFF2/"
echo "  Desktop fonts: $OUTPUT_DIR/TTF/"
echo "  Print fonts:   $OUTPUT_DIR/OTF/"
echo ""
