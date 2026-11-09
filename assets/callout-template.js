/* Callout Web site template engine.
   One function, buildSite(cfg, opts) -> complete HTML document string.
   Used by: the instant preview tool (browser), the Etsy editor (browser, offline),
   and the fulfilment script (Node: ops/fulfil.mjs). Single source of truth.

   cfg.style  = "bold" | "clean" | "classic"  (default picked from the trade)
   cfg.theme  = colour key from THEMES         (default picked from the trade)
   Never invents claims: every badge, hour, credential and photo comes from cfg. */
(function (root) {
  const esc = s => String(s == null ? "" : s).replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
  const lines = s => String(s || "").split(/\n|,/).map(x => x.trim()).filter(Boolean);

  const THEMES = {
    navy:   { brand: "#1d4e89", accent: "#f5b82e" },
    green:  { brand: "#1f5f43", accent: "#f2c230" },
    red:    { brand: "#9b2c23", accent: "#f2c230" },
    slate:  { brand: "#2b3a48", accent: "#58c4dc" },
    purple: { brand: "#43306f", accent: "#f0b44c" },
    black:  { brand: "#1b1d20", accent: "#e8c547" },
    orange: { brand: "#b4420f", accent: "#ffd166" },
    teal:   { brand: "#0e5c5a", accent: "#f4a259" }
  };
  const STYLES = { bold: "Bold", clean: "Clean", classic: "Classic" };

  // Simple line icons drawn for Callout Web (24x24, stroke).
  const ICONS = {
    drop: "M12 3c-3.6 4.6-6 7.9-6 11a6 6 0 0 0 12 0c0-3.1-2.4-6.4-6-11z M9.5 14.5a2.5 2.5 0 0 0 2.5 2.5",
    bolt: "M13 2 4 14h7l-1 8 9-12h-7l1-8z",
    roof: "M2 12 12 4l10 8 M5 10v10h14V10 M10 20v-5h4v5 M16 7V4h2v4.6",
    brick: "M3 5h18v14H3z M3 9.7h18 M3 14.3h18 M9 5v4.7 M15 5v4.7 M6 9.7v4.6 M12 9.7v4.6 M18 9.7v4.6 M9 14.3V19 M15 14.3V19",
    brush: "M4 3h12v6H4z M16 5h3v6h-7v3 M10 14h4v7h-4z",
    leaf: "M5 19C5 10 11 5 20 4c-1 9-6 15-15 15z M5 19l8-8",
    sparkle: "M11 3l2 5.5L18.5 10 13 11.5 11 17l-2-5.5L3.5 10 9 8.5z M18 15l.9 2.1L21 18l-2.1.9L18 21l-.9-2.1L15 18l2.1-.9z",
    key: "M8 15a4 4 0 1 1 0-8 4 4 0 0 1 0 8z M11 12.5l9 7.5 M17 17.5l2-2.4 M14.5 15.4l2-2.4",
    hammer: "M13 3l7 7-3 3-7-7z M11.5 7.5 3 16l3 3 8.5-8.5",
    trowel: "M3 15l8-8 6 6-8 8z M14 10l7-7",
    wrench: "M14.7 6.3a4 4 0 0 0-5.4 5.4L3 18l3 3 6.3-6.3a4 4 0 0 0 5.4-5.4l-2.5 2.5-2.5-.5-.5-2.5z",
    phone: "M5 3h4l2 5-2.5 1.5a11 11 0 0 0 6 6L16 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 5a2 2 0 0 1 2-2z",
    chat: "M4 4h16v12H8l-4 4z",
    pin: "M12 21s-6-5.6-6-11a6 6 0 0 1 12 0c0 5.4-6 11-6 11z M12 12.5a2.5 2.5 0 1 0 0-5 2.5 2.5 0 0 0 0 5z",
    check: "M5 12.5l4.5 4.5L19 7.5",
    clock: "M12 21a9 9 0 1 0 0-18 9 9 0 0 0 0 18z M12 7v5l3 2",
    shield: "M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z M8.5 12l2.5 2.5 4.5-4.5",
    arrow: "M5 12h14 M13 6l6 6-6 6"
  };
  const svg = (k, cls) => `<svg class="${cls || "ic"}" viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="${ICONS[k] || ICONS.wrench}"/></svg>`;

  function tradeInfo(trade) {
    const t = String(trade || "").toLowerCase();
    const m = (re, icon, style, theme) => re.test(t) && { icon, style, theme };
    return m(/plumb|heat|gas|boiler/, "drop", "bold", "navy") || m(/elec|spark/, "bolt", "bold", "slate") ||
      m(/roof|gutter/, "roof", "bold", "red") || m(/lock/, "key", "bold", "black") ||
      m(/build|brick|extension/, "brick", "classic", "black") || m(/carp|join/, "hammer", "classic", "teal") ||
      m(/plaster|render/, "trowel", "classic", "slate") || m(/paint|decor/, "brush", "classic", "purple") ||
      m(/landsc|garden|tree|fenc/, "leaf", "clean", "green") || m(/clean|wash/, "sparkle", "clean", "teal") ||
      { icon: "wrench", style: "bold", theme: "navy" };
  }

  // Fonts and look for each style. Colours come from the theme.
  const LOOK = {
    bold: { fonts: "family=Archivo:wght@400;600;700;800;900", d: '"Archivo",system-ui,sans-serif', b: '"Archivo",system-ui,sans-serif', r: "4px", bg: "#f3f3f1", card: "#fff" },
    clean: { fonts: "family=Plus+Jakarta+Sans:wght@400;600;700;800", d: '"Plus Jakarta Sans",system-ui,sans-serif', b: '"Plus Jakarta Sans",system-ui,sans-serif', r: "18px", bg: "#ffffff", card: "#f5f7f8" },
    classic: { fonts: "family=Fraunces:opsz,wght@9..144,600;9..144,700&family=Libre+Franklin:wght@400;600;700", d: '"Fraunces",Georgia,serif', b: '"Libre Franklin",system-ui,sans-serif', r: "3px", bg: "#f7f3ec", card: "#fffdf8" }
  };

  function buildSite(cfg, opts) {
    opts = opts || {};
    const name = cfg.name || "Your Business";
    const trade = cfg.trade || "Trade";
    const info = tradeInfo(trade);
    const style = STYLES[cfg.style] ? cfg.style : info.style;
    const t = THEMES[cfg.theme] || THEMES[info.theme];
    const L = LOOK[style];
    const phone = cfg.phone || "";
    const tel = phone.replace(/[^0-9+]/g, "");
    const services = (cfg.services || []).filter(s => s && s.name);
    const areas = Array.isArray(cfg.areas) ? cfg.areas : lines(cfg.areas);
    const creds = Array.isArray(cfg.credentials) ? cfg.credentials : lines(cfg.credentials);
    const photos = cfg.photos || [];   // [{src, caption}] src may be data: URI or relative path
    const town = cfg.town || "";
    const headline = cfg.headline || `Your local ${trade.toLowerCase()}${town ? " in " + town : ""}`;
    const intro = cfg.intro || `${trade} services${town ? " across " + town + " and nearby" : ""}. Call, message or send a quote request and we'll get back to you.`;
    const about = cfg.about || "";
    const formEmail = cfg.formEmail || "";
    const banner = opts.banner || cfg.banner || "";
    const digits = phone.replace(/[^0-9]/g, "");
    const waNum = /^07\d{9}$/.test(digits) ? "44" + digits.slice(1) : (/^447\d{9}$/.test(digits) ? digits : "");
    const wa = cfg.whatsapp !== false && waNum ? `https://wa.me/${waNum}?text=${encodeURIComponent("Hi " + name + ", I found you on your website and I'd like a quote.")}` : "";
    const hours = cfg.hours || "";
    const emergency = !!cfg.emergency;
    const initials = name.replace(/\(.*?\)/g, "").split(/\s+/).filter(w => /^[A-Za-z0-9]/.test(w) && !/^(and|the|of|ltd|limited|llp)$/i.test(w)).slice(0, 2).map(w => w[0].toUpperCase()).join("") || "C";

    // Headline: highlight the town if it appears.
    let h1 = esc(headline);
    if (town && headline.includes(town)) { const i = headline.lastIndexOf(town); h1 = esc(headline.slice(0, i)) + `<em>${esc(town)}</em>` + esc(headline.slice(i + town.length)); }

    const css = `:root{--bg:${L.bg};--card:${L.card};--ink:#141a20;--muted:#5a6570;--rule:rgba(20,26,32,.12);--brand:${t.brand};--accent:${t.accent};--on:#fff;--r:${L.r};--d:${L.d};--b:${L.b}}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#0e1317;--card:#161e24;--ink:#eaeef1;--muted:#a1adb6;--rule:rgba(255,255,255,.12);color-scheme:dark}}
:root[data-theme="dark"]{--bg:#0e1317;--card:#161e24;--ink:#eaeef1;--muted:#a1adb6;--rule:rgba(255,255,255,.12);color-scheme:dark}
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:var(--bg);color:var(--ink);font:17px/1.6 var(--b);-webkit-font-smoothing:antialiased}
img{max-width:100%;display:block}a{color:inherit}
.w{max-width:1120px;margin:0 auto;padding-left:max(18px,env(safe-area-inset-left,0px));padding-right:max(18px,env(safe-area-inset-right,0px))}
h1,h2,h3{font-family:var(--d);line-height:1.05;margin:0;text-wrap:balance;letter-spacing:-.01em}
h1{font-size:clamp(2.4rem,7.2vw,4.6rem)}h2{font-size:clamp(1.8rem,4.2vw,2.8rem)}h3{font-size:1.2rem;line-height:1.2}
p{margin:0;max-width:62ch}.ic{width:22px;height:22px;flex:none}
.banner{background:var(--accent);color:#14202b;text-align:center;font-weight:700;font-size:.82rem;padding:7px 16px;letter-spacing:.02em}
.top{position:sticky;top:0;z-index:20;background:color-mix(in srgb,var(--bg) 88%,transparent);backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px);border-bottom:1px solid var(--rule)}
.top .w{display:flex;align-items:center;justify-content:space-between;gap:14px;min-height:68px}
.logo{display:flex;align-items:center;gap:10px;text-decoration:none;min-width:0}.mark{width:40px;height:40px;border-radius:var(--r);background:var(--brand);color:var(--on);display:grid;place-items:center;font:800 .95rem var(--d);flex:none}
.logo b{font:700 1.08rem/1.15 var(--d);overflow:hidden;text-overflow:ellipsis}
.nav{display:none;gap:26px;font-weight:600;font-size:.95rem}.nav a{text-decoration:none;color:var(--muted)}.nav a:hover{color:var(--ink)}
.tcall{display:inline-flex;align-items:center;gap:8px;background:var(--brand);color:var(--on);text-decoration:none;font-weight:700;padding:10px 16px;border-radius:var(--r);white-space:nowrap;font-size:.95rem}
@media (min-width:860px){.nav{display:flex}}@media (max-width:520px){.tcall span{display:none}.tcall{padding:10px}}
.btn{display:inline-flex;align-items:center;gap:10px;background:var(--accent);color:#14202b;font-weight:800;padding:15px 22px;border-radius:var(--r);text-decoration:none;font-size:1.02rem;border:2px solid transparent}
.btn.o{background:transparent;border-color:currentColor;color:inherit}.btn.wa{background:#25d366;color:#08311a}.row{display:flex;gap:12px;flex-wrap:wrap}
.hero{position:relative;overflow:hidden}.hero .w{display:grid;gap:36px;padding-block:52px 64px;align-items:center}
@media (min-width:900px){.hero .w{grid-template-columns:1.15fr .85fr;padding-block:80px 92px}}
.eyebrow{display:inline-flex;align-items:center;gap:8px;font-weight:700;font-size:.8rem;letter-spacing:.14em;text-transform:uppercase}
.hero .s{display:flex;flex-direction:column;gap:22px}.hero p.lead{font-size:1.16rem}
.chips{display:flex;gap:8px;flex-wrap:wrap}.chips span{display:inline-flex;align-items:center;gap:6px;font-weight:600;font-size:.88rem;padding:6px 12px;border-radius:999px}
.chips .ic{width:16px;height:16px}
.visual{position:relative;aspect-ratio:4/4.4;border-radius:calc(var(--r)*1.4);overflow:hidden;max-width:460px;width:100%;justify-self:center}
.visual img{width:100%;height:100%;object-fit:cover}@media (max-width:899px){.visual{aspect-ratio:16/9;max-width:none}.art .big{width:30%;height:30%}.vcard{display:none}}
.art{position:absolute;inset:0;display:grid;place-items:center}.art .big{width:46%;height:46%}
.vcard{position:absolute;left:16px;right:16px;bottom:16px;background:var(--card);color:var(--ink);border-radius:var(--r);padding:16px 18px;display:flex;align-items:center;gap:14px;box-shadow:0 12px 30px rgba(0,0,0,.18)}
.vcard .mark{width:44px;height:44px}.vcard small{display:block;color:var(--muted);font-size:.82rem}.vcard b{font-size:1.05rem}
.strip{border-block:1px solid var(--rule);background:var(--card)}.strip .w{display:flex;flex-wrap:wrap;gap:12px 28px;padding-block:18px;font-weight:600;font-size:.95rem}
.strip span{display:inline-flex;align-items:center;gap:8px}.strip .ic{color:var(--brand)}
section{padding-block:72px}.head{display:flex;flex-direction:column;gap:12px;margin-bottom:34px}.head .eyebrow{color:var(--brand)}.head p{color:var(--muted)}
.svc{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:16px}
.svc article{background:var(--card);border:1px solid var(--rule);border-radius:var(--r);padding:24px;display:flex;flex-direction:column;gap:12px;min-width:0;transition:transform .2s,box-shadow .2s}
.svc article:hover{transform:translateY(-3px);box-shadow:0 14px 30px rgba(0,0,0,.08)}
.svc .n{display:flex;justify-content:space-between;align-items:center;color:var(--brand)}.svc .n small{font:700 .8rem var(--d);color:var(--muted);letter-spacing:.08em}
.svc .ib{width:46px;height:46px;border-radius:var(--r);display:grid;place-items:center;background:color-mix(in srgb,var(--brand) 12%,transparent)}
.svc p{color:var(--muted);font-size:.97rem}
.steps{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:16px;counter-reset:s}
.steps div{padding:24px;border-radius:var(--r);border:1px solid var(--rule);display:flex;flex-direction:column;gap:8px}
.steps div::before{counter-increment:s;content:counter(s);font:800 1.1rem var(--d);width:40px;height:40px;border-radius:50%;display:grid;place-items:center;background:var(--accent);color:#14202b;margin-bottom:6px}
.steps p{color:var(--muted);font-size:.97rem}
.areas{display:flex;flex-wrap:wrap;gap:10px}.areas span{display:inline-flex;align-items:center;gap:6px;background:var(--card);border:1px solid var(--rule);padding:8px 14px;border-radius:999px;font-weight:600;font-size:.95rem}
.areas .ic{width:16px;height:16px;color:var(--brand)}
.gal{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:14px}.gal figure{margin:0;display:flex;flex-direction:column;gap:8px}
.gal img,.gal .ph{width:100%;aspect-ratio:4/3;object-fit:cover;border-radius:var(--r)}
.gal .ph{display:grid;place-items:center;color:var(--muted);background:color-mix(in srgb,var(--brand) 6%,var(--card));border:2px dashed color-mix(in srgb,var(--brand) 30%,transparent)}.gal .ph .ic{width:34px;height:34px;opacity:.6}.gal figcaption{font-size:.86rem;color:var(--muted)}
.about{display:grid;gap:28px;align-items:center}@media (min-width:860px){.about{grid-template-columns:auto 1fr}}
.about .mark{width:120px;height:120px;font-size:2.4rem;border-radius:calc(var(--r)*1.6)}.about p{font-size:1.1rem}
.quote{background:var(--brand);color:var(--on)}.quote .w{display:grid;gap:36px}@media (min-width:900px){.quote .w{grid-template-columns:.9fr 1.1fr;align-items:start}}
.quote .head .eyebrow{color:var(--accent)}.quote .head p{color:inherit;opacity:.85}
.contact{display:flex;flex-direction:column;gap:12px}.contact a,.contact div{display:flex;align-items:center;gap:14px;text-decoration:none;padding:16px 18px;border-radius:var(--r);background:rgba(255,255,255,.1);font-weight:700}
.contact small{display:block;font-weight:400;opacity:.8;font-size:.85rem}
form{display:grid;gap:14px;background:var(--card);color:var(--ink);padding:26px;border-radius:calc(var(--r)*1.3);box-shadow:0 20px 50px rgba(0,0,0,.18)}
.two{display:grid;gap:14px}@media (min-width:560px){.two{grid-template-columns:1fr 1fr}}
label{font-weight:600;font-size:.92rem;display:grid;gap:6px}
input,textarea{font:inherit;padding:13px 14px;border:1px solid var(--rule);border-radius:var(--r);background:var(--bg);color:var(--ink);width:100%}
button{font:inherit;font-weight:800;background:var(--brand);color:var(--on);border:0;padding:16px;border-radius:var(--r);cursor:pointer;font-size:1.02rem}
form .fine{font-size:.82rem;color:var(--muted)}
a:focus-visible,button:focus-visible,input:focus-visible,textarea:focus-visible{outline:3px solid var(--accent);outline-offset:2px}
footer{padding-block:34px calc(34px + 64px);color:var(--muted);font-size:.9rem}footer .w{display:flex;flex-wrap:wrap;justify-content:space-between;gap:12px}
@media (min-width:800px){footer{padding-bottom:34px}}
.callbar{position:fixed;left:0;right:0;bottom:0;z-index:30;display:flex;gap:8px;padding:10px max(12px,env(safe-area-inset-right,0px)) calc(10px + env(safe-area-inset-bottom,0px)) max(12px,env(safe-area-inset-left,0px));background:color-mix(in srgb,var(--bg) 92%,transparent);backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px);border-top:1px solid var(--rule)}
.callbar a{flex:1;display:inline-flex;justify-content:center;align-items:center;gap:8px;font-weight:800;text-decoration:none;padding:14px;border-radius:var(--r);background:var(--brand);color:var(--on)}.callbar a.wa{background:#25d366;color:#08311a;flex:0 0 auto}
@media (min-width:800px){.callbar{display:none}}
${style === "bold" ? `
.hero{background:#121518;color:#fff}.hero::after{content:"";position:absolute;left:0;right:0;bottom:0;height:12px;background:repeating-linear-gradient(-45deg,var(--accent) 0 18px,#121518 18px 36px)}
.hero h1{text-transform:uppercase;font-weight:900;letter-spacing:-.02em;line-height:.95}.hero h1 em{font-style:normal;color:var(--accent)}
.hero .eyebrow{color:var(--accent)}.hero p.lead{color:rgba(255,255,255,.82)}.hero .chips span{background:rgba(255,255,255,.1);color:#fff}
.visual{background:var(--brand)}.art{background:radial-gradient(circle at 70% 25%,rgba(255,255,255,.18),transparent 55%),repeating-linear-gradient(90deg,rgba(255,255,255,.06) 0 1px,transparent 1px 28px),repeating-linear-gradient(0deg,rgba(255,255,255,.06) 0 1px,transparent 1px 28px);color:var(--accent)}
h2{text-transform:uppercase;font-weight:900;letter-spacing:-.015em}.svc article{border-width:0;border-left:4px solid var(--accent)}
` : ""}${style === "clean" ? `
.hero{background:linear-gradient(160deg,color-mix(in srgb,var(--brand) 10%,var(--bg)) 0%,var(--bg) 70%)}
.hero h1{font-weight:800;letter-spacing:-.03em}.hero h1 em{font-style:normal;color:var(--brand);background:linear-gradient(transparent 62%,color-mix(in srgb,var(--accent) 55%,transparent) 62%)}
.hero .eyebrow{color:var(--brand);background:color-mix(in srgb,var(--brand) 10%,transparent);padding:7px 14px;border-radius:999px;align-self:flex-start}
.hero p.lead{color:var(--muted)}.hero .chips span{background:var(--card);border:1px solid var(--rule)}.hero .btn.o{color:var(--brand)}
.visual{background:color-mix(in srgb,var(--brand) 14%,var(--bg));border-radius:40% 40% 24px 24px / 30% 30% 24px 24px}
.art{color:var(--brand);background:radial-gradient(circle at 50% 40%,color-mix(in srgb,var(--accent) 45%,transparent) 0 22%,transparent 23%)}
h2{font-weight:800;letter-spacing:-.025em}.svc article{border:0}.steps div{background:var(--card);border:0}
` : ""}${style === "classic" ? `
.hero{background:var(--brand);color:#fbf6ec}.hero h1{font-weight:700}.hero h1 em{color:var(--accent)}
.hero .eyebrow{color:var(--accent)}.hero .eyebrow::before,.hero .eyebrow::after{content:"";width:26px;height:1px;background:currentColor}
.hero p.lead{color:rgba(251,246,236,.85)}.hero .chips span{border:1px solid rgba(251,246,236,.35)}
.visual{background:color-mix(in srgb,var(--brand) 70%,#000);outline:1px solid rgba(251,246,236,.3);outline-offset:-14px}
.art{color:#fbf6ec}.art .ring{position:absolute;width:68%;aspect-ratio:1;border-radius:50%;border:2px solid var(--accent);box-shadow:0 0 0 10px color-mix(in srgb,var(--brand) 70%,#000),0 0 0 11px rgba(251,246,236,.35)}
@media (max-width:899px){.art .ring{width:auto;height:72%}.art .lbl{display:none}.vcard{display:none}}.art .lbl{position:absolute;top:12%;font:600 .78rem var(--b);letter-spacing:.3em;text-transform:uppercase;color:var(--accent)}
h2{font-weight:700}.head .eyebrow{font-family:var(--b)}.svc article{border-top:3px double var(--brand)}
.quote{background:color-mix(in srgb,var(--brand) 82%,#000)}
` : ""}`;

    const svcHtml = services.map((s, i) => `<article><div class="n"><span class="ib">${svg(info.icon)}</span><small>${String(i + 1).padStart(2, "0")}</small></div><h3>${esc(s.name)}</h3>${s.text ? `<p>${esc(s.text)}</p>` : ""}</article>`).join("");
    const areaHtml = areas.map(a => `<span>${svg("pin")}${esc(a)}</span>`).join("");
    const galHtml = photos.length
      ? photos.map(p => `<figure><img src="${esc(p.src)}" alt="${esc(p.caption || name + " job photo")}" loading="lazy">${p.caption ? `<figcaption>${esc(p.caption)}</figcaption>` : ""}</figure>`).join("")
      : (opts.placeholders === false ? "" : ["Your job photo goes here", "Before and after shots work well", "Phone photos are fine"].map(c => `<figure><div class="ph">${svg(info.icon)}</div><figcaption>${c}</figcaption></figure>`).join(""));

    // Trust strip: only facts from the order.
    const strip = [
      ...creds.map(c => `<span>${svg("shield")}${esc(c)}</span>`),
      emergency ? `<span>${svg("clock")}24/7 emergency callouts</span>` : "",
      hours ? `<span>${svg("clock")}${esc(hours)}</span>` : "",
      town ? `<span>${svg("pin")}Based in ${esc(town)}</span>` : "",
      areas.length > 1 ? `<span>${svg("check")}Covering ${areas.length} areas</span>` : "",
      wa ? `<span>${svg("chat")}WhatsApp welcome</span>` : ""
    ].filter(Boolean).join("");

    const chips = [emergency ? `<span>${svg("clock")}24/7 emergency callouts</span>` : "", hours ? `<span>${svg("clock")}${esc(hours)}</span>` : "", ...creds.slice(0, 2).map(c => `<span>${svg("shield")}${esc(c)}</span>`)].filter(Boolean).join("");

    const visual = photos.length
      ? `<div class="visual"><img src="${esc(photos[0].src)}" alt="${esc(photos[0].caption || name + " job photo")}"></div>`
      : `<div class="visual" aria-hidden="true"><div class="art">${style === "classic" ? `<div class="ring"></div><div class="lbl">${esc(trade)}</div>` : ""}${svg(info.icon, "big")}</div>${phone ? `<div class="vcard"><span class="mark">${svg("phone")}</span><div><small>Call ${esc(name)}</small><b>${esc(phone)}</b></div></div>` : ""}</div>`;

    const formAttr = formEmail
      ? `action="https://formsubmit.co/${esc(formEmail)}" method="POST"`
      : `onsubmit="event.preventDefault();this.querySelector('.ok').hidden=false"`;
    const formHidden = formEmail
      ? `<input type="hidden" name="_subject" value="New quote request from your website"><input type="hidden" name="_template" value="table"><input type="text" name="_honey" style="display:none" tabindex="-1" autocomplete="off">${cfg.leadsCc ? `<input type="hidden" name="_cc" value="${esc(cfg.leadsCc)}">` : ""}`
      : "";
    const formNote = formEmail ? "" : `<p class="ok fine" hidden role="status">Preview only: on the live site this sends the request to ${esc(name)} by email.</p>`;

    const schemaObj = { "@context": "https://schema.org", "@type": "HomeAndConstructionBusiness", name, telephone: phone, areaServed: areas, address: { "@type": "PostalAddress", addressLocality: town, addressCountry: "GB" } };
    if (emergency) schemaObj.openingHours = "Mo-Su 00:00-23:59"; else if (hours) schemaObj.description = "Opening hours: " + hours;
    if (opts.siteUrl) schemaObj.url = opts.siteUrl;
    const schema = JSON.stringify(schemaObj).replace(/</g, "\\u003c");

    const body = `${banner ? `<div class="banner">${esc(banner)}</div>` : ""}
<header class="top"><div class="w"><a class="logo" href="#top"><span class="mark">${esc(initials)}</span><b>${esc(name)}</b></a>
<nav class="nav" aria-label="Main">${svcHtml ? `<a href="#services">Services</a>` : ""}${areaHtml ? `<a href="#areas">Areas</a>` : ""}${photos.length ? `<a href="#work">Our work</a>` : ""}<a href="#quote">Get a quote</a></nav>
${phone ? `<a class="tcall" href="tel:${esc(tel)}">${svg("phone")}<span>${esc(phone)}</span></a>` : ""}</div></header>
<div class="hero" id="top"><div class="w"><div class="s">
<span class="eyebrow">${esc(trade)}${town ? " · " + esc(town) : ""}</span>
<h1>${h1}</h1><p class="lead">${esc(intro)}</p>
<div class="row">${phone ? `<a class="btn" href="tel:${esc(tel)}">${svg("phone")}Call ${esc(phone)}</a>` : ""}${wa ? `<a class="btn wa" href="${esc(wa)}" target="_blank" rel="noopener">${svg("chat")}WhatsApp</a>` : ""}<a class="btn o" href="#quote">Get a quote ${svg("arrow")}</a></div>
${chips ? `<div class="chips">${chips}</div>` : ""}</div>
${visual}</div></div>
${strip ? `<div class="strip"><div class="w">${strip}</div></div>` : ""}
<main>
${svcHtml ? `<section id="services"><div class="w"><div class="head"><span class="eyebrow">Services</span><h2>What we do</h2>${town ? `<p>${esc(trade)} services for homes and businesses in ${esc(town)} and the surrounding area.</p>` : ""}</div><div class="svc">${svcHtml}</div></div></section>` : ""}
${galHtml ? `<section id="work" style="padding-top:0"><div class="w"><div class="head"><span class="eyebrow">Our work</span><h2>Recent jobs</h2></div><div class="gal">${galHtml}</div></div></section>` : ""}
<section style="padding-top:0"><div class="w"><div class="head"><span class="eyebrow">Getting started</span><h2>How to book us</h2></div>
<div class="steps"><div><h3>Get in touch</h3><p>${phone ? "Call" : "Message"}${wa ? ", WhatsApp" : ""} or fill in the quote form with a few details about the job.</p></div>
<div><h3>We get back to you</h3><p>We'll talk the job through with you${town ? " and arrange a time in " + esc(town) + " or nearby" : ""}.</p></div>
<div><h3>Job done</h3><p>The work gets done and you know exactly who to call if you need us again.</p></div></div></div></section>
${areaHtml ? `<section id="areas" style="padding-top:0"><div class="w"><div class="head"><span class="eyebrow">Coverage</span><h2>Areas we cover</h2>${town ? `<p>Based in ${esc(town)}. We regularly work in:</p>` : ""}</div><div class="areas">${areaHtml}</div></div></section>` : ""}
${about ? `<section style="padding-top:0"><div class="w about"><span class="mark">${esc(initials)}</span><div class="head" style="margin:0"><span class="eyebrow">About us</span><h2>About ${esc(name)}</h2><p>${esc(about)}</p></div></div></section>` : ""}
<section class="quote" id="quote"><div class="w">
<div><div class="head"><span class="eyebrow">Free to ask</span><h2>Get a quote</h2><p>Tell us about the job and we'll get back to you.</p></div>
<div class="contact">${phone ? `<a href="tel:${esc(tel)}">${svg("phone")}<span>${esc(phone)}<small>Tap to call</small></span></a>` : ""}${wa ? `<a href="${esc(wa)}" target="_blank" rel="noopener">${svg("chat")}<span>WhatsApp<small>Send a message or photos of the job</small></span></a>` : ""}${hours || emergency ? `<div>${svg("clock")}<span>${emergency ? "24/7 emergency callouts" : esc(hours)}${emergency && hours ? `<small>${esc(hours)}</small>` : ""}</span></div>` : ""}</div></div>
<form ${formAttr}>${formHidden}
<div class="two"><label for="q-n">Your name<input id="q-n" name="name" required autocomplete="name"></label>
<label for="q-t">Phone number<input id="q-t" name="phone" required type="tel" autocomplete="tel"></label></div>
<label for="q-p">Postcode<input id="q-p" name="postcode" autocomplete="postal-code"></label>
<label for="q-m">What do you need doing?<textarea id="q-m" name="message" rows="4" required></textarea></label>
<button type="submit">Send request</button>${formNote}
<p class="fine">Your details are only used to reply to this enquiry.</p></form></div></section>
</main>
<footer><div class="w"><span>${esc(name)}${town ? " · " + esc(town) : ""}${phone ? " · " + esc(phone) : ""}${cfg.legal ? " · " + esc(cfg.legal) : ""}</span><span>Website by <a href="https://calloutwebhello-ops.github.io">Callout Web</a></span></div></footer>
${phone ? `<div class="callbar"><a href="tel:${esc(tel)}">${svg("phone")}Call now</a>${wa ? `<a class="wa" href="${esc(wa)}" target="_blank" rel="noopener" aria-label="WhatsApp">${svg("chat")}</a>` : ""}</div>` : ""}
<script type="application/ld+json">${schema}</script>
${formEmail ? `<script>(function(){var f=document.querySelector('#quote form');if(!f||!window.fetch)return;f.addEventListener('submit',function(e){e.preventDefault();var b=f.querySelector('button');b.disabled=true;b.textContent='Sending…';
var done=function(ok){var p=document.createElement('p');p.setAttribute('role','status');p.style.cssText='background:var(--card);color:var(--ink);padding:26px;border-radius:12px;font-weight:600';p.textContent=ok?'Thanks, your request has been sent. We\\'ll be in touch soon.':'Sorry, the form didn\\'t send. Please call us${phone ? " on " + esc(phone).replace(/'/g, "") : ""} instead.';f.replaceWith(p);};
fetch(f.action.replace('formsubmit.co/','formsubmit.co/ajax/'),{method:'POST',body:new FormData(f),headers:{Accept:'application/json'}}).then(function(r){done(r.ok);}).catch(function(){done(false);});});})();</script>` : ""}`;

    const title = `${name} | ${trade}${town ? " in " + town : ""}`;
    return `<!doctype html><html lang="en-GB"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>${esc(title)}</title><meta name="description" content="${esc(intro)}"><meta name="theme-color" content="${t.brand}">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="https://fonts.googleapis.com/css2?${L.fonts}&display=swap">
<style>${css}</style></head><body class="st-${style}">${body}</body></html>`;
  }

  function slugify(s) { return String(s || "site").toLowerCase().replace(/&/g, "and").replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "").slice(0, 60) || "site"; }

  const api = { buildSite, slugify, THEMES, STYLES, tradeInfo };
  if (typeof module !== "undefined" && module.exports) module.exports = api; else root.CalloutTemplate = api;
})(typeof window !== "undefined" ? window : globalThis);
