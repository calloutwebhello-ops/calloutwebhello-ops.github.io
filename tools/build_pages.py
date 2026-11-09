#!/usr/bin/env python3
"""Builds the static Callout Web marketing site into ./ (repo root).
Run from repo root:  python3 tools/build_pages.py
Generates: index.html, guides/*, demos/*, terms/, privacy/, order/pay/, 404.html, sitemap.xml, robots.txt
The preview tool (preview/index.html) and assets/ are hand-maintained."""
import html, json, subprocess, pathlib, datetime, sys, urllib.parse
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from content import GUIDES, COST_GUIDE

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = "https://calloutwebhello-ops.github.io"
OWNER = "Joshua Spiers"
EMAIL = "calloutweb.hello@gmail.com"
TODAY = datetime.date.today().isoformat()
e = lambda s: html.escape(str(s), quote=True)

CSS = """:root{--paper:#f2f4f1;--card:#fff;--ink:#16212b;--muted:#56636e;--rule:#cfd6d2;--hivis:#f2c230;--hivis-ink:#16212b;--blue:#1f4f7a;--ok:#2f7a4c;
--display:"Archivo","Arial Narrow",Arial,sans-serif;--body:"Public Sans",system-ui,-apple-system,"Segoe UI",sans-serif;--mono:"IBM Plex Mono",ui-monospace,Menlo,monospace}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--paper:#10171d;--card:#18222b;--ink:#e8edf0;--muted:#9aa8b2;--rule:#2c3a45;--blue:#7fb2e0;--ok:#6cc392;color-scheme:dark}}
:root[data-theme="dark"]{--paper:#10171d;--card:#18222b;--ink:#e8edf0;--muted:#9aa8b2;--rule:#2c3a45;--blue:#7fb2e0;--ok:#6cc392;color-scheme:dark}
*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.6 var(--body)}
.wrap{max-width:1040px;margin:0 auto;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
section{padding-block:52px;border-top:1px solid var(--rule)}
h1,h2,h3{font-family:var(--display);line-height:1.1;text-wrap:balance;margin:0}
h1{font-size:clamp(2.1rem,5.5vw,3.6rem);font-weight:800}h2{font-size:clamp(1.5rem,3.4vw,2.2rem);font-weight:800}h3{font-size:1.15rem;font-weight:700}
p{margin:0;max-width:65ch}a{color:var(--blue)}
.label{font:500 .75rem/1 var(--mono);letter-spacing:.12em;text-transform:uppercase;color:var(--muted)}
.stack{display:flex;flex-direction:column;gap:16px}
nav{display:flex;justify-content:space-between;align-items:center;gap:16px;padding-block:18px;flex-wrap:wrap}
.logo{font:800 1.3rem/1 var(--display);display:flex;align-items:center;gap:10px;color:var(--ink);text-decoration:none}.logo b{background:var(--hivis);color:var(--hivis-ink);padding:4px 8px;border-radius:3px}
.links{display:flex;gap:20px;flex-wrap:wrap}.links a{color:var(--ink);text-decoration:none;font-weight:600;font-size:.95rem}
.lead{font-size:1.15rem;color:var(--muted)}
.hl{background:linear-gradient(transparent 62%,var(--hivis) 62%)}
.btns{display:flex;gap:12px;flex-wrap:wrap}
.btn{display:inline-block;font:700 1rem/1 var(--body);padding:14px 20px;border-radius:4px;text-decoration:none;border:2px solid var(--ink);color:var(--ink)}
.btn.primary{background:var(--hivis);border-color:var(--hivis);color:var(--hivis-ink)}
:focus-visible{outline:3px solid var(--blue);outline-offset:2px}
.grid3{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}.grid3>*{min-width:0}
.steps{display:grid;grid-template-columns:repeat(4,1fr);gap:20px}.steps>div{border-top:4px solid var(--ink);padding-top:14px;min-width:0}
.steps .n{font:500 .8rem var(--mono);color:var(--muted)}
.dockets{display:grid;grid-template-columns:1fr 1fr;gap:24px;align-items:start}.plans3{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;align-items:start}.plans3 .btn{text-align:center}
.docket{background:var(--card);border:1px solid var(--rule);border-radius:4px;padding:24px;display:flex;flex-direction:column;gap:14px;min-width:0}
.docket header{display:flex;justify-content:space-between;align-items:baseline;gap:12px;border-bottom:2px dashed var(--rule);padding-bottom:12px;flex-wrap:wrap}
.price{font:800 2.4rem/1 var(--display)}.price small{font:500 .9rem var(--body);color:var(--muted)}
.docket ul{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:8px}.docket li{display:flex;gap:10px}.docket li::before{content:"\\2713";color:var(--ok);font-weight:700}
.tag{background:var(--hivis);color:var(--hivis-ink);font:700 .7rem/1 var(--mono);padding:5px 8px;border-radius:3px;letter-spacing:.08em;text-transform:uppercase}
.cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:14px}
.card{display:flex;flex-direction:column;gap:6px;background:var(--card);border:1px solid var(--rule);border-radius:4px;padding:16px;text-decoration:none;color:var(--ink);min-width:0}
.card span{color:var(--muted);font-size:.9rem}
details{border-bottom:1px solid var(--rule);padding-block:16px}summary{font-weight:700;cursor:pointer}details p{margin-top:10px;color:var(--muted)}
article{display:flex;flex-direction:column;gap:18px;padding-block:24px 56px;max-width:720px}
article h2{margin-top:18px}article ol{display:flex;flex-direction:column;gap:12px;padding-left:22px;margin:0}article li p{color:var(--muted)}
.cta{background:var(--ink);color:var(--paper);border-radius:4px;padding:24px;display:flex;flex-direction:column;gap:12px}
.cta p{opacity:.85}.cta .btn.primary{align-self:flex-start}
.tbl{overflow-x:auto}table{border-collapse:collapse;width:100%;min-width:560px;font-size:.95rem}th,td{text-align:left;padding:10px;border-bottom:1px solid var(--rule);vertical-align:top}th{font:500 .75rem var(--mono);text-transform:uppercase;letter-spacing:.08em;color:var(--muted)}
footer{padding-block:28px;font-size:.88rem;color:var(--muted);border-top:1px solid var(--rule);display:flex;flex-direction:column;gap:6px}
@media (max-width:820px){.grid3,.dockets,.plans3{grid-template-columns:1fr}.steps{grid-template-columns:1fr 1fr}}
@media (max-width:480px){.steps{grid-template-columns:1fr}.links a:not(.keep){display:none}}"""

