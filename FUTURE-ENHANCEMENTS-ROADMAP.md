# Warmth Engine Observatory - Future Enhancements Roadmap

## Purpose
This document provides implementation guidance for planned platform enhancements. Reference this when the platform is ready for each phase of development.

---

## PHASE 2: Historical Trend Visualization
**Timeline:** Months 3-6 (approximately January - April 2026)  
**Prerequisites:** Minimum 20 signals tracked, 12+ weeks of data

### Objective
Add visual trend indicators to show coordination signal velocity and patterns over time without cluttering the dashboard.

### Implementation Components

#### 1. Weekly Signal Velocity Chart

**Location:** Below stats dashboard, above signal list

**Visual Design:**
```
Signal Activity Trend (Last 12 Weeks)

  █
  █     █
  █ █   █ █
▃ █ █ █ █ █ ▅ █
─────────────────
Week of: Oct 1 → Dec 24

4 signals per week average
↗ Trend: Increasing activity
```

**Data Requirements:**
- Track signals by week added to platform
- Calculate 12-week rolling average
- Identify trend direction (↗ increasing, → stable, ↘ decreasing)

**Technical Implementation:**
- Add `week_added` field to signals.json
- Create simple ASCII/Unicode bar chart in HTML
- OR use lightweight charting library (Chart.js, minimal)
- Update automatically when new signals added

---

#### 2. WE GSI Historical Movement

**Location:** Near WE GSI gauge

**Visual Design:**
```
WE GSI Movement (Last 6 Assessments)

    58%
55% ─●───●─────●
        │   │   
        │   └─ Nov 15
        └───── Nov 1
```

**Data Requirements:**
- Store WE GSI value from each bi-weekly assessment
- Maintain assessment history (already in WE-GSI-ASSESSMENTS.md)
- Display last 6 assessments (3 months)

**Technical Implementation:**
- Parse WE-GSI-ASSESSMENTS.md for historical values
- Create mini sparkline chart
- Show dates on hover/tooltip
- Update with each new assessment

---

#### 3. Infrastructure Commitment Trend

**Location:** Stats dashboard enhancement

**Visual Design:**
```
INFRASTRUCTURE COMMITTED    $280B+ ↗

Growth: +$45B this month
        +$120B this quarter
        +$280B since launch
```

**Data Requirements:**
- Track cumulative infrastructure by month
- Calculate month-over-month growth
- Show quarterly and lifetime totals

**Technical Implementation:**
- Add `month_added` and `infrastructure_value` fields to signals.json
- Calculate deltas programmatically
- Display growth metrics below cumulative total

---

### Implementation Checklist

**Before implementing Phase 2:**
- [ ] Have at least 20 signals in archive
- [ ] Have at least 12 weeks of continuous data
- [ ] Have completed 6+ bi-weekly WE GSI assessments
- [ ] Current platform is stable and bug-free
- [ ] User feedback validates need for trend visualization

**Development sequence:**
1. Update signals.json schema (add week_added, month_added fields)
2. Backfill existing signals with these fields
3. Build signal velocity chart (simplest first)
4. Add WE GSI sparkline
5. Add infrastructure growth metrics
6. Test on mobile devices
7. Deploy and monitor usage

**Estimated effort:** 20-30 hours of development

---

## PHASE 3: Regional Sub-Indices + Signal Filtering
**Timeline:** Months 6-12 (approximately April - October 2026)  
**Prerequisites:** Minimum 50 signals tracked, geographic diversity in signals

### Objective
Enable users to filter and analyze signals by region and type, with regional WE GSI sub-indices showing coordination dynamics by geography.

### Implementation Components

#### 1. Geographic Tagging System

**Data Structure Addition:**
```json
{
  "id": "signal-001",
  "regions": ["North America"],  // NEW FIELD
  "countries": ["United States"],  // NEW FIELD
  "region_weights": {  // NEW FIELD
    "North America": 1.0,
    "Europe": 0.0,
    "Asia-Pacific": 0.0
  }
  // ... existing fields
}
```

