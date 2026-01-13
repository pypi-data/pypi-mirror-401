# HOLE Fonts - Deployment Guide

**For:** File system organization and project deployment
**Structure:** Simple 3-folder format-based organization
**Purpose:** Practical font management for web, desktop, and print projects

---

## Library Structure

### HOLE Foundation Font Library v0.1.0

```
HOLE-Font-Library-v0.1/
├── TTF/          ← 15,808 TrueType fonts (Desktop/Cross-platform)
├── OTF/          ← 15,808 OpenType fonts (Professional/Print)
└── WOFF2/        ← 15,807 Web fonts (Web deployment)
```

**Benefits of this structure:**
- ✅ **Simple:** Just 3 folders
- ✅ **Fast:** Direct file access
- ✅ **Practical:** Pick format needed
- ✅ **Scalable:** Easy R2 upload
- ✅ **No trees:** No complex nesting

---

## Use Cases

### Web Project Deployment

**Need web fonts for your site?**

```bash
# Navigate to WOFF2 folder
cd /Volumes/RAID/HOLE-Fonts/WOFF2/

# Find fonts you need
ls | grep -i helvetica

# Copy to project
cp Helvetica-Bold.woff2 ~/WebProject/public/fonts/
cp Helvetica-Regular.woff2 ~/WebProject/public/fonts/
```

**In your CSS:**
```css
@font-face {
  font-family: 'Helvetica';
  src: url('/fonts/Helvetica-Bold.woff2') format('woff2');
  font-weight: 700;
  font-display: swap;
}
```

### Desktop Font Installation

**Need to install fonts on Mac?**

```bash
# Find desktop font
cd /Volumes/RAID/HOLE-Fonts/TTF/

# List available
ls | grep -i arial

# Install
cp Arial-Bold.ttf ~/Library/Fonts/
```

### Print Project (High Quality)

**Need professional print fonts?**

```bash
# Use OTF for best quality
cd /Volumes/RAID/HOLE-Fonts/OTF/

# Find font
ls | grep -i garamond

# Copy to project
cp Garamond-Regular.otf ~/PrintProject/fonts/
```

### CloudFlare R2 Upload

**Upload entire web font library:**

```bash
# Upload WOFF2 folder to R2 bucket
rclone sync /Volumes/RAID/HOLE-Fonts/WOFF2/ \
  r2:hole-foundation-fonts/webfonts/ \
  --progress

# Result: Global CDN-delivered fonts!
```

---

## Automated Workflow

### Single Command Export + Organize

**Use the combined script:**

```bash
./export-and-organize.sh Input/NewFonts/ /Volumes/RAID/HOLE-Fonts/
```

**What it does:**
1. Converts all fonts (TTF, OTF, WOFF2)
2. Organizes into format folders
3. Cleans up temp files
4. Shows summary

**Result:**
```
/Volumes/RAID/HOLE-Fonts/
├── TTF/      ← All your .ttf files
├── OTF/      ← All your .otf files
└── WOFF2/    ← All your .woff2 files
```

### Manual Two-Step Process

**Step 1: Export**
```bash
uv run python -m hole_fonts.cli export Input/Fonts/ \
  --to /tmp/fonts-temp \
  --structure single-flat
```

**Step 2: Organize**
```bash
python3 organize-by-format.py /tmp/fonts-temp /Volumes/RAID/HOLE-Fonts/
```

---

## Finding Fonts

### Simple grep Search

```bash
# Find all Helvetica fonts in WOFF2
ls /Volumes/RAID/HOLE-Fonts/WOFF2/ | grep -i helvetica

# Find all bold fonts
ls /Volumes/RAID/HOLE-Fonts/WOFF2/ | grep -i bold

# Find specific font
ls /Volumes/RAID/HOLE-Fonts/WOFF2/ | grep -i "arial-bold"
```

### Count Fonts

```bash
# Total web fonts
ls /Volumes/RAID/HOLE-Fonts/WOFF2/ | wc -l

# Total desktop fonts
ls /Volumes/RAID/HOLE-Fonts/TTF/ | wc -l
```

