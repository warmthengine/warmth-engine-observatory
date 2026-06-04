#!/usr/bin/env python3
"""
generate_profiles.py — Produces profiles/index.html from actors-free.json.

Uses the exact SCP panel CSS classes and HTML structure from the homepage.
Actors collapsed by default via <details>/<summary>.
Run: python3 scripts/generate_profiles.py --input path/to/actors-free.json --output profiles/index.html
"""

import json, argparse, html as html_mod, os, sys
from datetime import date

# ── Constants matching index.html SCP panel ──
DN = ['AI Chip Design','Advanced Fabrication','Critical Equipment','AI Compute','Frontier Models','AI Regulation','Sovereign Investment']
DS = ['Chip','Fab','Equip','Compute','Models','Reg','Invest']
DC = ['hw','hw','hw','pl','pl','gv','gv']
DK = ['D1','D2','D3','D4','D5','D6','D7']
BC = {'PAA':'scp-badge-paa','AIK':'scp-badge-aik','ACS':'scp-badge-acs','Part':'scp-badge-part'}
BL = {'PAA':'PAA','AIK':'AIK','ACS':'ACS','Part':'Part'}
GN = {'PAA':'Principal AI Actors','AIK':'AI Infrastructure Keystones','ACS':'Advanced Capability States'}
GC = ['Grade 1','Grade 2','Grade 3']
GCLS = ['scp-src-g1','scp-src-g2','scp-src-g3']
LOCK_ICON = '🔒'

GROUP_ORDER = ['PAA','AIK','ACS','Part']

def esc(s):
    return html_mod.escape(s or '', quote=True)

def normalize(actor):
    dims = [1 if actor['dimensions'].get(k,{}).get('met') else 0 for k in DK]
    con = [actor['dimensions'].get(k,{}).get('constraint') for k in DK]
    hl = [actor['dimensions'].get(k,{}).get('constraint_headline') for k in DK]
    qhl = [actor['dimensions'].get(k,{}).get('qualification_headline') for k in DK]
    qual = [actor['dimensions'].get(k,{}).get('qualification') for k in DK]
    src = []
    for k in DK:
        dim = actor['dimensions'].get(k,{})
        s = dim.get('sources')
        if not s: src.append(None); continue
        p = s.get('primary',{}); c = s.get('corroborating',{})
        if not p.get('publisher'): src.append(None); continue
        src.append([p.get('grade'),p.get('publisher'),p.get('date'),p.get('qualifying_fact'),p.get('url'),
                     c.get('grade'),c.get('publisher'),c.get('date'),c.get('qualifying_fact'),c.get('url')])
    desig = actor.get('designation','Participant')
    d = 'Part' if desig == 'Participant' else desig
    return {
        'id': actor['id'], 'n': actor['name'], 's': actor.get('score',0),
        'd': d, 'dims': dims, 'con': con, 'hl': hl, 'qhl': qhl, 'qual': qual,
        'svd': actor.get('severance_detail'), 'src': src,
        'aik': actor.get('aik_profile'), 'sample': actor.get('sample', False)
    }

def star_svg():
    return '<span style="display:inline-block;vertical-align:super;margin-left:3px;line-height:1;"><svg width="10" height="10" viewBox="0 0 24 24" fill="rgba(255,215,0,0.25)" stroke="#FFD700" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg></span>'

def src_entry_html(label, s, offset):
    grade = s[offset]; pub = s[offset+1]; dt = s[offset+2]; fact = s[offset+3]; url = s[offset+4]
    if not pub: return ''
    gi = (grade or 1) - 1
    h = f'<div class="scp-src-entry">'
    h += f'<span class="scp-src-label">{label}</span> '
    h += f'<span class="scp-src-grade {GCLS[gi]}">{GC[gi]}</span>'
    h += f'{esc(pub)} · {esc(dt or "")}'
    if url: h += f' <a href="{esc(url)}" target="_blank" rel="noopener" class="scp-src-link">↗</a>'
    h += f'<br><span class="scp-src-fact">{esc(fact or "")}</span>'
    h += '</div>'
    return h

