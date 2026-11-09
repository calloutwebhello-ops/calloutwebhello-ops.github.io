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
.dockets{display:grid;grid-template-columns:1fr 1fr;gap:24px;align-items:start}
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
@media (max-width:820px){.grid3,.dockets{grid-template-columns:1fr}.steps{grid-template-columns:1fr 1fr}}
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
           ("Do I own the website?", "Yes. Your domain is registered in your name, and you can have the site files at any time."),
           ("Who builds it?", "Callout Web uses AI tools to build and look after sites, and every order is checked against the details you supply. We never add credentials or claims you haven't given us."),
           ("How fast is it?", "Usually live within one working day of payment and receiving your photos. Connecting your own domain can take up to 48 hours."),
           ("Will it get me to the top of Google?", "No one can honestly promise that. We build the site so Google can read it and link it to your Google Business Profile. Rankings depend on your area, competition and reviews."),
           ("What if I don't like it?", "You see the full design before paying, and two rounds of changes are included. If we can't put it right within 14 days of payment, we refund you.")]
    faq_html = "".join(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in faq)
    body = f"""<section style="border-top:0;padding-block:28px 56px" class="stack">
<span class="label">Websites for UK tradespeople</span>
<h1>See your new website in <span class="hl">60 seconds</span>. Free.</h1>
<p class="lead">Type your business name, trade and town. Your site builds itself on screen. Like it? Order online for £249 one-off and it goes live on your own address, usually the next working day. No calls, no meetings, no contracts.</p>
<div class="btns"><a class="btn primary" href="preview/">Build my free preview</a><a class="btn" href="#prices">See prices</a></div></section>
<section id="how" class="stack" style="gap:28px"><span class="label">How it works</span><h2>Four steps, all online</h2>
<div class="steps">
<div class="stack"><span class="n">1 · 1 minute</span><h3>Type your details</h3><p>Business name, trade, town, services and the areas you cover.</p></div>
<div class="stack"><span class="n">2 · instant</span><h3>See it live</h3><p>Your site appears as you type. Pick a colour, add job photos.</p></div>
<div class="stack"><span class="n">3 · 2 minutes</span><h3>Order and pay</h3><p>Secure card payment. You get a confirmation email straight away.</p></div>
<div class="stack"><span class="n">4 · next working day</span><h3>Go live</h3><p>We publish it, connect your form to your email and send your link.</p></div></div></section>
<section id="prices" class="stack" style="gap:28px"><span class="label">Prices</span><h2>Fixed prices</h2><p>Not VAT registered, so no VAT is added.</p>
<div class="dockets">
<div class="docket"><header><div class="stack" style="gap:6px"><span class="label">CW-01</span><h3>Launch Site</h3></div><span class="tag">Launch price</span></header>
<div class="price">£249 <small>one-off</small></div><ul><li>One-page mobile website with your services, areas and credentials</li><li>Tap-to-call button and a quote form that emails you</li><li>Your job photo gallery</li><li>Free hosting, with the domain registered in your name</li><li>Basic Google setup and a Google Business Profile checklist</li><li>Two rounds of changes by email</li></ul></div>
<div class="docket"><header><div class="stack" style="gap:6px"><span class="label">CW-02</span><h3>Care Plan</h3></div><span class="label">Optional</span></header>
<div class="price">£20 <small>per month</small></div><ul><li>Unlimited small edits by email (prices, photos, services)</li><li>Hosting, security and backups looked after</li><li>One Google Business Profile post written for you each month</li><li>Monthly summary of enquiries from your form</li><li>Cancel any time. The site stays yours.</li></ul></div></div></section>
<section class="stack" style="gap:20px"><span class="label">Examples</span><h2>Demonstration sites</h2><p>Callout Web is a new business. These sites are demonstrations for fictional companies, labelled as such. Real client sites will be shown here with permission.</p><div class="cards">{demo_cards}</div></section>
<section class="stack" style="gap:20px"><span class="label">Guides</span><h2>Website guides by trade</h2><div class="cards">{guide_cards}<a class="card" href="guides/website-cost/"><b>How much does a tradesman website cost?</b><span>UK price ranges compared</span></a></div></section>
<section id="faq" class="stack" style="gap:6px"><span class="label">Questions</span><h2 style="margin-bottom:10px">Common questions</h2>{faq_html}</section>"""
    schema = {"@context": "https://schema.org", "@type": "ProfessionalService", "name": "Callout Web", "url": SITE, "email": EMAIL,
              "areaServed": "GB", "description": "Websites for UK tradespeople, built and hosted for a fixed price.",
              "offers": [{"@type": "Offer", "name": "Launch Site", "price": "249", "priceCurrency": "GBP"}]}
    faq_schema = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}
    page("", "Callout Web | Websites for tradespeople, from £249", "Websites for UK plumbers, electricians, roofers, builders and other trades. See a free preview in 60 seconds, order online, live the next working day.", body, 0, [schema, faq_schema])
    (ROOT / "index.html").write_text((ROOT / "index.html").read_text())

