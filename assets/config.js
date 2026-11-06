/* Owner settings. The ONLY file that needs editing at setup time.
   Leave a value as "" until it exists; the site degrades gracefully. */
window.CALLOUT_CONFIG = {
  SITE_URL: "https://calloutwebhello-ops.github.io",   // change if a custom domain is added
  ORDER_EMAIL: "calloutweb.hello@gmail.com",       // receives orders (and fallback emails)
  WEB3FORMS_KEY: "",                               // Web3Forms access key. Public by design (it only lets people SEND to our inbox); restrict it to this domain in the Web3Forms dashboard
  // TEST MODE links (Stripe sandbox, no real money). Swap for live links before the site goes public.
  STRIPE_LAUNCH_LINK: "https://buy.stripe.com/test_8x26oH7WsfFeadY58U4Vy00",   // £249 Launch Site
  STRIPE_CARE_LINK: "https://buy.stripe.com/test_00weVdccI2Ss4TEcBm4Vy01",     // £20/month Care Plan
  LAUNCH_PRICE: 249,
  CARE_PRICE: 20,
  DEMO_MODE: false                                 // true = no real submissions (used for claude.ai preview copy)
};
