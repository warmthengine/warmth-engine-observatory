#!/usr/bin/env python3
"""
generate_profiles.py — Generate static SCP profiles page for warmthengine.com/profiles/
Usage: python3 scripts/generate_profiles.py --input path/to/actors-free.json --output profiles/index.html
"""

import json
import argparse
import html as _html
from pathlib import Path


def esc(s):
    if s is None:
        return ''
    return _html.escape(str(s))


DESIGNATION_ORDER = ['PAA', 'AIK', 'ACS', 'Participant']
DESIGNATION_LABELS = {
    'PAA': 'Principal AI Actors',
    'AIK': 'AI Infrastructure Keystones',
    'ACS': 'Advanced Capability States',
    'Participant': 'Participants',
}

ACTOR_ORDER = ['US', 'CN', 'JP', 'KR', 'NL', 'EU', 'TW', 'FR', 'DE', 'GB', 'IN', 'IL', 'RU', 'CA']

DIM_CATEGORIES = {
    'D1': 'hw', 'D2': 'hw', 'D3': 'hw',
    'D4': 'pl', 'D5': 'pl',
    'D6': 'gv', 'D7': 'gv',
}

GRADE_STYLES = {
    1: ('rgba(245,158,11,0.15)', '#F59E0B', 'rgba(245,158,11,0.35)'),
    2: ('rgba(59,130,246,0.15)',  '#3B82F6', 'rgba(59,130,246,0.35)'),
    3: ('rgba(100,116,139,0.15)', '#94A3B8', 'rgba(100,116,139,0.3)'),
}

