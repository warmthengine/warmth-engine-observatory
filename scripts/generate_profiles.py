#!/usr/bin/env python3
"""
generate_profiles.py — Grid-layout SCP profiles page.
Dimension dots column-align under pills. Actors collapsed by default.
Run: python3 scripts/generate_profiles.py --input path/to/actors-free.json --output profiles/index.html
"""
import json, argparse, html as H, os
from datetime import date

DN = ['AI Chip Design','Advanced Fabrication','Critical Equipment','AI Compute','Frontier Models','AI Regulation','Sovereign Investment']
DS = ['Chip','Fab','Equip','Compute','Models','Reg','Invest']
DC = ['hw','hw','hw','pl','pl','gv','gv']
DK = ['D1','D2','D3','D4','D5','D6','D7']
BC = {'PAA':'paa','AIK':'aik','ACS':'acs','Part':'part'}
BL = {'PAA':'PAA','AIK':'AIK','ACS':'ACS','Part':'Part'}
GN = {'PAA':'Principal AI Actors','AIK':'AI Infrastructure Keystones','ACS':'Advanced Capability States'}
GC = ['Grade 1','Grade 2','Grade 3']
GCLS = ['g1','g2','g3']
e = lambda s: H.escape(s or '', quote=True)

def norm(a):
    dims=[1 if a['dimensions'].get(k,{}).get('met') else 0 for k in DK]
    con=[a['dimensions'].get(k,{}).get('constraint') for k in DK]
    hl=[a['dimensions'].get(k,{}).get('constraint_headline') for k in DK]
    qhl=[a['dimensions'].get(k,{}).get('qualification_headline') for k in DK]
    qual=[a['dimensions'].get(k,{}).get('qualification') for k in DK]
    src=[]
    for k in DK:
        s=a['dimensions'].get(k,{}).get('sources')
        if not s: src.append(None); continue
        p=s.get('primary',{}); c=s.get('corroborating',{})
        if not p.get('publisher'): src.append(None); continue
        src.append([p.get('grade'),p.get('publisher'),p.get('date'),p.get('qualifying_fact'),p.get('url'),
                     c.get('grade'),c.get('publisher'),c.get('date'),c.get('qualifying_fact'),c.get('url')])
    d='Part' if a.get('designation')=='Participant' else a.get('designation','Part')
    return dict(id=a['id'],n=a['name'],s=a.get('score',0),d=d,dims=dims,con=con,hl=hl,qhl=qhl,qual=qual,
                svd=a.get('severance_detail'),src=src,aik=a.get('aik_profile'),sample=a.get('sample',False))

def star():
    return '<span class="sample-star"><svg width="11" height="11" viewBox="0 0 24 24" fill="rgba(255,215,0,0.3)" stroke="#FFD700" stroke-width="2.5"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg></span>'

def src_html(label, s, off):
    pub=s[off+1]; g=s[off]; dt=s[off+2]; fact=s[off+3]; url=s[off+4]
    if not pub: return ''
    gi=(g or 1)-1
    h=f'<div class="src-entry"><span class="src-label">{label}</span> '
    h+=f'<span class="src-grade {GCLS[gi]}">{GC[gi]}</span>'
    h+=f'{e(pub)} &middot; {e(dt or "")}'
    if url: h+=f' <a href="{e(url)}" target="_blank" rel="noopener" class="src-link">&#8599;</a>'
    h+=f'<br><span class="src-fact">{e(fact or "")}</span></div>'
    return h

