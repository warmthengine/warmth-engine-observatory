# WEO Maintenance Checklist

## Bi-Weekly Assessment (Every 2 Weeks)

### 1. Gather New Signals
- [ ] Review AI infrastructure news (Google News, TechCrunch, Bloomberg)
- [ ] Check government announcements (UK, US, EU, China)
- [ ] Review corporate earnings calls and press releases
- [ ] Verify primary sources for each signal

### 2. Score New Signals
- [ ] Apply five-dimensional scoring framework
- [ ] Assign signal weight (1-4)
- [ ] Calculate signal score and weighted score
- [ ] Add to signals.json and signals.csv

### 3. Calculate WE GSI

**CURRENT PHASE (Until January 2026):**
- [ ] Use ALL signals in archive for calculation
- [ ] Calculate as documented in WE-GSI-CALCULATION-001.md

**FUTURE PHASE (January 2026+):**
- [ ] Calculate 90 days back from today's date
- [ ] Filter signals.json to only signals within last 90 days
- [ ] Calculate WE GSI from filtered signals ONLY
- [ ] Archive count remains cumulative (all signals)

### 4. Update Files
- [ ] Update signals.json with new signals
- [ ] Update signals.csv with new signals
- [ ] Update config.js (gaugePosition = new WE GSI %)
- [ ] Create new WE-GSI-CALCULATION-00X.md for this assessment
- [ ] Update WE-GSI-ASSESSMENTS.md with new assessment

### 5. Update Website
- [ ] Add new signal HTML blocks to index.html
- [ ] Update stats dashboard if needed
- [ ] Commit all changes to GitHub
- [ ] Verify live site after 2-3 minutes

### 6. Quality Check
- [ ] Gauge shows correct WE GSI %
- [ ] Signal count is cumulative (grows)
- [ ] Infrastructure committed is cumulative (grows)
- [ ] All source links work
- [ ] Mobile display looks correct

---

## Monthly Tasks

### Archive Maintenance
- [ ] Verify all signal source URLs still work
- [ ] Update any broken links
- [ ] Check for retrospective coverage of events

### Methodology Review
- [ ] Review any user feedback
- [ ] Consider methodology refinements
- [ ] Update documentation if needed

---

## Quarterly Tasks

### Deep Analysis
- [ ] Publish quarterly deep-dive analysis
- [ ] Review regional patterns (when Phase 3 active)
- [ ] Assess methodology effectiveness
- [ ] Plan any platform enhancements

---

## Key Transition: January 2026

**IMPORTANT:** In January 2026, switch to 90-day rolling window

**Before January 2026:**
- Use ALL signals for WE GSI calculation

**After January 2026:**
- Use ONLY signals from last 90 days for WE GSI calculation
- Archive count remains cumulative
- Just filter by date when calculating

**How to filter:**
1. Look at today's date
2. Calculate date 90 days ago
3. Only use signals between those dates
4. That's it - no complex tracking needed