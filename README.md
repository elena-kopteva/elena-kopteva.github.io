# Elena Kopteva

Personal research website at [elena-kopteva.github.io](https://elena-kopteva.github.io).

The site uses static HTML, one shared CSS file, and a small script that preserves links to sections of the former homepage. GitHub Pages serves the files directly. There are no runtime packages, external fonts, or build requirements.

## Pages

- `index.html` introduces the scientist and three research directions.
- `research.html` contains the research explanations and related papers.
- `publications.html` lists every publication and research archive in `cv.json`.
- `cv.html` presents appointments, education, teaching, supervision, and the broader academic record.
- `art.html` contains a selection of visual work. Images link to the originals and preserve the full artwork.
- `contact.html` provides email, affiliation, and professional profiles.

The original photograph, research illustrations, artwork files, `assets/CV.pdf`, and `cv.json` remain in place. Former homepage links to `#research`, `#art`, and `#contact` open their respective pages. `#about` remains on the homepage.

## Editing

Edit homepage, research, art, and contact text directly in their HTML files. Shared layout and typography live in `assets/site.css`. The page headers and footers contain the same small navigation structure.

The academic data source is `cv.json`. After updating it, refresh the two academic pages with Python 3.

```sh
python tools/update_cv.py
python tools/check_links.py
```

The updater uses only Python's standard library. It preserves publication titles, authors, journal information, and existing identifiers. Commit the regenerated HTML along with the data. GitHub Pages needs no generation step.

`tools/page.py` contains the shared document shell used by the updater. If navigation or metadata changes, update this shell and the four manually edited pages.

## Local preview

From the repository directory, serve the site with Python 3.

```sh
python -m http.server 8765 --bind 127.0.0.1
```

Open [the local preview](http://127.0.0.1:8765). Main navigation and content work without JavaScript. JavaScript is used only to route old homepage section links.

© Elena Kopteva. All rights reserved for artwork. Academic text and code as noted.
