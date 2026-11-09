#!/usr/bin/env python3
"""Save new orders from a normalised inbox export and add ledger rows.

Usage: python3 ingest_orders.py <inbox.json> <repo_dir>
inbox.json = [{"id","from","subject","date","body"}...]  (see SKILL.md, step 1)
Idempotent: an order already in ops/orders/ or the ledger is skipped.
Prints a JSON summary: new orders, skipped, and emails that look like orders but failed to parse."""
import json, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from ops_lib import read_ledger, write_ledger, load_json, extract_order_json

inbox, repo = load_json(sys.argv[1]), pathlib.Path(sys.argv[2])
orders_dir = repo / "ops" / "orders"
orders_dir.mkdir(parents=True, exist_ok=True)
rows = read_ledger(repo)
known = {r["order_id"] for r in rows}
new, skipped, unparsed = [], [], []

for m in inbox:
    if "CW ORDER" not in (m.get("subject") or ""):
        continue
    order = extract_order_json(m.get("body") or "")
    if not order or not order.get("order_id"):
        unparsed.append({"email_id": m.get("id"), "subject": m.get("subject")})
        continue
    oid = order["order_id"]
    if oid in known or (orders_dir / f"{oid}.json").exists():
        skipped.append(oid)
        continue
    (orders_dir / f"{oid}.json").write_text(json.dumps(order, indent=2))
    cfg = order.get("config", {})
    rows.append({"order_id": oid, "created": order.get("created", m.get("date", "")),
                 "business": cfg.get("name", ""), "customer_email": order.get("email", ""),
                 "product": {"starter": "Starter", "pro": "Pro", "own": "Own"}.get(order.get("plan"), "Own") + (" + legacy Care Plan" if order.get("care_plan") else ""),
                 "amount_gbp": "", "status": "awaiting_payment", "paid_date": "", "live_url": "", "notes": ""})
    known.add(oid)
    new.append(oid)

write_ledger(repo, rows)
print(json.dumps({"new_orders": new, "already_known": skipped, "unparsed_order_emails": unparsed}, indent=2))
