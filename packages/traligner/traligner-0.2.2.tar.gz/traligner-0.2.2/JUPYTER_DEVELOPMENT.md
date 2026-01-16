# TRAligner Development in Jupyter Notebooks

## The Problem

After restructuring to the `src/` layout, the old way of importing doesn't work:
```python
import TRAligner as ta  # ❌ This fails now
```

## Solutions for Development Testing

### Solution 1: Install in Editable Mode (Recommended)

This is the **best practice** for development. Install the package in editable mode so changes are reflected immediately:

#### Using pip:
```bash
# In terminal, navigate to TRAligner directory
cd "/Users/hadarmiller/Dropbox (University of Haifa)/HaifaU/10_Text_Reuse/Data Bases And Systems/Framwork/Modules/TRAligner"

# Install in editable mode
pip install -e .
```

#### Using pipenv (if you use it):
```bash
cd TRAligner
pipenv install -e .
```

#### Then in Jupyter:
```python
# Now this works!
import traligner as ta

# Or import specific functions
from traligner import alignment, smith_waterman_alignment

# Check version
print(ta.__version__)  # Should show 0.2.0
```

**Benefits:**
- ✅ Changes to source code are immediately available (no reinstall needed)
- ✅ Works like the published package
- ✅ Clean imports: `import traligner`
- ✅ No path manipulation needed

---

### Solution 2: Add to sys.path (Quick Testing)

If you don't want to install, you can add the `src/` directory to Python's path:

```python
import sys
import os

# Add the src directory to the path
traligner_path = "/Users/hadarmiller/Dropbox (University of Haifa)/HaifaU/10_Text_Reuse/Data Bases And Systems/Framwork/Modules/TRAligner/src"
sys.path.insert(0, traligner_path)

# Now you can import
import traligner as ta

# Or import specific functions
from traligner import alignment, smith_waterman_alignment
```

**Benefits:**
- ✅ No installation needed
- ✅ Quick for one-off testing
- ✅ Works in any notebook

**Drawbacks:**
- ⚠️ Need to add path in every notebook
- ⚠️ Path manipulation can be fragile

---

### Solution 3: Use %pip magic (For Notebooks)

Install directly from the notebook:

```python
# In a Jupyter notebook cell
%pip install -e /Users/hadarmiller/Dropbox\ (University\ of\ Haifa)/HaifaU/10_Text_Reuse/Data\ Bases\ And\ Systems/Framwork/Modules/TRAligner

# Then restart kernel and import
import traligner as ta
```

---

## Complete Jupyter Notebook Example

Here's a complete notebook setup for development:

### Cell 1: Install Package (First Time Only)
```python
# Run this once, then restart kernel
%pip install -e /Users/hadarmiller/Dropbox\ (University\ of\ Haifa)/HaifaU/10_Text_Reuse/Data\ Bases\ And\ Systems/Framwork/Modules/TRAligner
```

### Cell 2: Import and Verify
```python
import traligner as ta
import pickle

print(f"✓ TRAligner version: {ta.__version__}")
print(f"✓ Available functions: {[x for x in dir(ta) if not x.startswith('_')]}")
```