def guide(slug, g):
    items = "".join(f"<li><h3>{e(h)}</h3><p>{e(t)}</p></li>" for h, t in g["must"])
    body = f"""<article><span class="label">Guide · {e(g['trade'])}</span><h1>{e(g['title'])}</h1><p class="lead">{e(g['lead'])}</p>
<h2>Five things every {e(g['trade'].lower())} website needs</h2><ol>{items}</ol>
<h2>What to avoid</h2><p>{e(g['avoid'])}</p>
<h2>See an example</h2><p>Here's a <a href="../../demos/{slug}/">demonstration {e(g['trade'].lower())} website</a> for a fictional business, built with the same template our clients get.</p>
<div class="cta"><span class="label" style="color:var(--hivis)">Free preview</span><h2>See yours in 60 seconds</h2><p>Type your business name and town, and your site builds on screen. Order online for £249 if you like it.</p><a class="btn primary" href="../../preview/?trade={urllib.parse.quote(g['trade'])}">Build my free preview</a></div>
<p class="label">Updated {TODAY}</p></article>"""
    schema = {"@context": "https://schema.org", "@type": "Article", "headline": g["title"], "dateModified": TODAY, "author": {"@type": "Organization", "name": "Callout Web"}}
    return page(f"guides/{slug}/", g["title"], g["lead"][:155], body, 2, schema)