**Regional Categories:**
- **North America:** USA, Canada, Mexico
- **Europe:** UK, EU member states, Switzerland, Norway
- **Asia-Pacific:** China, Japan, South Korea, India, Australia, Singapore, Taiwan
- **Other:** Middle East, Latin America, Africa (as signals emerge)

**Multi-Region Signals:**
- UK-U.S. deal = 50% Europe, 50% North America
- Use region_weights to split attribution

---

#### 2. Signal Type Taxonomy

**Add type classifications:**
```json
{
  "id": "signal-001",
  "primary_type": "Infrastructure Commitment",  // EXISTING
  "sub_types": [  // NEW FIELD
    "Data Centers",
    "Private Investment",
    "Energy Infrastructure"
  ],
  "actors": [  // NEW FIELD
    "Private Sector",
    "Technology Companies"
  ]
}
```

**Type Categories:**
- **Infrastructure Commitment:** Data centers, chips, networks, energy
- **Policy Framework:** Legislation, regulation, standards
- **Coordination Mechanism:** Treaties, agreements, frameworks
- **Corporate Partnership:** M&A, joint ventures, collaborations
- **Research Initiative:** Academic, public-private R&D

**Actor Categories:**
- Government (National, Regional, Local)
- Private Sector (Tech Companies, Investors, Utilities)
- Multilateral (UN, OECD, etc.)
- Academic/Research

---

#### 3. Interactive Filtering Interface

**Location:** Top of signals section

**Visual Design:**
```
┌────────────────────────────────────────────────────┐
│ Filter Signals                                     │
│                                                    │
│ Region:  [All Regions ▼]  [North America]        │
│          [Europe]  [Asia-Pacific]  [Other]        │
│                                                    │
│ Type:    [All Types ▼]  [Infrastructure]         │
│          [Policy]  [Partnership]  [Coordination]  │
│                                                    │
│ Time:    [All Time ▼]  [Last 30 days]           │
│          [Last 90 days]  [Last 6 months]         │
│                                                    │
│ Showing: 12 of 52 signals                         │
│ Infrastructure: $85B of $280B total               │
└────────────────────────────────────────────────────┘
```

**Functionality:**
- Multiple selection allowed (e.g., "Europe + Asia-Pacific")
- Filters combine (AND logic)
- Results update dynamically
- Show filtered counts and totals

**Technical Implementation:**
- JavaScript filtering (client-side, fast)
- Update signals.json with region/type metadata
- Build filter UI with checkboxes/dropdowns
- Recalculate displayed stats based on filters

---

#### 4. Regional WE GSI Sub-Indices

**Location:** New dashboard section or modal

**Visual Design:**
```
┌────────────────────────────────────────────────────┐
│ Regional WE GSI Sub-Indices                        │
│                                                    │
│ 🌎 North America                          62% ↗   │
│    └─ 28 signals tracked                          │
│    └─ $180B infrastructure                        │
│    └─ Status: MEDIUM/AMBER (trending GREEN)       │
│                                                    │
│ 🌍 Europe                                 58% →   │
│    └─ 15 signals tracked                          │
│    └─ $75B infrastructure                         │
│    └─ Status: MEDIUM/AMBER (stable)               │
│                                                    │
│ 🌏 Asia-Pacific                           48% ↘   │
│    └─ 9 signals tracked                           │
│    └─ $25B infrastructure                         │
│    └─ Status: MEDIUM/AMBER (trending RED)         │
└────────────────────────────────────────────────────┘
```

**Calculation Method:**
- Apply same WE GSI methodology to regional signal subsets
- Weight signals by region attribution (use region_weights)
- Minimum 8-10 signals per region for credible sub-index
- Update bi-weekly with main WE GSI

