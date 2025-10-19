# Weekly Workflow Guide

Complete step-by-step instructions for adding new signals to Warmth Engine Observatory.

**Estimated time per signal: 12-15 minutes**

---

## Prerequisites

- [ ] Text editor (VS Code, Sublime, Notepad++ recommended)
- [ ] New signal details ready (date, title, description, source URL)
- [ ] Impact and confidence assessments completed
- [ ] WE GSI position decision made (0-100)

---

## Step 1: Update config.js (1 minute)

**File:** `config.js`

```javascript
// Update these values:
const CONFIG = {
  gaugePosition: 55,              // ← NEW gauge position (0-100)
  previousGaugePosition: 50,      // ← Set to OLD position
  signalCount: 5,                 // ← Increment by 1
  totalCommitment: '$15B+',       // ← Add new commitment to total
  lastUpdateDate: '2025-10-23T14:00:00Z'  // ← Current date/time in ISO format
};
```

**Tips:**
- Use ISO 8601 format for dates: `YYYY-MM-DDTHH:MM:SSZ`
- Total commitment can be approximate (e.g., "$15B+")
- Gauge position is your analytical judgment (0=low coordination, 100=high coordination)

---

## Step 2: Add Signal to HTML (5-7 minutes)

**File:** `warmth-engine-observatory.html`

### 2.1 Copy Template

Open `_signal_template.html` and copy the entire signal block.

### 2.2 Paste in Correct Location

Find the `<!-- SIGNALS START -->` section and paste your new signal **at the top** (most recent first).

### 2.3 Update Signal Details

```html
<div class="signal" id="signal-005">  <!-- ← Increment ID -->
  <div class="signal-header">
    <span class="signal-date">2025-10-23</span>  <!-- ← New date -->
    <div class="signal-meta">
      <span class="impact-badge impact-high">High Impact</span>
      <span class="confidence-badge confidence-high">High Confidence</span>
    </div>
  </div>
  
  <h3>Your Signal Title Here</h3>  <!-- ← New title -->
  
  <p class="signal-description">
    Your signal description here. Include key facts, figures, and context.
  </p>
  
  <p class="signal-context">
    <strong>Context:</strong> Why this signal matters for AI infrastructure coordination...
  </p>
  
  <p class="signal-source">
    <strong>Source:</strong> 
    <a href="https://actual-source-url.com" target="_blank">
      Primary Source Title or Organization Name →
    </a>
  </p>
</div>
```

### 2.4 Adjust Impact/Confidence Badges

Available options:
- Impact: `impact-high`, `impact-medium`, `impact-low`
- Confidence: `confidence-high`, `confidence-medium`, `confidence-low`

---

## Step 3: Update signals.json (2 minutes)

**File:** `signals.json`

### 3.1 Update Metadata

```json
{
  "metadata": {
    "last_updated": "2025-10-23T14:00:00Z",  // ← Update
    "we_gsi": {
      "current": 55,      // ← New position
      "previous": 50,     // ← Old position
      "status": "MEDIUM/AMBER"  // ← Update if zone changed
    },
    "signal_count": 5,    // ← Increment
    "total_commitment": "$15B+"  // ← Update total
  },
```

### 3.2 Add New Signal Object

Add to the **beginning** of the `"signals"` array:

```json
{
  "id": "signal-005",
  "date": "2025-10-23",
  "title": "Your Signal Title",
  "description": "Full description text...",
  "impact": "High",
  "confidence": "High",
  "source_url": "https://actual-source-url.com",
  "context": "Context explanation..."
},
```

**Important:** Don't forget the comma after the closing brace!

---

## Step 4: Update signals.csv (1 minute)

**File:** `signals.csv`

Add a new row **after the header row** (most recent first):

```csv
signal-005,2025-10-23,"Your Signal Title",High,High,https://actual-source-url.com,"Context text here."
```

**CSV Tips:**
- Wrap text containing commas in double quotes
- Escape internal quotes by doubling them: `"He said ""hello"""`
- No line breaks within cells

---

## Step 5: Update feed.xml (2 minutes)

