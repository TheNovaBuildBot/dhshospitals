export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    // Redirect the apex domain to the canonical www host, preserving path and query.
    if (url.hostname === "dhshospitals.com") {
      url.hostname = "www.dhshospitals.com";
      return Response.redirect(url.toString(), 301);
    }
    return env.ASSETS.fetch(request);
  }
};
