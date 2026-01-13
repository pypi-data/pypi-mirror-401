# Quick Start: Publishing Onyx to PyPI

This is a condensed guide for publishing. See [PUBLISHING.md](PUBLISHING.md) for full details.

## First-Time Setup (Do Once)

### 1. Install Tools

```bash
# Install maturin (PyO3 build tool)
pip install maturin twine build

# Verify Rust is installed
rustc --version
```

### 2. Create PyPI Accounts

- **TestPyPI** (for testing): https://test.pypi.org/account/register/
- **PyPI** (production): https://pypi.org/account/register/

### 3. Generate API Tokens

**TestPyPI:**
1. Go to https://test.pypi.org/manage/account/token/
2. Create token named `onyx-test-upload`
3. Copy token (starts with `pypi-`)

**PyPI:**
1. Go to https://pypi.org/manage/account/token/
2. Create token named `onyx-upload`
3. Copy token

### 4. Configure Credentials

```bash
# Create ~/.pypirc
cat > ~/.pypirc <<EOF
[pypi]
username = __token__
password = pypi-YOUR-PRODUCTION-TOKEN-HERE

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-YOUR-TEST-TOKEN-HERE
EOF

chmod 600 ~/.pypirc
```

## Publishing Workflow

### Step 1: Prepare Release

```bash
# 1. Update version in BOTH pyproject.toml files
vim packages/onyx-core/pyproject.toml     # Change version = "0.1.0" to your new version
vim packages/onyx-client/pyproject.toml   # Keep versions in sync!

# 2. Update CHANGELOG.md
vim CHANGELOG.md    # Add release notes

# 3. Run all tests
cd packages
make test

# 4. Commit changes
git add .
git commit -m "Prepare release v0.1.0"
git push
```

### Step 2: Test with TestPyPI

#### Build and publish onyx-core

```bash
cd packages/onyx-core

# Build wheel
maturin build --release

# Publish to TestPyPI
maturin publish --repository testpypi
```

#### Build and publish onyx-client

```bash
cd packages/onyx-client

# Build package
python -m build

# Publish to TestPyPI
twine upload --repository testpypi dist/*
```

**Verify TestPyPI installation:**

```bash
# Create test environment
python -m venv test_env
source test_env/bin/activate  # On Windows: test_env\Scripts\activate

# Install from TestPyPI
pip install --index-url https://test.pypi.org/simple/ onyx-client[x402]

# Test import
python -c "import onyx; from onyx.x402 import X402Client; print(onyx.__version__)"

# Clean up
deactivate
rm -rf test_env
```

### Step 3: Create Git Tag

```bash
# Create and push tag
git tag -a v0.1.0 -m "Release v0.1.0"
git push origin v0.1.0
```

### Step 4: Publish to PyPI

#### Publish onyx-core

```bash
cd packages/onyx-core
maturin publish
```

#### Publish onyx-client

```bash
cd packages/onyx-client
twine upload dist/*
```

### Step 5: Verify Production

```bash
# Wait 2-3 minutes for PyPI to propagate

# Create fresh environment
python -m venv verify_env
source verify_env/bin/activate

# Install from PyPI
pip install onyx-client[x402]

# Test
python -c "import onyx; from onyx.x402 import X402Client; print(onyx.__version__)"

deactivate
```

### Step 6: Create GitHub Release

1. Go to https://github.com/onyxsolana/onyx-sdk/releases/new
2. Select tag `v0.1.0`
3. Title: `Onyx v0.1.0`
4. Copy release notes from CHANGELOG.md
5. Attach wheels from `packages/onyx-core/target/wheels/` (optional)
6. Attach dists from `packages/onyx-client/dist/` (optional)
7. Publish release

## Using GitHub Actions (Automated)

GitHub Actions will automatically publish when you push a tag:

```bash
# Just push a tag
git tag -a v0.1.0 -m "Release v0.1.0"
git push origin v0.1.0

# GitHub Actions will:
# 1. Build wheels for Linux, macOS, Windows
# 2. Create GitHub Release
# 3. Publish to PyPI (if PYPI_API_TOKEN secret is set)
```

**Setup GitHub Secret:**
1. Go to repository Settings → Secrets → Actions
2. New repository secret
3. Name: `PYPI_API_TOKEN`
4. Value: Your PyPI token
5. Save

## Makefile Commands

```bash
# Navigate to packages directory
cd packages

# Development
make install-dev    # Install all packages in development mode
make test          # Run all tests
make check         # Check all packages compile

# Building
make build         # Build all packages
make build-core    # Build onyx-core only
make build-client  # Build onyx-client only

# Publishing (not yet implemented - use manual commands above)
# make publish-test  # Publish to TestPyPI
# make publish       # Publish to PyPI

# Utility
make clean         # Clean build artifacts
```

## Troubleshooting

### "Package name already taken"

Check if the names are available:
- onyx-core: https://pypi.org/project/onyx-core/
- onyx-client: https://pypi.org/project/onyx-client/