**File:** `feed.xml`

### 5.1 Update Channel Metadata

```xml
<lastBuildDate>Thu, 23 Oct 2025 14:00:00 +0000</lastBuildDate>
```

**Date format:** `Day, DD Mon YYYY HH:MM:SS +0000` (RFC-822)

### 5.2 Add New Item

Insert **after** `<webMaster>` tag and **before** the first existing `<item>`:

```xml
<item>
  <title>Your Signal Title</title>
  <link>https://warmthengine.github.io/warmth-engine-observatory/#signal-005</link>
  <guid isPermaLink="true">https://warmthengine.github.io/warmth-engine-observatory/#signal-005</guid>
  <pubDate>Thu, 23 Oct 2025 00:00:00 +0000</pubDate>
  <description><![CDATA[
    <p><strong>Impact:</strong> High | <strong>Confidence:</strong> High</p>
    <p>Your full signal description here...</p>
    <p><strong>Context:</strong> Context explanation...</p>
    <p><a href="https://actual-source-url.com">View Source</a></p>
  ]]></description>
  <category>AI Infrastructure</category>
  <category>Your Category</category>
</item>
```

---

## Step 6: Update CHANGELOG.md (1 minute)

**File:** `CHANGELOG.md`

Add a new version entry at the top:

```markdown
## [1.1.0] - 2025-10-23

### Added
- New signal: Your Signal Title (2025-10-23)

### Changed
- WE GSI position updated: 50% → 55%
- Signal count: 4 → 5
- Total commitment: $13B+ → $15B+
```

---

## Step 7: Testing Checklist (2 minutes)

Before committing changes:

- [ ] HTML file loads without errors in browser
- [ ] New signal appears at top of list
- [ ] Stats dashboard shows updated numbers
- [ ] Gauge position updated correctly
- [ ] Trend arrow shows correct direction (↑ ↓ →)
- [ ] Source link works and opens in new tab
- [ ] JSON file validates (use jsonlint.com)
- [ ] CSV file opens correctly in Excel/Google Sheets
- [ ] RSS feed validates (use validator.w3.org/feed)
- [ ] "Last updated X hours ago" calculates correctly

---

## Step 8: Git Commit & Push (1 minute)

```bash
git add .
git commit -m "Add signal: [Brief title] - [Date]"
git push origin main
```

GitHub Pages will automatically deploy within 1-2 minutes.

---

## Monthly Maintenance

**At the start of each month:**

1. Reset stats in `config.js`:
   ```javascript
   signalCount: 0,
   totalCommitment: '$0',
   ```

2. Archive previous month's signals:
   - Copy signals to `archive.html`
   - Consider creating monthly archive pages

3. Update CHANGELOG with monthly summary

---

## Troubleshooting

### Issue: Gauge doesn't update
- Check `config.js` is saved
- Clear browser cache (Ctrl+Shift+R)
- Verify `gaugePosition` is 0-100

### Issue: JSON validation fails
- Check for missing commas between objects
- Verify all strings use double quotes
- Use jsonlint.com to find syntax errors

### Issue: RSS feed errors
- Verify RFC-822 date format in `<pubDate>`
- Check CDATA sections are properly closed
- Use validator.w3.org/feed to check

### Issue: Stats not calculating
- Check `lastUpdateDate` is valid ISO 8601
- Verify all number fields contain numbers (not strings)
- Check browser console for JavaScript errors

---

## Time-Saving Tips

1. **Keep template open** - Have `_signal_template.html` ready to copy
2. **Use find/replace** - Replace signal ID across all files at once
3. **Validate as you go** - Don't wait until end to test
4. **Batch similar edits** - Update all dates at once, all URLs at once
5. **Create keyboard shortcuts** - For commit commands, validators

---

## Questions?

If you encounter issues not covered here:
1. Check browser console for errors (F12)
2. Verify file syntax with online validators
3. Compare your changes with existing signals
4. Test locally before pushing to GitHub

**Remember:** The recency indicator motivates regular updates. Aim for 1-2 signals per week to keep the Observatory fresh and authoritative.