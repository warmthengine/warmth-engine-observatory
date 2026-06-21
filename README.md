# Warmth Engine Observatory (WEO)

**AI Infrastructure Coordination Dynamics**

[![Licence: CC BY 4.0](https://img.shields.io/badge/Licence-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

---

## Overview

The Warmth Engine Observatory tracks AI infrastructure coordination dynamics across geopolitical blocs through verified events and mapped Coordination Connections.

**Scope:** WEO tracks *systemic* AI infrastructure coordination — observable coordination dynamics between major power centres (currently nation-states and geopolitical blocs). This differs from operational AI infrastructure management, which addresses how organisations run their own AI systems.

**Live Platform:** [www.warmthengine.com](https://www.warmthengine.com)

---

## Platform Components

- **Event Database** — Verified AI infrastructure coordination events classified by tier (Cross-Bloc, Between-Bloc, Intra-Bloc) and domain (Energy/Infrastructure, Security, Technology, Trade), tagged by industry sector (11-category GICS-anchored taxonomy) and assessed for environmental intersections via Environmental Nexus Tags (5-type ENT taxonomy with Warmth Engine Ratio)
- **Coordination Connections** — Documented relationships between events revealing structural patterns across the database (Policy Cascade, Joint Issuance, Funding Flow, Regulatory Enablement, Response, Framework Family, Parallel Policy)
- **Interactive Map** — Geographic visualisation of global AI infrastructure deployment
- **Interactive Atlas** — Network, timeline, and connectedness analytical surface for exploring coordination topology and event relationships via Cytoscape.js
- **Evidence-Based Verification** — Every event verified through primary and corroborating sources with gold standard evidentiary requirements
- **Sovereign Capability Profiles** — 7-dimension framework assessing 14 state actors' sovereign control across the AI infrastructure stack, with four designation levels (PAA, AIK, ACS, Participant); includes qualification headlines, constraint summaries, sourced evidence, and severance analysis
- **Profiles Page** — Standalone `/profiles/` page rendering the full SCP panel with dimension filtering, actor detail expansion, and Dimension Watch table
- **Dimension Watch** — Forward-looking monitoring table identifying actors approaching a designation status change at the next assessment cycle, with trigger conditions and timeline estimates
- **MCP Integration** — Model Context Protocol server at `warmthengine.com/mcp` exposing fifteen programmatic tools for AI systems to query verified Coordination Intelligence (search_events, get_event, get_connections, get_connection_by_id, get_actors, get_coverage_stats, get_methodology, get_topology, traverse_coordination, get_capability_signatures, get_capability_links, get_threads, get_event_stack, query_scp, get_blocs)

---

## Architecture

The platform uses a decoupled architecture: HTML files serve as lightweight UI shells that fetch data dynamically from the WEO API (Cloudflare Worker + KV).

- **Data source:** Cloudflare KV via WEO API (`warmthengine.com/api/`)
- **MCP endpoint:** `warmthengine.com/mcp` (Model Context Protocol for AI agent access)
- **Authentication:** Token-based (`?token=weo_xxx`) for API and MCP consumers; password header for website
- **Fallback:** Static JSON file for API downtime resilience
- **Hosting:** GitHub Pages with custom domain
- **Routes:** Managed via `wrangler.toml` (`warmthengine.com/api/*` and `warmthengine.com/mcp*`)

Data updates flow through the API — no HTML changes required for new events or connections.

---

## Methodology Documentation

The WEO methodology is documented across four publications, all available on Zenodo with DOI registration:

### Core Documentation

| Publication | DOI |
|---|---|
| **WEO Methodology Manual** — Operational specification covering event verification, significance assessment, tier classification, domain classification, industry tagging, environmental nexus tagging, and Coordination Connection methodology | [`10.5281/zenodo.18427565`](https://doi.org/10.5281/zenodo.18427565) |
| **WEO Methodology Rationale** — Companion document providing empirical derivation, theoretical grounding, and calibration justification for all methodology components | [`10.5281/zenodo.18427582`](https://doi.org/10.5281/zenodo.18427582) |

### Methodology Extensions

| Publication | DOI |
|---|---|
| **Towards Coordination Science: A Framework for Measuring Geopolitical Coordination Dynamics Through Event Relationship Patterns** — Coordination Connection metrics and theoretical foundations (Layer 2 framework) | [`10.5281/zenodo.18427584`](https://doi.org/10.5281/zenodo.18427584) |
| **Tier-Crossing Dynamics in Coordination Networks: A Methodology Extension for Cross-Level Connection Analysis** — Analytical framework for examining Coordination Connections across different tiers | [`10.5281/zenodo.18427586`](https://doi.org/10.5281/zenodo.18427586) |

### Self-Hosted Documentation

The V1.4 Manual and Rationale are self-hosted as navigable HTML with granular section anchoring:

- **Manual:** [`warmthengine.com/research/methodology/manual/`](https://warmthengine.com/research/methodology/manual/) (448 section anchors)
- **Rationale:** [`warmthengine.com/research/methodology/rationale/`](https://warmthengine.com/research/methodology/rationale/) (172 section anchors)

A semantic dictionary (`data/weo-methodology-map.json`) maps 166 WEO-specific terms to their methodology section anchors, serving both human tooltip navigation and the MCP `get_methodology` tool.

---

## Repository Structure

```
warmth-engine-observatory/
├── index.html                  # Main platform (interactive map)
├── atlas.html                  # Interactive atlas (network/timeline/connectedness)
├── events.html                 # Events database
├── methodology.html            # Methodology overview
├── blocs.html                  # Bloc analysis
├── research.html               # Research publications
├── about.html                  # About WEO
├── support.html                # Supporter access
├── legal.html                  # Legal information
├── 404.html                    # Custom error page
├── profiles/
│   └── index.html                  # Sovereign Capability Profiles page (generated)
├── scripts/
│   └── generate_profiles.py        # Profiles page generator (actors JSON → HTML)
├── data/
│   ├── events-free.json            # Static fallback (free-tier event data)
│   └── weo-methodology-map.json    # 166 term-to-anchor semantic mappings
├── research/
│   └── methodology/
│       ├── manual/                 # Self-hosted V1.4 Manual (HTML + PDF)
│       └── rationale/              # Self-hosted V1.4 Rationale (HTML + PDF)
├── sitemap.xml                 # XML sitemap for search engines
├── robots.txt                  # Crawler directives
├── og-image.png                # Open Graph social preview image
├── favicon_48x48.png           # Browser tab icon (48px)
├── favicon_32x32.png           # Browser tab icon (32px)
├── favicon_16x16.png           # Browser tab icon (16px)
├── CNAME                       # Custom domain configuration
├── LICENSE.md                  # Licence information
└── README.md                   # This file
```

---

## Citation

If using this platform or its methodology in research, please cite:

```
Warmth Engine Observatory (WEO)
Warmth Engine, 2026
https://www.warmthengine.com
Licensed under CC BY 4.0
```

---

## Contact

- **Website:** [warmthengine.com](https://www.warmthengine.com)
- **Email:** warmthengine@proton.me

---

## Acknowledgements

This platform uses the following open-source libraries and typefaces:

- **[Leaflet](https://leafletjs.com/)** (BSD-2-Clause) — Interactive map functionality
- **[Leaflet.markercluster](https://github.com/Leaflet/Leaflet.markercluster)** (MIT) — Map marker clustering
- **[Geist](https://vercel.com/font)** (SIL Open Font Licence) — Primary typeface
- **[Geist Mono](https://vercel.com/font)** (SIL Open Font Licence) — Monospace typeface
- **[Cytoscape.js](https://js.cytoscape.org/)** (MIT) — Network graph visualisation (Atlas)

---

## Licence

Methodology documentation is licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).

The platform, event database, and data products are proprietary.

See [LICENSE.md](LICENSE.md) for full details.