If taken, choose different names and update `pyproject.toml` files.

### "File already exists"

You cannot overwrite existing versions on PyPI.

**Solution**: Increment version in both `pyproject.toml` files

### "Invalid credentials"

1. Check `~/.pypirc` has correct token
2. Ensure token starts with `pypi-`
3. Regenerate token if needed

### Build errors

```bash
# Update Rust
rustup update stable

# Clear cache
cd packages/onyx-core
cargo clean

# Clear Python cache
cd packages/onyx-client
rm -rf dist/ build/ *.egg-info

# Rebuild
cd packages
make build
```

### Import errors after installation

```bash
# x402 dependencies missing
pip install onyx-client[x402]

# ABI compatibility issues
python -c "import sys; print(sys.version)"
cd packages/onyx-core
maturin build --release --interpreter python3.12
```

## Quick Reference

```bash
# Complete publishing workflow
cd packages

# Test everything
make test

# Update versions
vim onyx-core/pyproject.toml      # Update version
vim onyx-client/pyproject.toml    # Update version (keep in sync!)
vim ../CHANGELOG.md                 # Add release notes

# Commit
git commit -am "Release v0.1.0"
git push

# Publish to TestPyPI (onyx-core)
cd onyx-core
maturin build --release
maturin publish --repository testpypi

# Publish to TestPyPI (onyx-client)
cd ../onyx-client
python -m build
twine upload --repository testpypi dist/*

# Test installation
python -m venv test_env
source test_env/bin/activate
pip install --index-url https://test.pypi.org/simple/ onyx-client[x402]
python -c "import onyx; print(onyx.__version__)"
deactivate

# Create tag
git tag -a v0.1.0 -m "Release v0.1.0"
git push origin v0.1.0

# Publish to PyPI (onyx-core)
cd onyx-core
maturin publish

# Publish to PyPI (onyx-client)
cd ../onyx-client
twine upload dist/*
```

## Environment Variables

```bash
# Set PyPI token as environment variable (alternative to ~/.pypirc)
export MATURIN_PYPI_TOKEN="pypi-your-token"

# Publish
cd packages/onyx-core
maturin publish

cd packages/onyx-client
TWINE_PASSWORD="$MATURIN_PYPI_TOKEN" twine upload dist/*
```

## Multi-Platform Builds

For building on your local machine for multiple platforms:

```bash
# Install targets
rustup target add x86_64-unknown-linux-gnu
rustup target add x86_64-apple-darwin
rustup target add x86_64-pc-windows-msvc
rustup target add aarch64-apple-darwin
rustup target add aarch64-unknown-linux-gnu

# Build onyx-core for each
cd packages/onyx-core
maturin build --release --target x86_64-unknown-linux-gnu
maturin build --release --target x86_64-apple-darwin  # macOS only
maturin build --release --target x86_64-pc-windows-msvc  # Windows only
maturin build --release --target aarch64-apple-darwin  # M1/M2 Macs
maturin build --release --target aarch64-unknown-linux-gnu  # ARM Linux

# Publish all wheels
maturin publish
```

**Recommendation**: Use GitHub Actions for multi-platform builds (easier and more reliable).

## Version Management

Follow semantic versioning:
- `0.1.0` → `0.2.1`: Bug fixes
- `0.1.0` → `0.3.0`: New features (backward compatible)
- `0.1.0` → `1.0.0`: Breaking changes or stable release

**IMPORTANT**: Keep package versions in sync:
- onyx-core: 0.1.0
- onyx-client: 0.1.0 (depends on onyx-core>=0.1.0)

## Package Structure

```
packages/
├── onyx-core/           # Rust + PyO3 bindings
│   ├── Cargo.toml         # Rust package config
│   ├── pyproject.toml     # Python package config
│   └── src/               # Rust source code
│
├── onyx-client/         # Python SDK
│   ├── pyproject.toml     # Python package config
│   ├── src/onyx/        # Python source code
│   │   ├── __init__.py
│   │   ├── client.py
│   │   └── x402/          # Optional x402 support
│   └── tests/
│
└── onyx-solana/         # Solana program (not published to PyPI)
    └── programs/onyx-solana/
```

## Installation Variants

After publishing, users can install:

```bash
# Basic (privacy features only)
pip install onyx-client

# With x402 payment support
pip install onyx-client[x402]

# Development
pip install onyx-client[dev]

# All extras
pip install onyx-client[x402,dev]
```

## Resources

- Full guide: [PUBLISHING.md](PUBLISHING.md)
- Architecture: [ARCHITECTURE.md](ARCHITECTURE.md)
- API Reference: [API_REFERENCE.md](API_REFERENCE.md)
- Maturin docs: https://www.maturin.rs/
- PyPI help: https://packaging.python.org/

## Support

- Issues: https://github.com/onyxsolana/onyx-sdk/issues
- Email: dev@onyx-sdk.com
- Security: security@onyx-sdk.com