INLINE_CSS = """
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

:root {
  --bg-primary: #0F172A;
  --bg-card: #1E293B;
  --bg-deep: #0B1120;
  --text-primary: #E2E8F0;
  --text-secondary: #94A3B8;
  --text-muted: #64748B;
  --accent: #3B82F6;
  --border: rgba(255,255,255,0.07);
  --scp-hw: #60A5FA;
  --scp-pl: #A78BFA;
  --scp-gv: #2DD4BF;
  --scp-paa: #F59E0B;
  --scp-aik: #06B6D4;
  --scp-acs: #A855F7;
  --scp-part: #64748B;
  --scp-met: #22C55E;
  --r-sm: 4px;
  --r-md: 6px;
  --r-pill: 20px;
}

html { scroll-behavior: smooth; }

body {
  background: var(--bg-primary);
  color: var(--text-primary);
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
  line-height: 1.6;
  -webkit-font-smoothing: antialiased;
}

a { color: var(--accent); text-decoration: none; }
a:hover { text-decoration: underline; }

.page-wrap { max-width: 900px; margin: 0 auto; padding: 0 20px 60px; }

/* ── Page header ── */
.page-header {
  padding: 48px 0 36px;
  border-bottom: 1px solid var(--border);
  margin-bottom: 40px;
}
.page-header h1 {
  font-size: 28px; font-weight: 700; color: var(--text-primary);
  letter-spacing: -0.02em; margin-bottom: 6px;
}
.page-subtitle { font-size: 15px; color: var(--text-secondary); margin-bottom: 18px; }
.page-framework {
  font-size: 13px; color: var(--text-secondary); line-height: 1.7;
  max-width: 720px; margin-bottom: 20px;
}
.page-meta {
  display: flex; gap: 20px; flex-wrap: wrap;
  font-size: 12px; color: var(--text-muted); margin-bottom: 24px;
}

/* ── Dimension legend ── */
.legend-heading {
  font-size: 11px; font-weight: 700; color: var(--text-muted);
  letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 10px;
}
.dim-legend {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 6px;
}
.legend-item {
  display: flex; align-items: flex-start; gap: 7px;
  font-size: 12px; line-height: 1.45; padding: 6px 8px;
  background: rgba(30,41,59,0.5); border-radius: var(--r-sm);
  border: 1px solid var(--border);
}
.legend-dot { width: 7px; height: 7px; border-radius: 50%; flex-shrink: 0; margin-top: 3px; }
.legend-key {
  font-family: 'SF Mono','Fira Code',monospace; font-size: 10px;
  color: var(--text-muted); flex-shrink: 0; min-width: 20px;
}
.legend-name { font-weight: 500; color: var(--text-secondary); flex-shrink: 0; min-width: 100px; }
.legend-desc { color: var(--text-muted); font-size: 11px; }

/* ── Designation groups ── */
.desig-section { margin-bottom: 48px; }
.desig-heading { display: flex; align-items: center; gap: 12px; margin-bottom: 18px; }
.desig-heading h2 { font-size: 14px; font-weight: 700; letter-spacing: 0.01em; white-space: nowrap; }
.desig-line { flex: 1; height: 1px; background: var(--border); }
.desig-paa .desig-heading h2 { color: var(--scp-paa); }
.desig-aik .desig-heading h2 { color: var(--scp-aik); }
.desig-acs .desig-heading h2 { color: var(--scp-acs); }
.desig-participant .desig-heading h2 { color: var(--scp-part); }

/* ── Actor cards ── */
.actor-card {
  background: var(--bg-card); border: 1px solid var(--border);
  border-radius: var(--r-md); margin-bottom: 14px; overflow: hidden;
}
.actor-header {
  padding: 14px 20px 12px; border-bottom: 1px solid var(--border);
}
.actor-title-row {
  display: flex; align-items: center; justify-content: space-between;
  flex-wrap: wrap; gap: 8px; margin-bottom: 10px;
}
.actor-name {
  font-size: 17px; font-weight: 700; color: var(--text-primary);
  display: flex; align-items: center; gap: 8px;
}
.actor-meta { display: flex; align-items: center; gap: 10px; flex-wrap: wrap; }
.actor-score {
  font-family: 'SF Mono','Fira Code',monospace; font-size: 13px;
  font-weight: 700; color: var(--text-secondary);
  background: rgba(255,255,255,0.05); padding: 2px 8px;
  border-radius: var(--r-sm); border: 1px solid var(--border);
}
.actor-badge {
  font-size: 11px; font-weight: 700; letter-spacing: 0.04em;
  padding: 3px 10px; border-radius: var(--r-pill); border: 1px solid;
}
.badge-paa   { background: rgba(245,158,11,0.15); color: #F59E0B;   border-color: rgba(245,158,11,0.35); }
.badge-aik   { background: rgba(6,182,212,0.12);  color: #22D3EE;   border-color: rgba(6,182,212,0.3); }
.badge-acs   { background: rgba(168,85,247,0.12); color: #C084FC;   border-color: rgba(168,85,247,0.3); }
.badge-participant { background: rgba(100,116,139,0.12); color: #64748B; border-color: rgba(100,116,139,0.25); }
.sample-badge {
  font-size: 10px; font-weight: 600;
  background: rgba(255,215,0,0.1); color: #FFD700;
  border: 1px solid rgba(255,215,0,0.25); padding: 1px 6px;
  border-radius: 3px; letter-spacing: 0.03em;
}

/* ── Dimension bar ── */
.dim-bar { display: flex; gap: 4px; align-items: center; }
.dim-bar-dot {
  width: 10px; height: 10px; border-radius: 50%; border: 1.5px solid;
  flex-shrink: 0;
}
.dim-bar-dot.hw.met  { background: var(--scp-hw);  border-color: var(--scp-hw); }
.dim-bar-dot.pl.met  { background: var(--scp-pl);  border-color: var(--scp-pl); }
.dim-bar-dot.gv.met  { background: var(--scp-gv);  border-color: var(--scp-gv); }
.dim-bar-dot.hw.nmet { background: transparent; border-color: rgba(96,165,250,0.3); }
.dim-bar-dot.pl.nmet { background: transparent; border-color: rgba(167,139,250,0.3); }
.dim-bar-dot.gv.nmet { background: transparent; border-color: rgba(45,212,191,0.3); }

/* ── Actor body ── */
.actor-body { padding: 0 20px 14px; }

/* ── Dimensions list ── */
.dimensions-list { list-style: none; }

.dim-item { border-bottom: 1px solid rgba(255,255,255,0.04); padding: 9px 0; }
.dim-item:last-of-type { border-bottom: none; }

.dim-header {
  display: flex; align-items: center; gap: 7px;
  font-size: 13px; flex-wrap: wrap;
}
.dim-dot { width: 6px; height: 6px; border-radius: 50%; flex-shrink: 0; }
.dim-dot.hw     { background: rgba(96,165,250,0.3); }
.dim-dot.pl     { background: rgba(167,139,250,0.3); }
.dim-dot.gv     { background: rgba(45,212,191,0.3); }
.dim-dot.hw.met { background: var(--scp-hw); }
.dim-dot.pl.met { background: var(--scp-pl); }
.dim-dot.gv.met { background: var(--scp-gv); }
.dim-key {
  font-family: 'SF Mono','Fira Code',monospace; font-size: 10px;
  color: var(--text-muted); flex-shrink: 0; min-width: 20px;
}
.dim-name  { color: var(--text-secondary); flex: 1; }
.dim-status { font-size: 11px; font-weight: 700; flex-shrink: 0; }
.dim-met   { color: var(--scp-met); }
.dim-nmet  { color: var(--text-muted); }

.dim-qual-hl {
  font-size: 12px; color: #CBD5E1; line-height: 1.55;
  padding: 4px 0 2px 13px;
}
.dim-constraint {
  font-size: 12px; color: var(--text-muted); line-height: 1.55;
  padding: 4px 0 2px 13px; font-style: italic;
}
.constraint-label { font-style: normal; font-weight: 700; color: var(--text-secondary); }

.dim-details-dd { padding: 2px 0 2px 13px; }
details.dim-details summary {
  font-size: 11px; color: var(--text-muted); cursor: pointer;
  padding: 3px 0; display: inline-flex; align-items: center; gap: 5px;
  list-style: none; -webkit-appearance: none; transition: color 0.15s;
}
details.dim-details summary::-webkit-details-marker { display: none; }
details.dim-details summary::before { content: '▸'; font-size: 9px; }
details.dim-details[open] summary::before { content: '▾'; }
details.dim-details summary:hover { color: var(--text-secondary); }

.dim-qual-block {
  margin-top: 6px; padding: 10px 12px;
  background: rgba(15,23,42,0.6); border-radius: var(--r-sm);
  border: 1px solid var(--border);
  font-size: 12px; color: var(--text-secondary); line-height: 1.65;
}

/* ── Sources ── */
.src-block {
  margin-top: 6px; padding: 10px 12px;
  background: rgba(15,23,42,0.6); border-radius: var(--r-sm);
  border: 1px solid var(--border);
}
.src-entry {
  padding: 8px 0; border-bottom: 1px solid rgba(255,255,255,0.04);
}
.src-entry:last-child { border-bottom: none; padding-bottom: 0; }
.src-meta {
  display: flex; flex-wrap: wrap; align-items: center; gap: 8px; margin-bottom: 5px;
}
.src-type  { font-size: 10px; font-weight: 700; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.05em; }
.src-grade { font-size: 10px; font-weight: 700; padding: 1px 7px; border-radius: 3px; }
.src-pub   { font-size: 11px; color: var(--text-secondary); }
.src-date  { font-size: 10px; color: var(--text-muted); }
.src-fact  { font-size: 11px; color: var(--text-secondary); line-height: 1.55; margin-bottom: 5px; }
.src-link  { font-size: 11px; color: var(--accent); }

/* ── AIK chokepoint ── */
.aik-profile {
  margin-top: 12px; padding: 10px 12px;
  background: rgba(6,182,212,0.06); border: 1px solid rgba(6,182,212,0.15);
  border-radius: var(--r-sm);
}
.aik-label  {
  font-size: 10px; font-weight: 700; color: #94A3B8;
  letter-spacing: 0.07em; text-transform: uppercase; margin-bottom: 4px;
}
.aik-nature   { font-size: 13px; color: #CBD5E1; font-weight: 500; line-height: 1.45; }
.aik-entities { font-size: 11px; color: var(--text-muted); font-style: italic; line-height: 1.55; margin-top: 3px; }

/* ── Severance ── */
.actor-severance {
  font-size: 12px; color: var(--text-muted); margin-top: 12px;
  padding-top: 10px; border-top: 1px solid rgba(255,255,255,0.04);
  line-height: 1.55;
}
.sev-label  { font-weight: 700; color: var(--text-secondary); }
.sev-pass   { color: var(--scp-met); font-weight: 700; }
.sev-fail   { color: #F87171; font-weight: 700; }

/* ── Dimension watch ── */
.watch-section {
  margin-top: 48px; padding-top: 32px; border-top: 1px solid var(--border);
}
.watch-section h2 {
  font-size: 17px; font-weight: 700; color: var(--text-primary); margin-bottom: 8px;
}
.watch-desc { font-size: 13px; color: var(--text-muted); margin-bottom: 16px; }
.table-wrap { overflow-x: auto; -webkit-overflow-scrolling: touch; }
.watch-table { width: 100%; border-collapse: collapse; font-size: 12px; }
.watch-table th {
  text-align: left; font-size: 10px; font-weight: 700;
  color: var(--text-muted); text-transform: uppercase;
  letter-spacing: 0.06em; padding: 8px 12px;
  border-bottom: 1px solid var(--border); white-space: nowrap;
}
.watch-table td {
  padding: 10px 12px; border-bottom: 1px solid rgba(255,255,255,0.03);
  vertical-align: top; color: var(--text-secondary); line-height: 1.5;
}
.watch-table tr:last-child td { border-bottom: none; }
.watch-table tr:hover td { background: rgba(255,255,255,0.01); }
.dim-ref {
  font-family: 'SF Mono','Fira Code',monospace; font-size: 10px;
  color: var(--text-muted);
}
.w-met  { color: var(--scp-met); font-weight: 700; }
.w-nmet { color: var(--text-muted); }

/* ── Footer ── */
.page-footer {
  margin-top: 56px; padding-top: 24px; border-top: 1px solid var(--border);
  font-size: 12px; color: var(--text-muted); line-height: 1.8;
}
.footer-cta {
  font-size: 13px; color: var(--text-secondary); margin-bottom: 14px;
  padding: 10px 14px;
  background: rgba(59,130,246,0.05); border: 1px solid rgba(59,130,246,0.15);
  border-radius: var(--r-sm);
}
.footer-links { display: flex; flex-wrap: wrap; gap: 16px; margin-bottom: 12px; }
.footer-links a { color: var(--accent); }
.footer-copy { font-size: 11px; color: var(--text-muted); }

/* ── Responsive ── */
@media (max-width: 600px) {
  .page-header h1 { font-size: 22px; }
  .actor-title-row { flex-direction: column; align-items: flex-start; }
  .dim-legend { grid-template-columns: 1fr; }
  .page-meta { flex-direction: column; gap: 4px; }
  .actor-name { font-size: 15px; }
}
@media (max-width: 375px) {
  .page-wrap { padding: 0 12px 40px; }
  .page-header { padding: 32px 0 24px; }
}
"""


