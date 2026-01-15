# 📦 Publishing to PyPI

A clean, step-by-step guide for building and uploading AICCEL to PyPI.

---

## 1. Prerequisites
Ensure you have the latest building tools installed:
```bash
pip install --upgrade build twine
```

---

## 2. Preparation
1. **Update Version**: Ensure `version` in `pyproject.toml` and `__version__` in `aiccel/fast.py` are incremented.
2. **Clean Old Builds**: Delete existing `dist/` and `build/` folders to avoid uploading stale artifacts.
   ```bash
   Remove-Item -Recurse -Force dist, build
   ```

---

## 3. Build the Package
Generate the source distribution and wheel:
```bash
python -m build
```
This will create a `dist/` directory containing `.tar.gz` and `.whl` files.

---

## 4. Upload to PyPI
Use `twine` to securely upload your artifacts.

### To TestPyPI (Recommended first)
```bash
python -m twine upload --repository testpypi dist/*
```

### To Production PyPI
```bash
python -m twine upload dist/*
```

---

## 5. Verification
After uploading, verify the package can be installed in a clean environment:
```bash
pip install aiccel --upgrade
```

---

## 🛠️ Maintainer Notes
* **Credentials**: Use an API Token for PyPI. When prompted for a username, use `__token__`. The password is your token (including the `pypi-` prefix).
* **Tags**: It is recommended to create a Git tag matching the version (e.g., `git tag v3.0.7 && git push --tags`) after a successful upload.