**Benefits:**
- Shows geographic coordination patterns
- Identifies leading/lagging regions
- Supports geopolitical analysis
- Enables comparative research

---

#### 5. Advanced Analytics Page

**Location:** New page/tab (optional)

**Features:**
- Signal distribution by type (pie chart)
- Geographic heat map of signals
- Timeline view (signals on calendar)
- Infrastructure commitment by region (bar chart)
- Correlation analysis (WE GSI vs. infrastructure spend)

**When to build:**
- After Phase 3 core filtering is stable
- If user demand exists (validate first)
- If you have development resources

---

### Implementation Checklist

**Before implementing Phase 3:**
- [ ] Have at least 50 signals in archive
- [ ] Signals span at least 3 regions
- [ ] Have completed Phase 2 (trend visualization)
- [ ] User feedback requests filtering capability
- [ ] Platform traffic/usage justifies complexity

**Development sequence:**
1. Design regional taxonomy (finalize region list)
2. Design type taxonomy (finalize type/actor categories)
3. Backfill existing signals with region/type metadata (manual curation required)
4. Build filtering UI (start simple with dropdowns)
5. Implement client-side filtering logic
6. Calculate regional sub-indices
7. Add regional dashboard section
8. Test extensively (many edge cases)
9. Document regional methodology
10. Deploy and iterate based on feedback

**Estimated effort:** 60-80 hours of development + 10-20 hours metadata curation

---

## PHASE 4: API Enhancements & Webhooks
**Timeline:** Months 12-18 (approximately October 2026 - April 2027)  
**Prerequisites:** Phase 3 complete, institutional user demand validated

### Objective
Enable programmatic access and real-time notifications for institutional users and researchers.

### Implementation Components

#### 1. RESTful API Endpoints

**Base URL:** `https://api.warmthengine.com/v1/` (requires custom domain + backend)

**Endpoints:**
```
GET /signals                    // List all signals (with filtering)
GET /signals/{id}               // Get specific signal
GET /we-gsi                     // Current WE GSI + history
GET /we-gsi/regional            // Regional sub-indices
GET /infrastructure             // Cumulative commitments
GET /metadata                   // Platform metadata
```

**Authentication:**
- API keys for registered users
- Rate limiting (100 requests/hour free tier)
- Premium tier for institutional users

---

#### 2. Webhook Notifications

**Events:**
- New signal added
- WE GSI assessment published
- Major WE GSI movement (>5 points)
- Regional sub-index updates

**Delivery:**
- POST to user-specified endpoint
- Payload includes signal/assessment data
- Retry logic for failed deliveries

**Use Cases:**
- Automated monitoring systems
- Slack/Discord notifications
- Research data pipelines
- Trading signal systems

---

#### 3. Data Export Enhancements

**Current:** JSON, CSV, RSS (static files)

**Enhanced:**
- Excel export with charts
- PDF report generation
- Custom date range exports
- Filtered dataset exports
- Historical snapshots

---

### Implementation Note

**Phase 4 requires backend infrastructure:**
- Current platform is static (GitHub Pages)
- API/webhooks need server-side logic
- Consider: AWS Lambda, Vercel Functions, or dedicated backend
- Cost implications: $50-200/month for hosting
- May require transitioning to paid infrastructure

**Decision point:** Implement only if commercial tier exists (paying institutional users who need API access)

---

## IMPLEMENTATION PRINCIPLES

### When to Build Each Phase

**Phase 2 (Trends):** Build when...
- ✅ You have meaningful historical data (20+ signals, 12+ weeks)
- ✅ Manual trend tracking becomes tedious
- ✅ Users ask "How has this changed over time?"

**Phase 3 (Regional):** Build when...
- ✅ You have geographic diversity (signals from 3+ regions)
- ✅ Users ask "What's happening in [specific region]?"
- ✅ You have time for metadata curation (10-20 hours)

**Phase 4 (API):** Build when...
- ✅ You have institutional users willing to pay
- ✅ Manual data requests become frequent
- ✅ Revenue justifies infrastructure costs

