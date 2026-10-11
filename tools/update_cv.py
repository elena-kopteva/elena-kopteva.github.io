"""Regenerate the two static academic records after editing cv.json.

Run from any directory with Python 3. No third party packages are needed.
Publication titles and CV facts are reproduced from the existing source.
"""
from collections import defaultdict
from datetime import date
from html import escape
import json
from pathlib import Path

from page import page

ROOT = Path(__file__).resolve().parents[1]


def e(value):
    return escape(str(value), quote=True)


def paper_links(paper):
    links = []
    if paper.get('arxiv'):
        links.append((f"https://arxiv.org/abs/{paper['arxiv']}", 'arXiv'))
    elif paper.get('url') and not paper.get('doi'):
        links.append((paper['url'], 'Publication'))
    if paper.get('doi'):
        links.append((f"https://doi.org/{paper['doi']}", 'DOI'))
    if paper.get('inspire'):
        links.append((f"https://inspirehep.net/literature/{paper['inspire']}", 'INSPIRE'))
    return '<div class="text-links">' + ''.join(f'<a href="{e(url)}">{e(label)}</a>' for url, label in links) + '</div>' if links else ''


def publication(paper, index):
    title = e(paper['name'])
    if paper.get('url'):
        title = f'<a href="{e(paper["url"])}">{title}</a>'
    journal = e(paper.get('publisher', ''))
    if paper.get('volume'):
        journal += ' ' + e(paper['volume'])
    if paper.get('issue'):
        journal += '(' + e(paper['issue']) + ')'
    if paper.get('pages'):
        journal += ', ' + e(paper['pages'])
    journal += ' (' + e(paper['releaseDate']) + ')'
    anchor = 'arxiv-' + paper['arxiv'] if paper.get('arxiv') else 'publication-' + str(index)
    return f'''<li class="publication" id="{e(anchor)}">
  <h3>{title}</h3>
  <p>{e(', '.join(paper.get('authors', [])))}</p>
  <p class="metadata">{journal}</p>
  {paper_links(paper)}
</li>'''


def publications_content(data):
    groups = defaultdict(list)
    for index, paper in enumerate(data['publications'], 1):
        groups[paper['releaseDate']].append(publication(paper, index))
    years = sorted(groups, reverse=True)
    content = '''<div class="page-heading">
  <p class="eyebrow">Research record</p>
  <h1>Publications</h1>
  <p>Papers in general relativity, cosmology, black hole physics, and semantic dynamics in agent populations.</p>
  <div class="text-links"><a href="https://arxiv.org/a/kopteva_e_1">arXiv author page</a><a href="https://orcid.org/0000-0001-8364-0481">ORCID</a></div>
</div>'''
    content += '<nav class="contents" aria-label="Publication years">' + ''.join(f'<a href="#year-{e(y)}">{e(y)}</a>' for y in years) + '</nav>'
    for year in years:
        content += f'<section class="publication-year" id="year-{e(year)}" aria-labelledby="heading-{e(year)}"><h2 id="heading-{e(year)}">{e(year)}</h2><ol class="publication-list">' + '\n'.join(groups[year]) + '</ol></section>'
    if data.get('researchOutputs'):
        content += '<section class="cv-section" id="research-archives"><h2>Research archives</h2><ol class="publication-list">' + ''.join(publication(p, 'archive-' + str(i)) for i, p in enumerate(data['researchOutputs'])) + '</ol></section>'
    return content


def detail(value):
    if isinstance(value, dict):
        return '<ul>' + ''.join('<li>' + e(k.replace('_', ' ').capitalize()) + '. ' + detail(v) + '</li>' for k, v in value.items()) + '</ul>'
    if isinstance(value, list):
        return '<ul>' + ''.join('<li>' + detail(v) + '</li>' for v in value) + '</ul>'
    if str(value).startswith(('https://', 'http://')):
        return f'<a href="{e(value)}">{e(value)}</a>'
    return e(value)