def render_source(label, src):
    grade = src.get('grade', 3)
    bg, color, border = GRADE_STYLES.get(grade, GRADE_STYLES[3])
    grade_label = f'Grade {grade}'
    pub = esc(src.get('publisher', ''))
    date = esc(src.get('date', ''))
    fact = esc(src.get('qualifying_fact', ''))
    url = esc(src.get('url', ''))
    return f"""<div class="src-entry">
  <div class="src-meta">
    <span class="src-type">{label}</span>
    <span class="src-grade" style="background:{bg};color:{color};border:1px solid {border};">{grade_label}</span>
    <span class="src-pub">{pub}</span>
    <span class="src-date">{date}</span>
  </div>
  <p class="src-fact">{fact}</p>
  <a href="{url}" class="src-link" target="_blank" rel="noopener noreferrer">View source →</a>
</div>"""


def render_dimension(dim_key, dim_data, dim_info, is_sample):
    met = dim_data.get('met', False)
    cat = DIM_CATEGORIES.get(dim_key, 'hw')
    dot_class = f"dim-dot {cat}{' met' if met else ''}"
    dim_name = esc(dim_info.get('name', dim_key))
    status_class = 'dim-met' if met else 'dim-nmet'
    status_label = 'Met' if met else 'Not Met'

    detail_rows = ''

    if met:
        qual_headline = dim_data.get('qualification_headline')
        constraint = dim_data.get('constraint')
        qualification = dim_data.get('qualification')
        sources = dim_data.get('sources')

        if qual_headline:
            detail_rows += f'<dd class="dim-qual-hl">{esc(qual_headline)}</dd>\n'

        if constraint:
            detail_rows += f'<dd class="dim-constraint"><em>{esc(constraint)}</em></dd>\n'

        if is_sample and qualification:
            detail_rows += f"""<dd class="dim-details-dd">
  <details class="dim-details">
    <summary>Qualification</summary>
    <div class="dim-qual-block">{esc(qualification)}</div>
  </details>
</dd>
"""

        if is_sample and sources:
            src_entries = ''
            for label, src in [('Primary', sources.get('primary')), ('Corroborating', sources.get('corroborating'))]:
                if src:
                    src_entries += render_source(label, src)
            detail_rows += f"""<dd class="dim-details-dd">
  <details class="dim-details">
    <summary>Sources</summary>
    <div class="src-block">{src_entries}</div>
  </details>
</dd>
"""
    else:
        constraint_headline = dim_data.get('constraint_headline')
        constraint = dim_data.get('constraint')

        if constraint_headline:
            detail_rows += (
                f'<dd class="dim-constraint">'
                f'<span class="constraint-label">Constraint:</span> {esc(constraint_headline)}'
                f'</dd>\n'
            )

        if is_sample and constraint:
            detail_rows += f'<dd class="dim-constraint">{esc(constraint)}</dd>\n'

    return f"""<div class="dim-item">
<dt class="dim-header">
  <span class="{dot_class}"></span>
  <span class="dim-key">{dim_key}</span>
  <span class="dim-name">{dim_name}</span>
  <span class="dim-status {status_class}">{status_label}</span>
</dt>
{detail_rows}</div>"""


