"""Check the site's local pages, assets, and fragment links with Python 3."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import sys

ROOT = Path(__file__).resolve().parents[1]


class Document(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.ids = set()
        self.links = []
        self.errors = []
        self.feed(path.read_text(encoding='utf-8'))

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get('id'):
            if attrs['id'] in self.ids:
                self.errors.append('Duplicate id ' + attrs['id'])
            self.ids.add(attrs['id'])
        for key in ('href', 'src'):
            if attrs.get(key):
                self.links.append(attrs[key])
        if tag == 'img' and not attrs.get('alt'):
            self.errors.append('Image without descriptive alt text')


def main():
    documents = {path: Document(path) for path in ROOT.glob('*.html')}
    errors, checked = [], 0
    for path, document in documents.items():
        errors.extend(f'{path.name}: {error}' for error in document.errors)
        for link in document.links:
            url = urlsplit(link)
            if url.scheme or url.netloc:
                continue
            checked += 1
            target = (path.parent / unquote(url.path)).resolve() if url.path else path
            if not target.is_file():
                errors.append(f'{path.name}: missing file {link}')
            elif url.fragment and target in documents and unquote(url.fragment) not in documents[target].ids:
                errors.append(f'{path.name}: missing fragment {link}')
    if errors:
        print('\n'.join(errors))
        return 1
    print(f'Checked {len(documents)} pages and {checked} local links. All files and fragments resolve.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
