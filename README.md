# Warmth Engine Observatory (WEO)

**AI Infrastructure Coordination Dynamics**

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

---

## Overview

The Warmth Engine Observatory tracks AI infrastructure coordination dynamics across geopolitical blocs through verified events and mapped coordination connections.

**Scope:** WEO tracks *systemic* AI infrastructure coordination — observable coordination dynamics between major power centres (currently nation-states and geopolitical blocs). This differs from operational AI infrastructure management, which addresses how organisations run their own AI systems.

**Live Platform:** [www.warmthengine.com](https://www.warmthengine.com)

---

## Platform Components

- **Event Database** — Verified AI infrastructure coordination events classified by tier (Cross-Bloc, Between-Bloc, Intra-Bloc) and domain (Energy/Infrastructure, Security, Technology, Trade), and tagged by industry sector (11-category GICS-anchored taxonomy)
- **Coordination Connections** — Documented relationships between events revealing structural patterns across the database (Policy Cascade, Joint Issuance, Funding Flow, Regulatory Enablement, Response, Framework Family, Parallel Policy)
- **Interactive Map** — Geographic visualisation of global AI infrastructure deployment
- **Evidence-Based Verification** — Every event verified through primary and corroborating sources with gold-standard evidentiary requirements

---

## Methodology Documentation

The WEO methodology is documented across four publications, all available on Zenodo with DOI registration:

### Core Documentation

| Publication | DOI |
|---|---|
| **WEO Methodology Manual** — Operational specification covering event verification, significance assessment, tier classification, domain classification, industry tagging, and coordination connection methodology | [`10.5281/zenodo.18427565`](https://doi.org/10.5281/zenodo.18427565) |
| **WEO Methodology Rationale** — Companion document providing empirical derivation, theoretical grounding, and calibration justification for all methodology components | [`10.5281/zenodo.18427582`](https://doi.org/10.5281/zenodo.18427582) |

### Methodology Extensions

| Publication | DOI |
|---|---|
| **Towards Coordination Science: A Framework for Measuring Geopolitical Coordination Dynamics Through Event Relationship Patterns** — Coordination connection metrics and theoretical foundations (Layer 2 framework) | [`10.5281/zenodo.18427584`](https://doi.org/10.5281/zenodo.18427584) |
| **Tier-Crossing Dynamics in Coordination Networks: A Methodology Extension for Cross-Level Connection Analysis** — Analytical framework for examining coordination connections across different tiers | [`10.5281/zenodo.18427586`](https://doi.org/10.5281/zenodo.18427586) |

---

## Repository Structure

```
warmth-engine-observatory/
├── index.html          # Main platform (interactive map)
├── events.html         # Events database
├── methodology.html    # Methodology overview
├── blocs.html          # Bloc analysis
├── research.html       # Research publications
├── about.html          # About WEO
├── support.html        # Supporter access
├── legal.html          # Legal information
├── 404.html            # Custom error page
├── og-image.png        # Open Graph social preview image
├── favicon_32x32.png   # Browser tab icon (32px)
├── favicon_16x16.png   # Browser tab icon (16px)
├── CNAME               # Custom domain configuration
├── LICENSE.md          # License information
└── README.md           # This file
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

This platform uses the following open-source libraries:

- **[Leaflet](https://leafletjs.com/)** (BSD-2-Clause) — Interactive map functionality
- **[Leaflet.markercluster](https://github.com/Leaflet/Leaflet.markercluster)** (MIT) — Map marker clustering
- **[Inter](https://rsms.me/inter/)** (SIL Open Font License) — Primary typeface
- **[JetBrains Mono](https://www.jetbrains.com/lp/mono/)** (SIL Open Font License) — Monospace typeface

---

## License

Methodology documentation is licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).

The platform, event database, and data products are proprietary.

See [LICENSE.md](LICENSE.md) for full details.
