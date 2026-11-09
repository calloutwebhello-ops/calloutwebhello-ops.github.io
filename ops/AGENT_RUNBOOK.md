# Callout Web — AI operator runbook

This file is the complete instruction set for the AI agent that runs Callout Web.
The owner (Joshua Spiers) only handles: approvals, identity/legal, refunds, and anything flagged ESCALATE.

## Systems
| System | What it does | Access the agent needs |
|---|---|---|
| Website (this repo) on GitHub Pages | Marketing pages, SEO guides, instant preview tool, client sites under `/sites/` | Git push to the repo |
| Web3Forms → Gmail (calloutweb.hello@gmail.com) | Delivers orders (`CW ORDER …` subject) with an `order_json` field; customers can also email orders directly as a fallback | Gmail connector: search, read, label, send/draft |
| Stripe Payment Links | Takes payment; `client_reference_id` = order ID | Stripe connector (read payments) or Stripe receipt emails in Gmail |
| Gmail labels + Stripe | **The only places customer data is stored.** Order status = Gmail label on the order email: `CW/Awaiting payment`, `CW/Paid`, `CW/Needs info`, `CW/Live`, `CW/Escalate`, `CW/Abandoned`. Money = Stripe. | Gmail + Stripe connectors |

## Customer data rule
Never commit orders, ledgers, reports or customer emails to GitHub (the repo is public). `ops/ledger.csv` and `ops/orders/` are scratch copies built fresh in the run folder from Gmail labels and deleted at the end of every run. The daily report is emailed to the owner, not committed. Client site files under `sites/` are public by design and contain only what the customer chose to publish.

## Daily run (scheduled, once each weekday)
1. **Collect new orders.** In Gmail search `subject:"CW ORDER" newer_than:2d`. For each order ID not already in `ops/ledger.csv`: save the `order_json` value verbatim to `ops/orders/<ORDER_ID>.json`, add a ledger row with status `awaiting_payment`.
2. **Match payments.** Check Stripe (connector) for successful payments in the last 7 days, or Gmail for Stripe "payment received" emails. Match on `client_reference_id` = order ID, otherwise on customer email + £249. Set ledger `paid_date`, `amount`, status `paid`. Never mark paid without seeing the payment.
3. **Fulfil paid orders.**
   - If the customer replied with photos, save up to 6 images to `sites/<slug>/img/` (01.jpg … 06.jpg). If the connector can't fetch attachments, proceed without photos and say so in the delivery email.
   - Run `node ops/fulfil.mjs ops/orders/<ORDER_ID>.json`. If it exits non-zero, email the customer one polite message asking for the missing/invalid detail listed in `problems`, set status `needs_info`, stop for this order.
   - Read the generated page. Check: name, phone and credentials match the order exactly; nothing invented; no placeholder text.
   - Run `python3 tools/build_pages.py` so the new site is added to sitemap.xml, then commit (`site: <slug> for <ORDER_ID>`) and push.
   - After the customer clicks FormSubmit's activation link, FormSubmit gives a random form code: replace their email in the site's form with it (`formEmail` in the order config) and republish, so their email isn't visible in the page code. Wait for GitHub Pages, then fetch `SITE_URL/sites/<slug>/` and confirm it loads.
   - Send the delivery email (template D1). Status → `live`.
4. **Chase unpaid orders** once only: 2 days after the order, send template P1. After 7 days, status → `abandoned`.
5. **Answer support emails** (anything else in the inbox from customers) using `ops/SUPPORT_FAQ.md`. Change requests from paid customers (within 2 rounds, or any time on Care Plan): edit `ops/orders/<ID>.json` `config`, re-run fulfil, push, reply with the link.
6. **ESCALATE to owner** (do not act; label the email `ESCALATE` and list it in the report): refund requests, complaints, chargebacks, legal threats, anything about money not covered above, requests to add claims/credentials without evidence, anything you're unsure about.
7. **Report.** Email the report to the owner (subject `Callout Web report YYYY-MM-DD`): new orders, payments (verified £), sites delivered, open issues, escalations. Then delete the run's scratch files.

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
> Help customers find it (10 minutes, worth it):
> 1. Google: open your Google Business Profile (search your business name on Google while signed in, or go to business.google.com), choose Edit profile > Contact > Website, and paste {url}. No profile yet? Create one free at business.google.com.
> 2. Put {url} on your Facebook page, Yell listing, van, quotes and invoices.
> 3. Ask your last few happy customers for a Google review.
> Need a change? Just reply to this email.
> Know another tradesperson without a website? Send them {referral_link}. When they join a monthly plan, you both get your next month free.
> Thanks for choosing Callout Web.

