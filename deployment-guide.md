# Deployment Guide

Complete instructions for deploying Warmth Engine Observatory from GitHub Pages to your custom domain.

---

## Phase 1: GitHub Repository Setup (5 minutes)

### 1.1 Create Repository

1. Go to https://github.com/new
2. Repository name: `warmth-engine-observatory`
3. Description: "AI Infrastructure Coordination Monitoring Platform"
4. Visibility: **Public** (required for GitHub Pages free tier)
5. ✅ Initialize with README (you'll replace it)
6. Click **Create repository**

### 1.2 Clone Repository Locally

```bash
git clone https://github.com/warmthengine/warmth-engine-observatory.git
cd warmth-engine-observatory
```

---

## Phase 2: Upload Files (10 minutes)

### 2.1 Required File Structure

Ensure your local folder contains:

```
warmth-engine-observatory/
├── warmth-engine-observatory.html
├── archive.html
├── config.js
├── _signal_template.html
├── signals.json
├── signals.csv
├── feed.xml
├── CHANGELOG.md
├── WEEKLY_WORKFLOW.md
├── DEPLOYMENT_GUIDE.md
├── README.md
├── favicon-32x32.png
├── favicon-16x16.png
├── bitcoin-qr.png
└── ethereum-qr.png
```

### 2.2 Initial Commit

```bash
git add .
git commit -m "Initial commit: Warmth Engine Observatory v1.0.0"
git push origin main
```

---

## Phase 3: Enable GitHub Pages (2 minutes)

### 3.1 Configure GitHub Pages

1. Go to your repository on GitHub
2. Click **Settings** tab
3. Scroll to **Pages** section (left sidebar)
4. Under **Source**, select:
   - Branch: `main`
   - Folder: `/ (root)`
5. Click **Save**

### 3.2 Wait for Deployment

- GitHub will show: "Your site is live at `https://warmthengine.github.io/warmth-engine-observatory/`"
- First deployment takes 1-2 minutes
- Subsequent updates deploy in ~30 seconds

### 3.3 Test Stealth Launch URL

Visit: `https://warmthengine.github.io/warmth-engine-observatory/warmth-engine-observatory.html`

**Verify:**
- [ ] Page loads correctly
- [ ] Gauge displays properly
- [ ] All links work
- [ ] Stats dashboard shows correct numbers
- [ ] JSON/CSV/RSS links work

---

## Phase 4: Custom Domain Setup (15 minutes)

### 4.1 DNS Configuration

**At your domain registrar** (Namecheap, GoDaddy, Cloudflare, etc.):

#### Option A: Apex Domain (warmthengine.com)

Add these **A records**:

```
Type: A
Host: @
Value: 185.199.108.153
TTL: 3600
```

```
Type: A
Host: @
Value: 185.199.109.153
TTL: 3600
```

```
Type: A
Host: @
Value: 185.199.110.153
TTL: 3600
```

```
Type: A
Host: @
Value: 185.199.111.153
TTL: 3600
```

Add this **CNAME record** for www:

```
Type: CNAME
Host: www
Value: warmthengine.github.io
TTL: 3600
```

#### Option B: Subdomain (observatory.warmthengine.com)

Add this **CNAME record**:

```
Type: CNAME
Host: observatory
Value: warmthengine.github.io
TTL: 3600
```

**DNS Propagation:** Changes take 5 minutes to 48 hours (usually ~1 hour)

### 4.2 Configure Custom Domain in GitHub

1. Back in **Settings → Pages**
2. Under **Custom domain**, enter: `warmthengine.com`
3. Click **Save**
4. Wait for DNS check (green checkmark appears when successful)

### 4.3 Enable HTTPS

1. After DNS verification, check: **✅ Enforce HTTPS**
2. Certificate provisioning takes ~15 minutes
3. GitHub uses Let's Encrypt (automatic, free, renews automatically)

---

## Phase 5: Update URLs in Files (5 minutes)

Once custom domain is live, update hardcoded URLs:

### 5.1 Files to Update

**feed.xml**
```xml
<link>https://warmthengine.com/</link>
<atom:link href="https://warmthengine.com/feed.xml" rel="self" type="application/rss+xml"/>
<!-- Update all item links too -->
```

**signals.json**
```json
"api_info": {
  "url": "https://warmthengine.com/signals.json"
}
```

**warmth-engine-observatory.html** (if hardcoded URLs exist)
- Search for `warmthengine.github.io`
- Replace with `warmthengine.com`

### 5.2 Commit Changes

```bash
git add .
git commit -m "Update URLs to custom domain"
git push origin main
```

---

## Phase 6: Pre-Launch Testing (10 minutes)

### 6.1 Functional Testing

Visit `https://warmthengine.com/warmth-engine-observatory.html`

**Core Features:**
- [ ] Page loads over HTTPS (padlock icon in browser)
- [ ] Gauge renders correctly
- [ ] Gauge position matches config.js
- [ ] Trend arrow shows correct direction
- [ ] Stats dashboard displays accurate numbers
- [ ] "Last updated X hours ago" calculates correctly
- [ ] All section expand/collapse toggles work
- [ ] Section state persists after page reload (localStorage)

**Navigation:**
- [ ] Archive link works
- [ ] Back to main page link works from archive
- [ ] Smooth scrolling to methodology section
- [ ] All anchor links work (#methodology, #faq, etc.)

**Data Access:**
- [ ] JSON feed loads: `/signals.json`
- [ ] CSV downloads: `/signals.csv`
- [ ] RSS validates: `/feed.xml` (test at validator.w3.org/feed)

**Signal Details:**
- [ ] All 4 signals display correctly
- [ ] Source links open in new tabs
- [ ] Source links go to correct URLs
- [ ] Impact/confidence badges display properly

**Responsive Design:**
- [ ] Test on mobile (or use browser dev tools)
- [ ] Test on tablet
- [ ] Gauge resizes appropriately
- [ ] Text remains readable at all sizes

### 6.2 Print Testing

1. Press Ctrl+P (or Cmd+P)
2. Check print preview:
   - [ ] Clean, professional layout
   - [ ] No navigation elements
   - [ ] Gauge renders correctly
   - [ ] Source URLs are visible
   - [ ] Page breaks appropriately

### 6.3 Browser Testing

Test in multiple browsers:
- [ ] Chrome/Edge (Chromium)
- [ ] Firefox
- [ ] Safari (if available)

### 6.4 SEO/Metadata Testing

1. Share URL on Twitter - verify card preview
2. Share URL on LinkedIn - verify card preview
3. Check with https://www.opengraph.xyz/
   - [ ] Title displays correctly
   - [ ] Description is accurate
   - [ ] Image loads (if og:image added)

### 6.5 Performance Testing

1. Check page load speed: https://pagespeed.web.dev/
   - Target: 90+ score
2. Check mobile performance
3. Verify no console errors (F12 → Console tab)

---

## Phase 7: Soft Launch Strategy (As Needed)

### 7.1 Private Testing (Week 1)

Share with 5-10 trusted contacts for feedback:

**Feedback checklist to send:**
- Is the purpose immediately clear?
- Is the WE GSI concept understandable?
- Are the signals compelling and well-sourced?
- Any broken links or display issues?
- Does it feel authoritative/credible?
- Would you bookmark this and return weekly?

### 7.2 Targeted Launch (Week 2-3)

Share with 20-50 people in relevant communities:
- AI safety researchers
- Infrastructure policy experts
- Energy/grid analysts
- Tech journalists

**Launch message template:**
```
Launching the Warmth Engine Observatory - tracking AI infrastructure 
coordination signals through a new analytical framework (C-MAD).

Week 1 data: 4 signals, $13B+ in commitments across three continents.

Live: https://warmthengine.com
JSON: https://warmthengine.com/signals.json
RSS: https://warmthengine.com/feed.xml

Feedback welcome. Weekly updates.
```

### 7.3 Official Launch (Week 4+)

Point `warmthengine.com` root to the Observatory:

**Option A: Redirect root to observatory**
Create `index.html` in repository root:
```html
<!DOCTYPE html>
<html>
<head>
  <meta http-equiv="refresh" content="0; url=warmth-engine-observatory.html">
  <title>Redirecting...</title>
</head>
<body>
  <p>Redirecting to <a href="warmth-engine-observatory.html">Warmth Engine Observatory</a>...</p>
</body>
</html>
```

**Option B: Make observatory the root**
Rename `warmth-engine-observatory.html` to `index.html`

---

## Phase 8: Ongoing Maintenance

### 8.1 Weekly Tasks (20-30 minutes)

Follow `WEEKLY_WORKFLOW.md` for adding signals.

### 8.2 Monthly Tasks (30 minutes)

- Reset cumulative stats (signal count, total commitment)
- Review and update gauge position based on monthly trends
- Archive previous month's signals
- Update CHANGELOG with monthly summary
- Review and replace any placeholder URLs with real sources

### 8.3 Quarterly Tasks (1-2 hours)

- Review methodology for potential updates
- Analyze WE GSI trends and write brief report
- Gather user feedback and implement improvements
- Check all external links still work
- Update dependencies if any (minimal for static site)

### 8.4 Annual Tasks (Half day)

- Major methodology review (C-MAD framework evolution)
- Consider adding new data visualizations
- Write annual report on coordination trends
- Review and update FAQ based on common questions
- Consider adding historical data analysis features

---

## Troubleshooting

### Issue: Custom domain not working

**Diagnosis:**
```bash
# Check DNS propagation
nslookup warmthengine.com

# Should return GitHub's IPs
185.199.108.153
185.199.109.153
185.199.110.153
185.199.111.153
```

**Solutions:**
- Wait longer (DNS can take up to 48 hours)
- Check DNS records at registrar are exact
- Try different DNS server: `nslookup warmthengine.com 8.8.8.8`
- Clear browser DNS cache: `chrome://net-internals/#dns`

### Issue: HTTPS certificate not provisioning

**Solutions:**
- Verify DNS is fully propagated first
- Uncheck "Enforce HTTPS", save, wait 5 minutes, re-check
- Remove custom domain, wait 5 minutes, re-add
- Check GitHub Status page for issues

### Issue: Changes not appearing

**Solutions:**
- Wait 30-60 seconds for deployment
- Clear browser cache (Ctrl+Shift+R)
- Check "Actions" tab for deployment status
- Verify files pushed successfully: `git status`

### Issue: 404 errors on subpages

**Solutions:**
- Verify file names match exactly (case-sensitive)
- Check files are in root directory, not subfolder
- Ensure all files pushed: `git ls-files`
- Check for typos in links

### Issue: RSS feed won't validate

**Solutions:**
- Test at validator.w3.org/feed
- Check RFC-822 date format in `<pubDate>`
- Verify XML is well-formed (closing tags match)
- Check for unescaped special characters (&, <, >)
- Use CDATA for HTML content in descriptions

### Issue: Stats not updating automatically

**Solutions:**
- Check JavaScript console for errors (F12)
- Verify `config.js` is valid JavaScript
- Check `lastUpdateDate` is valid ISO 8601 format
- Verify browser allows localStorage
- Clear localStorage: `localStorage.clear()` in console

### Issue: Gauge not displaying

**Solutions:**
- Check browser supports CSS custom properties
- Verify `gaugePosition` is 0-100 in config.js
- Check for CSS conflicts with browser extensions
- Test in incognito mode to rule out extensions
- Check browser console for errors

---

## Security Best Practices

### File Permissions
- Keep repository public (required for free GitHub Pages)
- Don't commit sensitive data (API keys, passwords)
- Review commits before pushing

### HTTPS
- Always use HTTPS (enforced via GitHub Pages)
- Update all external links to use HTTPS
- Check for mixed content warnings

### Dependencies
- No external JavaScript libraries = minimal attack surface
- Keep dependencies (if added later) updated
- Use Subresource Integrity (SRI) for any CDN resources

---

## Backup Strategy

### Automatic Backups
Git itself is your backup - every commit is saved forever.

### Manual Backup (Quarterly)
```bash
# Download entire repository
git clone https://github.com/warmthengine/warmth-engine-observatory.git backup-2025-Q4

# Or export as ZIP from GitHub
# Repo page → Code → Download ZIP
```

### Export Data
```bash
# Save signals as JSON
curl https://warmthengine.com/signals.json > backup-signals-2025-10.json

# Save as CSV
curl https://warmthengine.com/signals.csv > backup-signals-2025-10.csv
```

---

## Migration Path (If Needed)

### Moving to Different Host

If you later want to move off GitHub Pages:

1. **Any static host works** (Netlify, Vercel, Cloudflare Pages)
2. **Export repository** as ZIP
3. **Upload to new host**
4. **Update DNS** to point to new host
5. **Update URLs** in feed.xml and signals.json

No database or server-side code means migration is simple.

---

## Success Metrics

Track these metrics to measure Observatory success:

### Week 1
- [ ] Site loads without errors
- [ ] RSS feed has 5+ subscribers
- [ ] 10+ page views per day

### Month 1
- [ ] 20+ RSS subscribers
- [ ] 100+ unique visitors
- [ ] 3+ citations/references in articles or papers
- [ ] Maintaining weekly update schedule

### Quarter 1
- [ ] 50+ RSS subscribers
- [ ] 500+ unique visitors
- [ ] 10+ citations in research or policy documents
- [ ] Recognized as authoritative source

### Year 1
- [ ] 200+ RSS subscribers
- [ ] 5,000+ unique visitors
- [ ] Cited in major publications or policy reports
- [ ] THE definitive platform for AI infrastructure coordination monitoring

---

## Support & Resources

### Documentation
- This guide: `DEPLOYMENT_GUIDE.md`
- Weekly updates: `WEEKLY_WORKFLOW.md`
- Version history: `CHANGELOG.md`
- Repository info: `README.md`

### GitHub Pages Docs
- https://docs.github.com/en/pages

### Validation Tools
- RSS: https://validator.w3.org/feed/
- JSON: https://jsonlint.com/
- HTML: https://validator.w3.org/
- SEO: https://www.opengraph.xyz/

### DNS Tools
- https://dnschecker.org/
- https://mxtoolbox.com/

---

## Final Pre-Launch Checklist

Before official launch:

**Content:**
- [ ] All placeholder URLs replaced with real sources
- [ ] All signal descriptions are accurate and well-written
- [ ] Methodology section is clear and comprehensive
- [ ] FAQ answers common questions
- [ ] Contact information is correct

**Technical:**
- [ ] Custom domain working over HTTPS
- [ ] All links tested and working
- [ ] JSON/CSV/RSS feeds validate
- [ ] Mobile responsive
- [ ] Print stylesheet works
- [ ] No console errors
- [ ] Page load speed is good (90+ PageSpeed score)

**Legal/Ethics:**
- [ ] All sources properly attributed
- [ ] No copyright violations
- [ ] Methodology is transparent
- [ ] Analytical limitations acknowledged

**Launch Prep:**
- [ ] Launch announcement drafted
- [ ] Target audience list ready
- [ ] RSS feed URL ready to share
- [ ] Response plan for feedback/questions
- [ ] First 2-3 weeks of signals already identified

---

## You're Ready to Launch! 🚀

Your Warmth Engine Observatory is now live and maintainable. Remember:

1. **Weekly updates** keep the platform authoritative
2. **Primary sources** maintain credibility
3. **Analytical humility** preserves trust
4. **Consistent quality** builds reputation

Good luck with your DEFINITIVE tier intelligence platform!