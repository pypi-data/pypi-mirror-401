# Publishing to PyPI

## Prerequisites

1. **PyPI Account**: Create accounts on both:
   - Test PyPI: https://test.pypi.org/account/register/
   - PyPI: https://pypi.org/account/register/

2. **API Tokens**: Generate API tokens for authentication:
   - Test PyPI: https://test.pypi.org/manage/account/token/
   - PyPI: https://pypi.org/manage/account/token/

## Before Publishing

### 1. Update Version

Edit `pyproject.toml`:
```toml
[project]
version = "0.1.0"  # Update this for each release
```

### 2. Update Metadata

In `pyproject.toml`, update:
```toml
authors = [
    {name = "Your Name", email = "your.email@example.com"}
]

[project.urls]
Homepage = "https://github.com/yourusername/sentinel-rs"
Repository = "https://github.com/yourusername/sentinel-rs"
```

### 3. Test Everything

```bash
# Run all tests
.venv/bin/pytest tests/ -v

# Run the demo
python demo.py

# Generate and test with real data
python scripts/generate_logs.py -n 100000 -o test.log
python -c "
import sentinel_rs
rules = {r'@\S+': '@[HIDDEN]'}
lines = sentinel_rs.scrub_logs_parallel('test.log', 'out.log', rules)
print(f'Processed {lines:,} lines')
"
```

## Publishing Steps

### Option 1: Publish to Test PyPI First (Recommended)

```bash
# Build the wheel
maturin build --release

# Install twine for uploading
pip install twine

# Upload to Test PyPI
twine upload --repository testpypi target/wheels/*

# Test installation from Test PyPI
pip install --index-url https://test.pypi.org/simple/ sentinel-rs
python -c "import sentinel_rs; print('Success!')"
```

### Option 2: Use Maturin Directly

```bash
# Test PyPI
maturin publish --repository testpypi

# Production PyPI
maturin publish
```

### Option 3: Production PyPI

Once you're confident everything works:

```bash
# Build wheel
maturin build --release

# Upload to PyPI
twine upload target/wheels/*
```

Or with maturin:
```bash
maturin publish
```

## Configuration File (~/.pypirc)

Create `~/.pypirc` with your API tokens:

```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-your-api-token-here

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-your-testpypi-token-here
```

**Important:** Never commit this file to git!

## Post-Publishing

### Verify Installation

```bash
# Create a fresh environment
python -m venv test_env
source test_env/bin/activate  # or test_env\Scripts\activate on Windows

# Install from PyPI
pip install sentinel-rs

# Test it works
python -c "
import sentinel_rs
print('Version:', sentinel_rs.__version__)
result = sentinel_rs.scrub_text('test@example.com', {r'@\S+': '@[HIDDEN]'})
print('Test:', result)
"
```

### Create GitHub Release

1. Tag the release:
```bash
git tag -a v0.1.0 -m "Release version 0.1.0"
git push origin v0.1.0
```

2. Create release on GitHub with:
   - Release notes
   - Link to PyPI package
   - Binary wheels (from `target/wheels/`)

## Version Scheme

Follow Semantic Versioning (semver.org):

- `0.1.0` - Initial release
- `0.1.1` - Bug fixes
- `0.2.0` - New features (backward compatible)
- `1.0.0` - Stable API, production ready
- `2.0.0` - Breaking changes

## Troubleshooting

### "Package already exists"
- You can't overwrite a version on PyPI
- Increment the version number in `pyproject.toml`
- Rebuild and republish

### "Invalid authentication"
- Check your API token in `~/.pypirc`
- Ensure no extra spaces or newlines
- Try regenerating the token

### "Wheel build failed"
- Ensure Rust is installed: `rustc --version`
- Try: `cargo clean && maturin build --release`
- Check `Cargo.toml` syntax

### Platform-specific wheels
- By default, maturin builds for your current platform
- For cross-compilation, see: https://www.maturin.rs/distribution.html
- Or use GitHub Actions for multi-platform builds

## GitHub Actions (CI/CD)

Consider setting up automated publishing with GitHub Actions:
- Build wheels for multiple platforms (Linux, macOS, Windows)
- Run tests on all platforms
- Auto-publish on git tag

Example: https://github.com/PyO3/maturin-action

## Checklist Before Publishing

- [ ] All tests pass
- [ ] Version number updated in `pyproject.toml`
- [ ] README.md is complete and accurate
- [ ] LICENSE file exists
- [ ] Author and URLs updated in `pyproject.toml`
- [ ] Demo works correctly
- [ ] Tested on fresh Python environment
- [ ] Git commits pushed
- [ ] Tagged release in git

## After Publishing

Update your README badges:
```markdown
[![PyPI](https://img.shields.io/pypi/v/sentinel-rs.svg)](https://pypi.org/project/sentinel-rs/)
[![Downloads](https://pepy.tech/badge/sentinel-rs)](https://pepy.tech/project/sentinel-rs)
```

Announce on:
- GitHub Discussions/README
- Python community forums
- Twitter/LinkedIn
- Reddit (r/rust, r/Python)

---

**Ready to publish?** Start with Test PyPI to be safe!