def entry(record):
    heading_key = next((k for k in ('course', 'title', 'name', 'topic', 'language', 'organization', 'institution') if record.get(k)), None)
    heading = e(record[heading_key]) if heading_key else ''
    start, end = record.get('startDate'), record.get('endDate')
    period = ''
    if start:
        end_label = str(end)[:4] if end and str(end).lower() != 'present' else 'present'
        period = str(start)[:4] + '–' + end_label
    elif record.get('date'):
        period = record['date']
    elif record.get('period'):
        period = record['period']
    elif record.get('releaseDate'):
        period = record['releaseDate']
    skip = {heading_key, 'startDate', 'endDate', 'date', 'period', 'releaseDate'}
    labels = {'studyType': 'Degree', 'area': 'Field', 'thesis': 'Thesis', 'supervisor': 'Supervisor', 'grantNumber': 'Grant', 'role': 'Role', 'amount': 'Award', 'keywords': 'Topics', 'language': 'Language', 'isbn': 'ISBN', 'topics': 'Topics', 'topic': 'Research', 'students': 'Students', 'studentCoauthors': 'Student coauthors'}
    body = ''
    for key, value in record.items():
        if key in skip or not value:
            continue
        if key == 'terms':
            body += '<table class="teaching-terms"><thead><tr><th scope="col">Term</th><th scope="col">Students</th><th scope="col">Notes</th></tr></thead><tbody>'
            for term in value:
                body += '<tr>' + ''.join('<td>' + e(term.get(k, '')) + '</td>' for k in ('term', 'enrollment', 'note')) + '</tr>'
            body += '</tbody></table>'
        elif key in {'position', 'department', 'institution', 'organization', 'location', 'summary', 'note', 'provider', 'venue', 'event', 'publisher', 'subtitle', 'type', 'url', 'role', 'program', 'fluency', 'format', 'level'}:
            body += '<p>' + detail(value) + '</p>'
        elif key in {'highlights', 'awards'}:
            body += detail(value)
        elif key in {'authors', 'keywords', 'topics'}:
            body += '<p>' + e('; '.join(value)) + '</p>'
        else:
            label = labels.get(key, key.replace('_', ' ').capitalize())
            if isinstance(value, (list, dict)):
                body += '<p class="metadata">' + e(label) + '</p>' + detail(value)
            else:
                body += '<dl class="cv-detail"><dt>' + e(label) + '</dt><dd>' + detail(value) + '</dd></dl>'
    return '<article class="cv-entry">\n<h3>' + heading + '</h3>\n' + (f'<p class="metadata">{e(period)}</p>\n' if period else '') + body + '\n</article>\n'


def cv_content(data):
    updated = date.fromisoformat(data['_lastUpdated']).strftime('%B %d, %Y').replace(' 0', ' ')
    content = f'''<div class="page-heading">
  <p class="eyebrow">Academic record</p>
  <h1>Curriculum vitae</h1>
  <p>Visiting Research Scientist<br>Department of Physics, University of Illinois Urbana-Champaign</p>
  <div class="text-links"><a href="assets/CV.pdf">CV (PDF)</a><a href="cv.json">Structured CV (JSON)</a><a href="publications.html">Publications</a></div>
  <p class="metadata" style="margin-top: 18px">Record updated {updated}.</p>
</div>'''
    sections = [('work', 'Appointments'), ('education', 'Education'), ('grants', 'Grants and fellowships'), ('memberships', 'Memberships'), ('teaching', 'Teaching'), ('supervision', 'Student supervision'), ('talks', 'Talks'), ('service', 'Academic service'), ('outreach', 'Outreach'), ('skills', 'Research tools'), ('training', 'Training'), ('books', 'Books'), ('languages', 'Languages'), ('interests', 'Other interests')]
    content += '<nav class="contents" aria-label="CV sections">' + ''.join(f'<a href="#{key}">{title}</a>' for key, title in sections if data.get(key)) + '</nav>'
    for key, title in sections:
        records = data.get(key)
        if not records:
            continue
        content += f'<section class="cv-section" id="{key}"><h2>{title}</h2>'
        if isinstance(records, dict):
            for category, people in records.items():
                content += '<h3>' + {'phd': 'Doctoral research', 'undergraduate': 'Undergraduate research', 'highSchool': 'High school research'}.get(category, e(category)) + '</h3>'
                content += ''.join(entry(record) for record in people)
        else:
            content += ''.join(entry(record) for record in records)
        content += '</section>'
    return content


def main():
    data = json.loads((ROOT / 'cv.json').read_text(encoding='utf-8'))
    for filename, title, description, content in [
        ('publications.html', 'Publications | Elena Kopteva', 'Publications in gravitation, cosmology, black hole physics, and agent research by Elena Kopteva.', publications_content(data)),
        ('cv.html', 'Curriculum vitae | Elena Kopteva', 'Academic appointments, education, research, teaching, and supervision. Elena Kopteva, University of Illinois Urbana-Champaign.', cv_content(data)),
    ]:
        (ROOT / filename).write_text(page(title, description, content, filename), encoding='utf-8')
    print(f"Updated publications.html and cv.html from cv.json. {len(data['publications'])} publications.")


if __name__ == '__main__':
    main()
