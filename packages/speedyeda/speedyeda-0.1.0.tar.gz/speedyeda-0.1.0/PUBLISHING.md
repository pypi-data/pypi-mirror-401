# Publishing FastEDA to PyPI

## 📦 Package Built Successfully!

Your package has been built and is ready for publication:
- **Package Name**: `fast-eda` (on PyPI)
- **Module Name**: `fasteda` (for imports)
- **Source distribution**: `fast_eda-0.1.0.tar.gz`
- **Wheel distribution**: `fast_eda-0.1.0-py3-none-any.whl`

> **Note**: The original name `fasteda` was already taken on PyPI, so we're publishing as `fast-eda`. Users will install with `pip install fast-eda` but import with `import fasteda`.

## 🚀 Steps to Publish to PyPI

### 1. Create PyPI Account
If you don't have one already:
- Go to https://pypi.org/account/register/
- Verify your email

### 2. Create API Token
For secure authentication:
1. Go to https://pypi.org/manage/account/token/
2. Create a new API token
3. Give it a descriptive name (e.g., "fasteda-upload")
4. Set scope to "Entire account" or specific to this project
5. **Copy the token** (it starts with `pypi-`)

### 3. Configure Credentials

Save your token in `~/.pypirc`:

```ini
[pypi]
username = __token__
password = pypi-YOUR_TOKEN_HERE
```

Replace `pypi-YOUR_TOKEN_HERE` with your actual token.

### 4. Upload to PyPI

#### Option A: Test on TestPyPI First (Recommended)

```bash
# Upload to TestPyPI
./venv/bin/python -m twine upload --repository testpypi dist/*

# Test installation from TestPyPI
pip install --index-url https://test.pypi.org/simple/ fasteda
```

#### Option B: Upload to Production PyPI

```bash
# Upload to PyPI
./venv/bin/python -m twine upload dist/*
```

### 5. Verify Installation

```bash
# After publishing, test installation
pip install fast-eda

# Try it out
fasteda --version
fasteda sample_data.csv --fun
```

## ⚠️ Important Notes

1. **Version Uniqueness**: Once you upload version `0.1.0`, you cannot upload it again. To make changes, increment the version in `pyproject.toml`.

2. **Package Name**: The name `fasteda` will be checked for availability. If taken, you'll need to choose a different name.

3. **Git Repository**: Make sure to push your code to GitHub:
   ```bash
   git init
   git add .
   git commit -m "Initial commit - FastEDA v0.1.0"
   git remote add origin https://github.com/Dawaman43/fasteda.git
   git push -u origin main
   ```

4. **README on PyPI**: Your `README.md` will be displayed on the PyPI project page.

## 📝 Future Releases

To publish a new version:

1. Update version in `pyproject.toml`
2. Make your changes
3. Rebuild: `./venv/bin/python -m build`
4. Upload: `./venv/bin/python -m twine upload dist/*`

## 🔗 Useful Links

- **PyPI Package Page**: https://pypi.org/project/fast-eda/ (after publishing)
- **GitHub Repository**: https://github.com/Dawaman43/fasteda
- **Twine Documentation**: https://twine.readthedocs.io/

---

**Ready to publish?** Run the command above when you have your PyPI API token!
