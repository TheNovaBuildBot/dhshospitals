#!/usr/bin/env node
/**
 * IndexNow submission for DHS Multispecialty Hospital
 *
 * Reads the deployed sitemap.xml and submits every URL to the IndexNow
 * protocol endpoint at https://api.indexnow.org/indexnow. IndexNow notifies
 * participating search engines (Bing, Yandex, Naver, Seznam, and indirectly
 * other engines that consume IndexNow signals) that the URLs are fresh.
 *
 * Usage:
 *   node scripts/indexnow-submit.js
 *
 * Optional args:
 *   --sitemap=<url>    override the sitemap URL (default: live www site)
 *   --dry-run          print the payload but do not POST
 */

const HOST = "www.dhshospitals.com";
const KEY = "bbb7d3aa967d5f205f42f00cd9eaedc9";
const KEY_LOCATION = `https://${HOST}/${KEY}.txt`;

const args = process.argv.slice(2);
const sitemapUrl =
  args.find((a) => a.startsWith("--sitemap="))?.split("=")[1] ||
  `https://${HOST}/sitemap.xml`;
const dryRun = args.includes("--dry-run");

async function fetchSitemap(url) {
  const res = await fetch(url, { headers: { "User-Agent": "NovaBuildBot/IndexNow" } });
  if (!res.ok) throw new Error(`Failed to fetch sitemap: ${res.status} ${res.statusText}`);
  return await res.text();
}

function extractUrls(xml) {
  // Simple <loc>...</loc> extraction — sitemap.xml has no namespaces inside <loc>.
  const out = [];
  const re = /<loc>([^<]+)<\/loc>/g;
  let m;
  while ((m = re.exec(xml)) !== null) {
    const u = m[1].trim();
    if (u.startsWith(`https://${HOST}/`)) out.push(u);
  }
  return out;
}

async function submitToIndexNow(urls) {
  const payload = {
    host: HOST,
    key: KEY,
    keyLocation: KEY_LOCATION,
    urlList: urls,
  };

  if (dryRun) {
    console.log("DRY RUN — would POST:");
    console.log(JSON.stringify(payload, null, 2));
    return { status: 0, body: "dry-run" };
  }

  const res = await fetch("https://api.indexnow.org/indexnow", {
    method: "POST",
    headers: {
      "Content-Type": "application/json; charset=utf-8",
      "User-Agent": "NovaBuildBot/IndexNow",
    },
    body: JSON.stringify(payload),
  });
  const body = await res.text();
  return { status: res.status, body };
}

(async () => {
  console.log(`Sitemap: ${sitemapUrl}`);
  console.log(`Key location: ${KEY_LOCATION}`);

  const xml = await fetchSitemap(sitemapUrl);
  const urls = extractUrls(xml);
  console.log(`Found ${urls.length} URLs in sitemap.`);

  if (urls.length === 0) {
    console.error("No URLs to submit. Aborting.");
    process.exit(1);
  }

  const { status, body } = await submitToIndexNow(urls);
  console.log(`IndexNow responded: ${status}`);
  if (body) console.log(body);

  // IndexNow returns 200 (received) or 202 (accepted for processing) on success.
  // 400 = bad request, 403 = key invalid, 422 = URLs don't match host, 429 = rate limit.
  if (status === 200 || status === 202) {
    console.log("Success.");
  } else if (status >= 400) {
    console.error("Submission failed.");
    process.exit(1);
  }
})().catch((err) => {
  console.error("Error:", err.message);
  process.exit(1);
});
