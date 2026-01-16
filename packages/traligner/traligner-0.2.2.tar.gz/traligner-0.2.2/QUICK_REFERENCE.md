# TRAligner Quick Reference

## Package Information
- **Name**: traligner
- **Version**: 0.2.0
- **Location**: `/Users/hadarmiller/Dropbox (University of Haifa)/HaifaU/10_Text_Reuse/Data Bases And Systems/Framwork/Modules/TRAligner/`
- **GitHub**: https://github.com/millerhadar/traligner
- **License**: MIT

## Directory Structure
```
TRAligner/
├── src/traligner/          # Main package (import from here)
├── tests/                  # Test suite
├── setup.py               # Package metadata
├── pyproject.toml         # Modern packaging
├── CHANGELOG.md           # Version history
└── LICENSE                # MIT License
```

## Quick Commands

### Development
```bash
cd TRAligner/

# Edit source code
nano src/traligner/text_alignment_clean.py

# Run tests
pytest tests/

# Check imports
python -c "import sys; sys.path.insert(0, 'src'); import traligner"
```

### Git Operations
```bash
# Check status
git status

# Commit changes
git add .
git commit -m "Description of changes"

# Push to GitHub
git push origin main

# Tag new version
git tag -a v0.3.0 -m "Version 0.3.0"
git push origin --tags
```

### Publishing New Version

**1. Update version number:**
```bash
# Edit these files:
nano setup.py              # Change version="0.2.0" to version="0.3.0"
nano pyproject.toml        # Change version = "0.2.0" to version = "0.3.0"
nano src/traligner/__init__.py  # Change __version__ = "0.2.0" to "0.3.0"
```

**2. Update changelog:**
```bash
nano CHANGELOG.md
# Add new section:
## [0.3.0] - 2025-XX-XX
### Added
- New feature description
### Fixed
- Bug fix description
```

**3. Build and publish:**
```bash
# Clean previous builds
rm -rf dist/ build/ src/*.egg-info

# Build
python3 -m build

# Test on TestPyPI
python3 -m twine upload --repository testpypi dist/*

# Publish to PyPI
python3 -m twine upload dist/*
```

**4. Git tag:**
```bash
git add setup.py pyproject.toml src/traligner/__init__.py CHANGELOG.md
git commit -m "Bump version to 0.3.0"
git tag -a v0.3.0 -m "Version 0.3.0"
git push origin main --tags
```

## Installation (for users)

After publishing to PyPI:
```bash
pip install traligner
```

Local development installation:
```bash
cd TRAligner/
pip install -e .
```

## Import Examples

```python
# Import main functions
from traligner import alignment, smith_waterman_alignment

# Or import everything
import traligner

# Check version
print(traligner.__version__)  # 0.2.0
```

## Common Tasks

### Adding a new function
1. Edit `src/traligner/text_alignment_clean.py` or `alignment_tools.py`
2. Add function name to `src/traligner/__init__.py` exports
3. Add tests to `tests/test_alignment.py`
4. Update `API_REFERENCE.md` with documentation

### Fixing a bug
1. Create branch: `git checkout -b fix/bug-description`
2. Fix the bug in `src/traligner/`
3. Add test to prevent regression
4. Commit: `git commit -m "Fix: description"`
5. Merge to main and push

### Running tests
```bash
# All tests
pytest tests/

# Specific test
pytest tests/test_alignment.py::test_alignment_and_scoring

# With coverage
pytest tests/ --cov=traligner
```

## Troubleshooting

**Import errors:**
```bash
# Make sure you're in the right directory
pwd  # Should end with /TRAligner

# Check Python can find the package
python -c "import sys; sys.path.insert(0, 'src'); import traligner"
```

**Git issues:**
```bash
# Check remote
git remote -v

# Reset if needed
git reset --hard origin/main

# Check history
git log --oneline
```

**Build errors:**
```bash
# Clean everything
rm -rf dist/ build/ src/*.egg-info __pycache__ src/traligner/__pycache__

# Try building again
python3 -m build
```

## Important Notes

✅ **Always develop in `TRAligner/` directory** (not in published/ or archive/)
✅ **Source code is in `src/traligner/`** (not in root)
✅ **Tests go in `tests/`** directory
✅ **Update CHANGELOG.md** for every release
✅ **Tag releases in Git** with `v` prefix (v0.2.0, v0.3.0, etc.)
✅ **Test on TestPyPI first** before production PyPI

## Backup Locations

- Current: `../backups/TRAligner_backup_20251106/`
- Old published: `../archive/TRAlignerP_v0.1.0_20251106/`

## Resources

- README.md - User documentation
- API_REFERENCE.md - Complete API docs
- CHANGELOG.md - Version history
- MIGRATION_SUMMARY.md - Migration details
- setup.py - Package configuration
- pyproject.toml - Modern packaging config