def detail_html(a):
    h = ''
    for i in range(7):
        d = a['dims'][i]
        h += '<div class="scp-dim-row">'
        h += f'<span class="scp-dim-name"><span class="scp-dim-dot {DC[i]}"></span>{DN[i]}</span>'
        h += f'<span class="scp-dim-st {"scp-dim-met" if d else "scp-dim-not"}">{"Met" if d else "Not Met"}</span>'
        h += '</div>'
        # Qualification headline (MET)
        if d and a['qhl'][i]:
            h += f'<div class="scp-dim-qual-hl">{esc(a["qhl"][i])}</div>'
        # Constraint
        if d and a['con'][i]:
            h += f'<div class="scp-dim-constraint">{esc(a["con"][i])}</div>'
        elif not d and a['con'][i]:
            h += f'<div class="scp-dim-constraint"><span class="scp-dim-con-label">Constraint:</span> {esc(a["con"][i])}</div>'
        elif not d and a['hl'][i]:
            h += f'<div class="scp-dim-constraint"><span class="scp-dim-con-label">Constraint:</span> {esc(a["hl"][i])}</div>'
        # Qualification expandable (paid tier — only US sample has this data)
        if d and a['qual'][i]:
            h += '<details class="scp-expand"><summary class="scp-qual-trigger"><span class="scp-src-icon">▸</span> Qualification</summary>'
            h += f'<div class="scp-qual-block">{esc(a["qual"][i])}</div></details>'
        # Sources
        if a['src'][i]:
            s = a['src'][i]
            h += '<details class="scp-expand"><summary class="scp-src-trigger"><span class="scp-src-icon">ⓘ</span> Sources</summary>'
            h += '<div class="scp-src-block">'
            h += src_entry_html('Primary', s, 0)
            h += src_entry_html('Corroborating', s, 5)
            h += '</div></details>'
        elif d or (not d and (a['con'][i] or a['hl'][i])):
            h += f'<div class="scp-src-lock">{LOCK_ICON} Sources (supporter access)</div>'

    # AIK Chokepoint Profile
    if a['aik'] and a['d'] == 'AIK':
        h += '<div class="scp-aik">'
        h += '<div class="scp-aik-label">Chokepoint Profile</div>'
        h += f'<div class="scp-aik-nature">{esc(a["aik"].get("chokepoint_nature",""))}</div>'
        h += f'<div class="scp-aik-entities">{esc(a["aik"].get("key_entities",""))}</div>'
        h += '</div>'

    # Severance
    if a['svd']:
        sev_word = 'PASS' if 'PASS' in (a.get('svd','') or '') or a.get('d') in ('PAA','AIK') else 'FAIL'
        # Check actual data
        h += f'<div class="scp-sev"><strong>Severance:</strong> {esc(a["svd"])}</div>'
    elif a['d'] in ('PAA','AIK','ACS'):
        h += f'<div class="scp-src-lock">{LOCK_ICON} Severance analysis (supporter access)</div>'

    return h

def row_html(a):
    name_suffix = star_svg() if a['sample'] else ''
    h = f'<span class="scp-row-name" title="{esc(a["n"])}">{esc(a["n"])}{name_suffix}</span>'
    h += '<div class="scp-row-bar">'
    for i in range(7):
        seg_cls = f' {DC[i]}-m' if a['dims'][i] else ''
        h += f'<div class="scp-row-seg{seg_cls}" data-di="{i}"></div>'
    h += '</div>'
    h += f'<span class="scp-row-score">{a["s"]}/7</span>'
    h += f'<span class="scp-row-badge"><span class="scp-badge {BC[a["d"]]}">{BL[a["d"]]}</span></span>'
    h += '<span class="scp-row-chev">▼</span>'
    return h

def dim_watch_html(watches):
    if not watches: return ''
    h = '<div class="scp-watch">'
    h += '<h2 class="scp-watch-title">Dimension Watch</h2>'
    h += '<p class="scp-watch-desc">Dimensions approaching a status change at the next assessment cycle.</p>'
    h += '<div class="scp-watch-wrap"><table class="scp-watch-table">'
    h += '<thead><tr><th>Actor</th><th>Dimension</th><th>Current</th><th>Expected</th><th>Trigger</th><th>Timeline</th></tr></thead>'
    h += '<tbody>'
    for w in watches:
        dim_key = w.get('dimension','')
        dim_idx = DK.index(dim_key) if dim_key in DK else -1
        dim_name = DN[dim_idx] if dim_idx >= 0 else dim_key
        dim_cat = DC[dim_idx] if dim_idx >= 0 else ''
        current = w.get('current','')
        expected = w.get('expected_change','')
        # Fix "Probable MET" -> "Possible MET"
        if expected == 'Probable MET': expected = 'Possible MET'
        cur_cls = 'scp-dim-met' if current == 'MET' else 'scp-dim-not'
        actor_id = w.get('actor_id','').lower()
        h += '<tr>'
        h += f'<td><a href="#{actor_id}" class="scp-watch-actor">{esc(w.get("actor_id",""))}</a></td>'
        h += f'<td><span class="scp-dim-dot {dim_cat}" style="display:inline-block;margin-right:4px;"></span>{esc(dim_name)}</td>'
        h += f'<td class="{cur_cls}">{esc(current)}</td>'
        h += f'<td>{esc(expected)}</td>'
        h += f'<td>{esc(w.get("trigger",""))}</td>'
        h += f'<td>{esc(w.get("timeline",""))}</td>'
        h += '</tr>'
    h += '</tbody></table></div></div>'
    return h

