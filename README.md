# Callout Web: self-serve website business (AI-operated)

Static site + order pipeline. No server, no monthly costs.

## How a customer buys (no human in the loop)
1. Finds a guide page on Google (`/guides/...`) or the home page.
2. Builds a live preview of their own site in the browser (`/preview/`). Nothing leaves their device.
3. Presses **Order**: details go to FormSubmit → Gmail (`CW ORDER <id>`), customer gets an automatic confirmation email.
4. Redirected to `/order/pay/` → Stripe Payment Link (carries `client_reference_id=<order id>`).
5. The AI operator's daily scheduled run (see `ops/AGENT_RUNBOOK.md`) matches payment → runs `node ops/fulfil.mjs` → pushes `sites/<slug>/` → emails the live link.

## Repo layout
- `assets/callout-template.js`: the one template used by preview, Etsy builder and fulfilment
- `assets/config.js`: **owner settings** (Stripe links, email, site URL)
- `preview/`: instant preview + order tool
- `tools/build_pages.py`: regenerates home, guides, demos, legal pages, sitemap (`python3 tools/build_pages.py`)
- `tools/content.py`: guide content
- `tools/make_editor.py`: builds the offline Etsy builder
- `ops/`: runbook, support FAQ, fulfilment script, ledger, orders, reports
- `sites/`: delivered client sites

## One-time owner setup (identity, money, accounts: things the AI must not do)
| # | Step | Time | Why only you |
|---|---|---|---|
| 1 | Create a free GitHub account and a public repo `calloutweb`; upload this folder; Settings → Pages → deploy from `main` / root | 15 min | Account creation |
| 2 | Connect GitHub to Claude so the operator can push | 5 min | Authorisation |
| 3 | Create a Stripe account (ID + bank), then two Payment Links: £249 "Launch Site" (one-off) and £20/month "Care Plan"; set "after payment" to redirect to `<site>/order/thanks/`. Send the two links to Claude | 20 min | Identity verification, financial account |
| 4 | Connect the Gmail (calloutweb.hello@gmail.com) and Stripe connectors in Claude settings | 5 min | Authorisation |
| 5 | Place one test order on the live site and click FormSubmit's activation email | 3 min | Inbox owner must confirm |
| 6 | Google Search Console: add the site, verify (Claude adds the verification file), submit `sitemap.xml` | 10 min | Account ownership |
| 7 | Approve the scheduled daily operator task | 1 min | Standing permission |
| opt | Buy `calloutweb.co.uk` (~£5–10/yr) | 5 min | Spending |
| opt | Etsy shop for the DIY builder (ID, small listing fee) | 30 min | Identity, spending |
