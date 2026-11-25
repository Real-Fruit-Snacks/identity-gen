const VERSION = "1.13.0";
const CACHE = "identity-gen-v2.1.1-" + VERSION;
const ASSETS = ["./", "./index.html", "./manifest.json", "./icon.svg", "./favicon.ico", "./icons/apple-touch-icon.png", "./icons/icon-192.png", "./icons/icon-512.png", "./icons/icon-maskable-512.png",
  "./fonts/big-shoulders-stencil-latin-ext.woff2", "./fonts/big-shoulders-stencil-latin.woff2",
  "./fonts/albert-sans-latin-ext.woff2", "./fonts/albert-sans-latin.woff2",
  "./fonts/azeret-mono-latin-ext.woff2", "./fonts/azeret-mono-latin.woff2"];

self.addEventListener("install", (event) => {
  event.waitUntil(caches.open(CACHE).then((c) => c.addAll(ASSETS)));   // wait: the page offers the update and asks us to take over
});

self.addEventListener("activate", (event) => {
  event.waitUntil(caches.keys().then((keys) => Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k)))).then(() => self.clients.claim()));
});

self.addEventListener("message", (event) => { if (event.data === "SKIP_WAITING") self.skipWaiting(); });

// Same-origin requests: serve from the network when available and refresh the cache; fall back to the cache offline.
// Only successful responses are cached; for an error (a 404 or 503) the cached copy is served when there is one.
// Cross-origin requests (illustrated avatars, photo sources) are left alone.
self.addEventListener("fetch", (event) => {
  const url = new URL(event.request.url);
  if (url.origin !== location.origin || event.request.method !== "GET") return;
  event.respondWith(
    fetch(event.request).then((res) => {
      if (res.ok) { const copy = res.clone(); caches.open(CACHE).then((c) => c.put(event.request, copy)); return res; }
      return res.status >= 400 ? caches.match(event.request).then((hit) => hit || res) : res;
    }).catch(() => caches.match(event.request).then((hit) => hit || caches.match("./index.html")))
  );
});