def render_dim_bar(dimensions):
    dots = []
    for dk in ['D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7']:
        met = dimensions.get(dk, {}).get('met', False)
        cat = DIM_CATEGORIES[dk]
        mc = 'met' if met else 'nmet'
        dots.append(f'<span class="dim-bar-dot {cat} {mc}" title="{dk}"></span>')
    return '<div class="dim-bar">' + ''.join(dots) + '</div>'


def render_actor(actor, dimensions_meta):
    actor_id = actor['id'].lower()
    name = esc(actor['name'])
    score = actor.get('score', 0)
    designation = actor.get('designation', 'Participant')
    is_sample = actor.get('sample', False)
    severance = actor.get('severance')
    severance_detail = actor.get('severance_detail', '')
    aik_profile = actor.get('aik_profile')
    dimensions = actor.get('dimensions', {})

    badge_class = f'badge-{designation.lower()}'

    dim_bar_html = render_dim_bar(dimensions)

    dims_html = ''
    for dk in ['D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7']:
        dims_html += render_dimension(dk, dimensions.get(dk, {}), dimensions_meta.get(dk, {}), is_sample)

    aik_html = ''
    if aik_profile:
        nature = esc(aik_profile.get('chokepoint_nature', ''))
        entities = esc(aik_profile.get('key_entities', ''))
        aik_html = f"""<div class="aik-profile">
  <div class="aik-label">Chokepoint Profile</div>
  <div class="aik-nature">{nature}</div>
  <div class="aik-entities">{entities}</div>
</div>"""

    sev_html = ''
    if severance is not None:
        sev_class = 'sev-pass' if severance == 'PASS' else 'sev-fail'
        sev_text = f'<span class="{sev_class}">{esc(severance)}</span>'
        if severance_detail:
            sev_text += f' — {esc(severance_detail)}'
        sev_html = f'<div class="actor-severance"><span class="sev-label">Severance:</span> {sev_text}</div>'

    sample_badge = '<span class="sample-badge">Sample</span> ' if is_sample else ''

    return f"""<article id="{actor_id}" class="actor-card">
  <header class="actor-header">
    <div class="actor-title-row">
      <h3 class="actor-name">{sample_badge}{name}</h3>
      <div class="actor-meta">
        <span class="actor-score">{score}/7</span>
        <span class="actor-badge {badge_class}">{esc(designation)}</span>
      </div>
    </div>
    {dim_bar_html}
  </header>
  <div class="actor-body">
    <dl class="dimensions-list">
{dims_html}
    </dl>
    {aik_html}
    {sev_html}
  </div>
</article>"""


