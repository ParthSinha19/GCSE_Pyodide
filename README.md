# GCSE AI & Machine Learning Lab

A browser-based Python lab for GCSE students (Years 9-11), hosted free on GitHub Pages using [JupyterLite](https://jupyterlite.readthedocs.io/). Students open a web address and code. No installs, no accounts, no server.

Python runs **inside each student's browser** (via Pyodide / WebAssembly). GitHub Pages only serves static files.

```
Student browser -> GitHub Pages (static files) -> JupyterLite -> Pyodide Python
                                                   -> NumPy / Matplotlib / pandas / scikit-learn
```

---

## Contents

1. [Quick start for the teacher/administrator](#quick-start-teacheradministrator)
2. [Student guide](#student-guide)
3. [Administrator guide](#administrator-guide)
4. [How the build works](#how-the-build-works)
5. [Package compatibility and limits](#package-compatibility-and-limits)
6. [Troubleshooting](#troubleshooting)
7. [Final acceptance test](#final-acceptance-test)
8. [Repository layout](#repository-layout)

---

## Quick start (teacher/administrator)

1. Create a GitHub repository and push this project to the `main` branch.
2. In the repository go to **Settings -> Pages** and set **Source** to **GitHub Actions**.
3. Push any change (or open **Actions -> Build and deploy -> Run workflow**).
4. After the workflow finishes, the site is live at `https://USERNAME.github.io/REPOSITORY/`.
5. Open it and run `00_environment_check.ipynb` (the **Check my setup works** button) to confirm everything works in your school's browsers.

Give students the web address. That is all they need.

> **School networks:** the first time a student opens a notebook, the browser downloads Python and the packages from the **jsDelivr CDN** (`cdn.jsdelivr.net`). If your school filter blocks it, ask IT to allow `cdn.jsdelivr.net`. See [Troubleshooting](#troubleshooting) for the self-hosting alternative. Test this on a real school computer before your first lesson.

---

## Student guide

### Open JupyterLab
Click **Start Coding** on the home page. The first load takes longer (up to a minute on slow Wi-Fi) while Python loads. After that it is much quicker.

### Create a notebook
1. Click **Start Coding**.
2. Choose **File -> New -> Notebook** (or click the **Python** tile on the Launcher).
3. If asked to pick a kernel, choose **Python**.
4. Type code in a cell and press **Shift + Enter** to run it.

```python
import numpy as np
import matplotlib.pyplot as plt
print("Hello, machine learning!")
```

### Open a lesson
Click **Start** next to a lesson on the home page. The lesson opens as a notebook. You can change it freely: **your changes never alter the original lesson**.

### Run Python, write Markdown
* Click a cell and press **Shift + Enter** to run it.
* Use the **+** button to add a cell, the scissors/bin icons to cut/delete, and drag cells to rearrange.
* To write text, change the cell type from **Code** to **Markdown** in the toolbar.
* **Kernel -> Restart Kernel** gives you a clean start if things get confusing.

### Save your work (do this every time)
1. Press **Ctrl + S** (Cmd + S on Mac). This saves inside your browser.
2. Choose **File -> Download** to get your `.ipynb` file.
3. Keep the file somewhere safe (for example your school drive or a USB stick).

**Downloading is the reliable way to keep your work.** Browser storage can be cleared by the school (shared computers, logging out, "clear browsing data").

### Continue your work later
1. Open the website and click **Start Coding**.
2. In the file list on the left, click the **upload** (up-arrow) button and choose your `.ipynb` file. You can also drag the file into the file list.
3. Double-click the notebook to open it. Click **Run -> Run All Cells** to rebuild your outputs.

---

## Administrator guide

You do not need to install anything to maintain the site: edit files on github.com (or in Git) and push to `main`. The workflow rebuilds and redeploys automatically (about 2-4 minutes).

### Add or change a notebook
1. Put the `.ipynb` file in `content/notebooks/`, e.g. `07_clustering.ipynb`.
2. Save notebooks **with outputs cleared** (Kernel -> Restart Kernel and Clear All Outputs) so they stay small and clean.
3. To show it on the home page, add an entry to `website/lessons.json`:
   ```json
   { "level": "Level 5", "title": "Clustering", "blurb": "Find groups in data.", "file": "07_clustering.ipynb" }
   ```
   Use `"file": null` to show a "Coming soon" row.
4. Commit and push.

Direct link to any notebook: `https://USERNAME.github.io/REPOSITORY/lab/index.html?path=notebooks/02_numpy.ipynb`

**Important - updates to existing notebooks:** JupyterLite copies the teacher notebooks into each student's browser storage the first time they open the site. If you later *edit* a lesson, students who already opened it keep their old copy (this also protects their work). For a substantive update, publish it under a new file name (e.g. `02_numpy_v2.ipynb`). JupyterLite also supports a `?reset` URL option that clears browser storage for the site, but that deletes student work, so test it first and warn students to download their notebooks.

### Add a dataset
1. Put the CSV in `content/data/` (keep files small: classroom scale, ideally under 1 MB).
2. Students load it with a path relative to the file list root:
   ```python
   import pandas as pd
   df = pd.read_csv("data/students.csv")
   ```
Included datasets: `iris.csv`, `example.csv`, `students.csv`, `house_prices.csv`, `simple_classification.csv` (the last three are synthetic/made-up data).

### Add or update a Python package
Students never install packages. You decide what is preloaded. JupyterLite uses **Pyodide**, so only packages built for it, or pure-Python packages, work in the browser. `pip install` on its own is not enough.

**Step 1 - is it already part of Pyodide? (most packages you will want are)**
Add its name to the `packages` list in `jupyter-lite.json`:
```json
"loadPyodideOptions": { "packages": ["numpy", "matplotlib", "pandas", "scikit-learn", "scipy", "statsmodels"] }
```
Then check that name exists in this Pyodide version:
```bash
pip install -r requirements.txt
python scripts/check_packages.py
```
GitHub Actions runs the same check on every push, so a typo or unsupported package fails the build instead of breaking the lab. Each preloaded package makes the first start-up slower, so only add what lessons need. See the full list at <https://pyodide.org/en/stable/usage/packages-in-pyodide.html>.

**Step 2 - not in Pyodide, but pure Python (e.g. seaborn)?**
Notebook authors can put this at the top of the lesson notebook:
```python
%pip install seaborn
```
This downloads from PyPI in the student's browser, so the school network must allow it. For a fully self-contained site, put the package's `py3-none-any.whl` file in a `pypi/` folder at the repository root; the JupyterLite build indexes wheels from there. Test either approach with the check notebook before relying on it.

**Step 3 - compiled code that is not in Pyodide (e.g. TensorFlow, PyTorch, XGBoost)?**
It cannot run in the browser. Students who try it get a normal "No module named" error; the home page FAQ tells them to ask you.

**Versions are pinned.** `requirements.txt` pins `jupyterlite-core` and `jupyterlite-pyodide-kernel`. The kernel version decides the Pyodide version (and so the NumPy / scikit-learn versions students get). To upgrade: change both pins together, run `./scripts/build.sh` and `python scripts/check_packages.py`, then run every notebook in the browser before pushing.

### Build and preview locally
```bash
python -m venv .venv && source .venv/bin/activate     # Windows: .venv\Scripts\activate
pip install -r requirements.txt
./scripts/build.sh                                    # builds into ./_output
python -m http.server --directory _output 8000        # open http://localhost:8000
```
Notes: use a web server (not by double-clicking `index.html`). Use a private window or clear site data if you see old versions, because JupyterLite caches aggressively.

### Deploy
Push to `main`. That is the whole process.

### How GitHub Actions works here
`.github/workflows/deploy.yml` does this on every push to `main`:
1. Installs the pinned build tools (`requirements.txt`).
2. Checks every package in `jupyter-lite.json` exists in Pyodide.
3. Validates all notebooks.
4. Runs `scripts/build.sh`: builds JupyterLite, bundles everything in `content/` (notebooks and data), applies `jupyter-lite.json`, and copies `website/` over the default home page.
5. Publishes `_output/` to GitHub Pages.

Pull requests run the build and checks but do not deploy.

### Change the home page
Edit `website/index.html` and `website/styles.css`. Keep links **relative** (e.g. `lab/index.html`, never `/lab/index.html`) so the site works under `/REPOSITORY/`.

### Project-site paths
JupyterLite uses relative URLs (`baseUrl: ./`), and the home page uses relative links, so no base-path setting is needed for `https://USERNAME.github.io/REPOSITORY/`. If you add a custom domain later nothing needs to change.

---

## How the build works

| You edit | Becomes |
|---|---|
| `content/notebooks/*.ipynb` | Lessons available inside JupyterLite (`notebooks/` folder in the file list) |
| `content/data/*.csv` | Files students read with `pd.read_csv("data/...")` |
| `jupyter-lite.json` | JupyterLite settings, including the preloaded Python packages |
| `jupyter_lite_config.json` | Build settings (which folders and apps to build) |
| `website/` | The home page, copied on top of JupyterLite's default index |

Student work never touches the repository. It lives in the student's browser and in the `.ipynb` files they download.

---

## Package compatibility and limits

Verified from the Pyodide package list for the pinned version (Pyodide 314.0.6, Python 3.14): NumPy 2.4.6, Matplotlib 3.10.8, pandas 3.0.2, scikit-learn 1.8.0, SciPy 1.18.0 are all available. Re-run `python scripts/check_packages.py` after any upgrade.

Intended for classroom scale. Known limits:

* Small datasets and short training runs only. No GPU, no deep learning libraries, no long jobs.
* Anything using threads/multiprocessing (for example `n_jobs=-1` in scikit-learn) runs single-threaded or fails; leave `n_jobs` at its default.
* Packages with compiled code must exist in Pyodide. Network access from the browser (for `%pip install`, `requests`) is restricted by the browser and school filters.
* The kernel starts slower with more preloaded packages. Expect a noticeable first load; later loads are cached by the browser.
* Matplotlib draws static images inline. Interactive widgets are not set up.
* Notebooks in browser storage can be lost if the school clears browsing data; that is why downloading is part of the student routine.

---

## Troubleshooting

| Problem | What to do |
|---|---|
| Page loads but notebook stays on "Starting kernel" | Wait up to a minute on the first run. If it never finishes, the browser probably cannot reach `cdn.jsdelivr.net`. Ask IT to allow it. |
| Site works at home but not in school | Network filter. Allow `cdn.jsdelivr.net` (Python and packages). If `%pip install` is used, also `pypi.org` and `files.pythonhosted.org`. |
| `ModuleNotFoundError: No module named ...` | Spelling, or the package is not in the browser lab. See [Add or update a Python package](#add-or-update-a-python-package). |
| Graph does not appear | Run `%matplotlib inline` in an earlier cell, then call `plt.show()`. |
| `FileNotFoundError` for a CSV | Use the path `data/filename.csv`, and check the file is listed in the file browser under `data/`. |
| Students see an old version of a lesson | Browser caching or an existing browser copy. See "updates to existing notebooks" above. |
| Workflow fails at "Check browser packages" | A name in `jupyter-lite.json` is not in Pyodide. Fix the spelling or remove it. |
| Workflow fails at "deploy" | In **Settings -> Pages**, set Source to **GitHub Actions**. |
| Page shows 404 for `/lab/` | Open the site through `https://USERNAME.github.io/REPOSITORY/` (with the trailing slash). |
| Works locally, blank under `/REPOSITORY/` | A link in your own edits starts with `/`. Make it relative. |
| Want to avoid the CDN dependency | Build with a self-hosted Pyodide: download a Pyodide release archive matching `PYODIDE_VERSION` in `jupyterlite_pyodide_kernel/constants.py` and run `jupyter lite build --contents content --output-dir _output --pyodide <path-or-url-to-archive>`. This makes the site much larger and is untested in this project. Try it on a branch first. |

---

## Final acceptance test

Run this on the **deployed** site in Chrome or Edge on a school computer:

1. Open the site -> **Start Coding**.
2. **File -> New -> Notebook** (Python).
3. Run `import numpy as np; print(np.arange(5).mean())`.
4. Draw a Matplotlib graph and check it appears under the cell.
5. Run `from sklearn.datasets import load_iris; load_iris().data.shape`.
6. Train a model (open `00_environment_check.ipynb` and **Run All**).
7. Press Ctrl+S, then **File -> Download**.
8. Close the browser. Reopen the site. **Start Coding**.
9. Upload the downloaded `.ipynb`, open it, **Run All**.
10. Open `data/example.csv` through `pd.read_csv("data/example.csv")`.

---

## Repository layout

```
.
├── README.md
├── requirements.txt            # pinned build tools (not student packages)
├── jupyter-lite.json           # JupyterLite settings + preloaded browser packages
├── jupyter_lite_config.json    # build settings
├── content/                    # TEACHER-EDITABLE
│   ├── notebooks/              # lessons (00 environment check, 01-06)
│   └── data/                   # small CSV datasets
├── website/                    # home page (index.html, styles.css, lessons.json)
├── scripts/
│   ├── build.sh                # full build (same as CI)
│   └── check_packages.py       # verifies package names against Pyodide
└── .github/workflows/deploy.yml
```

Layout note: notebooks and data sit inside `content/` (rather than at the repository top level) so JupyterLite can bundle them with their `notebooks/` and `data/` folders intact.

## Privacy

No accounts, no analytics, no tracking, no backend. Notebooks are processed and stored in the student's own browser. Nothing is sent to an AI service or third-party server by this project. (The browser does download Python and packages from the jsDelivr CDN; that is a normal file download and sends no notebook content.)
