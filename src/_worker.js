// NOTE: having _worker.js at the site root puts Cloudflare Pages in
// "Advanced Mode" — the platform's automatic src/_redirects handling is
// bypassed for every request, so any 301s needed by the site must be
// applied explicitly here before falling through to static asset serving.
const PAGE_REDIRECTS = {
  "/departments/icu": "/departments/icu-critical-care/",
  "/departments/icu/": "/departments/icu-critical-care/"
};

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    // Redirect the apex domain to the canonical www host, preserving path and query.
    if (url.hostname === "dhshospitals.com") {
      url.hostname = "www.dhshospitals.com";
      return Response.redirect(url.toString(), 301);
    }

    const target = PAGE_REDIRECTS[url.pathname];
    if (target) {
      url.pathname = target;
      return Response.redirect(url.toString(), 301);
    }

    return env.ASSETS.fetch(request);
  }
};
