# WEO Responsive MOT Fixes Log — May 2026

Source: `SCP_Design/WEO_RESPONSIVE_MOT_MAY_2026.md`

## Summary

| Section | Findings | Status |
|---------|----------|--------|
| 1 — Breakpoint Consistency | F-001 | ✅ Done |
| 2 — Canvas & Interactive Elements | F-008, F-028 | ✅ Done |
| 3 — Touch Targets | F-011, F-012, F-013, F-014 | ✅ Done |
| 4 — Text Readability | F-015, F-016 | ✅ Done |
| 5 — Mobile Navigation | F-020 | ✅ Done |
| 6 — Viewport / dvh | F-023, F-024, F-025 | ✅ Done |

---

## Per-Finding Detail

### F-001 — blocs.html breakpoint 769px → 768px
- **File:** `blocs.html`
- **Change:** `@media (min-width: 769px)` → `@media (min-width: 768px)` (line 1045)

### F-008 — filter-select font-size 16px (iOS zoom prevention)
- **Files:** `events.html`, `atlas.html`
- **Change:** `.filter-select { font-size: 16px; }` added to mobile `@media (max-width: 767px)` block; `.filter-time-selects select { font-size: 16px; }` added to atlas mobile block

### F-011 — modal-close touch target (events.html)
- **File:** `events.html`
- **Change:** `.modal-close` — added `min-width: 44px; min-height: 44px; display: flex; align-items: center; justify-content: center;`

### F-012 — access-modal-close touch target
- **Files:** `events.html`, `index.html`, `SCP_Design/index.html`
- **Change:** `.access-modal-close` — added `min-width: 44px; min-height: 44px; display: flex; align-items: center; justify-content: center;`

### F-013 — panel-close touch target (index.html)
- **File:** `index.html`
- **Change:** Desktop `.panel-close` width/height 32px → 44px (line 1555); mobile override 28px → 44px (line 2591)

### F-014 — weo-nav-toggle touch target (8 files)
- **Files:** `atlas.html`, `events.html`, `methodology.html`, `about.html`, `blocs.html`, `research.html`, `support.html`, `legal.html`
- **Change:** Added `min-width: 44px; min-height: 44px;` to `.weo-nav-toggle` inside mobile `@media (max-width: 767px)` block

### F-015 — legend-sample-star font-size (index.html)
- **File:** `index.html`
- **Change:** `.legend-sample-star { font-size: 9px }` → `font-size: 10px` (line 1262)

### F-016 — weo-nav-logo font-size (atlas.html)
- **File:** `atlas.html`
- **Change:** `.weo-nav-logo { font-size: 8px }` → `font-size: 10px` (line 302)

### F-020 — aria-expanded on nav toggle (6 files)
- **Files:** `methodology.html`, `about.html`, `blocs.html`, `research.html`, `support.html`, `legal.html`
- **Change (JS):** Added `const isOpen = navLinks.classList.contains('open'); navToggle.setAttribute('aria-expanded', isOpen);` after `navLinks.classList.toggle('open')`
- **Change (HTML):** Added `aria-expanded="false"` to `<button class="weo-nav-toggle">` in each file

### F-023 — detail-panel height 100dvh (index.html)
- **File:** `index.html`
- **Change:** Added `height: 100dvh;` after `height: 100vh;` (line 1302) as progressive enhancement

### F-024 — scp-panel height 100dvh + JS pinning (SCP_Design/index.html)
- **File:** `SCP_Design/index.html`
- **Change (CSS):** Added `height: 100dvh;` after `height: 100vh;` on `.scp-panel` (line 5676)
- **Change (JS):** Added `if (window.innerWidth <= 767) { panel.style.height = window.innerHeight + 'px'; }` in `openSCP()` (line 11534)

### F-025 — atlas-panel-v2 max-height 100dvh (atlas.html)
- **File:** `atlas.html`
- **Change:** Added `max-height: 100dvh;` after `max-height: 100vh;` in mobile block (line 3618)

### F-028 — atlas-network min-height 300px (atlas.html)
- **File:** `atlas.html`
- **Change:** `#atlas-network { min-height: 300px; }` added to mobile `@media (max-width: 767px)` block

---

## QA Checklist

- [ ] iOS Safari: no 100vh overflow on detail panel (index), scp-panel, atlas bottom sheet
- [ ] iOS Safari: no auto-zoom on filter selects (events, atlas)
- [ ] Touch targets ≥ 44×44px: panel-close (index), nav toggle (all 8 files), modal-close (events, index, SCP)
- [ ] `aria-expanded` updates correctly on nav toggle open/close (6 files)
- [ ] Atlas canvas visible on mobile (min-height 300px)
- [ ] blocs.html breakpoint: two-column layout switches at 768px not 769px
- [ ] legend-sample-star star icon legible at 10px
- [ ] weo-nav-logo text legible at 10px
