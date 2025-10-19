// ==============================================
// WARMTH ENGINE OBSERVATORY - CONFIGURATION
// ==============================================
// Update these values weekly to refresh the site
// All changes propagate automatically across pages

const CONFIG = {
    // === WE GLOBAL STABILITY INDEX ===
    // Current gauge position (0-100)
    gaugePosition: 58,
    
    // Previous position for trend arrow
    // Shows: "↑ from 45%" or "↓ from 55%" or "→ from 50%"
    previousGaugePosition: 50,
    
    // Last update timestamp (ISO 8601 format: YYYY-MM-DDTHH:MM:SSZ)
    // Used for "Updated X hours ago" calculation
    lastUpdateDate: '2025-10-15T00:00:00Z',
    
    // === STATS DASHBOARD ===
    // Number of signals tracked this month
    signalCount: 4,
    
    // Total infrastructure commitments this month
    // Format: "$XB+" or "$XM+" (displays exactly as written)
    totalCommitment: '$40B+',
    
    // === MONTHLY RESET REMINDER ===
    // At start of new month, reset:
    // - signalCount to 0
    // - totalCommitment to "$0B+"
    // Then increment as new signals arrive
    
    // === METADATA (Optional - change rarely) ===
    // Site title for search engines
    siteTitle: 'Warmth Engine Observatory - C-MAD Monitoring Framework',
    
    // Site description for social media previews
    siteDescription: 'Independent monitoring of AI infrastructure coordination patterns. Track strategic commitments, policy frameworks, and technological sovereignty dynamics.',
    
    // Current framework version
    frameworkVersion: '1.0',
    
    // Framework last updated date (display format)
    frameworkLastUpdated: 'October 2025'
};

// ==============================================
// USAGE NOTES
// ==============================================
/*
WEEKLY UPDATE WORKFLOW:

1. ADD NEW SIGNAL to HTML
   - Copy template from _signal_template.html
   - Fill in details
   - Paste at TOP of "Recent Coordination Signals" section

2. UPDATE THIS CONFIG FILE:
   
   a) If WE GSI changed:
      - Set previousGaugePosition = old gaugePosition
      - Set gaugePosition = new value
   
   b) Update timestamp:
      - Set lastUpdateDate to current time in UTC
      - Format: 'YYYY-MM-DDTHH:MM:SSZ'
      - Example: '2025-10-23T14:30:00Z'
   
   c) Update stats:
      - Increment signalCount by 1
      - Add signal's $ amount to totalCommitment
   
3. UPDATE DATA FILES:
   - Add signal to signals.json
   - Add row to signals.csv
   - Add entry to feed.xml
   
4. UPDATE CHANGELOG:
   - Note what changed in CHANGELOG.md

MONTHLY RESET:
At start of new month:
- signalCount: Reset to 0
- totalCommitment: Reset to "$0B+"
- Continue adding as new signals arrive

EXAMPLES:

Example 1: New signal, WE GSI unchanged
---------------------------------------
gaugePosition: 50          // Same
previousGaugePosition: 50  // Same
lastUpdateDate: '2025-10-23T14:30:00Z'  // Updated
signalCount: 5             // Was 4, now 5
totalCommitment: '$14.5B+' // Was $13B+, added $1.5B

Example 2: New signal, WE GSI increased
---------------------------------------
gaugePosition: 55          // Increased from 50
previousGaugePosition: 50  // Old value
lastUpdateDate: '2025-10-23T14:30:00Z'
signalCount: 5
totalCommitment: '$14.5B+'

Example 3: Start of new month
---------------------------------------
gaugePosition: 55          // Unchanged from last month
previousGaugePosition: 50  // Unchanged
lastUpdateDate: '2025-11-01T09:00:00Z'  // New month
signalCount: 0             // RESET
totalCommitment: '$0B+'    // RESET

RECENCY INDICATOR:
Automatically shows:
- < 1 hour: "Just now" (green)
- 1-23 hours: "X hours ago" (green)
- 1-2 days: "X days ago" (green)
- 3-6 days: "X days ago" (normal)
- 1+ weeks: "X weeks ago" (normal)
- 1+ months: "X months ago" (normal)

DEPLOYMENT:
- GitHub Pages: Commit this file with your updates
- Changes take effect immediately after push
- No need to edit multiple files - this updates everything!
*/