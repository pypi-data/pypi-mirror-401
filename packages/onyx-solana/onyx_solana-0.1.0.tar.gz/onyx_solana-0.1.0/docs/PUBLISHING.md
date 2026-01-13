# Publishing Onyx to PyPI

This guide covers how to publish the Onyx SDK packages to PyPI (Python Package Index).

## Overview

Onyx is a unified Python package with embedded Rust cryptographic backend:

- **onyx-solana**: Single Python package (Rust + Python via maturin) - PyPI name
- **Import name**: `from onyx import ...` (not `from onyx_solana`)
- **packages/onyx-solana**: Separate on-chain Anchor program (not published to PyPI)

This guide focuses on publishing the unified `onyx-solana` package to PyPI.

## Prerequisites

### 1. Create PyPI Accounts

**Production PyPI:**
- Create account at https://pypi.org/account/register/
- Verify your email address
- Enable 2FA (recommended)

**Test PyPI (for testing):**
- Create account at https://test.pypi.org/account/register/
- Verify your email address

### 2. Generate API Tokens

**For PyPI:**
1. Go to https://pypi.org/manage/account/token/
2. Click "Add API token"
3. Name: `onyx-upload`
4. Scope: "Entire account" (or specific project after first upload)
5. Copy the token (starts with `pypi-`)
6. Store securely - you won't see it again!

**For TestPyPI:**
1. Go to https://test.pypi.org/manage/account/token/
2. Follow same steps as above
3. Copy the token (starts with `pypi-`)

### 3. Configure Credentials

Store your tokens securely:

```bash
# Option 1: Using environment variables (recommended for CI/CD)
export MATURIN_PYPI_TOKEN="pypi-your-token-here"

# Option 2: Using ~/.pypirc file
cat > ~/.pypirc <<EOF
[pypi]
username = __token__
password = pypi-your-production-token-here

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-your-test-token-here
EOF

chmod 600 ~/.pypirc
```

## Installation Requirements

Install required tools:

```bash
# Install Rust (if not already installed)
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# Install maturin (PyO3 build tool)
pip install maturin

# Install build tools
pip install build twine
```

## Pre-Publication Checklist

Before publishing, verify:

- [ ] All tests pass: `make test`
- [ ] Version numbers updated in all `pyproject.toml` files
- [ ] README.md is up to date
- [ ] CHANGELOG.md exists and is updated
- [ ] License file exists (MIT)
- [ ] No secrets in code
- [ ] Git tags created for the version

## Publishing Process

### Step 1: Update Version

Update version in the root `pyproject.toml` file:

**pyproject.toml:**
```toml
[project]
name = "onyx-solana"
version = "0.1.0"  # Update this version
```

Also update in **Cargo.toml:**
```toml
[package]
name = "onyx-solana"
version = "0.1.0"  # Update this version
```

**Note**: Only one version to manage in the unified structure!

### Step 2: Create Git Tag

```bash
# Create version tag
git tag -a v0.1.0 -m "Release v0.1.0"
git push origin v0.1.0

# Or push all tags
git push --tags
```

### Step 3: Build the Package

Build the unified onyx package:

```bash
# From root directory
make build

# Or directly with maturin
PYO3_USE_ABI3_FORWARD_COMPATIBILITY=1 maturin build --release

# Output will be in target/wheels/ directory
# Example: target/wheels/onyx-0.1.0-cp312-cp312-linux_x86_64.whl
```

**Note**: Maturin builds both Rust and Python code in one step!

### Step 4: Test with TestPyPI (Recommended First)

Publish to TestPyPI first:

```bash
# Publish using maturin
PYO3_USE_ABI3_FORWARD_COMPATIBILITY=1 maturin publish --repository testpypi

# Or manually with twine
twine upload --repository testpypi target/wheels/*
```

**Test the installation:**

```bash
# Create test environment
python -m venv test_env
source test_env/bin/activate

# Install from TestPyPI
pip install --index-url https://test.pypi.org/simple/ onyx-solana

# Test import
python -c "from onyx import OnyxClient; print('Success!')"

# Clean up
deactivate
rm -rf test_env
```

