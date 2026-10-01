#!/usr/bin/env bash
# Build the whole site into ./_output (same steps as GitHub Actions).
set -euo pipefail
cd "$(dirname "$0")/.."
rm -rf _output .jupyterlite.doit.db
jupyter lite build --contents content --output-dir _output
# The landing page replaces JupyterLite's default index.html.
cp -r website/. _output/
touch _output/.nojekyll
echo "Built. Preview with:  python -m http.server --directory _output 8000"