FONTS = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@700;800&family=Public+Sans:wght@400;500;600;700&family=IBM+Plex+Mono:wght@500&display=swap">'

def page(path, title, desc, body, depth, schema=None):
    up = "../" * depth
    sch = f'<script type="application/ld+json">{json.dumps(schema)}</script>' if schema else ""
    doc = f"""<!doctype html><html lang="en-GB"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{e(title)}</title><meta name="description" content="{e(desc)}"><link rel="canonical" href="{SITE}/{path}">
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}">{FONTS}<style>{CSS}</style>{sch}</head><body>
<div class="wrap"><nav><a class="logo" href="{up or './'}"><b>CALLOUT</b> web</a><div class="links"><a href="{up}#how">How it works</a><a href="{up}#prices">Prices</a><a href="{up}guides/">Guides</a><a class="keep" href="{up}preview/">Free preview</a></div></nav>
{body}
<footer><span>Callout Web · Websites for UK tradespeople · Run by {OWNER} (sole trader) · Not VAT registered</span>
<span>Email <a href="mailto:{EMAIL}">{EMAIL}</a> · <a href="{up}terms/">Terms</a> · <a href="{up}privacy/">Privacy</a></span></footer></div></body></html>"""
    out = ROOT / path / "index.html" if not path.endswith(".html") else ROOT / path
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(doc)
    return path

def build_demos():
    demos = []
    for slug, g in GUIDES.items():
        d = g["demo"]
        cfg = {"name": d["name"].replace(" (demo)", ""), "trade": g["trade"], "town": d["town"], "phone": "01632 960 000",
               "theme": g["theme"], "areas": [d["town"], "and surrounding areas"], "credentials": d["credentials"],
               "services": [{"name": s.split(" - ")[0], "text": (s.split(" - ") + [""])[1]} for s in d["services"]],
               "about": "This is a demonstration site for a fictional business, made by Callout Web to show what a trade website looks like. A real site uses your own words, photos and credentials."}
        demos.append((slug, cfg))
    js = ROOT / "assets/callout-template.js"
    script = f"""const T=require({json.dumps(str(js))});const fs=require('fs');const path=require('path');
const demos={json.dumps(demos)};
for(const [slug,cfg] of demos){{const dir=path.join({json.dumps(str(ROOT))},'demos',slug);fs.mkdirSync(dir,{{recursive:true}});
fs.writeFileSync(path.join(dir,'index.html'),T.buildSite(cfg,{{banner:'DEMONSTRATION SITE: '+cfg.name+' is a fictional business made by Callout Web. The phone number is not real.'}}).replace('<head>','<head><meta name="robots" content="noindex">'));}}"""
    subprocess.run(["node", "-e", script], check=True)
    return demos

