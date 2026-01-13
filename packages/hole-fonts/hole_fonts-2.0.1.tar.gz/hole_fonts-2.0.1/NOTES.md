# HOLE Fonts - Development Notes

## v0.1 - Current Implementation

### Family Name Detection (Simple Approach)

**Current Behavior:**
- When processing a **directory**: Uses the folder name as the family name
  - Example: `Input/AgencyFb/` → All fonts grouped under "AgencyFb"
- When processing a **single file**: Auto-detects family from filename
  - Example: `Input/Helvetica-Bold.ttf` → "Helvetica"

**Rationale:**
- Simple and direct - no complicated logic
- User has full control via folder organization
- Clean and predictable behavior

**Limitations:**
- Doesn't handle mixed folders (multiple families in one directory)
- Requires user to pre-organize fonts by family

### Directory Structure ✓

Each font family has subdirectories for each format:
```
Library/
└── AgencyFb/
    ├── ttf/
    │   ├── Font-Regular.ttf
    │   └── Font-Bold.ttf
    ├── otf/
    │   ├── Font-Regular.otf
    │   └── Font-Bold.otf
    └── woff2/
        ├── Font-Regular.woff2
        └── Font-Bold.woff2
```

## v0.2 - Planned Enhancements

### Smart Family Detection with Metadata

**Goal:** Handle mixed folders intelligently using Adobe Typekit metadata

**Approach:**
1. Query Typekit API for font metadata
2. Get authoritative family name, designer, foundry
3. Use metadata to properly group fonts even from mixed sources
4. Fallback to current logic if metadata unavailable

**Benefits:**
- Handles mixed download folders automatically
- Accurate family grouping based on foundry data
- Enriched metadata stored with fonts
- Better organization of font collections

**Example Workflow:**
```
Input/Downloaded-Fonts/
├── Helvetica-Bold.ttf
├── Arial-Regular.ttf
├── AgencyFB-Light.ttf
└── Times-Italic.ttf
```

With metadata:
1. Query Typekit for each font
2. Discover: Helvetica → Linotype, Arial → Monotype, etc.
3. Auto-organize:
   ```
   Library/
   ├── Helvetica/
   ├── Arial/
   ├── AgencyFB/
   └── Times/
   ```
4. Include metadata.json with designer, foundry, history

### Additional v0.2 Features

- [ ] Metadata enrichment from Typekit API
- [ ] Search fonts by designer, foundry, classification
- [ ] HTML catalog generation
- [ ] Font validation and quality checks
- [ ] Preview/specimen generation

## Design Decisions

### Why defer complex logic to v0.2?

1. **Metadata is authoritative**: Typekit API provides canonical family names
2. **Avoid false positives**: Filename-based detection can be unreliable
3. **Keep v0.1 simple**: Focus on core conversion functionality
4. **Better UX**: User organizes folders now, automation later

### File Organization Philosophy

**v0.1 (Manual):**
- User organizes Input folders by family
- Folder name = Family name
- Simple, explicit, no surprises

**v0.2 (Automated):**
- System queries metadata
- Auto-detects families
- Handles any input structure
- Metadata enrichment included

## Future Considerations

### v0.3 and Beyond

- **License Management**: Track usage rights, restrictions
- **Client Projects**: Link fonts to specific projects
- **Variable Fonts**: Handle font variations properly
- **Subsetting**: Generate optimized subsets for web
- **CSS Generation**: Auto-generate @font-face declarations
- **Integration**: Sync with Figma, Adobe CC, etc.

## Technical Debt

None identified yet - v0.1 is clean foundation

## Questions for Future

1. Should we support multi-library setups? (personal, client, brand)
2. How to handle font versions/updates?
3. Cloud backup/sync strategy?
4. Team collaboration features?

---

**Last Updated:** 2025-12-26
**Current Version:** v0.1.0
**Next Milestone:** v0.2 - Typekit Integration
