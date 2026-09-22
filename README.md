# toluwagbemiga.github.io

Personal portfolio site for Tolulope Gbenga — Software Engineer (Android & Blockchain).

Live at: https://toluwagbemiga.github.io

## Stack

Plain HTML, CSS and JavaScript. No build step, no framework, no bundler — just static files served by GitHub Pages.

## Structure

```
index.html                       Main site
css/styles.css                   All styles (design tokens, light/dark themes)
js/main.js                       Theme toggle, mobile nav, project filters, scroll reveal
assets/favicon.svg               Favicon (generated SVG monogram)
assets/og-image.png              Social preview image
assets/Tolulope_Gbenga_CV.pdf    Downloadable CV (generated from cv.html)
cv.html                          Standalone, print-ready CV source (A4)
404.html                         Custom not-found page
robots.txt / sitemap.xml         Basic SEO
.nojekyll                        Disables Jekyll processing on GitHub Pages
```

## Updating content

All content is sourced from Tolulope's verified profile data. To update:

1. Edit `index.html` directly (experience, projects, skills, etc. are hand-written HTML; the skills grid is rendered from a small JS array at the bottom of the file).
2. Edit `cv.html` for the CV, then regenerate the PDF with Playwright:
   ```
   page.goto("file:///path/to/cv.html")
   page.pdf(path="assets/Tolulope_Gbenga_CV.pdf", format="A4", print_background=True)
   ```
3. Commit and push to `main` — GitHub Pages deploys automatically.

## Local preview

```
python -m http.server 8000
```
