#!/usr/bin/env node
// Callout Web fulfilment: order JSON -> live client site files.
// Usage: node ops/fulfil.mjs ops/orders/<ORDER_ID>.json [--preview]
//  - Reads the order (the order_json field FormSubmit emailed us, saved verbatim).
//  - Validates it, builds the site with the same template the customer previewed.
//  - Writes sites/<slug>/index.html (served at SITE_URL/sites/<slug>/) and,
//    if the order has a domain, a standalone copy in ops/out/<slug>/ with a CNAME
//    file, ready to push to its own GitHub Pages repo.
//  - Never invents content: only fields present in the order are used.
import fs from "node:fs";
import path from "node:path";
import { createRequire } from "node:module";
const require = createRequire(import.meta.url);
const ROOT = path.resolve(path.dirname(new URL(import.meta.url).pathname), "..");
const T = require(path.join(ROOT, "assets/callout-template.js"));

const file = process.argv[2];
if (!file) { console.error("usage: node ops/fulfil.mjs <order.json> [--preview]"); process.exit(2); }
const order = JSON.parse(fs.readFileSync(file, "utf8"));
const c = order.config || {};

const problems = [];
if (!order.order_id) problems.push("missing order_id");
if (!c.name) problems.push("missing business name");
if (!c.town) problems.push("missing town");
if (!/^[0-9+ ()-]{7,20}$/.test(c.phone || "")) problems.push("phone missing or not a phone number");
if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(order.email || "")) problems.push("customer email invalid");
const text = JSON.stringify(c).toLowerCase();
for (const bad of ["<script", "javascript:", "onerror="]) if (text.includes(bad)) problems.push("unsafe content: " + bad);
if (problems.length) { console.error(JSON.stringify({ ok: false, problems }, null, 2)); process.exit(1); }

const slug = T.slugify(c.name);
const siteDir = path.join(ROOT, "sites", slug);
fs.mkdirSync(path.join(siteDir, "img"), { recursive: true });

// Photos: the operator saves customer-supplied images into sites/<slug>/img/ before running this.
const photos = fs.readdirSync(path.join(siteDir, "img"))
  .filter(f => /\.(jpe?g|png|webp)$/i.test(f)).sort().slice(0, 6)
  .map(f => ({ src: "img/" + f, caption: "" }));

const cfg = { ...c, photos, formEmail: process.argv.includes("--preview") ? "" : order.email, legal: c.legal || "" };
const htmlOut = T.buildSite(cfg, { placeholders: false, banner: process.argv.includes("--preview") ? "PREVIEW · not live yet" : "" });
fs.writeFileSync(path.join(siteDir, "index.html"), htmlOut);

let standalone = null;
if (order.domain) {
  const dom = String(order.domain).toLowerCase().replace(/^https?:\/\//, "").replace(/\/.*$/, "");
  if (/^[a-z0-9-]+(\.[a-z0-9-]+)+$/.test(dom)) {
    standalone = path.join(ROOT, "ops/out", slug);
    fs.mkdirSync(path.join(standalone, "img"), { recursive: true });
    fs.writeFileSync(path.join(standalone, "index.html"), htmlOut);
    fs.writeFileSync(path.join(standalone, "CNAME"), dom + "\n");
    for (const p of photos) fs.copyFileSync(path.join(siteDir, p.src), path.join(standalone, p.src));
  }
}
console.log(JSON.stringify({ ok: true, order_id: order.order_id, slug, site: `sites/${slug}/`, photos: photos.length, standalone }, null, 2));
