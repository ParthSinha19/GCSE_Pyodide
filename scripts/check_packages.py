#!/usr/bin/env python3
"""Check that every package listed in jupyter-lite.json exists in the Pyodide
version the build will use.

This does NOT run the packages (that needs a real browser - use
content/notebooks/00_environment_check.ipynb for that). It catches the most
common admin mistake: listing a package that Pyodide does not ship.

Needs: pip install -r requirements.txt, and Node.js (for `npm pack`).
Usage: python scripts/check_packages.py
"""
import json, re, subprocess, sys, tarfile, tempfile
from pathlib import Path

from jupyterlite_pyodide_kernel.constants import PYODIDE_VERSION

ROOT = Path(__file__).resolve().parent.parent
KERNEL = "@jupyterlite/pyodide-kernel-extension:kernel"

def norm(name):
    return re.sub(r"[-_.]+", "-", name).lower()

cfg = json.loads((ROOT / "jupyter-lite.json").read_text())
wanted = cfg["jupyter-config-data"]["litePluginSettings"][KERNEL]["loadPyodideOptions"]["packages"]

with tempfile.TemporaryDirectory() as tmp:
    subprocess.run(["npm", "pack", f"pyodide@{PYODIDE_VERSION}", "--silent"], cwd=tmp, check=True, stdout=subprocess.DEVNULL)
    tgz = next(Path(tmp).glob("pyodide-*.tgz"))
    with tarfile.open(tgz) as t:
        lock = json.load(t.extractfile("package/pyodide-lock.json"))

available = {norm(k): v for k, v in lock["packages"].items()}
print(f"Pyodide {PYODIDE_VERSION} (Python {lock['info']['python']})")
missing = []
for name in wanted:
    pkg = available.get(norm(name))
    if pkg:
        print(f"  ok       {name} {pkg['version']}")
    else:
        print(f"  MISSING  {name}")
        missing.append(name)

if missing:
    print("\nNot shipped with this Pyodide version: " + ", ".join(missing))
    print("If the package is pure Python, students can use '%pip install NAME' in a notebook,")
    print("or you can add its .whl file to a 'pypi/' folder. See README -> 'Adding a package'.")
    sys.exit(1)
print("\nAll packages are available.")