def detail(a):
    h=''
    for i in range(7):
        d=a['dims'][i]
        h+=f'<div class="det-dim"><span class="det-dim-name"><span class="det-dot {DC[i]}"></span>{DN[i]}</span>'
        h+=f'<span class="det-st {"det-met" if d else "det-not"}">{"Met" if d else "Not Met"}</span></div>'
        if d and a['qhl'][i]:
            h+=f'<div class="det-qhl">{e(a["qhl"][i])}</div>'
        if d and a['con'][i]:
            h+=f'<div class="det-con">{e(a["con"][i])}</div>'
        elif not d and a['con'][i]:
            h+=f'<div class="det-con"><span class="det-con-label">Constraint:</span> {e(a["con"][i])}</div>'
        elif not d and a['hl'][i]:
            h+=f'<div class="det-con"><span class="det-con-label">Constraint:</span> {e(a["hl"][i])}</div>'
        if d and a['qual'][i]:
            h+='<details class="det-expand"><summary class="det-exp-trig">&#9656; Qualification</summary>'
            h+=f'<div class="det-exp-body">{e(a["qual"][i])}</div></details>'
        if a['src'][i]:
            h+='<details class="det-expand"><summary class="det-exp-trig">&#9432; Sources</summary>'
            h+=f'<div class="det-exp-body">{src_html("Primary",a["src"][i],0)}{src_html("Corroborating",a["src"][i],5)}</div></details>'
        elif d or (not d and (a['con'][i] or a['hl'][i])):
            h+='<div class="det-lock">&#128274; Sources (supporter access)</div>'
    if a['aik'] and a['d']=='AIK':
        h+='<div class="det-aik"><div class="det-aik-label">Chokepoint Profile</div>'
        h+=f'<div class="det-aik-nature">{e(a["aik"].get("chokepoint_nature",""))}</div>'
        h+=f'<div class="det-aik-ent">{e(a["aik"].get("key_entities",""))}</div></div>'
    if a['svd']:
        h+=f'<div class="det-sev"><strong>Severance:</strong> {e(a["svd"])}</div>'
    elif a['d'] in ('PAA','AIK','ACS'):
        h+='<div class="det-lock">&#128274; Severance analysis (supporter access)</div>'
    return h

def actor_row(a):
    ns=star() if a['sample'] else ''
    dots=''
    for i in range(7):
        if a['dims'][i]:
            dots+=f'<span class="dot dot-met {DC[i]}" data-di="{i}"></span>'
        else:
            dots+=f'<span class="dot dot-unmet" data-di="{i}"></span>'
    h=f'<details class="actor" id="{a["id"].lower()}">'
    h+=f'<summary class="row"><span class="row-name" title="{e(a["n"])}">{e(a["n"])}{ns}</span>'
    h+=f'<span class="row-dots">{dots}</span>'
    h+=f'<span class="row-score">{a["s"]}/7</span>'
    h+=f'<span class="row-badge"><span class="badge badge-{BC[a["d"]]}">{BL[a["d"]]}</span></span>'
    h+=f'<span class="row-chev">&#9660;</span></summary>'
    h+=f'<div class="det">{detail(a)}</div></details>'
    return h

def pills(actors):
    cts=[0]*7
    for a in actors:
        for i in range(7):
            if a['dims'][i]: cts[i]+=1
    h='<div class="pills-row"><span class="pills-spacer"></span><span class="pills-grid">'
    for i in range(7):
        h+=f'<span class="pill {DC[i]}" data-dim="{i}"><span class="pill-dot"></span>{DS[i]} <span class="pill-ct">{cts[i]}</span></span>'
    h+='</span></div>'
    return h

def watch_html(ws):
    if not ws: return ''
    h='<div class="watch"><h2 class="watch-title">Dimension Watch</h2>'
    h+='<p class="watch-desc">Dimensions approaching a status change at the next assessment cycle.</p>'
    h+='<table class="watch-tbl"><thead><tr><th>Actor</th><th>Dimension</th><th>Current</th><th>Potential</th><th>Trigger</th><th>Timeline</th></tr></thead><tbody>'
    for w in ws:
        dk=w.get('dimension',''); di=DK.index(dk) if dk in DK else -1
        dn=DN[di] if di>=0 else dk; dc=DC[di] if di>=0 else ''
        exp=w.get('expected_change','')
        if exp=='Probable MET': exp='Possible MET'
        cur=w.get('current',''); cc='det-met' if cur=='MET' else 'det-not'
        aid=w.get('actor_id','').lower()
        tr_cls=f' class="watch-row-{dc}"' if dc else ''
        h+=f'<tr{tr_cls}><td><a href="#{aid}" class="watch-link">{e(w.get("actor_id",""))}</a></td>'
        h+=f'<td><span class="det-dot {dc}" style="display:inline-block;margin-right:5px;"></span>{e(dn)}</td>'
        h+=f'<td class="{cc}">{e(cur)}</td><td>{e(exp)}</td><td>{e(w.get("trigger",""))}</td><td>{e(w.get("timeline",""))}</td></tr>'
    h+='</tbody></table></div>'
    return h

