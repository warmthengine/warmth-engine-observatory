# Changelog

All notable changes to the Warmth Engine Observatory will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-10-16

### Added

#### Initial Release
- Initial release of Warmth Engine Observatory
- WE Global Stability Index (WE GSI) monitoring system
- 4 coordination signals (October 10-15, 2025)
- C-MAD Methodology Framework v1.0
- JSON API endpoint (signals.json)
- CSV data export (signals.csv)
- RSS 2.0 feed (feed.xml)

#### Observatory Features
- Dynamic WE GSI gauge with 0-100% precision
- Three-zone gauge background (RED/AMBER/GREEN)
- Smooth color interpolation on position indicator
- Trend arrow showing directional change from previous position
- Stats dashboard with:
  - Real-time signal count
  - Cumulative monthly commitment totals
  - Recency indicator (auto-calculated "X hours ago")
- Source citations for all signals (clickable links to primary sources)
- Print-optimized stylesheet for professional document output
- Section state memory (localStorage tracks expanded/collapsed sections)
- Admin panel (accessible via ?admin=true query parameter)
- Archive page for historical signal tracking
- Mobile-responsive design

#### Documentation
- Comprehensive methodology section
- C-MAD framework explanation
- Analytical Prophecy approach documentation
- FAQ section
- Support information with cryptocurrency donation options

#### Data Access
- JSON API for programmatic access
- CSV export for spreadsheet analysis
- RSS feed for subscription-based monitoring
- All formats include complete signal metadata

### Technical Specifications
- Pure HTML/CSS/JavaScript (no backend required)
- GitHub Pages ready
- SEO optimized with Open Graph and Twitter Card metadata
- Favicon support (32x32 and 16x16)
- Cross-browser compatible
- Accessible navigation structure

---

## Template for Future Updates

When adding new signals or making changes, copy this template:

```markdown
## [X.Y.Z] - YYYY-MM-DD

### Added
- New signal: [Signal Title] (YYYY-MM-DD)
- [Any new features]

### Changed
- WE GSI position updated: [old]% → [new]%
- [Any methodology updates]

### Fixed
- [Any bug fixes]

### Data Updates
- Signal count: [old] → [new]
- Total commitment: [old] → [new]
```

---

## Versioning Guide

- **Major version (X.0.0)**: Methodology framework changes
- **Minor version (0.X.0)**: New features or significant signal additions
- **Patch version (0.0.X)**: Bug fixes, content corrections, routine signal updates

---

## Maintenance Notes

- **Monthly resets**: Signal count and total commitment reset at the start of each month
- **Weekly updates**: Expect 1-2 new signals per week
- **Gauge updates**: WE GSI position changes reflect cumulative analysis of all signals
- **Source verification**: All placeholder URLs should be replaced with actual primary sources before official launch