// Flipped by AMKAR: keeps the planner opening when there is no reception.
// Always asks the network first so updates show straight away, and falls back
// to the last copy saved on this device when the network is slow or missing.
const BUILD = "20261118105506";
const CACHE = "flipped-v1";
const SHELL = ["./", "pdf-lib.min.js", "manifest.webmanifest", "icon-192.png", "icon-512.png", "apple-touch-icon.png"];

self.addEventListener("install", (e) => {
  self.skipWaiting();
  e.waitUntil(caches.open(CACHE).then((c) => Promise.all(SHELL.map((u) => c.add(new Request(u, { cache: "no-cache" })).catch(() => {})))));
});

self.addEventListener("activate", (e) => {
  e.waitUntil(caches.keys().then((ks) => Promise.all(ks.filter((k) => k !== CACHE).map((k) => caches.delete(k)))).then(() => self.clients.claim()));
});

function cached(req) {
  return caches.match(req, { ignoreSearch: true }).then((m) => m || (req.mode === "navigate" ? caches.match("./") : undefined));
}

self.addEventListener("fetch", (e) => {
  const req = e.request;
  if (req.method !== "GET" || new URL(req.url).origin !== self.location.origin) return;
  e.respondWith(new Promise((resolve, reject) => {
    let done = false;
    const timer = setTimeout(() => {
      cached(req).then((m) => { if (m && !done) { done = true; resolve(m); } });
    }, 4000);
    fetch(req, { cache: "no-cache" }).then((res) => {
      clearTimeout(timer);
      if (res && res.ok) { const copy = res.clone(); caches.open(CACHE).then((c) => c.put(req, copy)).catch(() => {}); }
      if (!done) { done = true; resolve(res); }
    }).catch((err) => {
      clearTimeout(timer);
      if (done) return;
      cached(req).then((m) => { done = true; m ? resolve(m) : reject(err); });
    });
  }));
});