def cost_guide():
    c = COST_GUIDE
    rows = "".join(f"<tr><td>{e(a)}</td><td>{e(b)}</td><td>{e(d)}</td></tr>" for a, b, d in c["rows"])
    notes = "".join(f"<li><p>{e(n)}</p></li>" for n in c["notes"])
    body = f"""<article><span class="label">Guide · Prices</span><h1>{e(c['title'])}</h1><p class="lead">{e(c['lead'])}</p>
<div class="tbl"><table><thead><tr><th>Option</th><th>Typical cost</th><th>Trade-offs</th></tr></thead><tbody>{rows}</tbody></table></div>
<p class="label">Prices are typical ranges seen on UK providers' websites, November 2026. Check current prices with each provider.</p>
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
<h2>1. What you're buying</h2><p>A Launch Site is a one-page website built from the details and photos you give us, published on free hosting and connected to a domain name registered in your name. The Care Plan is an optional monthly service for edits and upkeep.</p>
<h2>2. Your information</h2><p>You're responsible for the accuracy of everything you give us, including credentials, registrations, prices and claims. We won't add credentials or claims you haven't supplied, and we may refuse content that's unlawful or misleading.</p>
<h2>3. Payment</h2><p>The Launch Site is paid in full before it goes live. Care Plan subscriptions are billed monthly in advance and can be cancelled at any time, effective at the end of the current month.</p>
<h2>4. Changes and refunds</h2><p>Two rounds of changes are included before or after launch, requested by email within 30 days of launch. If we can't deliver a site that matches your order within 14 days of payment, you can have a full refund.</p>
<h2>5. Ownership</h2><p>Once paid, you own the website content and design files made for you, and the domain is in your name. The underlying template code is licensed to you for use on your own business website.</p>
<h2>6. Availability</h2><p>We use reputable free hosting but can't guarantee uninterrupted availability. We aren't liable for lost business or indirect losses. Our total liability is limited to the amount you paid us in the previous 12 months.</p>
<h2>7. Business customers</h2><p>Our services are for businesses and sole traders acting for their trade.</p>
<h2>8. Law</h2><p>These terms are governed by the law of England and Wales.</p></article>"""
    priv = f"""<article><h1>Privacy notice</h1><p class="label">Last updated {TODAY}</p>
<p>Callout Web ({OWNER}, sole trader, UK) is the controller of the personal data described here. Contact: {EMAIL}.</p>
<h2>What we collect</h2><p>When you order: your name, business details, email, phone number, photos you send, and your order details. Payments are processed by our payment provider; we don't see or store your full card details.</p>
<h2>Why</h2><p>To build, publish and support your website (contract), to keep financial records (legal obligation), and to answer your enquiries (legitimate interests).</p>
<h2>Who processes it</h2><p>Email (Google), form delivery (FormSubmit), payment processing (Stripe), website hosting (GitHub Pages or Cloudflare), and AI tools (Anthropic's Claude) used to build sites and draft replies.</p>
<h2>How long</h2><p>Order and financial records for 6 years. Everything else is deleted within 12 months of the end of our service, or sooner if you ask.</p>
<h2>Your rights</h2><p>You can ask to see, correct or delete your data, or object to how we use it, by emailing {EMAIL}. You can also complain to the Information Commissioner's Office (ico.org.uk).</p>
<h2>Preview tool</h2><p>The free preview runs in your browser. Nothing you type there, or any photo you add, is sent to us unless you press Order.</p></article>"""
    page("terms/", "Terms of service | Callout Web", "Terms for Callout Web website orders.", terms, 1)
    page("privacy/", "Privacy notice | Callout Web", "How Callout Web uses your data.", priv, 1)

def order_pages():
    pay = """<section style="border-top:0" class="stack"><span class="label">Step 2 of 2</span><h1>Order received. Now pay securely.</h1>
<p class="lead">Your order reference is <b id="oid">being created</b>. We'll email you a confirmation shortly.</p>
<div class="btns"><a class="btn primary" id="paylink" href="#">Pay £249 by card</a></div>
<p id="care" hidden>You asked for the Care Plan. After paying for your site, <a id="carelink" href="#">set up the £20/month Care Plan here</a>.</p>
<p id="nopay" hidden class="lead">Online payment isn't switched on yet. We'll email you a secure payment link within one working day.</p>
<p>After paying, reply to your confirmation email with up to 6 job photos. Your site will usually go live the next working day.</p></section>
<script src="../../assets/config.js"></script>
<script>(function(){const C=window.CALLOUT_CONFIG||{};const q=new URLSearchParams(location.search);const id=(q.get('id')||'').replace(/[^A-Za-z0-9_-]/g,'').slice(0,190);
document.getElementById('oid').textContent=id||'(see your email)';
const add=(u)=>u+(u.includes('?')?'&':'?')+'client_reference_id='+encodeURIComponent(id);
if(C.STRIPE_LAUNCH_LINK){document.getElementById('paylink').href=add(C.STRIPE_LAUNCH_LINK);}else{document.getElementById('paylink').hidden=true;document.getElementById('nopay').hidden=false;}
if(q.get('care')&&C.STRIPE_CARE_LINK){document.getElementById('care').hidden=false;document.getElementById('carelink').href=add(C.STRIPE_CARE_LINK);}})();</script>"""
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

if __name__ == "__main__":
    demos = build_demos()
    home(demos)
    paths = ["", "preview/", "guides/", "guides/website-cost/", "terms/", "privacy/"]
    paths += [guide(s, g) for s, g in GUIDES.items()]
    guides_index(); cost_guide(); legal(); order_pages()
    sitemap(paths)
    print("built", len(paths), "indexable pages and", len(demos), "demos")