### Cell 3: Test Alignment Function
```python
# Your existing test from tests.py
suspect_sequence = ['Tanakh_Torah_Numbers_3_15',
                    'Tanakh_Writings_Psalms_68_7',
                    'Tanakh_Writings_Psalms_68_7',
                    'Tanakh_Torah_Genesis_44_16',
                    'Tanakh_Writings_Psalms_68_7',
                    'Tanakh_Torah_Numbers_3_15',
                    'Tanakh_Torah_Numbers_1_49',
                    'Tanakh_Torah_Exodus_32_26',
                    'Tanakh_Torah_Exodus_32_26',
                    'Tanakh_Torah_Numbers_3_15',
                    'Tanakh_Torah_Genesis_46_27',
                    'Tanakh_Torah_Genesis_46_27',
                    'Tanakh_Torah_Numbers_3_15',
                    'Tanakh_Torah_Numbers_3_15',
                    'Tanakh_Torah_Numbers_3_15',
                    'Tanakh_Torah_Numbers_3_16']

potential_sequence = ['Tanakh_Torah_Numbers_3_15',
                     'Tanakh_Torah_Numbers_1_49',
                     'Tanakh_Torah_Exodus_32_26',
                     'Tanakh_Torah_Exodus_32_26',
                     'Tanakh_Torah_Numbers_3_15',
                     'Tanakh_Torah_Genesis_46_27',
                     'Tanakh_Torah_Numbers_3_15',
                     'Tanakh_Torah_Numbers_3_15',
                     'Tanakh_Torah_Numbers_3_16']

# Align the sequences
als, df_sus_a, sus_m, src_m = ta.alignment(suspect_sequence,
                                           potential_sequence, 
                                           match_score=30,
                                           mismatch_score=1,
                                           methods={"ignore_tokens": ["*"]})

# Simple score
alignment_score = ta.alignmentScore(als, verbose=False)
print("Alignment Simple Score:", alignment_score[0])
```

---

## Reloading Changes During Development

If you modify the source code and want to reload:

### Option A: Restart Kernel (Recommended)
1. Make changes to `src/traligner/text_alignment_clean.py`
2. In Jupyter: Kernel → Restart Kernel
3. Re-run your import cells

### Option B: Use autoreload (Advanced)
```python
# At the top of your notebook
%load_ext autoreload
%autoreload 2

import traligner as ta

# Now changes to source files are automatically reloaded
```

---

## Troubleshooting

### Issue: "No module named 'traligner'"

**Solution 1**: Install in editable mode
```bash
cd TRAligner
pip install -e .
```

**Solution 2**: Add to sys.path
```python
import sys
sys.path.insert(0, '/Users/hadarmiller/Dropbox (University of Haifa)/HaifaU/10_Text_Reuse/Data Bases And Systems/Framwork/Modules/TRAligner/src')
import traligner as ta
```

### Issue: "ModuleNotFoundError: No module named 'pandas'"

Install dependencies:
```bash
pip install numpy pandas python-Levenshtein
```

Or install with all dependencies:
```bash
cd TRAligner
pip install -e .
```

### Issue: Changes not reflected

1. Restart Jupyter kernel
2. Or use `%autoreload` magic (see above)

### Issue: Old imports still trying "import TRAligner"

Update your notebook cells to use the new package name:
```python
# Old way (doesn't work anymore)
import TRAligner as ta  # ❌

# New way
import traligner as ta  # ✅
```

---

## Best Practice: Virtual Environment

For clean development, use a virtual environment:

```bash
# Create virtual environment
cd TRAligner
python3 -m venv venv

# Activate it
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate  # On Windows

# Install in editable mode
pip install -e .

# Install Jupyter
pip install jupyter

# Start Jupyter
jupyter notebook
```

---

## Quick Start Checklist

- [ ] Remove old `__init__.py` from TRAligner root (✅ Already done!)
- [ ] Install TRAligner in editable mode: `pip install -e .`
- [ ] Update notebook imports from `import TRAligner` to `import traligner`
- [ ] Restart Jupyter kernel
- [ ] Test imports: `import traligner as ta`
- [ ] Verify version: `print(ta.__version__)`

---

## Summary

**For development in Jupyter:**

1. **Install once** (recommended):
   ```bash
   cd TRAligner
   pip install -e .
   ```

2. **Import in notebooks**:
   ```python
   import traligner as ta
   ```

3. **When you make changes**:
   - Restart Kernel
   - Or use `%autoreload 2`

The old `import TRAligner` won't work anymore because:
- The package is now named `traligner` (lowercase)
- It's in the `src/` directory structure
- The old root `__init__.py` has been removed

**The new way is cleaner and follows Python best practices!** ✨
