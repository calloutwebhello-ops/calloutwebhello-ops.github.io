/* Callout Web site template engine.
   One function, buildSite(cfg, opts) -> complete HTML document string.
   Used by: the instant preview tool (browser), the Etsy editor (browser, offline),
   and the fulfilment script (Node: ops/fulfil.mjs). Single source of truth. */
(function (root) {
  const esc = s => String(s == null ? "" : s).replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
  const lines = s => String(s || "").split(/\n|,/).map(x => x.trim()).filter(Boolean);

  const THEMES = {
    navy:   { brand: "#1d4e89", accent: "#f5b82e" },
    green:  { brand: "#1f5f43", accent: "#f2c230" },
    red:    { brand: "#8e2a24", accent: "#f2c230" },
    slate:  { brand: "#2b3a48", accent: "#58c4dc" },
    purple: { brand: "#43306f", accent: "#f0b44c" },
    black:  { brand: "#1b1d20", accent: "#e8c547" }
  };

  function buildSite(cfg, opts) {
    opts = opts || {};
    const t = THEMES[cfg.theme] || THEMES.navy;
    const phone = cfg.phone || "";
    const tel = phone.replace(/[^0-9+]/g, "");
    const services = (cfg.services || []).filter(s => s && s.name);
    const areas = Array.isArray(cfg.areas) ? cfg.areas : lines(cfg.areas);
    const creds = Array.isArray(cfg.credentials) ? cfg.credentials : lines(cfg.credentials);
    const photos = cfg.photos || [];   // [{src, caption}] src may be data: URI or relative path
    const town = cfg.town || "";
    const name = cfg.name || "Your Business";
    const trade = cfg.trade || "Trade";
    const headline = cfg.headline || `Trusted local ${trade.toLowerCase()}${town ? " in " + town : ""}`;
    const intro = cfg.intro || `Free quotes, tidy work and clear prices${town ? " across " + town + " and nearby" : ""}. Call or send a quote request.`;
    const about = cfg.about || "";
    const formEmail = cfg.formEmail || "";
    const banner = opts.banner || cfg.banner || "";

    const css = `:root{--bg:#f6f7f9;--card:#fff;--ink:#14202b;--muted:#596673;--rule:#d8dee4;--brand:${t.brand};--on:#fff;--accent:${t.accent};--d:"Barlow Condensed","Arial Narrow",Arial,sans-serif;--b:"Source Sans 3",system-ui,-apple-system,"Segoe UI",sans-serif}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#0f151b;--card:#17212a;--ink:#e9eef2;--muted:#9fb0bd;--rule:#2b3945;color-scheme:dark}}
:root[data-theme="dark"]{--bg:#0f151b;--card:#17212a;--ink:#e9eef2;--muted:#9fb0bd;--rule:#2b3945;color-scheme:dark}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:17px/1.6 var(--b)}
.w{max-width:1000px;margin:0 auto;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
h1,h2,h3{font-family:var(--d);line-height:1.05;margin:0;text-wrap:balance}h1{font-size:clamp(2.3rem,7vw,4rem)}h2{font-size:clamp(1.7rem,4vw,2.4rem)}h3{font-size:1.3rem}
p{margin:0;max-width:65ch}.s{display:flex;flex-direction:column;gap:14px}
.banner{background:var(--accent);color:#14202b;text-align:center;font-weight:700;font-size:.85rem;padding:8px 16px}
.top{background:var(--brand);color:var(--on)}.top .w{padding-block:18px;display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap}
.top strong{font:700 1.4rem var(--d);letter-spacing:.02em}.top a{font-weight:700;color:var(--on);font-size:1.1rem;text-decoration:none}
.hero{background:var(--brand);color:var(--on)}.hero .w{padding-block:36px 56px}.hero p{opacity:.92;font-size:1.15rem}
.btn{display:inline-block;background:var(--accent);color:#14202b;font-weight:700;padding:14px 22px;border-radius:6px;text-decoration:none;font-size:1.05rem}
.btn.o{background:transparent;color:var(--on);border:2px solid var(--on)}.row{display:flex;gap:12px;flex-wrap:wrap}
.badges{display:flex;gap:8px;flex-wrap:wrap}.badges span{border:1px solid rgba(255,255,255,.5);padding:5px 10px;border-radius:4px;font-size:.85rem}
section{padding-block:48px;border-bottom:1px solid var(--rule)}
.svc{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:16px}.svc div{background:var(--card);border:1px solid var(--rule);border-radius:6px;padding:18px;min-width:0}
.svc p{color:var(--muted);font-size:.97rem;margin-top:6px}
.areas{display:flex;flex-wrap:wrap;gap:8px}.areas span{background:var(--card);border:1px solid var(--rule);padding:6px 12px;border-radius:20px;font-size:.95rem}
.gal{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:12px}.gal figure{margin:0;display:flex;flex-direction:column;gap:6px}
.gal img,.gal .ph{width:100%;aspect-ratio:4/3;max-width:100%;object-fit:cover;border-radius:6px}
.gal .ph{background:repeating-linear-gradient(45deg,var(--rule) 0 10px,var(--card) 10px 20px)}.gal figcaption{font-size:.85rem;color:var(--muted)}
form{display:grid;gap:12px;max-width:520px}label{font-weight:600;font-size:.95rem;display:grid;gap:4px}
input,textarea{font:inherit;padding:12px;border:1px solid var(--rule);border-radius:6px;background:var(--card);color:var(--ink)}
button{font:inherit;font-weight:700;background:var(--brand);color:var(--on);border:0;padding:14px;border-radius:6px;cursor:pointer}
a:focus-visible,button:focus-visible,input:focus-visible,textarea:focus-visible{outline:3px solid var(--accent);outline-offset:2px}
footer{padding-block:28px;color:var(--muted);font-size:.9rem}footer a{color:inherit}
.callbar{position:sticky;bottom:0;background:var(--accent);text-align:center;padding:12px max(16px,env(safe-area-inset-right,0px)) calc(12px + env(safe-area-inset-bottom,0px)) max(16px,env(safe-area-inset-left,0px));font-weight:700}
.callbar a{color:#14202b;text-decoration:none}@media (min-width:800px){.callbar{display:none}}`;

    const svcHtml = services.map(s => `<div><h3>${esc(s.name)}</h3>${s.text ? `<p>${esc(s.text)}</p>` : ""}</div>`).join("");
    const areaHtml = areas.map(a => `<span>${esc(a)}</span>`).join("");
    const credHtml = creds.map(c => `<span>${esc(c)}</span>`).join("");
    const galHtml = photos.length
      ? photos.map(p => `<figure><img src="${esc(p.src)}" alt="${esc(p.caption || name + " job photo")}" loading="lazy">${p.caption ? `<figcaption>${esc(p.caption)}</figcaption>` : ""}</figure>`).join("")
      : (opts.placeholders === false ? "" : ["Your job photo", "Your job photo", "Your job photo"].map(c => `<figure><div class="ph"></div><figcaption>${c}</figcaption></figure>`).join(""));

    const formAttr = formEmail
      ? `action="https://formsubmit.co/${esc(formEmail)}" method="POST"`
      : `onsubmit="event.preventDefault();this.querySelector('.ok').hidden=false"`;
    const formExtra = formEmail
      ? `<input type="hidden" name="_subject" value="New quote request from your website"><input type="hidden" name="_template" value="table"><input type="text" name="_honey" style="display:none" tabindex="-1" autocomplete="off">`
      : `<p class="ok" hidden role="status">Preview only: on the live site this sends the request to ${esc(name)} by email.</p>`;

    const schema = JSON.stringify({ "@context": "https://schema.org", "@type": "HomeAndConstructionBusiness", name, telephone: phone, areaServed: areas, address: { "@type": "PostalAddress", addressLocality: town, addressCountry: "GB" } }).replace(/</g, "\\u003c");

    const body = `${banner ? `<div class="banner">${esc(banner)}</div>` : ""}
<header class="top"><div class="w"><strong>${esc(name)}</strong>${phone ? `<a href="tel:${esc(tel)}">${esc(phone)}</a>` : ""}</div></header>
<div class="hero"><div class="w s"><h1>${esc(headline)}</h1><p>${esc(intro)}</p>
<div class="row">${phone ? `<a class="btn" href="tel:${esc(tel)}">Call ${esc(phone)}</a>` : ""}<a class="btn o" href="#quote">Request a quote</a></div>
${credHtml ? `<div class="badges">${credHtml}</div>` : ""}</div></div>
<main class="w">
${svcHtml ? `<section class="s"><h2>What we do</h2><div class="svc">${svcHtml}</div></section>` : ""}
${areaHtml ? `<section class="s"><h2>Areas we cover</h2>${town ? `<p>Based in ${esc(town)}. We regularly work in:</p>` : ""}<div class="areas">${areaHtml}</div></section>` : ""}
${galHtml ? `<section class="s"><h2>Recent work</h2><div class="gal">${galHtml}</div></section>` : ""}
${about ? `<section class="s"><h2>About ${esc(name)}</h2><p>${esc(about)}</p></section>` : ""}
<section class="s" id="quote"><h2>Request a quote</h2><p>Tell us about the job and we'll get back to you.</p>
<form ${formAttr}>${formExtra.startsWith("<input") ? formExtra : ""}
<label for="q-n">Your name<input id="q-n" name="name" required autocomplete="name"></label>
<label for="q-t">Phone number<input id="q-t" name="phone" required type="tel" autocomplete="tel"></label>
<label for="q-p">Postcode<input id="q-p" name="postcode" autocomplete="postal-code"></label>
<label for="q-m">What do you need doing?<textarea id="q-m" name="message" rows="4" required></textarea></label>
<button type="submit">Send request</button>${formExtra.startsWith("<p") ? formExtra : ""}
<p style="font-size:.85rem;color:var(--muted)">Your details are only used to reply to this enquiry.</p></form></section>
</main>
<div class="w"><footer>${esc(name)}${town ? " · " + esc(town) : ""}${phone ? " · " + esc(phone) : ""}${cfg.legal ? " · " + esc(cfg.legal) : ""}<br>Website by <a href="https://calloutwebhello-ops.github.io">Callout Web</a></footer></div>
${phone ? `<div class="callbar"><a href="tel:${esc(tel)}">Tap to call ${esc(phone)}</a></div>` : ""}
<script type="application/ld+json">${schema}</script>`;

    const title = `${name} | ${trade}${town ? " in " + town : ""}`;
    return `<!doctype html><html lang="en-GB"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>${esc(title)}</title><meta name="description" content="${esc(intro)}">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700&family=Source+Sans+3:wght@400;600;700&display=swap">
<style>${css}</style></head><body>${body}</body></html>`;
  }

  function slugify(s) { return String(s || "site").toLowerCase().replace(/&/g, "and").replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "").slice(0, 60) || "site"; }

  const api = { buildSite, slugify, THEMES };
  if (typeof module !== "undefined" && module.exports) module.exports = api; else root.CalloutTemplate = api;
})(typeof window !== "undefined" ? window : globalThis);