def render_watch(watch_list, actors_by_id, dimensions_meta):
    rows = ''
    for item in watch_list:
        actor_id = item.get('actor_id', '')
        actor_name = esc(actors_by_id.get(actor_id, {}).get('name', actor_id))
        dim = item.get('dimension', '')
        dim_name = esc(dimensions_meta.get(dim, {}).get('name', ''))
        current = esc(item.get('current', ''))
        expected = esc(item.get('expected_change', ''))
        trigger = esc(item.get('trigger', ''))
        timeline = esc(item.get('timeline', ''))
        cur_class = 'w-met' if item.get('current') == 'MET' else 'w-nmet'
        rows += f"""<tr>
  <td><a href="#{actor_id.lower()}">{actor_name}</a></td>
  <td><span class="dim-ref">{esc(dim)}</span> {dim_name}</td>
  <td class="{cur_class}">{current}</td>
  <td>{expected}</td>
  <td>{trigger}</td>
  <td>{timeline}</td>
</tr>
"""
    return f"""<section class="watch-section">
  <h2>Dimension Watch</h2>
  <p class="watch-desc">Dimensions under active monitoring for potential status change at next assessment.</p>
  <div class="table-wrap">
    <table class="watch-table">
      <thead>
        <tr>
          <th>Actor</th>
          <th>Dimension</th>
          <th>Current</th>
          <th>Expected Change</th>
          <th>Trigger</th>
          <th>Timeline</th>
        </tr>
      </thead>
      <tbody>
{rows}
      </tbody>
    </table>
  </div>
</section>"""


