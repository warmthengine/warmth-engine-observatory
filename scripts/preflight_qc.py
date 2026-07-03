#!/usr/bin/env python3
"""
Pre-deploy QC assertions for the WEO event corpus.

Runs three schema-shape / threshold guards that the automated deploy gates
(leak / topology / fingerprint) do NOT cover. Each corresponds to a real
Loop 31 defect that reached production:

  1. Integer event IDs        -> broke events.html openModal (=== strict eq)
  2. Below-threshold infra     -> MSU-270 (~$27-31M) entered below the §3.7
                                  physical-infrastructure $100M minimum
  3. ENT tag missing "name"    -> rendered "undefined" in the badge UI

Usage (standalone):
    python3 preflight_qc.py path/to/events-canonical.json
    # exit 0 = clean (warnings allowed); exit 1 = one or more HARD failures

Programmatic:
    from preflight_qc import run_qc
    hard, warn = run_qc(events)      # events = list of event dicts
    # hard = list[str] blocking failures; warn = list[str] advisories

Design notes on Check 2 (threshold): investment is free text in mixed
currencies. We HARD-FAIL only the unambiguous case — an explicit USD figure
whose maximum is below $100M (this is exactly how MSU-270 was expressed).
When no USD figure is parseable (e.g. EUR/RMB/KRW-denominated), we WARN for
manual §3.7 confirmation rather than block a legitimate deploy. This keeps
false positives at zero on the current corpus while still catching the
named failure mode.
"""
import json
import re
import sys

THRESHOLD_USD_MILLIONS = 100.0

# Magnitude multipliers, expressed in millions of USD.
_UNIT = {
    'trillion': 1_000_000.0, 'tn': 1_000_000.0, 't': 1_000_000.0,
    'billion': 1_000.0, 'bn': 1_000.0, 'b': 1_000.0,
    'million': 1.0, 'mn': 1.0, 'm': 1.0,
}

# Match $ / US$ / USD amounts, optional low-high range, with a magnitude word.
#   "$27-31M"  "US$6.1B"  "USD 2.13 billion"  "$100 billion"
_USD_RE = re.compile(
    r'(?:US\$|USD|\$)\s?'
    r'([0-9][0-9.,]*)'                       # low / sole figure
    r'(?:\s?[-–]\s?([0-9][0-9.,]*))?'   # optional range high
    r'\s?(trillion|billion|million|bn|tn|mn|[bmt])\b',
    re.I,
)


def _max_usd_millions(text):
    """Largest USD figure in `text`, in millions; None if none found."""
    best = None
    for lo, hi, unit in _USD_RE.findall(text or ''):
        mult = _UNIT[unit.lower()]
        for raw in (lo, hi):
            if not raw:
                continue
            val = float(raw.replace(',', '')) * mult
            best = val if best is None else max(best, val)
    return best


def run_qc(events):
    """Return (hard_failures, warnings) as lists of human-readable strings."""
    hard, warn = [], []

    for e in events:
        eid = e.get('id')

        # --- Check 1: event ID must be a string ------------------------------
        if not isinstance(eid, str):
            hard.append(
                "Check 1 (ID type): event id %r is %s, must be a string "
                "(integer IDs break events.html openModal ===)."
                % (eid, type(eid).__name__)
            )

        # --- Check 2: Infrastructure §3.7 $100M threshold -------------------
        if e.get('type') == 'Infrastructure':
            inv = e.get('investment', '') or ''
            mu = _max_usd_millions(inv)
            if mu is None:
                warn.append(
                    "Check 2 (§3.7 threshold): E%s Infrastructure has no "
                    "auto-parseable USD figure — confirm >= $100M manually. "
                    "investment=%r" % (eid, inv[:80])
                )
            elif mu < THRESHOLD_USD_MILLIONS:
                hard.append(
                    "Check 2 (§3.7 threshold): E%s Infrastructure max USD "
                    "~$%.0fM is below the $100M physical-infrastructure "
                    "minimum. investment=%r" % (eid, mu, inv[:80])
                )

        # --- Check 3: every ENT tag carries a name -------------------------
        for tag in (e.get('environmentalNexusTags') or []):
            name = tag.get('name')
            if not (isinstance(name, str) and name.strip()):
                hard.append(
                    "Check 3 (ENT name): E%s ENT tag %s missing 'name' "
                    "(renders 'undefined')." % (eid, tag.get('type', '?'))
                )

    return hard, warn


def main(argv):
    path = argv[1] if len(argv) > 1 else 'weo-api/events-canonical.json'
    with open(path) as f:
        data = json.load(f)
    events = data['events'] if isinstance(data, dict) else data

    hard, warn = run_qc(events)

    print("[PREFLIGHT QC] %d events checked" % len(events))
    if warn:
        print("  WARN (%d, non-blocking):" % len(warn))
        for w in warn:
            print("    - " + w)
    if hard:
        print("  HARD FAIL (%d):" % len(hard))
        for h in hard:
            print("    ✗ " + h)
        print("  PREFLIGHT QC FAILED — resolve before KV upload.")
        return 1
    print("  ✓ All hard checks passed%s." %
          (" (%d warning(s) — see above)" % len(warn) if warn else ""))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
