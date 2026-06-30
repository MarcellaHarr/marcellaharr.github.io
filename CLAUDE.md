# Marcella Harris · Data Portfolio

A static GitHub Pages portfolio site showcasing Marcella's data analytics projects across R, SQL, Excel, Python, and web development.


## How it works
- `index.html` is the homepage — it serves as the editorial hub with featured project cards and blog-style articles
- Root-level HTML files (`r-studio.html`, `excel.html`, `web-dev.html`, `sql-repo.html`, `jupyter.html`, `follow-along.html`) are the per-discipline repo landing pages linked in the nav
- `repos/` holds individual project detail pages (e.g. `sprightlyHomeschool.html`, `nashvilleHousing.html`)
- `assets/img/` stores project visuals, organized into subdirectories by project name (e.g. `ny-street-trees/`, `sprightly-homeschool/`)
- `_config.yml` configures the Jekyll theme fallback for GitHub Pages


## Tech Layers
- **Framework**: None — pure static HTML; Bootstrap 5.3 used for layout and components
- **Language**: HTML5, CSS3, vanilla JavaScript (front-end); Python 3.14.3 (via UV, back-end/scripting layer in progress)
- **Database**: None (static site); featured projects reference MySQL and SQL Server externally
- **Styling**: Bootstrap 5.3 (`assets/css/bootstrap.min.css`), custom `assets/css/blog.css`, Google Fonts (Playfair Display), dark/light theme toggle via `assets/js/color-modes.js`
- **Testing**: ESLint 9.5 (JS linting only, no test suite)


## Project Structure
```
marcellaharr.github.io/
├── index.html                  # Homepage — featured cards + blog articles
├── web-dev.html                # Web Dev repo landing page
├── r-studio.html               # R-Studio repo landing page
├── excel.html                  # Excel repo landing page
├── sql-repo.html               # SQL repo landing page
├── jupyter.html                # Jupyter repo landing page
├── follow-along.html           # Follow-Along repo landing page
├── repos/                      # Individual project detail pages
│   ├── sprightlyHomeschool.html
│   ├── nashvilleHousing.html
│   ├── googleCyclisticCasestudy.html
│   ├── usaGovernors.html
│   ├── wgu.html
│   └── articleSkeleton.html    # Template for new project write-ups
├── assets/
│   ├── css/                    # blog.css (custom), bootstrap.min.css, style.css (DocSearch)
│   ├── js/                     # bootstrap.bundle.min.js, color-modes.js (theme toggle)
│   └── img/                    # Project images grouped by project subfolder
├── _config.yml                 # Jekyll config (GitHub Pages)
├── pyproject.toml              # UV Python project (Python ≥ 3.14, no deps yet)
├── main.py                     # Python entry point (placeholder)
├── package.json                # Node — ESLint only
└── .gitportfolio-venv/         # UV virtual environment (gitignored)
```


## Development
```bash
uv sync                    # Install Python dependencies (from pyproject.toml)
npm install                # Install Node dependencies (ESLint)
npx eslint assets/js/      # Lint JavaScript files
# Open any .html file with VS Code Live Server to preview
```
> There is no build step — all HTML files are served as-is by GitHub Pages.


## Code Standards
- Follow ESLint rules (config in `package.json` / `.eslintrc` if added)
- Use Bootstrap 5.3 utility classes and grid system — do not introduce a second CSS framework
- Inline styles exist throughout; minimize adding new ones — prefer `blog.css` or scoped `<style>` blocks
- Dark/light theme is driven by `data-bs-theme-value` attributes and `color-modes.js` — do not hardcode colors that break in either mode
- Python code lives in `main.py` and any future modules; managed with UV (`uv add <pkg>`)


## Project-Specific Rules
- New repo landing pages follow the pattern of existing root-level HTML files — copy structure from `web-dev.html`
- New project detail pages go in `repos/` — use `articleSkeleton.html` as the starting template
- Project images go in a new `assets/img/<project-name>/` subfolder, not the root or `images/` (legacy, gitignored)
- The `bootstrap/` folder is a gitignored submodule — do not edit files inside it
- Nav links appear identically across every page — update all pages when a nav item changes


## Important Notes
- Site is deployed via GitHub Pages at `https://marcellaharr.github.io` — all merges to `main` are live
- The `images/` folder is gitignored (legacy path) — use `assets/img/` for all new images
- Python environment: UV venv at `.gitportfolio-venv/`, Python 3.14.3, no packages installed yet
- `_config.yml` sets `jekyll-theme-cayman` as fallback theme — GitHub Pages may apply it if `index.html` is absent
- Accent color is `#712cf9` (violet); light yellow `#FFFFC0` is used on active nav links


## Common Mistakes to Avoid
- DON'T: Add new images to the root `images/` folder — it is gitignored.
- DON'T: Hardcode light-mode colors; test changes in both dark and light theme.
- DON'T: Edit files inside `bootstrap/` — it is a gitignored submodule.
- DON'T: Push untested nav changes — the nav block is duplicated across every HTML file.
- ALWAYS: Ask me follow-up questions until you have 95% confidence in what needs to be built.
- ALWAYS: Use `articleSkeleton.html` as the base when creating a new project detail page.
- ALWAYS: Add new project images to `assets/img/<project-name>/` as a subfolder.
- ALWAYS: Mirror nav changes across all root-level and `repos/` HTML files.


## Applied Learning
The first Python environment for this project was initialized on macOS using UV (`uv init` + `uv venv .gitportfolio-venv`), migrating from a previous Windows setup.