def render_legend(dimensions_meta):
    items = ''
    for dk in ['D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7']:
        info = dimensions_meta.get(dk, {})
        cat = DIM_CATEGORIES[dk]
        cat_var = {'hw': 'var(--scp-hw)', 'pl': 'var(--scp-pl)', 'gv': 'var(--scp-gv)'}[cat]
        name = esc(info.get('name', dk))
        desc = esc(info.get('description', ''))
        items += f"""<div class="legend-item">
  <span class="legend-dot" style="background:{cat_var};"></span>
  <span class="legend-key">{dk}</span>
  <span class="legend-name">{name}</span>
  <span class="legend-desc">{desc}</span>
</div>
"""
    return f'<div class="dim-legend">\n{items}</div>'


def generate_html(data):
    meta = data['metadata']
    dims = data['dimensions']
    actors = data['actors']
    watch = data.get('dimension_watch', [])

    actors_by_id = {a['id']: a for a in actors}

    groups = {d: [] for d in DESIGNATION_ORDER}
    for actor_id in ACTOR_ORDER:
        if actor_id in actors_by_id:
            actor = actors_by_id[actor_id]
            groups.setdefault(actor.get('designation', 'Participant'), []).append(actor)

    sections_html = ''
    for des in DESIGNATION_ORDER:
        group = groups.get(des, [])
        if not group:
            continue
        label = DESIGNATION_LABELS.get(des, des)
        des_class = f'desig-{des.lower()}'
        actors_html = ''.join(render_actor(a, dims) for a in group)
        sections_html += f"""<section class="desig-section {des_class}">
  <div class="desig-heading">
    <h2>{label} ({len(group)})</h2>
    <div class="desig-line"></div>
  </div>
  {actors_html}
</section>
"""

    assessment_date = esc(meta.get('assessment_date', ''))
    methodology_version = esc(meta.get('methodology_version', ''))
    total_actors = meta.get('total_actors', 14)

    legend_html = render_legend(dims)
    watch_html = render_watch(watch, actors_by_id, dims)

    json_ld = json.dumps({
        "@context": "https://schema.org",
        "@type": "Dataset",
        "name": "WEO Sovereign Capability Profiles",
        "description": "Nation-state AI infrastructure capability assessments across 7 dimensions for 14 actors",
        "url": "https://warmthengine.com/profiles/",
        "creator": {
            "@type": "Organisation",
            "name": "Warmth Engine Observatory",
            "url": "https://warmthengine.com"
        },
        "dateModified": "2026-06-03",
        "license": "https://warmthengine.com/research/methodology/manual/"
    }, indent=2)

    framework_desc = (
        "The Sovereign Capability Profile (SCP) framework assesses nation-state control of the AI infrastructure "
        "stack across seven dimensions: chip design, advanced fabrication, critical equipment, AI compute, frontier "
        "models, AI regulation, and sovereign investment. Actors are designated as Principal AI Actors (PAA), "
        "AI Infrastructure Keystones (AIK), Advanced Capability States (ACS), or Participants through a three-gate "
        "framework evaluating dimensional breadth, severance resilience, and platform sustainability."
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Sovereign Capability Profiles — AI Infrastructure Assessments | Warmth Engine Observatory</title>
  <meta name="description" content="Nation-state AI infrastructure assessments across 14 actors. Chip design, fabrication, equipment, compute, frontier models, regulation, and sovereign investment dimensions evaluated with sourced evidence.">
  <link rel="canonical" href="https://warmthengine.com/profiles/">
  <meta property="og:title" content="Sovereign Capability Profiles — Warmth Engine Observatory">
  <meta property="og:description" content="Which nations control the AI infrastructure stack? 14 actors assessed across 7 dimensions with sourced evidence.">
  <meta property="og:type" content="website">
  <meta property="og:url" content="https://warmthengine.com/profiles/">
  <script type="application/ld+json">
{json_ld}
  </script>
  <style>
{INLINE_CSS}
  </style>
</head>
<body>
  <div class="page-wrap">
    <header class="page-header">
      <h1>Sovereign Capability Profiles</h1>
      <p class="page-subtitle">Actor Designation Framework — {total_actors} actors assessed</p>
      <p class="page-framework">{framework_desc}</p>
      <div class="page-meta">
        <span>Assessment date: {assessment_date}</span>
        <span>Methodology: V{methodology_version}</span>
        <span>Register: SCP-REG-009</span>
      </div>
      <p class="legend-heading">Dimensions</p>
      {legend_html}
    </header>

    <main>
{sections_html}
      {watch_html}
    </main>

    <footer class="page-footer">
      <p class="footer-cta">Full analysis and sources for all actors available with supporter access.</p>
      <div class="footer-links">
        <a href="/?scp=open">Explore the interactive Sovereign Capability Profiles →</a>
        <a href="/research/methodology/manual/">Methodology Manual →</a>
      </div>
      <p class="footer-copy">SCP Register v1.0 · Assessment: May 2026 · Methodology V1.4 · © 2026 Warmth Engine</p>
    </footer>
  </div>
</body>
</html>"""


def main():
    parser = argparse.ArgumentParser(description='Generate static SCP profiles page')
    parser.add_argument('--input',  required=True, help='Path to actors-free.json')
    parser.add_argument('--output', required=True, help='Output path for index.html')
    args = parser.parse_args()

    input_path  = Path(args.input).expanduser()
    output_path = Path(args.output).expanduser()

    with open(input_path, encoding='utf-8') as f:
        data = json.load(f)

    html = generate_html(data)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f'Generated: {output_path}')


if __name__ == '__main__':
    main()
