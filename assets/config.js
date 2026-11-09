/* Owner settings. The ONLY file that needs editing at setup time.
   Leave a value as "" until it exists; the site degrades gracefully. */
window.CALLOUT_CONFIG = {
  SITE_URL: "https://calloutwebhello-ops.github.io",   // change if a custom domain is added
  ORDER_EMAIL: "calloutweb.hello@gmail.com",       // receives orders (and fallback emails)
  WEB3FORMS_KEY: "b06b2d6e-7ea5-473f-8744-b29bd6b77c82", // Web3Forms access key. Public by design (it only lets people SEND to our inbox)
  LEADS_CC: "calloutweb.hello+leads@gmail.com",    // client quote forms CC this address so we can count enquiries for monthly reports (disclosed in terms/privacy)
  // LIVE Stripe Payment Links (real money). Each link carries ?client_reference_id=<order id>.
  PLANS: {
    starter: { name: "Starter", price: 19, period: "month", link: "https://buy.stripe.com/6oU14m24LfuvbJEe5VgIo02" },
    pro:     { name: "Pro",     price: 39, period: "month", link: "https://buy.stripe.com/28E6oG8t9befaFA5zpgIo03" },
    own:     { name: "Own it",  price: 249, period: "one-off", link: "https://buy.stripe.com/5kQ00i38Pgyz2945zpgIo00" }
  },
  // Retired: £20/month Care Plan link (deactivated in Stripe), test-mode links in the Stripe sandbox.
  OUTREACH_APPROVED: true,                          // preview-first B2B outreach (ops/outreach.py). Approved by the owner on 9 Nov 2026: max 10 sends per weekday, 100 total for the first campaign.
  DEMO_MODE: false                                 // true = no real submissions (used for claude.ai preview copy)
};