def pills_html(actors):
    # Count met dimensions
    counts = [0]*7
    for a in actors:
        for i in range(7):
            if a['dims'][i]: counts[i] += 1
    h = '<div class="scp-pills">'
    for i in range(7):
        h += f'<span class="scp-pill {DC[i]}" data-dim="{i}">'
        h += f'<span class="scp-pill-dot"></span>{DS[i]} <span class="scp-pill-ct">{counts[i]}</span>'
        h += '</span>'
    h += '</div>'
    return h

def build_page(data):
    actors = [normalize(a) for a in data['actors']]
    meta = data.get('metadata', {})
    watches = data.get('dimension_watch', [])

    # Map actor IDs to names for dimension watch
    id_to_name = {a['id']: a['n'] for a in actors}

    # Group actors
    groups = {'PAA':[],'AIK':[],'ACS':[],'Part':[]}
    for a in actors:
        groups[a['d']].append(a)

    # Fix dimension watch actor names
    for w in watches:
        aid = w.get('actor_id','')
        if aid in id_to_name:
            w['_name'] = id_to_name[aid]

    # ── Build body content ──
    body = ''
    body += pills_html(actors)
    body += '<div class="scp-body">'

    idx = 0
    for gk in ['PAA','AIK','ACS']:
        grp = groups[gk]
        if not grp: continue
        body += f'<div class="scp-grp">{GN[gk]} ({len(grp)})<span class="scp-grp-line"></span></div>'
        for a in grp:
            aid = f'scp-r{idx}'
            body += f'<details class="scp-actor" id="{a["id"].lower()}">'
            body += f'<summary class="scp-row">{row_html(a)}</summary>'
            body += f'<div class="scp-detail">{detail_html(a)}</div>'
            body += '</details>'
            idx += 1
        if gk == 'PAA':
            body += '<div class="scp-paa-fold"><div class="scp-paa-fold-label">Ecosystem anchors</div></div>'

    # Participants
    parts = groups['Part']
    body += f'<details class="scp-part-group">'
    body += f'<summary class="scp-part-toggle"><span class="scp-part-arr">▶</span> {len(parts)} Participants</summary>'
    body += '<div class="scp-part-rows">'
    for a in parts:
        aid = f'scp-r{idx}'
        body += f'<details class="scp-actor" id="{a["id"].lower()}">'
        body += f'<summary class="scp-row">{row_html(a)}</summary>'
        body += f'<div class="scp-detail">{detail_html(a)}</div>'
        body += '</details>'
        idx += 1
    body += '</div></details>'

    body += dim_watch_html(watches)
    body += '</div>'  # scp-body

    assessment_date = meta.get('assessment_date', '2026-05-06')
    meth_version = meta.get('methodology_version', '1.4')
    reg_version = meta.get('register_version', 'SCP-REG-009')
    today = date.today().isoformat()

    page = f'''<!DOCTYPE html>
<html lang="en-GB">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="weo-version" content="1.3.0">
  <title>Sovereign Capability Profiles — AI Infrastructure Assessments | Warmth Engine Observatory</title>
  <meta name="description" content="Nation-state AI infrastructure assessments across 14 actors. Chip design, fabrication, equipment, compute, frontier models, regulation, and sovereign investment dimensions evaluated with sourced evidence.">
  <link rel="canonical" href="https://warmthengine.com/profiles/">
  <meta property="og:title" content="Sovereign Capability Profiles — Warmth Engine Observatory">
  <meta property="og:description" content="Which nations control the AI infrastructure stack? 14 actors assessed across 7 dimensions with sourced evidence.">
  <meta property="og:type" content="website">
  <meta property="og:url" content="https://warmthengine.com/profiles/">
  <meta property="og:image" content="https://www.warmthengine.com/og-image.png">
  <link rel="icon" type="image/png" sizes="48x48" href="/favicon_48x48.png">
  <link rel="icon" type="image/png" sizes="32x32" href="/favicon_32x32.png">
  <link rel="icon" type="image/png" sizes="16x16" href="/favicon_16x16.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Geist:wght@100..900&family=Geist+Mono:wght@100..900&display=swap" rel="stylesheet">
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "Dataset",
    "name": "WEO Sovereign Capability Profiles",
    "description": "Nation-state AI infrastructure capability assessments across 7 dimensions for 14 actors",
    "url": "https://warmthengine.com/profiles/",
    "creator": {{ "@type": "Organization", "name": "Warmth Engine Observatory", "url": "https://warmthengine.com" }},
    "dateModified": "{today}",
    "license": "https://warmthengine.com/research/methodology/manual/"
  }}
  </script>
  <style>
    /* ── Reset ── */
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    *:focus {{ outline: none; }}
    *:focus-visible {{ outline: 2px solid #60a5fa; outline-offset: 2px; }}

    /* ── Tokens — exact match to index.html ── */
    :root {{
      --scp-hw: #60A5FA; --scp-plat: #A78BFA; --scp-gov: #2DD4BF;
      --scp-paa: #F59E0B; --scp-aik: #06B6D4; --scp-acs: #A855F7; --scp-part: #64748B;
      --weo-radius-sm: 4px; --weo-radius-md: 8px; --weo-radius-lg: 12px;
      --duration-fast: 150ms; --duration-normal: 250ms;
      --ease-out: cubic-bezier(0.33, 1, 0.68, 1);
    }}

    html {{ scroll-behavior: smooth; }}

    body {{
      font-family: 'Geist', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
      font-weight: 380;
      background: #0F172A;
      color: #E2E8F0;
      min-height: 100vh;
      -webkit-font-smoothing: antialiased;
    }}

    /* ── Page frame ── */
    .page-nav {{
      display: flex; justify-content: space-between; align-items: center;
      padding: 12px 32px;
      border-bottom: 1px solid rgba(51,65,85,0.5);
      font-size: 12px; font-weight: 480;
      background: #1E293B;
      position: sticky; top: 0; z-index: 100;
    }}
    .page-nav a {{ color: #94A3B8; text-decoration: none; transition: color var(--duration-fast); }}
    .page-nav a:hover {{ color: #E2E8F0; }}
    .nav-brand {{ color: #CBD5E1; font-weight: 580; display: flex; align-items: center; gap: 6px; }}
    .nav-brand span {{ font-size: 13px; }}
    .nav-links {{ display: flex; gap: 16px; }}

    .page-wrap {{
      max-width: 800px;
      margin: 0 auto;
      padding: 32px 24px 60px;
    }}

    /* ── Header ── */
    .scp-page-title {{ font-size: 22px; font-weight: 580; color: #F1F5F9; letter-spacing: 0.01em; }}
    .scp-page-subtitle {{ font-size: 13px; color: #94A3B8; margin-top: 4px; font-weight: 380; }}
    .scp-page-meta {{
      font-family: 'Geist Mono', 'Fira Code', monospace;
      font-size: 11px; font-weight: 480; color: #64748B;
      margin-top: 10px; letter-spacing: 0.02em;
    }}
    .scp-page-header {{
      padding-bottom: 20px;
      border-bottom: 1px solid rgba(51,65,85,0.5);
      margin-bottom: 4px;
    }}

    /* ── Dimension pills — exact match ── */
    .scp-pills {{
      display: flex; gap: 5px; padding: 14px 0;
      border-bottom: 1px solid rgba(51,65,85,0.5);
      flex-wrap: wrap;
    }}
    .scp-pill {{
      font-size: 12px; font-weight: 480; padding: 4px 11px; border-radius: 12px;
      border: 1px solid transparent; cursor: pointer;
      transition: all var(--duration-fast); user-select: none; white-space: nowrap;
      display: inline-flex; align-items: center; gap: 5px;
    }}
    .scp-pill .scp-pill-dot {{ width: 6px; height: 6px; border-radius: 50%; flex-shrink: 0; }}
    .scp-pill.hw {{ color: #7DB8F5; background: rgba(96,165,250,0.06); border-color: rgba(96,165,250,0.15); }}
    .scp-pill.hw .scp-pill-dot {{ background: var(--scp-hw); }}
    .scp-pill.pl {{ color: #B9A4F8; background: rgba(167,139,250,0.06); border-color: rgba(167,139,250,0.15); }}
    .scp-pill.pl .scp-pill-dot {{ background: var(--scp-plat); }}
    .scp-pill.gv {{ color: #5EDBC9; background: rgba(45,212,191,0.06); border-color: rgba(45,212,191,0.15); }}
    .scp-pill.gv .scp-pill-dot {{ background: var(--scp-gov); }}
    .scp-pill:hover.hw {{ background: rgba(96,165,250,0.12); border-color: rgba(96,165,250,0.3); }}
    .scp-pill:hover.pl {{ background: rgba(167,139,250,0.12); border-color: rgba(167,139,250,0.3); }}
    .scp-pill:hover.gv {{ background: rgba(45,212,191,0.12); border-color: rgba(45,212,191,0.3); }}
    .scp-pill.active.hw {{ background: rgba(96,165,250,0.2); border-color: rgba(96,165,250,0.5); color: #93C5FD; }}
    .scp-pill.active.pl {{ background: rgba(167,139,250,0.2); border-color: rgba(167,139,250,0.5); color: #C4B5FD; }}
    .scp-pill.active.gv {{ background: rgba(45,212,191,0.2); border-color: rgba(45,212,191,0.5); color: #5EEAD4; }}
    .scp-pill-ct {{ font-family: 'Geist Mono','Fira Code',monospace; font-size: 10px; opacity: 0.5; font-weight: 480; }}

    /* ── Body ── */
    .scp-body {{ padding-top: 4px; }}

    /* ── Group headers — exact match ── */
    .scp-grp {{
      font-size: 11px; font-weight: 580; color: #64748B;
      text-transform: uppercase; letter-spacing: 0.06em;
      padding: 16px 0 6px;
      display: flex; align-items: center; gap: 8px;
    }}
    .scp-grp-line {{ flex: 1; height: 1px; background: #334155; }}

    .scp-paa-fold {{ margin: 6px 0 0; border-bottom: 2px solid rgba(245,158,11,0.3); padding-bottom: 6px; }}
    .scp-paa-fold-label {{ font-size: 10px; color: rgba(245,158,11,0.5); text-align: right; letter-spacing: 0.03em; }}

    /* ── Actor rows — uses <details>/<summary> ── */
    .scp-actor {{ border-bottom: 1px solid rgba(255,255,255,0.03); }}
    .scp-actor[open] > .scp-row {{ background: rgba(51,65,85,0.15); }}
    .scp-actor[open] .scp-row-chev {{ transform: rotate(180deg); color: #94A3B8; }}

    .scp-row {{
      display: flex; align-items: center; padding: 10px 0;
      cursor: pointer; transition: background var(--duration-fast) var(--ease-out);
      list-style: none; /* removes default <summary> marker */
    }}
    .scp-row::-webkit-details-marker {{ display: none; }}
    .scp-row::marker {{ display: none; content: ''; }}
    .scp-row:hover {{ background: rgba(255,255,255,0.03); }}

    .scp-row-name {{
      font-size: 14px; font-weight: 480; color: #E2E8F0;
      width: 160px; flex-shrink: 0;
      white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
    }}
    .scp-row-bar {{ display: flex; gap: 3px; flex: 1; max-width: 140px; margin: 0 16px; }}
    .scp-row-seg {{
      flex: 1; height: 9px; border-radius: 2px;
      background: rgba(255,255,255,0.06);
      transition: all var(--duration-fast); position: relative;
    }}
    .scp-row-seg.hw-m {{ background: var(--scp-hw); }}
    .scp-row-seg.pl-m {{ background: var(--scp-plat); }}
    .scp-row-seg.gv-m {{ background: var(--scp-gov); }}
    .scp-row-seg.col-hl {{ outline: 2px solid rgba(255,255,255,0.5); outline-offset: 1px; z-index: 1; }}
    .scp-row-seg.col-hl.hw-m {{ outline-color: rgba(96,165,250,0.8); }}
    .scp-row-seg.col-hl.pl-m {{ outline-color: rgba(167,139,250,0.8); }}
    .scp-row-seg.col-hl.gv-m {{ outline-color: rgba(45,212,191,0.8); }}
    .scp-row-seg.col-dim {{ opacity: 0.2; }}

    .scp-row-score {{
      font-family: 'Geist Mono','Fira Code',monospace;
      font-size: 13px; font-weight: 480; color: #94A3B8;
      width: 36px; text-align: right; flex-shrink: 0;
    }}
    .scp-row-badge {{ margin-left: 12px; flex-shrink: 0; }}
    .scp-badge {{
      display: inline-block; padding: 3px 10px; border-radius: 12px;
      font-size: 11px; font-weight: 580; letter-spacing: 0.05em; text-transform: uppercase;
    }}
    .scp-badge-paa {{ background: rgba(245,158,11,0.15); color: var(--scp-paa); border: 1px solid rgba(245,158,11,0.35); }}
    .scp-badge-aik {{ background: rgba(6,182,212,0.12); color: #22D3EE; border: 1px solid rgba(6,182,212,0.3); }}
    .scp-badge-acs {{ background: rgba(168,85,247,0.12); color: #C084FC; border: 1px solid rgba(168,85,247,0.3); }}
    .scp-badge-part {{ background: rgba(100,116,139,0.12); color: var(--scp-part); border: 1px solid rgba(100,116,139,0.25); }}

    .scp-row-chev {{ font-size: 10px; color: #475569; margin-left: 10px; transition: transform var(--duration-normal) var(--ease-out); flex-shrink: 0; }}

    /* ── Expanded detail — exact match ── */
    .scp-detail {{
      padding: 10px 16px 18px;
      background: rgba(15,23,42,0.3);
    }}
    .scp-dim-row {{ display: flex; align-items: baseline; justify-content: space-between; padding: 5px 0; font-size: 13px; }}
    .scp-dim-name {{ color: #94A3B8; display: flex; align-items: center; gap: 7px; }}
    .scp-dim-dot {{ width: 6px; height: 6px; border-radius: 50%; flex-shrink: 0; }}
    .scp-dim-dot.hw {{ background: var(--scp-hw); }}
    .scp-dim-dot.pl {{ background: var(--scp-plat); }}
    .scp-dim-dot.gv {{ background: var(--scp-gov); }}
    .scp-dim-st {{ font-weight: 580; }}
    .scp-dim-met {{ color: #22C55E; }}
    .scp-dim-not {{ color: var(--scp-part); }}
    .scp-dim-constraint {{ font-size: 12px; color: #64748B; padding: 2px 0 5px 13px; font-style: italic; line-height: 1.5; }}
    .scp-dim-qual-hl {{ font-size: 12px; color: #CBD5E1; padding: 2px 0 5px 13px; line-height: 1.5; }}
    .scp-dim-con-label {{ font-style: normal; font-weight: 580; color: #94A3B8; letter-spacing: 0.01em; }}

    /* ── Expandable triggers ── */
    .scp-expand {{ margin-left: 13px; }}
    .scp-expand summary {{
      font-size: 11px; color: #475569; cursor: pointer;
      padding: 2px 0; display: inline-flex; align-items: center; gap: 4px;
      list-style: none; transition: color var(--duration-fast);
    }}
    .scp-expand summary::-webkit-details-marker {{ display: none; }}
    .scp-expand summary::marker {{ display: none; content: ''; }}
    .scp-expand summary:hover {{ color: #94A3B8; }}

    .scp-qual-trigger {{ font-size: 11px; color: #475569; }}
    .scp-src-trigger {{ font-size: 11px; color: #475569; }}
    .scp-src-icon {{ font-size: 10px; }}

    .scp-qual-block {{
      margin: 4px 0 8px; padding: 10px 14px;
      background: rgba(15,23,42,0.5); border-radius: var(--weo-radius-sm);
      border: 1px solid rgba(255,255,255,0.04);
      font-size: 11px; color: #94A3B8; line-height: 1.6;
    }}
    .scp-src-block {{
      margin: 4px 0 8px; padding: 10px 14px;
      background: rgba(15,23,42,0.5); border-radius: var(--weo-radius-sm);
      border: 1px solid rgba(255,255,255,0.04);
    }}
    .scp-src-entry {{ font-size: 11px; color: #94A3B8; line-height: 1.6; margin-bottom: 6px; }}
    .scp-src-entry:last-child {{ margin-bottom: 0; }}
    .scp-src-label {{ font-weight: 580; color: #64748B; text-transform: uppercase; letter-spacing: 0.04em; font-size: 10px; }}
    .scp-src-grade {{ font-family: 'Geist Mono',monospace; font-size: 10px; padding: 1px 6px; border-radius: 3px; margin-right: 4px; font-weight: 480; }}
    .scp-src-g1 {{ background: rgba(45,212,191,0.12); color: #5EEAD4; }}
    .scp-src-g2 {{ background: rgba(96,165,250,0.12); color: #93C5FD; }}
    .scp-src-g3 {{ background: rgba(148,163,184,0.12); color: #94A3B8; }}
    .scp-src-fact {{ color: #CBD5E1; }}
    .scp-src-link {{ color: var(--scp-aik); text-decoration: none; font-size: 10px; margin-left: 4px; }}
    .scp-src-link:hover {{ text-decoration: underline; }}
    .scp-src-lock {{ font-size: 11px; color: #475569; margin-left: 13px; padding: 3px 0; }}

    /* ── AIK Chokepoint ── */
    .scp-aik {{
      margin-top: 10px; padding: 9px 10px;
      background: rgba(6,182,212,0.04);
      border: 1px solid rgba(6,182,212,0.12);
      border-radius: var(--weo-radius-sm);
    }}
    .scp-aik-label {{ font-size: 10px; font-weight: 580; color: #94A3B8; letter-spacing: 0.06em; text-transform: uppercase; margin-bottom: 4px; }}
    .scp-aik-nature {{ font-size: 13px; color: #CBD5E1; font-weight: 380; line-height: 1.4; }}
    .scp-aik-entities {{ font-size: 12px; color: #64748B; font-style: italic; font-weight: 380; line-height: 1.5; margin-top: 3px; }}

    /* ── Severance ── */
    .scp-sev {{ font-size: 12px; color: #64748B; margin-top: 10px; padding-top: 10px; border-top: 1px solid rgba(255,255,255,0.04); line-height: 1.5; }}
    .scp-sev strong {{ color: #94A3B8; font-weight: 580; }}

    /* ── Participant group ── */
    .scp-part-group > summary {{
      padding: 10px 0; font-size: 12px; color: #94A3B8;
      cursor: pointer; display: flex; align-items: center; gap: 6px;
      border-bottom: 1px solid rgba(255,255,255,0.04);
      transition: background var(--duration-fast); user-select: none;
      list-style: none;
    }}
    .scp-part-group > summary::-webkit-details-marker {{ display: none; }}
    .scp-part-group > summary::marker {{ display: none; content: ''; }}
    .scp-part-group > summary:hover {{ background: rgba(255,255,255,0.03); }}
    .scp-part-arr {{ font-size: 10px; transition: transform var(--duration-normal) var(--ease-out); display: inline-block; }}
    .scp-part-group[open] .scp-part-arr {{ transform: rotate(90deg); }}

    /* ── Dimension Watch ── */
    .scp-watch {{
      margin-top: 32px; padding-top: 24px;
      border-top: 1px solid rgba(51,65,85,0.5);
    }}
    .scp-watch-title {{ font-size: 16px; font-weight: 580; color: #F1F5F9; margin-bottom: 6px; }}
    .scp-watch-desc {{ font-size: 12px; color: #64748B; margin-bottom: 16px; font-weight: 380; }}
    .scp-watch-wrap {{ overflow-x: auto; -webkit-overflow-scrolling: touch; }}
    .scp-watch-table {{ width: 100%; border-collapse: collapse; font-size: 12px; }}
    .scp-watch-table th {{
      text-align: left; font-size: 10px; font-weight: 580;
      color: #64748B; text-transform: uppercase;
      letter-spacing: 0.06em; padding: 8px 10px;
      border-bottom: 1px solid #334155; white-space: nowrap;
    }}
    .scp-watch-table td {{
      padding: 10px; border-bottom: 1px solid rgba(255,255,255,0.03);
      vertical-align: top; color: #94A3B8; line-height: 1.5; font-weight: 380;
    }}
    .scp-watch-table tr:last-child td {{ border-bottom: none; }}
    .scp-watch-table tr:hover td {{ background: rgba(255,255,255,0.01); }}
    .scp-watch-actor {{ color: var(--scp-aik); text-decoration: none; font-weight: 480; }}
    .scp-watch-actor:hover {{ text-decoration: underline; }}

    /* ── Footer ── */
    .scp-page-footer {{
      margin-top: 40px; padding-top: 20px;
      border-top: 1px solid rgba(51,65,85,0.5);
    }}
    .scp-footer-cta {{
      font-size: 12px; color: #94A3B8; margin-bottom: 12px;
      padding: 10px 14px;
      background: rgba(59,130,246,0.04); border: 1px solid rgba(59,130,246,0.12);
      border-radius: var(--weo-radius-sm); font-weight: 380;
    }}
    .scp-footer-links {{ display: flex; gap: 16px; margin-bottom: 10px; font-size: 12px; }}
    .scp-footer-links a {{ color: var(--scp-aik); text-decoration: none; }}
    .scp-footer-links a:hover {{ text-decoration: underline; }}
    .scp-footer-disclaimer {{
      font-size: 10px; color: #94A3B8; line-height: 1.5; opacity: 0.7; font-style: italic;
    }}
    .scp-footer-version {{
      font-family: 'Geist Mono','Fira Code',monospace;
      font-size: 10px; font-weight: 480; color: #94A3B8; opacity: 0.5; margin-top: 8px;
    }}
    .scp-footer-copy {{ font-size: 11px; color: #64748B; margin-top: 8px; }}

    /* ── Responsive ── */
    @media (max-width: 768px) {{
      .page-wrap {{ padding: 24px 16px 40px; }}
      .scp-row-name {{ width: 120px; font-size: 13px; }}
      .scp-row-bar {{ max-width: 100px; margin: 0 10px; }}
      .nav-links {{ gap: 10px; font-size: 11px; }}
    }}
    @media (max-width: 480px) {{
      .scp-row-name {{ width: 100px; font-size: 12px; }}
      .scp-row-bar {{ max-width: 80px; margin: 0 6px; }}
      .scp-dim-row {{ font-size: 12px; }}
      .scp-page-title {{ font-size: 18px; }}
      .page-nav {{ padding: 10px 16px; }}
    }}

    @media (prefers-reduced-motion: reduce) {{
      *, *::before, *::after {{
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
      }}
    }}
  </style>
</head>
<body>
  <nav class="page-nav">
    <a href="/" class="nav-brand"><span>Warmth Engine Observatory</span></a>
    <div class="nav-links">
      <a href="/">Map</a>
      <a href="/atlas.html">Atlas</a>
      <a href="/events.html">Events</a>
      <a href="/profiles/" aria-current="page" style="color:#E2E8F0;">Profiles</a>
      <a href="/about.html">About</a>
    </div>
  </nav>

  <div class="page-wrap">
    <div class="scp-page-header">
      <h1 class="scp-page-title">Sovereign Capability Profiles</h1>
      <div class="scp-page-subtitle">Actor Designation Framework — {meta.get('total_actors',14)} actors assessed</div>
      <div class="scp-page-meta">Assessment: {assessment_date.replace('-',' ')} · Methodology V{meth_version} · {reg_version}</div>
    </div>

    {body}

    <div class="scp-page-footer">
      <div class="scp-footer-cta">Full analysis and sources for all actors available with supporter access.</div>
      <div class="scp-footer-links">
        <a href="/">Explore the interactive map →</a>
        <a href="/research/methodology/manual/">Methodology Manual →</a>
      </div>
      <p class="scp-footer-disclaimer">Designation scores reflect assessed capabilities at the most recent evaluation date. They are not retrospective assessments of capabilities at the time each event in the database occurred.</p>
      <div class="scp-footer-version">SCP Register v1.0 · Assessment: {assessment_date} · Methodology V{meth_version}</div>
      <p class="scp-footer-copy">© 2026 Warmth Engine Observatory</p>
    </div>
  </div>

  <script>
    /* Dimension pill column highlighting */
    (function() {{
      var pills = document.querySelectorAll('.scp-pill');
      var segs = document.querySelectorAll('.scp-row-seg');
      var active = -1;
      pills.forEach(function(p) {{
        p.addEventListener('click', function() {{
          var di = parseInt(p.getAttribute('data-dim'));
          if (active === di) {{
            active = -1;
            pills.forEach(function(pp) {{ pp.classList.remove('active'); }});
            segs.forEach(function(s) {{ s.classList.remove('col-hl','col-dim'); }});
          }} else {{
            active = di;
            pills.forEach(function(pp) {{ pp.classList.remove('active'); }});
            p.classList.add('active');
            segs.forEach(function(s) {{
              var si = parseInt(s.getAttribute('data-di'));
              if (si === di) {{ s.classList.add('col-hl'); s.classList.remove('col-dim'); }}
              else {{ s.classList.add('col-dim'); s.classList.remove('col-hl'); }}
            }});
          }}
        }});
      }});
    }})();
  </script>
  <script data-goatcounter="https://warmthengine.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script>
  <script>(function(){{ var v=document.querySelector('meta[name="weo-version"]'); if(v) console.log('WEO v'+v.getAttribute('content')); }})();</script>
</body>
</html>'''
    return page

def main():
    parser = argparse.ArgumentParser(description='Generate static SCP profiles page')
    parser.add_argument('--input', required=True, help='Path to actors-free.json')
    parser.add_argument('--output', required=True, help='Output path for profiles/index.html')
    args = parser.parse_args()

    with open(args.input, 'r') as f:
        data = json.load(f)

    html_content = build_page(data)

    os.makedirs(os.path.dirname(args.output) or '.', exist_ok=True)
    with open(args.output, 'w') as f:
        f.write(html_content)

    print(f'Generated {args.output} ({len(html_content):,} bytes)')
    print(f'Actors: {len(data["actors"])}')

if __name__ == '__main__':
    main()