def home(demos):
    demo_cards = "".join(f'<a class="card" href="demos/{s}/"><b>{e(c["name"])}</b><span>{e(GUIDES[s]["trade"])} · demonstration site</span></a>' for s, c in demos)
    guide_cards = "".join(f'<a class="card" href="guides/{s}/"><b>Websites for {e(g["plural"])}</b><span>What to include and what to avoid</span></a>' for s, g in GUIDES.items())
    faq = [("Is the preview really free?", "Yes. The preview builds in your browser as you type. You only pay if you order."),
           ("Is there a contract or setup fee?", "No. Starter and Pro are monthly with no setup fee. Cancel any time by email and you won't be charged again."),
           ("Do I own the website?", "Your domain is always registered in your name. On Own it you own the site outright. On a monthly plan, if you cancel we send you the site files so you can host them anywhere."),
           ("Who builds it?", "Callout Web uses AI tools to build and look after sites, and every order is checked against the details you supply. We never add credentials or claims you haven't given us."),
           ("How fast is it?", "Usually live within one working day of payment. Connecting your own domain can take up to 48 hours."),
           ("Where do you work?", "Anywhere in the UK. Everything happens online, so it doesn't matter where you're based."),
           ("How do I know it's working?", "On Starter and Pro you get a short monthly email showing how many quote requests came through your site."),
           ("Will it get me to the top of Google?", "No one can honestly promise that. We build the site so Google can read it and link it to your Google Business Profile. Rankings depend on your area, competition and reviews."),
           ("What if I don't like it?", "You see the full design before paying. If we can't put it right within 14 days of payment, we refund you.")]
    faq_html = "".join(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in faq)
    body = f"""<section style="border-top:0;padding-block:28px 56px" class="stack">
<span class="label">Websites for UK tradespeople · anywhere in the UK</span>
<h1>See your new website in <span class="hl">60 seconds</span>. Free.</h1>
<p class="lead">Type your business name, trade and town. Your site builds itself on screen. Like it? Go live from <b>£19 a month</b>, with no setup fee, no contract and nothing to manage. Usually live the next working day.</p>
<div class="btns"><a class="btn primary" href="preview/">Build my free preview</a><a class="btn" href="#prices">See prices</a></div></section>
<section id="how" class="stack" style="gap:28px"><span class="label">How it works</span><h2>Four steps, all online</h2>
<div class="steps">
<div class="stack"><span class="n">1 · 1 minute</span><h3>Type your details</h3><p>Business name, trade, town, services and the areas you cover.</p></div>
<div class="stack"><span class="n">2 · instant</span><h3>See it live</h3><p>Your site appears as you type. Pick a colour, add job photos.</p></div>
<div class="stack"><span class="n">3 · 2 minutes</span><h3>Pick a plan and pay</h3><p>Secure card payment through Stripe. No setup fee on monthly plans.</p></div>
<div class="stack"><span class="n">4 · next working day</span><h3>Go live</h3><p>We publish it, connect your quote form to your email and send your link.</p></div></div></section>
<section id="prices" class="stack" style="gap:28px"><span class="label">Prices</span><h2>Simple prices, no contract</h2><p>Not VAT registered, so no VAT is added.</p>
<div class="plans3">
<div class="docket"><header><div class="stack" style="gap:6px"><span class="label">Most popular</span><h3>Starter</h3></div><span class="tag">No setup fee</span></header>
<div class="price">£19 <small>per month</small></div><ul><li>Mobile website with your services, areas and credentials</li><li>Call, WhatsApp and quote-request buttons</li><li>Your job photo gallery</li><li>Hosting, security and updates looked after</li><li>Small changes by email, any time</li><li>Monthly email: how many enquiries your site brought in</li><li>Cancel any time</li></ul><a class="btn primary" href="preview/?plan=starter">Start with a free preview</a></div>
<div class="docket"><header><div class="stack" style="gap:6px"><span class="label">More jobs from Google</span><h3>Pro</h3></div></header>
<div class="price">£39 <small>per month</small></div><ul><li>Everything in Starter</li><li>Up to 5 extra pages for your services or the towns you cover</li><li>A Google Business Profile post written for you every month</li><li>Review-request kit: a link and message to send happy customers</li><li>Priority changes</li><li>Cancel any time</li></ul><a class="btn" href="preview/?plan=pro">Preview for Pro</a></div>
<div class="docket"><header><div class="stack" style="gap:6px"><span class="label">Pay once</span><h3>Own it</h3></div></header>
<div class="price">£249 <small>one-off</small></div><ul><li>The same website, handed over</li><li>Free hosting</li><li>Two rounds of changes in the first 30 days</li><li>After that, changes £25 each</li></ul><a class="btn" href="preview/?plan=own">Preview to buy</a></div></div>
<p>Compare: pay-monthly trade web designers commonly charge around £30 a month, and directory-style packages can cost £399 upfront plus £36 a month (<a href="guides/website-cost/">see our price guide</a>).</p></section>
<section class="stack" style="gap:16px"><span class="label">Refer a trade</span><h2>Know another tradesperson without a website?</h2><p>Send them your referral link from your welcome email. When they join a monthly plan, you both get your next month free.</p></section>
<section class="stack" style="gap:20px"><span class="label">Free tools</span><h2>Free tools for tradespeople</h2><div class="cards"><a class="card" href="tools/quote-invoice/"><b>Free quote and invoice maker</b><span>Make a professional quote or invoice in your browser and save it as a PDF</span></a><a class="card" href="preview/"><b>Free website preview</b><span>See your site in 60 seconds</span></a></div></section>
<section class="stack" style="gap:20px"><span class="label">Examples</span><h2>Demonstration sites</h2><p>Callout Web is a new business. These sites are demonstrations for fictional companies, labelled as such. Real client sites will be shown here with permission.</p><div class="cards">{demo_cards}</div></section>
<section class="stack" style="gap:20px"><span class="label">Guides</span><h2>Website guides by trade</h2><div class="cards">{guide_cards}<a class="card" href="guides/website-cost/"><b>How much does a tradesman website cost?</b><span>UK price ranges compared</span></a></div></section>
<section id="faq" class="stack" style="gap:6px"><span class="label">Questions</span><h2 style="margin-bottom:10px">Common questions</h2>{faq_html}</section>"""
    schema = {"@context": "https://schema.org", "@type": "ProfessionalService", "name": "Callout Web", "url": SITE, "email": EMAIL,
              "areaServed": "GB", "description": "Websites for UK tradespeople, built, hosted and looked after from £19 a month.",
              "offers": [{"@type": "Offer", "name": "Starter", "price": "19", "priceCurrency": "GBP"},
                         {"@type": "Offer", "name": "Pro", "price": "39", "priceCurrency": "GBP"},
                         {"@type": "Offer", "name": "Own it", "price": "249", "priceCurrency": "GBP"}]}
    faq_schema = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}
    page("", "Callout Web | Websites for tradespeople from £19/month", "Websites for UK plumbers, electricians, roofers, builders and other trades. Free preview in 60 seconds. From £19/month, no setup fee, no contract.", body, 0, [schema, faq_schema])
    (ROOT / "index.html").write_text((ROOT / "index.html").read_text())

