"""Shared helpers for the Callout Web operator scripts (ledger + normalised inputs)."""
import csv, json, pathlib, re

LEDGER_FIELDS = ["order_id", "created", "business", "customer_email", "product", "amount_gbp",
                 "status", "paid_date", "live_url", "notes"]

def ledger_path(repo):
    return pathlib.Path(repo) / "ops" / "ledger.csv"

def read_ledger(repo):
    p = ledger_path(repo)
    if not p.exists():
        return []
    with p.open(newline="") as f:
        return list(csv.DictReader(f))

def write_ledger(repo, rows):
    p = ledger_path(repo)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=LEDGER_FIELDS, extrasaction="ignore", lineterminator="\n")
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in LEDGER_FIELDS})

def load_json(path):
    return json.loads(pathlib.Path(path).read_text())

ORDER_ID_RE = re.compile(r"\bCW[A-Z0-9]+-[a-z0-9-]+\b")

def extract_order_json(body):
    """FormSubmit emails contain the field 'order_json' followed by the JSON value.
    Find the first balanced {...} after the label and parse it."""
    i = body.find("order_json")
    if i < 0:
        i = body.find('{"order_id"')   # some form services relabel fields; fall back to the JSON itself
        if i < 0:
            return None
    start = body.find("{", i)
    if start < 0:
        return None
    depth, in_str, esc = 0, False, False
    for j in range(start, len(body)):
        ch = body[j]
        if in_str:
            if esc: esc = False
            elif ch == "\\": esc = True
            elif ch == '"': in_str = False
            continue
        if ch == '"': in_str = True
        elif ch == "{": depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                try:
                    return json.loads(body[start:j + 1])
                except json.JSONDecodeError:
                    return None
    return None
