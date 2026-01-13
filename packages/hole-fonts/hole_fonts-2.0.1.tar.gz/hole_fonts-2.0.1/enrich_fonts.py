#!/usr/bin/env python3
"""Quick script to enrich fonts with Typekit data"""

import json
from pathlib import Path
from hole_fonts.metadata import FontMetadata, VariableAxis
from hole_fonts.typekit import TypekitClient, TypekitEnricher

# Load database
print("Loading database...")
with open('HOLE-Fonts-RAID-Database.json', 'r') as f:
    data = json.load(f)

# Reconstruct FontMetadata objects
fonts = []
for font_dict in data['fonts']:
    # Convert axes back to VariableAxis objects
    if font_dict.get('axes'):
        font_dict['axes'] = [
            VariableAxis(**axis) for axis in font_dict['axes']
        ]
    metadata = FontMetadata(**font_dict)
    fonts.append(metadata)

print(f"Loaded {len(fonts)} fonts")

# Create Typekit client
API_KEY = "459aa874c56344b9c2f44b3a5edde401dc918fca"
client = TypekitClient(API_KEY)
enricher = TypekitEnricher(client)

print("\nEnriching with Typekit data...")
print("This will take ~14 minutes for 1,651 families...\n")

def progress_callback(current, total):
    print(f"  Progress: {current}/{total} fonts ({current*100//total}%)", end='\r')

enrichments = enricher.batch_enrich(fonts, progress_callback=progress_callback)

print(f"\n\n✓ Enriched {len(enrichments)} fonts with Typekit data\n")

# Save enriched database
output_data = {
    'version': '0.2.0',
    'total_fonts': len(fonts),
    'enriched_count': len(enrichments),
    'fonts': [f.to_dict() for f in fonts],
    'enrichments': enrichments
}

print("Saving enriched database...")
with open('HOLE-Fonts-RAID-Enriched.json', 'w') as f:
    json.dump(output_data, f, indent=2)

print(f"✓ Saved to HOLE-Fonts-RAID-Enriched.json")