def build_page(data):
    actors=[norm(a) for a in data['actors']]
    meta=data.get('metadata',{})
    groups={'PAA':[],'AIK':[],'ACS':[],'Part':[]}
    for a in actors: groups[a['d']].append(a)
    m=pills(actors)
    m+='<div class="matrix-body">'
    idx=0
    for gk in ['PAA','AIK','ACS']:
        g=groups[gk]
        if not g: continue
        m+=f'<div class="grp">{GN[gk]} ({len(g)})<span class="grp-line"></span></div>'
        for a in g: m+=actor_row(a); idx+=1
        if gk=='PAA':
            m+='<div class="paa-fold"><span class="paa-fold-label">Ecosystem anchors</span></div>'
    parts=groups['Part']
    m+=f'<details class="part-group"><summary class="part-toggle"><span class="part-arr">&#9654;</span> {len(parts)} Participants</summary><div class="part-inner">'
    for a in parts: m+=actor_row(a); idx+=1
    m+='</div></details>'
    m+=watch_html(data.get('dimension_watch',[]))
    m+='</div>'
    ad=meta.get('assessment_date','2026-05-06')
    mv=meta.get('methodology_version','1.4')
    rv=meta.get('register_version','SCP-REG-009')
    td=date.today().isoformat()
    return f'''<!DOCTYPE html>
<html lang="en-GB">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<meta name="weo-version" content="1.3.0">
<title>Sovereign Capability Profiles — AI Infrastructure Assessments | Warmth Engine Observatory</title>
<meta name="description" content="Nation-state AI infrastructure assessments across 14 actors and 7 dimensions. Chip design, fabrication, equipment, compute, frontier models, regulation, and sovereign investment.">
<link rel="canonical" href="https://warmthengine.com/profiles/">
<meta property="og:title" content="Sovereign Capability Profiles — Warmth Engine Observatory">
<meta property="og:description" content="Which nations control the AI infrastructure stack? 14 actors assessed across 7 dimensions.">
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
{{"@context":"https://schema.org","@type":"Dataset","name":"WEO Sovereign Capability Profiles","description":"Nation-state AI infrastructure capability assessments across 7 dimensions for 14 actors, applying the Actor Designation Framework (PAA, AIK, ACS, Participant) with qualification headlines, constraint summaries, and Dimension Watch monitoring upcoming status changes.","url":"https://warmthengine.com/profiles/","license":"https://www.warmthengine.com/legal.html","creator":{{"@type":"Organization","name":"Warmth Engine Observatory","url":"https://warmthengine.com"}},"dateModified":"{td}","inLanguage":"en-GB","isAccessibleForFree":true,"temporalCoverage":"{ad}/..","keywords":["sovereign capability profiles","AI infrastructure assessment","actor designation","PAA","AIK","ACS","7-dimension scoring","AI chip design","advanced fabrication","critical equipment","AI compute","frontier models","AI regulation","sovereign investment","Dimension Watch","geopolitical AI capability"]}}
</script>
<style>
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
*:focus{{outline:none}} *:focus-visible{{outline:2px solid #60a5fa;outline-offset:2px}}
:root{{
  --hw:#60A5FA;--pl:#A78BFA;--gv:#2DD4BF;
  --paa:#F59E0B;--aik:#06B6D4;--acs:#A855F7;--part:#64748B;
  --base:#0F172A;--raised:#1E293B;--border:#334155;
  --t1:#F1F5F9;--t2:#E2E8F0;--t3:#CBD5E1;--t4:#94A3B8;--t5:#64748B;
  --r-sm:4px;--r-md:8px;--r-lg:12px;
  --fast:150ms;--norm:250ms;--ease:cubic-bezier(.33,1,.68,1);
  --col-w:88px;
  --link:#3B82F6;--link-hover:#60A5FA;
}}
html{{scroll-behavior:smooth}}
body{{font-family:'Geist',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;font-weight:380;background:var(--base);color:var(--t2);min-height:100vh;-webkit-font-smoothing:antialiased}}

/* Nav */
.weo-nav{{display:flex;align-items:center;justify-content:space-between;padding:14px 36px;border-bottom:1px solid var(--border);position:sticky;top:0;z-index:100;background:var(--raised);box-shadow:0 1px 8px rgba(0,0,0,.3)}}
.weo-nav-brand{{display:flex;align-items:center;gap:8px;text-decoration:none;color:var(--t2);font-weight:600;font-size:.875rem;transition:color var(--fast) var(--ease)}}
.weo-nav-brand:hover{{color:#2DD4BF}}
.weo-nav-logo{{width:28px;height:28px;background:linear-gradient(135deg,rgba(45,212,191,.15) 0%,rgba(59,130,246,.1) 100%);border:1px solid rgba(45,212,191,.25);border-radius:6px;display:flex;align-items:center;justify-content:center;font-family:'Geist Mono',monospace;font-size:.5rem;font-weight:700;color:#2DD4BF}}
.weo-nav-links{{display:flex;align-items:center;gap:4px}}
.weo-nav-links a{{padding:4px 8px;color:var(--t4);text-decoration:none;font-size:.8125rem;font-weight:500;border-radius:var(--r-sm);transition:all var(--fast) var(--ease)}}
.weo-nav-links a:hover{{color:var(--t2);background:rgba(59,130,246,.1)}}
.weo-nav-links a.active{{color:#2DD4BF;background:rgba(45,212,191,.1)}}
.weo-nav-toggle{{display:none;width:32px;height:32px;background:var(--raised);border:1px solid var(--border);border-radius:var(--r-sm);cursor:pointer;flex-direction:column;align-items:center;justify-content:center;gap:4px}}
.weo-nav-toggle span{{display:block;width:16px;height:2px;background:var(--t4);border-radius:1px;transition:all var(--norm) var(--ease)}}
.weo-nav-toggle:hover{{background:rgba(59,130,246,.2);border-color:#60A5FA}}
.weo-nav-toggle:hover span{{background:var(--t2)}}
@media(max-width:767px){{.weo-nav{{position:relative;padding:12px 16px}} .weo-nav-links{{display:none;position:absolute;top:100%;left:0;right:0;flex-direction:column;background:rgba(15,23,42,.97);border:1px solid rgba(96,165,250,.2);border-top:2px solid rgba(96,165,250,.8);border-radius:var(--r-md);padding:8px;margin-top:8px;z-index:100;box-shadow:0 4px 24px rgba(0,0,0,.5),inset 0 1px 0 rgba(255,255,255,.03);backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px)}} .weo-nav-links.open{{display:flex}} .weo-nav-links a{{width:100%;padding:8px 16px}} .weo-nav-toggle{{display:flex;min-width:44px;min-height:44px}}}}

/* Panel */
.panel{{max-width:1100px;margin:36px auto;background:var(--raised);border:1px solid var(--border);border-radius:var(--r-lg);box-shadow:0 4px 32px rgba(0,0,0,.35),inset 0 1px 0 rgba(255,255,255,.03);padding:28px 36px 32px}}

/* Header */
.hdr{{padding-bottom:20px;border-bottom:1px solid rgba(51,65,85,.5)}}
.hdr-title{{font-size:22px;font-weight:580;color:var(--t1);letter-spacing:.01em}}
.hdr-sub{{font-size:13px;color:var(--t4);margin-top:3px;font-weight:380}}
.hdr-meta{{font-family:'Geist Mono','Fira Code',monospace;font-size:11px;font-weight:480;color:var(--t5);margin-top:8px;letter-spacing:.02em}}

/* Pills — column-aligned with dots below */
.pills-row{{display:flex;align-items:center;padding:16px 0 12px;border-bottom:1px solid rgba(51,65,85,.5)}}
.pills-spacer{{width:200px;flex-shrink:0}}
.pills-grid{{display:grid;grid-template-columns:repeat(7,var(--col-w));justify-items:center;gap:6px 0}}
.pill{{font-size:11px;font-weight:480;padding:4px 8px;cursor:pointer;transition:all var(--fast);user-select:none;white-space:nowrap;display:flex;align-items:center;justify-content:center;gap:4px;border-radius:10px;border:1px solid transparent}}
.pill .pill-dot{{width:6px;height:6px;border-radius:50%;flex-shrink:0}}
.pill.hw{{color:#7DB8F5}} .pill.hw .pill-dot{{background:var(--hw)}}
.pill.pl{{color:#B9A4F8}} .pill.pl .pill-dot{{background:var(--pl)}}
.pill.gv{{color:#5EDBC9}} .pill.gv .pill-dot{{background:var(--gv)}}
.pill:hover.hw{{background:rgba(96,165,250,.1);border-color:rgba(96,165,250,.25)}}
.pill:hover.pl{{background:rgba(167,139,250,.1);border-color:rgba(167,139,250,.25)}}
.pill:hover.gv{{background:rgba(45,212,191,.1);border-color:rgba(45,212,191,.25)}}
.pill.active.hw{{background:rgba(96,165,250,.18);border-color:rgba(96,165,250,.45);color:#93C5FD}}
.pill.active.pl{{background:rgba(167,139,250,.18);border-color:rgba(167,139,250,.45);color:#C4B5FD}}
.pill.active.gv{{background:rgba(45,212,191,.18);border-color:rgba(45,212,191,.45);color:#5EEAD4}}
.pill-ct{{font-family:'Geist Mono',monospace;font-size:9px;opacity:.5;font-weight:480}}

/* Groups */
.grp{{font-size:11px;font-weight:580;color:var(--t5);text-transform:uppercase;letter-spacing:.06em;padding:18px 0 6px;display:flex;align-items:center;gap:8px}}
.grp-line{{flex:1;height:1px;background:var(--border)}}
.paa-fold{{margin:6px 0 0;border-bottom:2px solid rgba(245,158,11,.3);padding-bottom:6px}}
.paa-fold-label{{display:block;font-size:10px;color:rgba(245,158,11,.5);text-align:right;letter-spacing:.03em}}

/* Actor rows — flex + grid dots */
.actor{{border-bottom:1px solid rgba(255,255,255,.03)}}
.actor[open]>.row{{background:rgba(51,65,85,.15)}}
.actor[open] .row-chev{{transform:rotate(180deg);color:var(--t4)}}
.row{{display:flex;align-items:center;padding:10px 0;cursor:pointer;transition:background var(--fast) var(--ease);list-style:none}}
.row::-webkit-details-marker,.row::marker{{display:none;content:''}}
.row:hover{{background:rgba(255,255,255,.025)}}
.row-name{{font-size:15px;font-weight:480;color:var(--t2);width:200px;flex-shrink:0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
.sample-star{{display:inline-block;vertical-align:super;margin-left:3px;line-height:1}}
.row-dots{{display:grid;grid-template-columns:repeat(7,var(--col-w));justify-items:center;align-items:center}}
.dot{{width:36px;height:14px;border-radius:4px;transition:all var(--fast)}}
.dot-met.hw{{background:var(--hw)}} .dot-met.pl{{background:var(--pl)}} .dot-met.gv{{background:var(--gv)}}
.dot-unmet{{background:transparent;border:1.5px solid rgba(255,255,255,.1)}}
.dot.col-hl{{transform:scale(1.3);box-shadow:0 0 8px rgba(255,255,255,.2)}}
.dot.col-hl.hw{{box-shadow:0 0 10px rgba(96,165,250,.4)}}
.dot.col-hl.pl{{box-shadow:0 0 10px rgba(167,139,250,.4)}}
.dot.col-hl.gv{{box-shadow:0 0 10px rgba(45,212,191,.4)}}
.dot.col-dim{{opacity:.15}}
.row-score{{font-family:'Geist Mono','Fira Code',monospace;font-size:14px;font-weight:480;color:var(--t4);width:44px;text-align:right;flex-shrink:0;margin-left:16px}}
.row-badge{{margin-left:12px;flex-shrink:0}}
.badge{{display:inline-block;padding:3px 11px;border-radius:12px;font-size:11px;font-weight:580;letter-spacing:.05em;text-transform:uppercase}}
.badge-paa{{background:rgba(245,158,11,.15);color:var(--paa);border:1px solid rgba(245,158,11,.35)}}
.badge-aik{{background:rgba(6,182,212,.12);color:#22D3EE;border:1px solid rgba(6,182,212,.3)}}
.badge-acs{{background:rgba(168,85,247,.12);color:#C084FC;border:1px solid rgba(168,85,247,.3)}}
.badge-part{{background:rgba(100,116,139,.12);color:var(--part);border:1px solid rgba(100,116,139,.25)}}
.row-chev{{font-size:10px;color:var(--t5);margin-left:10px;transition:transform var(--norm) var(--ease);flex-shrink:0}}

/* Detail */
.det{{padding:12px 20px 20px;background:rgba(15,23,42,.3);border-top:1px solid rgba(255,255,255,.03)}}
.det-dim{{display:flex;align-items:baseline;justify-content:space-between;padding:5px 0;font-size:13px}}
.det-dim-name{{color:var(--t4);display:flex;align-items:center;gap:7px}}
.det-dot{{width:6px;height:6px;border-radius:50%;flex-shrink:0;display:inline-block}}
.det-dot.hw{{background:var(--hw)}} .det-dot.pl{{background:var(--pl)}} .det-dot.gv{{background:var(--gv)}}
.det-st{{font-weight:580}} .det-met{{color:#22C55E}} .det-not{{color:var(--part)}}
.det-qhl{{font-size:12px;color:var(--t3);padding:2px 0 5px 14px;line-height:1.5}}
.det-con{{font-size:12px;color:var(--t5);padding:2px 0 5px 14px;font-style:italic;line-height:1.5}}
.det-con-label{{font-style:normal;font-weight:580;color:var(--t4);letter-spacing:.01em}}
.det-expand{{margin-left:14px}} .det-expand summary{{font-size:11px;color:var(--t5);cursor:pointer;padding:2px 0;list-style:none;transition:color var(--fast)}}
.det-expand summary::-webkit-details-marker,.det-expand summary::marker{{display:none;content:''}}
.det-expand summary:hover{{color:var(--t4)}}
.det-exp-body{{margin:4px 0 8px;padding:10px 14px;background:rgba(15,23,42,.5);border-radius:var(--r-sm);border:1px solid rgba(255,255,255,.04);font-size:11px;color:var(--t4);line-height:1.6}}
.det-lock{{font-size:11px;color:var(--t5);margin-left:14px;padding:3px 0}}
.src-entry{{font-size:11px;color:var(--t4);line-height:1.6;margin-bottom:6px}} .src-entry:last-child{{margin-bottom:0}}
.src-label{{font-weight:580;color:var(--t5);text-transform:uppercase;letter-spacing:.04em;font-size:10px}}
.src-grade{{font-family:'Geist Mono',monospace;font-size:10px;padding:1px 6px;border-radius:3px;margin-right:4px;font-weight:480}}
.g1{{background:rgba(45,212,191,.12);color:#5EEAD4}} .g2{{background:rgba(96,165,250,.12);color:#93C5FD}} .g3{{background:rgba(148,163,184,.12);color:var(--t4)}}
.src-fact{{color:var(--t3)}} .src-link{{color:var(--link);text-decoration:none;font-size:10px;margin-left:4px}} .src-link:hover{{color:var(--link-hover);text-decoration:underline}}

/* AIK / Sev */
.det-aik{{margin-top:10px;padding:10px 12px;background:rgba(6,182,212,.04);border:1px solid rgba(6,182,212,.12);border-radius:var(--r-sm)}}
.det-aik-label{{font-size:10px;font-weight:580;color:var(--t4);letter-spacing:.06em;text-transform:uppercase;margin-bottom:4px}}
.det-aik-nature{{font-size:13px;color:var(--t3);font-weight:380;line-height:1.4}}
.det-aik-ent{{font-size:12px;color:var(--t5);font-style:italic;font-weight:380;line-height:1.5;margin-top:3px}}
.det-sev{{font-size:12px;color:var(--t5);margin-top:10px;padding-top:10px;border-top:1px solid rgba(255,255,255,.04);line-height:1.5}}
.det-sev strong{{color:var(--t4);font-weight:580}}

/* Participants */
.part-group>summary{{padding:10px 0;font-size:13px;color:var(--t4);cursor:pointer;display:flex;align-items:center;gap:6px;border-bottom:1px solid rgba(255,255,255,.04);list-style:none;user-select:none;font-weight:480}}
.part-group>summary::-webkit-details-marker,.part-group>summary::marker{{display:none;content:''}}
.part-group>summary:hover{{color:var(--t2)}}
.part-arr{{font-size:10px;transition:transform var(--norm) var(--ease);display:inline-block}}
.part-group[open] .part-arr{{transform:rotate(90deg)}}

/* Watch */
.watch{{margin-top:48px;padding-top:22px;border-top:1px solid rgba(51,65,85,.5)}}
.watch-title{{font-size:17px;font-weight:580;color:var(--t1);margin-bottom:5px}}
.watch-desc{{font-size:12px;color:var(--t5);margin-bottom:14px;font-weight:380}}
.watch-tbl{{width:100%;border-collapse:collapse;font-size:12px}}
.watch-tbl th{{text-align:left;font-size:10px;font-weight:580;color:var(--t5);text-transform:uppercase;letter-spacing:.06em;padding:8px 10px;border-bottom:1px solid var(--border);white-space:nowrap}}
.watch-tbl td{{padding:10px;border-bottom:1px solid rgba(255,255,255,.03);vertical-align:top;color:var(--t4);line-height:1.5;font-weight:380}}
.watch-tbl tr:hover td{{background:rgba(255,255,255,.01)}}
.watch-tbl td:nth-child(5){{color:var(--t3)}}
.watch-tbl td:first-child{{border-left:3px solid transparent;padding-left:8px}}
.watch-row-hw td:first-child{{border-left-color:rgba(96,165,250,0.3)}}
.watch-row-pl td:first-child{{border-left-color:rgba(167,139,250,0.3)}}
.watch-row-gv td:first-child{{border-left-color:rgba(45,212,191,0.3)}}
.watch-tbl .det-dot{{width:8px;height:8px}}
.watch-link{{color:var(--link);text-decoration:none;font-weight:480}} .watch-link:hover{{color:var(--link-hover);text-decoration:underline}}

/* Footer */
.ftr{{margin-top:28px;padding-top:20px;border-top:1px solid rgba(51,65,85,.5)}}
.ftr-cta{{font-size:12px;color:var(--t4);margin-bottom:14px;padding:10px 16px;background:rgba(59,130,246,.04);border:1px solid rgba(59,130,246,.12);border-radius:var(--r-sm);font-weight:380}}
.ftr-links{{display:flex;gap:18px;margin-bottom:10px;font-size:12px}}
.ftr-links a{{color:var(--link);text-decoration:none}} .ftr-links a:hover{{color:var(--link-hover);text-decoration:underline}}
.ftr-disc{{font-size:10px;color:var(--t4);line-height:1.5;opacity:.7;font-style:italic}}
.ftr-ver{{font-family:'Geist Mono',monospace;font-size:10px;font-weight:480;color:var(--t4);opacity:.5;margin-top:8px}}
.ftr-copy{{font-size:11px;color:var(--t5);margin-top:8px}}
.ftr-legal{{font-size:11px;margin-top:4px}} .ftr-legal a{{color:var(--t4);text-decoration:none}} .ftr-legal a:hover{{color:var(--link)}}

/* Responsive */
@media(max-width:1140px){{.panel{{margin:24px 16px;padding:24px 24px 28px}} :root{{--col-w:64px}} .row-name,.pills-spacer{{width:160px}} .row-name{{font-size:14px}}}}
@media(max-width:860px){{:root{{--col-w:52px}} .row-name,.pills-spacer{{width:130px}} .row-name{{font-size:13px}} .dot{{width:12px;height:12px}} .row-score{{font-size:13px;width:38px}} .badge{{font-size:10px;padding:2px 8px}}}}
@media(max-width:640px){{:root{{--col-w:40px}} .row-name,.pills-spacer{{width:110px}} .row-name{{font-size:12px}} .dot{{width:10px;height:10px}} .pill{{font-size:9px}} .pill-ct{{font-size:8px}} .panel{{margin:16px 8px;padding:16px 12px 20px}} .hdr-title{{font-size:18px}} .row-score{{font-size:12px;width:34px;margin-left:8px}} .row-badge{{margin-left:6px}} .row-chev{{margin-left:4px}}}}
@media(prefers-reduced-motion:reduce){{*,*::before,*::after{{animation-duration:.01ms!important;animation-iteration-count:1!important;transition-duration:.01ms!important}}}}
</style>
</head>
<body>
<nav class="weo-nav">
  <a href="/" class="weo-nav-brand">
    <span class="weo-nav-logo">WEO</span>
    <span>Warmth Engine Observatory</span>
  </a>
  <button class="weo-nav-toggle" id="navToggle" aria-label="Toggle navigation" aria-expanded="false">
    <span></span><span></span><span></span>
  </button>
  <div class="weo-nav-links" id="navLinks">
    <a href="/">Map</a>
    <a href="/atlas.html">Atlas</a>
    <a href="/events.html">Events</a>
    <a href="/profiles/" class="active">Profiles</a>
    <a href="/blocs.html">Blocs</a>
    <a href="/methodology.html">Methodology</a>
    <a href="/research.html">Research</a>
    <a href="/about.html">About</a>
    <a href="/support.html">Support</a>
  </div>
</nav>
<div class="panel">
  <div class="hdr">
    <h1 class="hdr-title">Sovereign Capability Profiles</h1>
    <div class="hdr-sub">Actor Designation Framework &mdash; {meta.get('total_actors',14)} actors assessed</div>
    <div class="hdr-meta">Assessment: {ad} &middot; Methodology V{mv} &middot; {rv}</div>
  </div>
  {m}
  <div class="ftr">
    <div class="ftr-cta">Full analysis and sources for all actors available with supporter access.</div>
    <div class="ftr-links"><a href="/">Explore the interactive map &rarr;</a><a href="/research/methodology/manual/">Methodology Manual &rarr;</a></div>
    <p class="ftr-disc">Designation scores reflect assessed capabilities at the most recent evaluation date. They are not retrospective assessments of capabilities at the time each event in the database occurred.</p>
    <div class="ftr-ver">SCP Register v1.0 &middot; Assessment: {ad} &middot; Methodology V{mv}</div>
    <p class="ftr-copy">&copy; 2026 Warmth Engine Observatory</p>
    <p class="ftr-legal"><a href="/legal.html">Privacy Policy &amp; Terms of Service</a></p>
  </div>
</div>
<script>
(function(){{
  var pills=document.querySelectorAll('.pill'),dots=document.querySelectorAll('.dot'),active=-1;
  pills.forEach(function(p){{
    p.addEventListener('click',function(){{
      var di=parseInt(p.getAttribute('data-dim'));
      if(active===di){{active=-1;pills.forEach(function(pp){{pp.classList.remove('active')}});dots.forEach(function(d){{d.classList.remove('col-hl','col-dim')}})}}
      else{{active=di;pills.forEach(function(pp){{pp.classList.remove('active')}});p.classList.add('active');dots.forEach(function(d){{var si=parseInt(d.getAttribute('data-di'));if(si===di){{d.classList.add('col-hl');d.classList.remove('col-dim')}}else{{d.classList.add('col-dim');d.classList.remove('col-hl')}}}})}}
    }})
  }})
}})();
</script>
<script>
var navToggle=document.getElementById('navToggle');
var navLinks=document.getElementById('navLinks');
if(navToggle&&navLinks){{
  navToggle.addEventListener('click',function(){{
    navLinks.classList.toggle('open');
    navToggle.setAttribute('aria-expanded',navLinks.classList.contains('open'));
  }});
}}
</script>
<script data-goatcounter="https://warmthengine.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script>
<script>(function(){{var v=document.querySelector('meta[name="weo-version"]');if(v)console.log('WEO v'+v.getAttribute('content'))}})();</script>
</body>
</html>'''

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--input',required=True)
    p.add_argument('--output',required=True)
    a=p.parse_args()
    with open(a.input) as f: d=json.load(f)
    h=build_page(d)
    os.makedirs(os.path.dirname(a.output) or '.',exist_ok=True)
    with open(a.output,'w') as f: f.write(h)
    print(f'Generated {a.output} ({len(h):,} bytes, {len(d["actors"])} actors)')

if __name__=='__main__': main()