### Validate Before Building

**For each phase:**
1. **Check prerequisites** (data volume, diversity, stability)
2. **Validate user demand** (are people asking for this?)
3. **Assess effort vs. value** (is this the best use of time?)
4. **Build minimum viable version** (simple first, iterate)
5. **Monitor usage** (is anyone using it?)
6. **Iterate or deprecate** (double down or remove)

### Don't Build Too Early

**Common mistakes:**
- Building filtering before you have enough signals (premature optimization)
- Adding API before anyone asks for it (over-engineering)
- Creating dashboards without validating user needs (feature bloat)

**Better approach:**
- Launch simple
- Listen to users
- Add features users actually request
- Keep it maintainable

---

## SUCCESS METRICS

### Phase 2 Success Criteria
- [ ] Trend charts load in <1 second
- [ ] Mobile display remains clean
- [ ] Users reference trends in feedback
- [ ] No complaints about clutter

### Phase 3 Success Criteria
- [ ] Filters work on mobile
- [ ] At least 3 regions have 10+ signals
- [ ] Users actually use filters (track via analytics)
- [ ] Regional sub-indices cited in external reports

### Phase 4 Success Criteria
- [ ] 5+ institutional users paying for API access
- [ ] API uptime >99.5%
- [ ] Webhook delivery success rate >95%
- [ ] Revenue covers infrastructure costs + development time

---

## MAINTENANCE CONSIDERATIONS

### Ongoing Work Required

**Phase 2:** Minimal
- Trends update automatically when signals added
- Occasional chart design tweaks

**Phase 3:** Moderate
- Must tag each new signal with region/type
- Recalculate regional sub-indices bi-weekly
- Maintain taxonomy as new categories emerge
- ~30 min per bi-weekly update

**Phase 4:** Significant
- Monitor API performance
- Handle webhook failures
- User support for API integration
- Backend maintenance and security updates
- ~2-5 hours/month

### When to Outsource/Automate

**Consider automation:**
- Region detection via NLP (scan signal description for countries)
- Type classification via keywords
- Automatic infrastructure value extraction

**Consider outsourcing:**
- Backend API development (hire contractor)
- Mobile app development (if demand exists)
- Advanced analytics dashboard (data viz specialist)

---

## BUDGET ESTIMATES

### Phase 2 (Trends)
- **Development:** 20-30 hours × your time
- **Infrastructure:** $0 (static hosting remains free)
- **Total:** Free (your time only)

### Phase 3 (Regional)
- **Development:** 60-80 hours × your time
- **Metadata curation:** 10-20 hours × your time
- **Infrastructure:** $0 (static hosting remains free)
- **Total:** Free (your time only)

### Phase 4 (API)
- **Development:** 100-150 hours × your time OR $5K-15K contractor
- **Infrastructure:** $50-200/month (backend hosting)
- **Maintenance:** 2-5 hours/month ongoing
- **Total:** $5K-15K + $600-2,400/year

### ROI Calculation for Phase 4

**Break-even analysis:**
- Annual costs: ~$2K-5K (infrastructure + maintenance time)
- Required revenue: $167-417/month
- Institutional API users: $50-200/month each
- **Break-even:** 2-8 paying users

**Decision:** Only build Phase 4 if you have 5-10 institutional users ready to pay.

---

## REFERENCE WHEN READY

**Save this document and reference it when:**
1. You hit the prerequisites for each phase
2. Users request specific features
3. You're planning development sprints
4. You're evaluating feature priorities

**Update this document:**
- After completing each phase (add lessons learned)
- When user needs change (revise priorities)
- When new technologies emerge (update tech stack)

---

**Document Version:** 1.0  
**Last Updated:** October 2025  
**Next Review:** April 2026 (after 6 months of operation)

---

*Remember: Start simple, validate demand, build incrementally. The best feature is the one users actually need and use.*