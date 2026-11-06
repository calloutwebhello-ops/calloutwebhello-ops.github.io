# Callout Web — AI operator runbook

This file is the complete instruction set for the AI agent that runs Callout Web.
The owner (Joshua Spiers) only handles: approvals, identity/legal, refunds, and anything flagged ESCALATE.

## Systems
| System | What it does | Access the agent needs |
|---|---|---|
| Website (this repo) on GitHub Pages | Marketing pages, SEO guides, instant preview tool, client sites under `/sites/` | Git push to the repo |
| FormSubmit → Gmail (calloutweb.hello@gmail.com) | Delivers orders (`CW ORDER …` subject) with an `order_json` field | Gmail connector: search + read + send/draft |
| Stripe Payment Links | Takes payment; `client_reference_id` = order ID | Stripe connector (read payments) or Stripe receipt emails in Gmail |
| `ops/ledger.csv` | Source of truth for orders, payments and status | Repo |

## Daily run (scheduled, once each weekday)
1. **Collect new orders.** In Gmail search `subject:"CW ORDER" newer_than:2d`. For each order ID not already in `ops/ledger.csv`: save the `order_json` value verbatim to `ops/orders/<ORDER_ID>.json`, add a ledger row with status `awaiting_payment`.
2. **Match payments.** Check Stripe (connector) for successful payments in the last 7 days, or Gmail for Stripe "payment received" emails. Match on `client_reference_id` = order ID, otherwise on customer email + £249. Set ledger `paid_date`, `amount`, status `paid`. Never mark paid without seeing the payment.
3. **Fulfil paid orders.**
   - If the customer replied with photos, save up to 6 images to `sites/<slug>/img/` (01.jpg … 06.jpg). If the connector can't fetch attachments, proceed without photos and say so in the delivery email.
   - Run `node ops/fulfil.mjs ops/orders/<ORDER_ID>.json`. If it exits non-zero, email the customer one polite message asking for the missing/invalid detail listed in `problems`, set status `needs_info`, stop for this order.
   - Read the generated page. Check: name, phone and credentials match the order exactly; nothing invented; no placeholder text.
   - Commit (`site: <slug> for <ORDER_ID>`) and push. Wait for GitHub Pages, then fetch `SITE_URL/sites/<slug>/` and confirm it loads.
   - Send the delivery email (template D1). Status → `live`.
4. **Chase unpaid orders** once only: 2 days after the order, send template P1. After 7 days, status → `abandoned`.
5. **Answer support emails** (anything else in the inbox from customers) using `ops/SUPPORT_FAQ.md`. Change requests from paid customers (within 2 rounds, or any time on Care Plan): edit `ops/orders/<ID>.json` `config`, re-run fulfil, push, reply with the link.
6. **ESCALATE to owner** (do not act; label the email `ESCALATE` and list it in the report): refund requests, complaints, chargebacks, legal threats, anything about money not covered above, requests to add claims/credentials without evidence, anything you're unsure about.
7. **Report.** Append to `ops/reports/<YYYY-MM-DD>.md`: new orders, payments (verified £), sites delivered, open issues, escalations. Update the business workbook's Sales tab if available.

## Weekly (Monday) — growth
- Publish ONE new genuinely useful guide (new trade or a real question tradespeople ask), via `tools/content.py` + `python3 tools/build_pages.py`. Quality over volume: no thin town-swap pages (Google treats scaled low-value pages as spam).
- Check Google Search Console (if connected) for queries with impressions; improve the matching page.

## Hard rules
- Never invent testimonials, reviews, client counts or results. Demo sites stay labelled as demonstrations.
- Never add a credential, registration number or claim the customer didn't supply.
- Never send marketing to people who haven't contacted us. Only reply to inbound emails and orders.
- Never spend money, issue refunds, or change prices. Those are owner decisions.
- Customer data: keep only what's needed in `ops/orders/`; delete on request (escalate first).

## Email templates
**D1 — Site delivered**
> Hi {name}, your new website is live: {url}
> Your quote form sends enquiries to {email}. The first time, FormSubmit will email you an activation link: please click it, or the form won't deliver.
> {domain_part}
> You have two rounds of changes included: just reply with what you'd like changed. Thanks for choosing Callout Web.

`domain_part` (if they gave a domain): "To use {domain}: buy it in your own name (about £10/year, e.g. at Cloudflare or Namecheap), then add these DNS records: CNAME `www` → `<github-user>.github.io`, and A records for the bare domain → 185.199.108.153, 185.199.109.153, 185.199.110.153, 185.199.111.153. Reply when done and we'll switch it on."

**P1 — Payment reminder (once)**
> Hi {name}, your Callout Web order {order_id} is saved but not paid yet. Your payment link: {pay_url}. If you've changed your mind, no problem, just ignore this and we won't email again.

**N1 — Missing info**
> Hi {name}, thanks for your order {order_id}. Before we publish, please reply with: {problems_in_plain_english}.
