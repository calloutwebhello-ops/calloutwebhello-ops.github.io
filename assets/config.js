/* Owner settings. The ONLY file that needs editing at setup time.
   Leave a value as "" until it exists; the site degrades gracefully. */
window.CALLOUT_CONFIG = {
  SITE_URL: "https://calloutwebhello-ops.github.io",   // change if a custom domain is added
  ORDER_EMAIL: "calloutweb.hello@gmail.com",       // receives orders (and fallback emails)
  WEB3FORMS_KEY: "b06b2d6e-7ea5-473f-8744-b29bd6b77c82",                               // Web3Forms access key. Public by design (it only lets people SEND to our inbox); restrict it to this domain in the Web3Forms dashboard
  // LIVE Stripe Payment Links (real money). Test-mode links: launch https://buy.stripe.com/test_8x26oH7WsfFeadY58U4Vy00 / care https://buy.stripe.com/test_00weVdccI2Ss4TEcBm4Vy01
  STRIPE_LAUNCH_LINK: "https://buy.stripe.com/5kQ00i38Pgyz2945zpgIo00",   // £249 Launch Site
  STRIPE_CARE_LINK: "https://buy.stripe.com/dRmbJ05gXfuv7to9PFgIo01",     // £20/month Care Plan
  LAUNCH_PRICE: 249,
  CARE_PRICE: 20,
  DEMO_MODE: false                                 // true = no real submissions (used for claude.ai preview copy)
};