def guide(slug, g):
    items = "".join(f"<li><h3>{e(h)}</h3><p>{e(t)}</p></li>" for h, t in g["must"])
    body = f"""<article><span class="label">Guide · {e(g['trade'])}</span><h1>{e(g['title'])}</h1><p class="lead">{e(g['lead'])}</p>
<h2>Five things every {e(g['trade'].lower())} website needs</h2><ol>{items}</ol>
<h2>What to avoid</h2><p>{e(g['avoid'])}</p>
<h2>See an example</h2><p>Here's a <a href="../../demos/{slug}/">demonstration {e(g['trade'].lower())} website</a> for a fictional business, built with the same template our clients get.</p>
<div class="cta"><span class="label" style="color:var(--hivis)">Free preview</span><h2>See yours in 60 seconds</h2><p>Type your business name and town, and your site builds on screen. Live from £19 a month if you like it, with no setup fee.</p><a class="btn primary" href="../../preview/?trade={urllib.parse.quote(g['trade'])}">Build my free preview</a></div>
<p class="label">Updated {TODAY}</p></article>"""
    schema = {"@context": "https://schema.org", "@type": "Article", "headline": g["title"], "dateModified": TODAY, "author": {"@type": "Organization", "name": "Callout Web"}}
    return page(f"guides/{slug}/", g["title"], g["lead"][:155], body, 2, schema)

def cost_guide():
    c = COST_GUIDE
    rows = "".join(f"<tr><td>{e(a)}</td><td>{e(b)}</td><td>{e(d)}</td></tr>" for a, b, d in c["rows"])
    notes = "".join(f"<li><p>{e(n)}</p></li>" for n in c["notes"])
    body = f"""<article><span class="label">Guide · Prices</span><h1>{e(c['title'])}</h1><p class="lead">{e(c['lead'])}</p>
<div class="tbl"><table><thead><tr><th>Option</th><th>Typical cost</th><th>Trade-offs</th></tr></thead><tbody>{rows}</tbody></table></div>
<p class="label">Prices are typical ranges seen on UK providers' websites and reviews, November 2026. Check current prices with each provider. Sources: {" · ".join(f'<a href="{u}">{e(t)}</a>' for t, u in c.get("sources", []))}</p>
<h2>Things to check before you pay anyone</h2><ol>{notes}</ol>
<div class="cta"><span class="label" style="color:var(--hivis)">Free preview</span><h2>See your site before you spend a penny</h2><a class="btn primary" href="../../preview/">Build my free preview</a></div></article>"""
    return page("guides/website-cost/", c["title"], c["lead"][:155], body, 2)

