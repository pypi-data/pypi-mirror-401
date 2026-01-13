# HOLE Fonts - Directory Reference

**Critical paths for resuming work after reboot**

---

## Project Directory
```
/Users/jth/Documents/HOLE-Fonttools-Project/
```
**Contains:**
- Python package source code (`hole_fonts/`)
- Project configuration (`pyproject.toml`, `config.yaml`)
- Documentation (this file, PROJECT-STATUS.md, SESSION-MEMORY.md)
- Test databases (*.json files)
- Scripts (`enrich_fonts.py`, etc.)

---

## Font Library Locations

### Primary: RAID Drive (FAST - Use This!)
```
/Volumes/HOLE-RAID-DRIVE/HOLE-Assets/HOLE-Fonts/
├── TTF/     (11,047 fonts)
├── OTF/     (11,047 fonts)
├── WOFF2/   (11,047 fonts)
└── WOFF/    (minimal)
```
**Status:** Scanned ✓
**Database:** `HOLE-Fonts-RAID-Database.json` + `HOLE-Fonts-RAID-Enriched.json`
**Performance:** ~10-20 fonts/second scan speed
**Use for:** Production scans, testing, searches

### Secondary: iCloud Master Library (SLOW - Avoid for Bulk Operations)
```
/Volumes/80F9F6D9-7BEF-4B9D-BE79-A7E2F900F1ED/Library/Daemon Containers/85C492CA-B246-4619-9E1D-E222C06C5FC9/Data/Library/Mobile Documents/com~apple~CloudDocs/HOLE-Font-Library-iCloud/HOLE-Fonts-Master-Claude-Certified/
```
**Contains:** 32,796 fonts (complete master collection)
**Status:** NOT scanned (iCloud sync too slow)
**Performance:** Very slow I/O (stuck during scan attempt)
**Use for:** Individual font access only, not bulk operations

### Test Fonts
```
/Users/jth/Documents/HOLE-Fonttools-Project/Input/
```
**Contains:** 4,241 test fonts
**Status:** Scanned ✓
**Database:** `test-scan.json`
**Use for:** Development testing, quick validation

---

## Output Locations

### Databases (Project Root)
```
/Users/jth/Documents/HOLE-Fonttools-Project/
├── HOLE-Fonts-RAID-Database.json       (8.1 MB - Full metadata)
├── HOLE-Fonts-RAID-Enriched.json       (8.1 MB - With Typekit data)
├── test-scan.json                      (3.1 MB - Test database)
└── dedup-report.json                   (28 KB - Duplicate analysis)
```

### Build Artifacts (Will be created)
```
/Users/jth/Documents/HOLE-Fonttools-Project/dist/
└── hole_fonts-0.2.0-py3-none-any.whl   (Python wheel - not created yet)
```

---

## Claude Desktop Skill Location
```
/Users/jth/.claude/skills/hole-fonts/
├── SKILL.md
└── ... (skill resources)
```
**Package:** `hole-fonts.zip` (for distribution)

---

## Git Repository

### Remote
(Not yet set up - will be added during release)

### Local
```
/Users/jth/Documents/HOLE-Fonttools-Project/.git/
```
**Branch:** main
**Status:** Ready for v0.2.0 commit

---

## Volume Mounting Notes

### If volumes aren't mounted after reboot:

**RAID Drive:**
```bash
# Check if mounted
ls /Volumes/HOLE-RAID-DRIVE

# If not mounted, check Disk Utility or:
diskutil list
diskutil mount "HOLE-RAID-DRIVE"
```

**iCloud UUID Volume:**
```bash
# Usually auto-mounted by macOS
ls /Volumes/80F9F6D9-7BEF-4B9D-BE79-A7E2F900F1ED
```

---

## Quick Commands After Reboot

### Verify Environment
```bash
cd /Users/jth/Documents/HOLE-Fonttools-Project
uv sync
uv run hole-fonts --help
```

### Check Databases
```bash
ls -lh *.json
```

### Verify Font Locations
```bash
# RAID drive (should be fast)
ls /Volumes/HOLE-RAID-DRIVE/HOLE-Assets/HOLE-Fonts/

# iCloud (may be slow)
ls /Volumes/80F9F6D9-7BEF-4B9D-BE79-A7E2F900F1ED/Library/Daemon\ Containers/*/Data/Library/Mobile\ Documents/com~apple~CloudDocs/HOLE-Font-Library-iCloud/
```

### Test Search
```bash
uv run python -c "
import json
db = json.load(open('HOLE-Fonts-RAID-Database.json'))
print(f'Database loaded: {len(db[\"fonts\"]):,} fonts')
print(f'Ready for searches!')
"
```

---

## Relative Paths (from project root)

- Databases: `./HOLE-Fonts-RAID-Database.json`
- Test fonts: `./Input/`
- Output: `./Output/`
- Package: `./hole_fonts/`
- Skill: `~/.claude/skills/hole-fonts/`

---

## Important Notes

1. **Always use RAID drive for bulk operations** - iCloud is too slow
2. **Database files are large** (8+ MB) - don't commit to git
3. **Package needs reinstall after reboot** - run `uv sync --reinstall-package hole-fonts`
4. **Typekit API key is stored in SESSION-MEMORY.md** - use for enrichment
5. **27 unique AgencyFB fonts** - good test case for search functionality

---

**Last scan:** 2025-12-29 06:32 AM
**Next action:** Create v0.2.0 release and push to GitHub
