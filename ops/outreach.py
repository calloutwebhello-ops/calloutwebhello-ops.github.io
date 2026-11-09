#!/usr/bin/env python3
"""Preview-first outreach drafts (OFF until the owner approves it in writing).

Builds a personalised preview link and a short, compliant email draft for each
prospect in a CSV. It never sends anything: the operator turns the output into
Gmail DRAFTS, and only when OUTREACH_APPROVED is true in assets/config.js.

UK rules this script enforces (PECR / UK GDPR, B2B):
  - Only corporate subscribers: limited companies / LLPs (company_type = ltd or llp).
    Sole traders and partnerships are treated like individuals: no unsolicited email.
  - Only a generic business address published by the company (e.g. info@, enquiries@).
  - Every email identifies us and has a one-line opt-out; opt-outs go on the suppression list forever.
  - Small volume (max 10 per run) and one email per company, no chasers unless they reply.

Usage: python3 ops/outreach.py prospects.csv out.json [--suppress suppress.txt]
CSV columns: business,trade,town,phone,email,company_type,source_url
"""
import csv, json, sys, re, urllib.parse, pathlib

SITE = "https://calloutwebhello-ops.github.io"
MAX_PER_RUN = 10
GENERIC = re.compile(r"^(info|enquiries|enquiry|hello|contact|office|admin|sales|bookings|mail)@", re.I)

def main():
    src, out = sys.argv[1], sys.argv[2]
    supp = set()
    if "--suppress" in sys.argv:
        p = pathlib.Path(sys.argv[sys.argv.index("--suppress") + 1])
        if p.exists():
            supp = {l.strip().lower() for l in p.read_text().splitlines() if l.strip()}
    drafts, skipped = [], []
    for r in csv.DictReader(open(src, newline="")):
        email = (r.get("email") or "").strip().lower()
        why = None
        if (r.get("company_type") or "").strip().lower() not in ("ltd", "llp"):
            why = "not a limited company/LLP (sole traders need consent first)"
        elif not GENERIC.match(email):
            why = "not a generic business address"
        elif email in supp or email.split("@")[-1] in supp:
            why = "on suppression list"
        if why:
            skipped.append({"business": r.get("business"), "reason": why}); continue
        if len(drafts) >= MAX_PER_RUN:
            skipped.append({"business": r.get("business"), "reason": "daily cap reached"}); continue
        q = urllib.parse.urlencode({k: v for k, v in {"name": r["business"], "trade": r.get("trade", ""), "town": r.get("town", ""), "phone": r.get("phone", ""), "ref": "outreach"}.items() if v})
        link = f"{SITE}/preview/?{q}"
        body = (f"Hi {r['business']} team,\n\n"
                f"I couldn't find a website for {r['business']}, so I made you a free preview of one. It takes a few seconds to load and you can change anything on it:\n{link}\n\n"
                f"If you like it, it can go live from £19 a month with no setup fee and no contract. If not, no problem at all.\n\n"
                f"Callout Web (run by Joshua Spiers, UK sole trader) · {SITE}\n"
                f"I found your details at {r.get('source_url') or 'a public business listing'}. Reply STOP and I won't email you again.")
        drafts.append({"to": email, "subject": f"A free website preview for {r['business']}", "body": body, "source_url": r.get("source_url", "")})
    json.dump({"drafts": drafts, "skipped": skipped}, open(out, "w"), indent=2)
    print(json.dumps({"drafts": len(drafts), "skipped": len(skipped)}))

if __name__ == "__main__":
    main()