### List by Pattern

```bash
# All sans serif fonts (if in name)
ls /Volumes/RAID/HOLE-Fonts/WOFF2/ | grep -i sans

# All italic fonts
ls /Volumes/RAID/HOLE-Fonts/WOFF2/ | grep -i italic
```

---

## R2 Integration Strategy

### Current Setup (Local)

```
RAID Drive
└── HOLE-Fonts/
    ├── TTF/
    ├── OTF/
    └── WOFF2/
```

### Future Setup (Cloud + Local)

```
CloudFlare R2 Bucket
└── hole-foundation-fonts/
    ├── TTF/     ← Upload from local
    ├── OTF/     ← Upload from local
    └── WOFF2/   ← Upload from local
         ↓
    macFUSE mount
         ↓
/Volumes/HOLE-Fonts-Cloud/ ← Appears as local drive
```

### Upload to R2

**One-time setup:**
```bash
# Install rclone
brew install rclone

# Configure R2 remote
rclone config
# Choose: CloudFlare R2
# Enter access key, secret key
```

**Upload fonts:**
```bash
# Upload all WOFF2 (for web delivery)
rclone sync /Volumes/RAID/HOLE-Fonts/WOFF2/ \
  r2:hole-foundation-fonts/WOFF2/ \
  --progress

# Upload TTF (for desktop)
rclone sync /Volumes/RAID/HOLE-Fonts/TTF/ \
  r2:hole-foundation-fonts/TTF/ \
  --progress
```

### Access Fonts from R2

**Web delivery:**
```html
<!-- Direct R2 URL -->
<link rel="preload"
      href="https://hole-fonts.r2.dev/WOFF2/Helvetica-Bold.woff2"
      as="font"
      type="font/woff2"
      crossorigin>
```

**macFUSE mount:**
```bash
# Mount R2 bucket as local drive
rclone mount r2:hole-foundation-fonts /Volumes/HOLE-Fonts-Cloud --daemon

# Now appears as local folder
cd /Volumes/HOLE-Fonts-Cloud/WOFF2/
```

---

## Version Management

### Current Version

**HOLE Foundation Font Library v0.1.0**
- **Location:** `/Volumes/RAID/HOLE-Fonts/` or `/Volumes/.../HOLE-Font-Library-v0.1/`
- **Created:** December 2025
- **Fonts:** 15,808 per format
- **Total:** 47,423 files

### Future Versions

**When adding new fonts:**

```bash
# Create new version
./export-and-organize.sh Input/NewFonts/ \
  /Volumes/RAID/HOLE-Font-Library-v0.2/

# Or update existing
./export-and-organize.sh Input/NewFonts/ \
  /Volumes/RAID/HOLE-Fonts/
```

**Version tracking:**
- v0.1.0 - Initial library (current)
- v0.2.0 - With metadata
- v0.3.0 - With validation
- v1.0.0 - Production ready

---

## Backup Strategy

### Local Backup

```bash
# Backup to external drive
rsync -av /Volumes/RAID/HOLE-Fonts/ \
  /Volumes/Backup/HOLE-Fonts-v0.1-backup/
```

### Cloud Backup (R2)

```bash
# Full library to R2
rclone sync /Volumes/RAID/HOLE-Fonts/ \
  r2:hole-foundation-fonts-backup/v0.1/ \
  --progress
```

### iCloud (Current)

Already backed up via iCloud path on external drive.

---

## Quick Reference

### Get Web Font
```bash
cp /Volumes/RAID/HOLE-Fonts/WOFF2/FontName.woff2 ~/WebProject/fonts/
```

### Get Desktop Font
```bash
cp /Volumes/RAID/HOLE-Fonts/TTF/FontName.ttf ~/Library/Fonts/
```

### Upload to R2
```bash
rclone sync /Volumes/RAID/HOLE-Fonts/WOFF2/ r2:bucket/WOFF2/
```

### Search for Font
```bash
ls /Volumes/RAID/HOLE-Fonts/WOFF2/ | grep -i "searchterm"
```

---

**Simple. Fast. Practical.** ✨
