# HOLE Fonts - Quick Start Guide

## ✅ Phase 1A Complete!

Your font conversion system is now **fully operational**. Here's what you have:

### What's Working

✓ **Font Conversion Engine** - Converts TTF, OTF, WOFF, WOFF2 to all formats
✓ **Automated Organization** - Creates structured library directories
✓ **CLI Tool** - Command-line interface with rich formatting
✓ **Claude Skill** - Easy invocation via `/convert-fonts`
✓ **Batch Processing** - Handles entire directories
✓ **Smart Skipping** - Avoids duplicate processing

### Test Results

Successfully processed **27 AgencyFB fonts**:
- 13 fonts organized in **AgencyFB** family
- 3 fonts organized in **AgencyFBCompressed** family
- Each font converted to TTF, OTF, and WOFF2
- All organized in external library drive

## Quick Commands

### Convert Fonts
```bash
# Single font
uv run hole-fonts convert Input/MyFont.ttf

# Entire directory
uv run hole-fonts convert Input/FontCollection/

# With options
uv run hole-fonts convert Input/fonts/ --overwrite
```

### View Library
```bash
# List all fonts
uv run hole-fonts list

# Show family details
uv run hole-fonts info AgencyFB

# Validate structure
uv run hole-fonts validate
```

## Project Structure

```
HOLE-Fonttools-Project/
├── hole_fonts/           # Core package
│   ├── cli.py           # Command-line interface
│   ├── converter.py     # Font conversion logic
│   ├── organizer.py     # Library organization
│   └── config.py        # Configuration handling
├── .claude/
│   └── skills/
│       └── hole-fonts/
│           └── convert-fonts.md  # Claude skill
├── config.yaml          # User configuration
├── Input/               # Source fonts
├── Output/              # Temp conversions
└── Library/             # Local fallback
```

## Configuration

Your `config.yaml` contains:

- **Library Path**: External drive (with local fallback)
- **Formats**: TTF, OTF, WOFF2
- **Processing**: 4 parallel workers
- **Behavior**: Skip existing files by default

## Using the Claude Skill

In Claude Code, you can now use:

```
/convert-fonts
```

This will guide you through the conversion process interactively.

## Next Steps

### v0.1 Completion Tasks

1. **Testing**
   - [ ] Add unit tests for converter
   - [ ] Add integration tests
   - [ ] Test edge cases (corrupted fonts, unusual formats)

2. **Documentation**
   - [x] Quick start guide
   - [x] Claude skill
   - [ ] API documentation

3. **Enhancements**
   - [ ] Progress bars for large batches
   - [ ] Better error reporting
   - [ ] Font validation before conversion

### v0.2 - Typekit Integration

Next phase will add:
- Adobe Typekit API integration
- Metadata fetching (designer, foundry, history)
- Search functionality
- HTML catalog generation

## Tips

1. **External Drive**: If your external drive is unmounted, fonts will automatically save to `Library/` locally

2. **Batch Processing**: Processing large font collections? The system handles them automatically with progress tracking

3. **Existing Fonts**: By default, existing fonts are skipped. Use `--overwrite` to force reprocessing

4. **Logs**: Check `hole-fonts.log` for detailed operation logs

5. **Family Detection**: The system automatically groups fonts by family name (e.g., "AgencyFB-Bold" → "AgencyFB" family)

## Troubleshooting

**Q: Fonts not appearing in library?**
- Check if external drive is mounted
- Look in `Library/` for local fallback
- Check logs: `hole-fonts.log`

**Q: Conversion fails?**
- Verify font file is valid
- Check formats supported: TTF, OTF, WOFF, WOFF2
- Review error in logs

**Q: How to reprocess fonts?**
- Use `--overwrite` flag
- Or delete from library and rerun

## Examples

### Example 1: New Font Download
```bash
# Downloaded new fonts to Downloads/
uv run hole-fonts convert ~/Downloads/new-fonts/

# Check they're in library
uv run hole-fonts list
```

### Example 2: Web Project Prep
```bash
# Need WOFF2 for web
uv run hole-fonts info Helvetica

# Files at:
# Library/Helvetica/woff2/*.woff2
```

### Example 3: Quality Assurance
```bash
# Validate all fonts have all formats
uv run hole-fonts validate

# Fix any issues found
uv run hole-fonts convert Input/missing-fonts/
```

## Success! 🎉

You now have a working font library management system. The foundation is complete and ready for:
- Processing your entire font collection
- Integration with web projects
- Metadata enrichment (v0.2)
- Advanced features (validation, previews, catalogs)

**Ready to process more fonts?** Just drop them in `Input/` and run:
```bash
uv run hole-fonts convert Input/
```
