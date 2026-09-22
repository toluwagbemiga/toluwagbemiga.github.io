# toluwagbemiga.github.io

Tolulope Gbenga's personal site, live at <https://toluwagbemiga.github.io>.

Plain HTML, CSS and JavaScript: no framework and no build pipeline to deploy. `index.html` is
generated from `data/profile.json`, so the site's facts live in one file.

## Editing the site

1. Edit `data/profile.json` (experience, projects, skills, certifications, what you're open to).
2. Rebuild:

   ```bash
   python build.py            # regenerate index.html
   python build.py --pdf      # also re-print assets/Tolulope_Gbenga_CV.pdf from cv.html
   ```

   Needs `jinja2` (and Playwright for `--pdf`).
3. Check it locally: `python -m http.server` and open <http://localhost:8000>.
4. Commit and push to `main`. GitHub Pages publishes within a minute or two.

## Layout

| Path | What it is |
|---|---|
| `data/profile.json` | Every fact on the site |
| `templates/index.html.j2` | Page template |
| `build.py` | Renders the template, groups and tags projects, prints the CV PDF |
| `css/styles.css` | Design tokens, dark and light themes, layout |
| `js/main.js` | Theme toggle, mobile nav, project filters, scroll reveals |
| `cv.html` | Print-ready CV, the source of the PDF |
| `assets/` | CV PDF, favicon, social preview image |

The theme follows the visitor's system setting and can be switched in the header; the choice is
remembered. Nothing on the site is collected or tracked.