def guides_index():
    cards = "".join(f'<a class="card" href="{s}/"><b>{e(g["title"])}</b><span>{e(g["trade"])}</span></a>' for s, g in GUIDES.items())
    body = f'<section style="border-top:0" class="stack"><span class="label">Guides</span><h1>Website guides for tradespeople</h1><div class="cards">{cards}<a class="card" href="website-cost/"><b>{e(COST_GUIDE["title"])}</b><span>Prices</span></a></div></section>'
    return page("guides/", "Website guides for UK tradespeople | Callout Web", "Practical guides on what a plumber, electrician, roofer, builder, decorator, landscaper, cleaner or locksmith website needs.", body, 1)

def legal():
    terms = f"""<article><h1>Terms of service</h1><p class="label">Last updated {TODAY}</p>
<p>These terms apply when you order from Callout Web, a business run by {OWNER} as a sole trader in the United Kingdom. Contact: {EMAIL}.</p>
<h2>1. What you're buying</h2><p>A website built from the details and photos you give us, published on free hosting and, if you want, connected to a domain name registered in your name. Starter (£19/month) and Pro (£39/month) include hosting, upkeep, small changes by email and a monthly enquiry report; Pro adds extra pages and a monthly Google Business Profile post. Own it (£249 one-off) is the site handed over with two rounds of changes in the first 30 days.</p>
<h2>2. Your information</h2><p>You're responsible for the accuracy of everything you give us, including credentials, registrations, prices and claims. We won't add credentials or claims you haven't supplied, and we may refuse content that's unlawful or misleading.</p>
<h2>3. Payment and cancelling</h2><p>Monthly plans are billed in advance by card through Stripe and can be cancelled any time by emailing us; you won't be charged again and the plan ends at the end of the month you've paid for. When a monthly plan ends we take the site offline and, on request, send you the site files so you can host them yourself. Own it is paid in full before the site goes live.</p>
<h2>4. Changes and refunds</h2><p>On monthly plans, small changes are included while you're subscribed. On Own it, two rounds of changes are included within 30 days of launch. If we can't deliver a site that matches your order within 14 days of payment, you can have a full refund.</p>
<h2>5. Ownership</h2><p>You own your business content and photos, and any domain is registered in your name. On Own it, once paid, you own the site files made for you; on monthly plans, you can have them when you leave. The underlying template code is licensed to you for use on your own business website.</p>
<h2>6. Enquiry reports</h2><p>On monthly plans, a copy of each quote request sent through your site's form is also sent to our business inbox so we can count enquiries for your monthly report. We use these copies only for that report and delete them within 90 days. We act as your data processor for them.</p>
<h2>7. Availability</h2><p>We use reputable free hosting but can't guarantee uninterrupted availability. We aren't liable for lost business or indirect losses. Our total liability is limited to the amount you paid us in the previous 12 months.</p>
<h2>8. Business customers</h2><p>Our services are for businesses and sole traders acting for their trade.</p>
<h2>9. Law</h2><p>These terms are governed by the law of England and Wales.</p></article>"""
    priv = f"""<article><h1>Privacy notice</h1><p class="label">Last updated {TODAY}</p>
<p>Callout Web ({OWNER}, sole trader, UK) is the controller of the personal data described here. Contact: {EMAIL}.</p>
<h2>What we collect</h2><p>When you order: your name, business details, email, phone number, photos you send, and your order details. Payments are processed by our payment provider; we don't see or store your full card details.</p>
<h2>Why</h2><p>To build, publish and support your website (contract), to keep financial records (legal obligation), and to answer your enquiries (legitimate interests).</p>
<h2>Who processes it</h2><p>Email (Google), form delivery (FormSubmit), payment processing (Stripe), website hosting (GitHub Pages or Cloudflare), and AI tools (Anthropic's Claude) used to build sites and draft replies.</p>
<h2>How long</h2><p>Order and financial records for 6 years. Everything else is deleted within 12 months of the end of our service, or sooner if you ask.</p>
<h2>Your rights</h2><p>You can ask to see, correct or delete your data, or object to how we use it, by emailing {EMAIL}. You can also complain to the Information Commissioner's Office (ico.org.uk).</p>
<h2>Enquiries sent through our clients' websites</h2><p>If you send a quote request through a website we host, it goes to that business. A copy also comes to us so we can count enquiries for the business's monthly report; we don't contact you or use it for anything else, and we delete it within 90 days.</p>
<h2>Preview tool</h2><p>The free preview runs in your browser. Nothing you type there, or any photo you add, is sent to us unless you press Order.</p></article>"""
    page("terms/", "Terms of service | Callout Web", "Terms for Callout Web website orders.", terms, 1)
    page("privacy/", "Privacy notice | Callout Web", "How Callout Web uses your data.", priv, 1)