### Step 5: Publish to Production PyPI

Once TestPyPI works:

```bash
# Publish using maturin (recommended)
PYO3_USE_ABI3_FORWARD_COMPATIBILITY=1 maturin publish

# Or using the Makefile
make publish

# Or manually with twine
twine upload target/wheels/*
```

### Step 6: Verify Installation

```bash
# Create fresh environment
python -m venv verify_env
source verify_env/bin/activate

# Install from PyPI
pip install onyx-solana

# Test import
python -c "import onyx; from onyx.x402 import X402Client; print('Success!')"

deactivate
```

## Building for Multiple Platforms

For maximum compatibility, build wheels for multiple platforms.

### Option 1: Using GitHub Actions (Recommended)

Create `.github/workflows/release.yml`:

```yaml
name: Release

on:
  push:
    tags:
      - 'v*'

jobs:
  build:
    name: Build onyx-solana (${{ matrix.os }})
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
        python-version: ['3.12']
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}

      - name: Build wheels (onyx-core)
        uses: PyO3/maturin-action@v1
        with:
          working-directory: packages/onyx-core
          args: --release --out dist
          manylinux: auto

      - name: Upload wheels
        uses: actions/upload-artifact@v4
        with:
          name: wheels-rust-${{ matrix.os }}
          path: packages/onyx-core/dist

  build-python:
    name: Build onyx-client
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Install build tools
        run: pip install build

      - name: Build package
        run: |
          cd packages/onyx-client
          python -m build

      - name: Upload dist
        uses: actions/upload-artifact@v4
        with:
          name: dist-python
          path: packages/onyx-client/dist

  release:
    name: Publish to PyPI
    runs-on: ubuntu-latest
    needs: [build-rust, build-python]
    steps:
      - uses: actions/download-artifact@v4
        with:
          pattern: wheels-rust-*
          path: dist-rust
          merge-multiple: true

      - uses: actions/download-artifact@v4
        with:
          name: dist-python
          path: dist-python

      - name: Publish onyx-core to PyPI
        uses: PyO3/maturin-action@v1
        env:
          MATURIN_PYPI_TOKEN: ${{ secrets.PYPI_API_TOKEN }}
        with:
          command: upload
          args: --skip-existing dist-rust/*

      - name: Publish onyx-client to PyPI
        uses: pypa/gh-action-pypi-publish@release/v1
        with:
          password: ${{ secrets.PYPI_API_TOKEN }}
          packages-dir: dist-python/
```

Add your PyPI token to GitHub Secrets:
1. Go to your repository settings
2. Secrets and variables → Actions
3. New repository secret
4. Name: `PYPI_API_TOKEN`
5. Value: Your PyPI token

### Option 2: Using Makefile (Local)

Use the provided Makefile:

```bash
cd packages

# Build all packages
make build

# Publish to TestPyPI
make publish-test

# Publish to PyPI (after testing)
make publish
```

### Option 3: Manual Cross-compilation

```bash
# Install cross-compilation targets
rustup target add x86_64-unknown-linux-gnu
rustup target add aarch64-unknown-linux-gnu
rustup target add x86_64-apple-darwin
rustup target add aarch64-apple-darwin
rustup target add x86_64-pc-windows-msvc

# Build onyx-core for each target
cd packages/onyx-core
maturin build --release --target x86_64-unknown-linux-gnu
maturin build --release --target aarch64-unknown-linux-gnu
maturin build --release --target x86_64-apple-darwin
maturin build --release --target aarch64-apple-darwin
maturin build --release --target x86_64-pc-windows-msvc
```

## Package-Specific Notes

### onyx-core

- Uses maturin for building Rust extension
- Requires Rust toolchain
- Builds platform-specific wheels
- Contains native code (cdylib)

**Dependencies:**
- BN254 curve operations
- Poseidon hash
- Groth16 proving system
- PyO3 bindings

### onyx-client

- Pure Python package (no compilation)
- Depends on onyx-core
- Optional x402 dependencies
- Platform-independent

**Installation variants:**
```bash
# Basic (privacy features only)
pip install onyx-client

# With x402 support
pip install onyx-client[x402]

# Development
pip install onyx-client[dev]

# All extras
pip install onyx-client[x402,dev]
```