`domain_part` (if they gave a domain): "To use {domain}: buy it in your own name (about £10/year, e.g. at Cloudflare or Namecheap), then add these DNS records: CNAME `www` → `<github-user>.github.io`, and A records for the bare domain → 185.199.108.153, 185.199.109.153, 185.199.110.153, 185.199.111.153. Reply when done and we'll switch it on."

**P1 — Payment reminder (once)**
> Hi {name}, your Callout Web order {order_id} is saved but not paid yet. Your payment link: {pay_url}. If you've changed your mind, no problem, just ignore this and we won't email again.

**N1 — Missing info**
> Hi {name}, thanks for your order {order_id}. Before we publish, please reply with: {problems_in_plain_english}.

## Plans (from 9 Nov 2026)
| Plan | Price | Stripe | What we deliver |
|---|---|---|---|
| Starter | £19/month, no setup, cancel any time | live payment link (plan=starter) | Site, hosting, small edits by email, monthly enquiry report |
| Pro | £39/month | live payment link (plan=pro) | Starter + up to 5 extra service/town pages, 1 Google Business Profile post drafted each month (sent to the customer to paste), review-request kit, priority edits |
| Own it | £249 one-off | live payment link (plan=own) | Site handed over, 2 rounds of changes in 30 days, then £25 per edit (escalate for a payment link) |
Legacy: orders with `care_plan: true` are the old £249 + £20/month offer; honour what they bought.

## Monthly enquiry report (Starter/Pro) — 1st working day of each month
Client quote forms CC `calloutweb.hello+leads@gmail.com`. Count last month's FormSubmit copies per client site (match the site name in the email), email each subscriber one line: "In <month>, your website sent you N quote requests." Never forward or reuse the enquirers' details; delete lead copies older than 90 days.

## Cancellations
Customer emails to cancel: reply confirming, label CW/Escalate so the owner cancels the Stripe subscription (Claude has no write access to subscriptions), and after the paid month ends, remove `sites/<slug>/` and send them the site files if they asked.

## Referrals
Each customer's referral link is `https://calloutwebhello-ops.github.io/preview/?ref=<their slug>` — include it in the welcome (D1) email: "Know another tradesperson? When they join a monthly plan using your link, you both get your next month free." When a paid order's `ref` matches a live customer's slug, put "Referral credit: <both businesses>" under Needs owner (the owner applies the free month in Stripe).

## Outreach (approved 9 Nov 2026; runs only while OUTREACH_APPROVED is true)
Campaign 1: up to 100 companies in total, max 10 new emails per weekday, from calloutweb.hello@gmail.com. Count = threads labelled CW/Outreach.

How to find prospects (proven on 9 Nov; about 1 in 5 directory listings yields a usable email):
1. Search trade-body and directory listings for UK limited companies by trade + town (e.g. corc.co.uk/members, fmb.org.uk/builder, checkatrade, trustatrader, freeindex, myjobquote). Rotate trades and towns across the whole UK.
2. Keep only companies whose name or site states Ltd/Limited/LLP, and that publish a business email (info@, enquiries@, or a business-name address like companyname@gmail.com). Never use a person's named address or a sole trader/partnership.
3. Fetch their website (if any). Only email if ONE of these is verifiably true: (a) no website at all; (b) a concrete, checkable problem you saw yourself: broken or mistyped email link, menu links that go nowhere, visible typos, out-of-date copyright (3+ years), placeholder text, no mobile viewport. Quote the exact problem. If their site is fine, skip them.
4. Check suppression: skip anyone already labelled CW/Outreach or who replied STOP (label CW/Do not contact).

Email format (keep it this short and kind): greeting to "<Company> team"; the specific problem in one or two sentences (or "I couldn't find a website for you"); the personalised preview link https://calloutwebhello-ops.github.io/preview/?name=..&trade=..&town=..&phone=..&ref=outreach; "If you like it, it can go live from £19 a month with no setup fee and no contract. If not, no problem at all."; sign "Josh, Callout Web (Joshua Spiers, UK sole trader) · site URL"; source line "I found your details on <source>. Reply STOP and I won't email you again." Label the sent thread CW/Outreach.

Replies: STOP/unsubscribe → reply once "Done, you won't hear from us again", label CW/Do not contact. Interested → answer from SUPPORT_FAQ and point them to their preview link. Complaints → CW/Escalate. Never send a follow-up to someone who hasn't replied.
Report daily: sent today, total sent, replies, opt-outs, orders with ref=outreach.
