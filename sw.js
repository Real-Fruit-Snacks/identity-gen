const VERSION = "1.9.0";
const CACHE = "identity-gen-" + VERSION;
const ASSETS = ["./", "./index.html", "./manifest.json", "./icons/icon-192.png", "./icons/icon-512.png", "./icons/icon-maskable-512.png"];

self.addEventListener("install", (event) => {
  event.waitUntil(caches.open(CACHE).then((c) => c.addAll(ASSETS)));   // wait: the page offers the update and asks us to take over
});

self.addEventListener("activate", (event) => {
  event.waitUntil(caches.keys().then((keys) => Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k)))).then(() => self.clients.claim()));
});

self.addEventListener("message", (event) => { if (event.data === "SKIP_WAITING") self.skipWaiting(); });

// Same-origin requests: serve from the network when available and refresh the cache; fall back to the cache offline.
// Cross-origin requests (illustrated avatars, photo sources) are left alone.
self.addEventListener("fetch", (event) => {
  const url = new URL(event.request.url);
  if (url.origin !== location.origin || event.request.method !== "GET") return;
  event.respondWith(
    fetch(event.request).then((res) => { const copy = res.clone(); caches.open(CACHE).then((c) => c.put(event.request, copy)); return res; })
      .catch(() => caches.match(event.request).then((hit) => hit || caches.match("./index.html")))
  );
});