## Troubleshooting

### Build Errors

**Issue: Rust compiler errors**
```bash
# Update Rust toolchain
rustup update stable

# Clear build cache
cd packages/onyx-core
cargo clean
```

**Issue: Missing dependencies**
```bash
# Install development headers (Linux)
sudo apt-get install build-essential libssl-dev pkg-config

# macOS
xcode-select --install
```

### Upload Errors

**Issue: "File already exists"**
```bash
# Increment version in pyproject.toml
# You cannot replace existing versions
```

**Issue: "Invalid credentials"**
```bash
# Regenerate API token
# Update ~/.pypirc or environment variable
```

**Issue: "Package name already taken"**
```bash
# Check if name is available
# onyx-core: https://pypi.org/project/onyx-core/
# onyx-client: https://pypi.org/project/onyx-client/
```

### Testing Issues

**Issue: Import fails after installation**
```bash
# Check for ABI compatibility issues
python -c "import sys; print(sys.version)"

# Rebuild for correct Python version
cd packages/onyx-core
maturin build --release --interpreter python3.12
```

**Issue: x402 imports fail**
```bash
# Install x402 dependencies
pip install onyx-client[x402]
```

## Version Management

Follow semantic versioning (SemVer):
- **MAJOR** (1.0.0): Breaking changes
- **MINOR** (0.1.0): New features, backward compatible
- **PATCH** (0.0.1): Bug fixes, backward compatible

Example progression:
- `0.1.0` - Initial release
- `0.2.1` - Bug fixes
- `0.3.0` - New features (e.g., multi-chain privacy)
- `1.0.0` - Production ready, stable API

**Important:** Keep all package versions in sync:
- onyx-core: 0.1.0
- onyx-client: 0.1.0 (depends on onyx-core>=0.1.0)

## Security Best Practices

1. **Never commit tokens**: Add to `.gitignore`
   ```bash
   echo "*.pypirc" >> .gitignore
   echo ".env" >> .gitignore
   ```

2. **Use scoped tokens**: After first upload, create project-scoped token

3. **Enable 2FA**: On your PyPI account

4. **Scan for vulnerabilities**:
   ```bash
   pip install safety
   safety check
   ```

5. **Sign releases**: Use GPG signatures
   ```bash
   gpg --detach-sign --armor dist/onyx-client-0.1.0.tar.gz
   ```

## Post-Publication Tasks

After successful publication:

### 1. Verify on PyPI

- onyx-core: https://pypi.org/project/onyx-core/
- onyx-client: https://pypi.org/project/onyx-client/
- Verify metadata, description, links
- Check supported platforms

### 2. Update Documentation

- Add installation instructions to README
- Update version badges
- Create release notes

### 3. Announce Release

- GitHub Release: Create release from tag
- Social media / community channels
- Update project website

### 4. Monitor

- Check for installation issues
- Monitor download stats:
  - https://pypistats.org/packages/onyx-core
  - https://pypistats.org/packages/onyx-client
- Address bug reports

## Resources

- **PyPI Documentation**: https://packaging.python.org/
- **Maturin Guide**: https://www.maturin.rs/
- **PyO3 Documentation**: https://pyo3.rs/
- **Python Packaging**: https://packaging.python.org/en/latest/tutorials/packaging-projects/
- **Semantic Versioning**: https://semver.org/

## Quick Reference

```bash
# Development workflow
cd packages
make install-dev              # Install all packages locally
make test                     # Run all tests

# Release workflow (onyx-core)
cd packages/onyx-core
maturin build --release       # Build wheel
maturin publish --repository testpypi  # Test publish
maturin publish               # Production publish

# Release workflow (onyx-client)
cd packages/onyx-client
python -m build               # Build package
twine upload --repository testpypi dist/*  # Test publish
twine upload dist/*           # Production publish

# Verify
pip install onyx-client[x402]
python -c "import onyx; from onyx.x402 import X402Client; print('Success!')"
```

---

**Note**: This is a multi-package monorepo. Each package has its own version and publishing cycle, but versions should be kept in sync for consistency.
