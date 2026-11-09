#!/usr/bin/env python3
"""Match verified payments to orders and mark them paid in the ledger.

Usage: python3 match_payments.py <payments.json> <repo_dir>
payments.json = [{"id","status","amount_gbp","email","client_reference_id","created"}...]
Only payments with status "succeeded"/"paid"/"complete" count.
Match order: client_reference_id == order_id, else same customer email AND amount == that order's plan price (Starter 19, Pro 39, Own it 249)
AND exactly one awaiting order for that email (otherwise it's ambiguous and is reported, not matched).
Never marks anything paid without a payment record. Prints a JSON summary."""
import json, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from ops_lib import read_ledger, write_ledger, load_json

payments, repo = load_json(sys.argv[1]), pathlib.Path(sys.argv[2])
PLAN_PRICES = {"starter": 19.0, "pro": 39.0, "own": 249.0}
rows = read_ledger(repo)
by_id = {r["order_id"]: r for r in rows}
used = {r["notes"].split("payment:")[1].split()[0] for r in rows if "payment:" in r.get("notes", "")}
matched, unmatched, ignored = [], [], []

for p in payments:
    pid = str(p.get("id", ""))
    if str(p.get("status", "")).lower() not in ("succeeded", "paid", "complete"):
        ignored.append({"payment": pid, "reason": "status " + str(p.get("status"))}); continue
    if pid in used:
        ignored.append({"payment": pid, "reason": "already recorded"}); continue
    row = by_id.get(p.get("client_reference_id") or "")
    how = "client_reference_id"
    if row is None:
        cands = [r for r in rows if r["status"] == "awaiting_payment"
                 and r["customer_email"].lower() == str(p.get("email", "")).lower()]
        amt = float(p.get("amount_gbp") or 0)
        want = PLAN_PRICES.get((cands[0].get("product") or "").split(" ")[0].lower()) if len(cands) == 1 else None
        if len(cands) == 1 and ((want and abs(amt - want) < 0.01) or (not want and any(abs(amt - v) < 0.01 for v in PLAN_PRICES.values()))):
            row, how = cands[0], "email+amount"
        else:
            unmatched.append({"payment": pid, "email": p.get("email"), "amount_gbp": p.get("amount_gbp"),
                              "reason": "no unique awaiting order for this payment"}); continue
    if row["status"] not in ("awaiting_payment", "needs_info"):
        unmatched.append({"payment": pid, "order_id": row["order_id"], "reason": f"order status is {row['status']}"}); continue
    row["status"] = "paid"
    row["amount_gbp"] = str(p.get("amount_gbp", ""))
    row["paid_date"] = str(p.get("created", ""))[:10]
    row["notes"] = (row.get("notes", "") + f" payment:{pid} via {how}").strip()
    used.add(pid)
    matched.append({"order_id": row["order_id"], "payment": pid, "matched_by": how, "amount_gbp": p.get("amount_gbp")})

write_ledger(repo, rows)
print(json.dumps({"matched": matched, "unmatched_payments": unmatched, "ignored": ignored}, indent=2))
