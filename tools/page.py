"""Shared document shell for the optional CV and publication updater."""
import html
import json

ORIGIN = 'https://elena-kopteva.github.io'
NAV = [('Research', 'research.html'), ('Publications', 'publications.html'),
       ('CV', 'cv.html'), ('Art', 'art.html'), ('Contact', 'contact.html')]


def page(title, description, content, filename, person=None):
    navigation = '\n'.join(
        f'        <a href="{url}"' + (' aria-current="page"' if url == filename else '') + f'>{label}</a>'
        for label, url in NAV)
    canonical = ORIGIN + ('/' if filename == 'index.html' else '/' + filename)
    structured = ''
    if person:
        structured = '\n  <script type="application/ld+json">\n' + json.dumps(person, ensure_ascii=False, indent=2) + '\n  </script>'
    legacy = '\n  <script src="assets/legacy-links.js" defer></script>' if filename == 'index.html' else ''
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}</title>
  <meta name="description" content="{html.escape(description, quote=True)}">
  <meta name="color-scheme" content="light">
  <link rel="canonical" href="{canonical}">
  <meta property="og:title" content="{html.escape(title, quote=True)}">
  <meta property="og:description" content="{html.escape(description, quote=True)}">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="{ORIGIN}/assets/profile.jpg">
  <meta property="og:image:alt" content="Elena Kopteva beside a blackboard">
  <link rel="stylesheet" href="assets/site.css">{legacy}{structured}
</head>
<body>
  <a class="skip-link" href="#main">Skip to content</a>
  <header class="site-header container">
    <div class="header-inner">
      <a class="brand" href="index.html"{' aria-current="page"' if filename == 'index.html' else ''}>Elena Kopteva</a>
      <nav class="site-nav" aria-label="Main navigation">
{navigation}
      </nav>
    </div>
  </header>
  <main id="main" class="container" tabindex="-1">
{content}
  </main>
  <footer class="site-footer container">
    <div class="footer-inner">
      <span>© Elena Kopteva</span>
      <div class="footer-links">
        <a href="https://orcid.org/0000-0001-8364-0481">ORCID</a>
        <a href="https://arxiv.org/a/kopteva_e_1">arXiv</a>
        <a href="mailto:koptieva@illinois.edu">Email</a>
      </div>
    </div>
  </footer>
</body>
</html>
'''
