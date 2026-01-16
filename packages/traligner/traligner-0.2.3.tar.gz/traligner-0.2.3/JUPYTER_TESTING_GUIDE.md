# Development Testing Guide for TRAligner in Jupyter Notebook

## The Problem

After restructuring to the `src/` layout, the old import method doesn't work:
```python
import TRAligner as ta  # ❌ This no longer works!
```

## Solution Options

### Option 1: Import from the package name (Recommended)

The package is now called `traligner` (lowercase), not `TRAligner`:

```python
# Import the package
import traligner as ta

# Or import specific functions
from traligner import alignment, smith_waterman_alignment

# Use it
alignment_sequences, df_suspect_alignment, suspect_matrix, source_matrix = ta.alignment(
    suspect_t,
    src_t, 
    match_score=3, 
    mismatch_score=1,
    methods=methods_t
)
```

### Option 2: Add src/ to Python path (For Development Testing)

If you want to test without installing, add this at the top of your notebook:

```python
import sys
import os

# Add the src directory to Python path
traligner_path = '/Users/hadarmiller/Dropbox (University of Haifa)/HaifaU/10_Text_Reuse/Data Bases And Systems/Framwork/Modules/TRAligner/src'
if traligner_path not in sys.path:
    sys.path.insert(0, traligner_path)

# Now import as traligner (not TRAligner)
import traligner as ta

# Or import specific functions
from traligner import alignment, smith_waterman_alignment
```

### Option 3: Install in Editable Mode (Best for Development)

This allows you to edit the code and have changes immediately available:

```bash
# In terminal
cd /Users/hadarmiller/Dropbox\ \(University\ of\ Haifa\)/HaifaU/10_Text_Reuse/Data\ Bases\ And\ Systems/Framwork/Modules/TRAligner

# Install in editable mode
pip install -e .
```

Then in your notebook:
```python
# Simple import
import traligner as ta

# Use it
result = ta.alignment(suspect_t, src_t, match_score=3, mismatch_score=1, methods=methods_t)
```

## Complete Jupyter Notebook Example

Here's a complete cell-by-cell example:

### Cell 1: Setup Python Path (Option 2)
```python
import sys
import os

# Add TRAligner src to path
traligner_src = '/Users/hadarmiller/Dropbox (University of Haifa)/HaifaU/10_Text_Reuse/Data Bases And Systems/Framwork/Modules/TRAligner/src'
if traligner_src not in sys.path:
    sys.path.insert(0, traligner_src)

print("✓ TRAligner src added to path")
```

### Cell 2: Import TRAligner
```python
# Import as traligner (new package name)
import traligner as ta

# Check version
print(f"TRAligner version: {ta.__version__}")

# Check available functions
print(f"Available functions: {[x for x in dir(ta) if not x.startswith('_')][:5]}")
```

### Cell 3: Your Alignment Code
```python
# Your existing code - just change TRAligner to traligner
suspect_t = ["word1", "word2", "word3"]
src_t = ["word1", "word2", "word3"]

methods_t = {
    "extra_seperators": [""],
    "missing_seperators": [""],
}

# This now works!
alignment_sequences, df_suspect_alignment, suspect_matrix, source_matrix = ta.alignment(
    suspect_t,
    src_t, 
    match_score=3, 
    mismatch_score=1,
    methods=methods_t
)

print("✓ Alignment completed successfully")
```

## Key Changes Summary

| Old (Before Migration) | New (After Migration) |
|------------------------|----------------------|
| `import TRAligner as ta` | `import traligner as ta` |
| Package directory: `TRAligner/` | Package directory: `TRAligner/` |
| Code location: `TRAligner/*.py` | Code location: `TRAligner/src/traligner/*.py` |
| Package name: `TRAligner` | Package name: `traligner` |

## Why the Change?

1. **Professional naming**: Python packages use lowercase names (e.g., `numpy`, `pandas`, not `NumPy`, `Pandas`)
2. **src/ layout**: Better separation between package code and development files
3. **PyPI standards**: Following Python packaging best practices

## Troubleshooting

### Error: `ModuleNotFoundError: No module named 'traligner'`

**Solution A**: Use the path insertion method (Option 2 above)

**Solution B**: Install in editable mode:
```bash
cd TRAligner
pip install -e .
```

### Error: `AttributeError: module 'traligner' has no attribute 'alignment'`

**Check 1**: Make sure you imported `traligner`, not `TRAligner`
```python
import traligner as ta  # ✓ Correct
import TRAligner as ta  # ✗ Wrong
```

**Check 2**: Verify the function is exported in `__init__.py`
```python
# This should work
print(dir(ta))
```

### Error: `ModuleNotFoundError: No module named 'pandas'`

Install dependencies:
```bash
pip install pandas numpy python-Levenshtein
```

Or install with all dependencies:
```bash
cd TRAligner
pip install -e .
```

## Quick Reference

**For quick testing in Jupyter (no installation):**
```python
import sys
sys.path.insert(0, '/Users/hadarmiller/Dropbox (University of Haifa)/HaifaU/10_Text_Reuse/Data Bases And Systems/Framwork/Modules/TRAligner/src')
import traligner as ta
```

**For proper development:**
```bash
# Terminal
cd TRAligner
pip install -e .
```

```python
# Jupyter
import traligner as ta
```

## Migration Checklist for Your Notebooks

- [ ] Change `import TRAligner as ta` → `import traligner as ta`
- [ ] Add path insertion cell at the top (if not using pip install)
- [ ] Update any hardcoded references from `TRAligner` to `traligner`
- [ ] Test all functions work correctly
- [ ] Update notebook documentation/comments

---

**Remember**: The package name is now `traligner` (lowercase), but the directory is still `TRAligner` (with capital letters). This is normal and follows Python conventions!