def order_pages():
    pay = """<section style="border-top:0" class="stack"><span class="label">Step 2 of 2</span><h1>Order received. Now pay securely.</h1>
<p class="lead">Your order reference is <b id="oid">being created</b>. We'll email you a confirmation shortly.</p>
<p class="lead" id="planline"></p>
<div class="btns"><a class="btn primary" id="paylink" href="#">Pay by card</a></div>
<p id="nopay" hidden class="lead">Online payment isn't switched on yet. We'll email you a secure payment link within one working day.</p>
<p>Payments are handled by Stripe. After paying, reply to your confirmation email with up to 6 job photos if you have them. Your site will usually go live the next working day.</p></section>
<script src="../../assets/config.js"></script>
<script>(function(){const C=window.CALLOUT_CONFIG||{};const q=new URLSearchParams(location.search);const id=(q.get('id')||'').replace(/[^A-Za-z0-9_-]/g,'').slice(0,190);
const P=C.PLANS||{};const key=(q.get('plan')||'starter').replace(/[^a-z]/g,'');const plan=P[key]||P.starter;
document.getElementById('oid').textContent=id||'(see your email)';
const add=(u)=>u+(u.includes('?')?'&':'?')+'client_reference_id='+encodeURIComponent(id);
if(plan&&plan.link){document.getElementById('planline').textContent='Plan: '+plan.name+', £'+plan.price+(plan.period==='month'?' a month, no setup fee, cancel any time':' one-off');
 const a=document.getElementById('paylink');a.href=add(plan.link);a.textContent='Pay £'+plan.price+(plan.period==='month'?'/month':'')+' by card';}
else{document.getElementById('paylink').hidden=true;document.getElementById('nopay').hidden=false;}})();</script>"""
    page("order/pay/", "Pay for your website | Callout Web", "Complete your Callout Web order.", pay, 2)
    thanks = """<section style="border-top:0" class="stack"><h1>Payment received. Thank you.</h1><p class="lead">We'll email you within one working day with your live link. If you haven't sent your job photos yet, reply to your confirmation email with them.</p></section>"""
    page("order/thanks/", "Thank you | Callout Web", "Payment received.", thanks, 2)
    nf = '<section style="border-top:0" class="stack"><h1>Page not found</h1><p><a href="/">Go to the home page</a> or <a href="/preview/">build a free preview</a>.</p></section>'
    page("404.html", "Page not found | Callout Web", "Not found", nf, 0)

def sitemap(paths):
    # Delivered client sites are public pages too: list them so Google finds them without anyone asking.
    paths = list(paths) + sorted(f"sites/{d.name}/" for d in (ROOT / "sites").glob("*") if (d / "index.html").exists())
    urls = "".join(f"<url><loc>{SITE}/{p}</loc><lastmod>{TODAY}</lastmod></url>" for p in paths)
    (ROOT / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>')
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nDisallow: /order/\nSitemap: {SITE}/sitemap.xml\n")

def tools_page():
    body = r"""<section style="border-top:0;padding-block:20px 8px" class="stack noprint"><span class="label">Free tool · no sign-up</span>
<h1>Free quote and invoice maker for tradespeople</h1>
<p class="lead">Fill in the boxes, check the preview, then press <b>Save as PDF</b> and send it to your customer. It works in your browser, and nothing you type is sent to us. Your business details are remembered on this device for next time.</p></section>
<div class="qi">
<form class="qi-form noprint" id="qf" autocomplete="on">
<div class="seg2" role="group" aria-label="Document type"><label><input type="radio" name="kind" value="Quote" checked> Quote</label><label><input type="radio" name="kind" value="Invoice"> Invoice</label></div>
<fieldset><legend>Your business</legend>
<label for="b_name">Business name<input id="b_name" placeholder="Hartley Plumbing &amp; Heating"></label>
<label for="b_addr">Address<textarea id="b_addr" rows="2" placeholder="12 High Street, Bristol, BS1 1AA"></textarea></label>
<label for="b_contact">Phone and email<input id="b_contact" placeholder="07700 900123 · you@example.co.uk"></label>
<label for="b_pay">How to pay you (invoices)<textarea id="b_pay" rows="2" placeholder="Bank transfer to: Name, sort code 00-00-00, account 00000000"></textarea></label>
<label class="chk2"><input type="checkbox" id="b_vat"> I'm VAT registered (adds 20% VAT)</label>
<label for="b_vatno">VAT number<input id="b_vatno" placeholder="GB123456789"></label></fieldset>
<fieldset><legend>Customer and job</legend>
<label for="c_name">Customer name<input id="c_name" placeholder="Mrs J Smith"></label>
<label for="c_addr">Customer address<textarea id="c_addr" rows="2" placeholder="4 Park Road, Bristol"></textarea></label>
<div class="two2"><label for="d_no">Number<input id="d_no" value="001"></label><label for="d_date">Date<input id="d_date" type="date"></label></div>
<label for="d_terms">Valid for / payment due<input id="d_terms" value="30 days"></label></fieldset>
<fieldset><legend>Items</legend><div id="items"></div><button type="button" class="btn" id="add">Add a line</button></fieldset>
<label for="notes">Notes<textarea id="notes" rows="3" placeholder="Includes all materials. Work guaranteed for 12 months."></textarea></label>
<button type="button" class="btn primary" id="print">Save as PDF / print</button>
<p class="hint">In the print window, choose "Save as PDF" as the printer.</p>
</form>
<div class="doc" id="doc" aria-live="polite"></div>
</div>
<section class="stack noprint" style="gap:12px"><div class="cta"><span class="label" style="color:var(--hivis)">Look the part online too</span><h2>Get a website that matches your paperwork</h2><p>See your own trade website in 60 seconds, free. Live from £19 a month, no setup fee, no contract.</p><a class="btn primary" href="../../preview/">Build my free preview</a></div></section>
<style>
.qi{display:grid;grid-template-columns:minmax(0,400px) minmax(0,1fr);gap:24px;align-items:start;padding-block:16px 40px}
.qi-form{display:flex;flex-direction:column;gap:14px}.qi-form fieldset{border:1px solid var(--rule);border-radius:6px;padding:14px;display:grid;gap:10px;margin:0}
.qi-form legend{font:500 .75rem var(--mono);letter-spacing:.1em;text-transform:uppercase;color:var(--muted);padding:0 6px}
.qi-form label{display:grid;gap:4px;font-weight:600;font-size:.9rem}.qi-form input,.qi-form textarea{font:inherit;font-size:.95rem;padding:9px 10px;border:1px solid var(--rule);border-radius:5px;background:var(--card);color:var(--ink);width:100%}
.chk2{display:flex!important;gap:8px;align-items:center;font-weight:400!important}.chk2 input{width:auto!important}
.two2{display:grid;grid-template-columns:1fr 1fr;gap:10px}.seg2{display:flex;gap:16px;font-weight:700}.seg2 input{width:auto}
.line{display:grid;grid-template-columns:1fr 64px 90px 32px;gap:6px}.line button{border:1px solid var(--rule);background:var(--card);color:var(--ink);border-radius:5px;cursor:pointer}
.hint{font-size:.85rem;color:var(--muted);margin:0}
.doc{background:#fff;color:#111;border:1px solid var(--rule);border-radius:6px;padding:32px;font:14px/1.5 "Public Sans",Arial,sans-serif;min-width:0;overflow-x:auto}
.doc h2{font:800 1.8rem/1 "Archivo",Arial,sans-serif;margin:0 0 4px;color:#111}.doc .top{display:flex;justify-content:space-between;gap:20px;flex-wrap:wrap;margin-bottom:22px}
.doc .muted{color:#555;white-space:pre-line}.doc table{width:100%;border-collapse:collapse;margin:14px 0;min-width:0}.doc th,.doc td{border-bottom:1px solid #ddd;padding:8px 6px;text-align:left;color:#111}.doc td.n,.doc th.n{text-align:right;font-variant-numeric:tabular-nums}
.doc .tot{margin-left:auto;width:min(280px,100%)}.doc .tot td{border:0;padding:3px 6px}.doc .tot tr:last-child td{font-weight:800;border-top:2px solid #111}
@media (max-width:860px){.qi{grid-template-columns:1fr}}
@media print{body{background:#fff}nav,footer,.noprint{display:none!important}.qi{display:block;padding:0}.doc{border:0;padding:0}.wrap{max-width:none}}
</style>
<script>
(function(){const $=id=>document.getElementById(id);const KEY="cw-qi-business";const keep=["b_name","b_addr","b_contact","b_pay","b_vatno"];
try{const s=JSON.parse(localStorage.getItem(KEY)||"{}");keep.forEach(k=>{if(s[k])$(k).value=s[k];});if(s.b_vat)$("b_vat").checked=true;}catch(e){}
$("d_date").valueAsDate=new Date();
const esc=s=>String(s||"").replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const money=n=>"£"+(Math.round(n*100)/100).toLocaleString("en-GB",{minimumFractionDigits:2,maximumFractionDigits:2});
function addLine(d,q,p){const r=document.createElement("div");r.className="line";r.innerHTML='<input aria-label="Description" placeholder="Description" value="'+esc(d)+'"><input aria-label="Quantity" type="number" min="0" step="any" value="'+(q??1)+'"><input aria-label="Price each" type="number" min="0" step="0.01" placeholder="£ each" value="'+(p??"")+'"><button type="button" aria-label="Remove line">×</button>';r.querySelector("button").onclick=()=>{r.remove();draw();};$("items").appendChild(r);}
addLine("Labour",1,"");addLine("Materials",1,"");
function draw(){const kind=document.querySelector("input[name=kind]:checked").value;const vat=$("b_vat").checked;
 const rows=[...document.querySelectorAll(".line")].map(r=>{const i=r.querySelectorAll("input");const q=parseFloat(i[1].value)||0,p=parseFloat(i[2].value)||0;return {d:i[0].value,q,p,t:q*p};}).filter(x=>x.d||x.t);
 const sub=rows.reduce((a,x)=>a+x.t,0),v=vat?sub*0.2:0;
 $("doc").innerHTML='<div class="top"><div><h2>'+kind.toUpperCase()+'</h2><div class="muted">'+esc(kind)+' no. '+esc($("d_no").value)+'<br>Date: '+esc($("d_date").value?new Date($("d_date").value).toLocaleDateString("en-GB"):"")+'<br>'+(kind==="Quote"?"Valid for: ":"Payment due: ")+esc($("d_terms").value)+'</div></div><div><b>'+esc($("b_name").value||"Your business")+'</b><div class="muted">'+esc($("b_addr").value)+'<br>'+esc($("b_contact").value)+(vat&&$("b_vatno").value?'<br>VAT no. '+esc($("b_vatno").value):'')+'</div></div></div>'
 +'<div><b>For:</b> '+esc($("c_name").value)+'<div class="muted">'+esc($("c_addr").value)+'</div></div>'
 +'<table><thead><tr><th>Description</th><th class="n">Qty</th><th class="n">Each</th><th class="n">Total</th></tr></thead><tbody>'+rows.map(x=>'<tr><td>'+esc(x.d)+'</td><td class="n">'+x.q+'</td><td class="n">'+money(x.p)+'</td><td class="n">'+money(x.t)+'</td></tr>').join("")+'</tbody></table>'
 +'<table class="tot"><tr><td>Subtotal</td><td class="n">'+money(sub)+'</td></tr>'+(vat?'<tr><td>VAT 20%</td><td class="n">'+money(v)+'</td></tr>':'')+'<tr><td>Total</td><td class="n">'+money(sub+v)+'</td></tr></table>'
 +(vat?'':'<p class="muted">Not VAT registered.</p>')+($("notes").value?'<p class="muted">'+esc($("notes").value)+'</p>':'')+(kind==="Invoice"&&$("b_pay").value?'<p><b>How to pay</b><br><span class="muted">'+esc($("b_pay").value)+'</span></p>':'');
 try{const s={};keep.forEach(k=>s[k]=$(k).value);s.b_vat=$("b_vat").checked;localStorage.setItem(KEY,JSON.stringify(s));}catch(e){}}
$("qf").addEventListener("input",draw);$("add").onclick=()=>{addLine("",1,"");draw();};$("print").onclick=()=>{draw();window.print();};draw();})();
</script>"""
    schema = {"@context": "https://schema.org", "@type": "WebApplication", "name": "Free quote and invoice maker for tradespeople", "applicationCategory": "BusinessApplication", "offers": {"@type": "Offer", "price": "0", "priceCurrency": "GBP"}, "url": f"{SITE}/tools/quote-invoice/"}
    return page("tools/quote-invoice/", "Free Quote & Invoice Maker for Tradespeople (UK) | Callout Web", "Make a professional quote or invoice for your trade business in your browser and save it as a PDF. Free, no sign-up, works on your phone.", body, 2, schema)

if __name__ == "__main__":
    demos = build_demos()
    home(demos)
    paths = ["", "preview/", "guides/", "guides/website-cost/", "terms/", "privacy/"]
    paths += [guide(s, g) for s, g in GUIDES.items()]
    guides_index(); cost_guide(); legal(); order_pages()
    paths += [tools_page()]
    sitemap(paths)
    print("built", len(paths), "indexable pages and", len(demos), "demos")
