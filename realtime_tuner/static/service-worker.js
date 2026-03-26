const CACHE_NAME = 'tuner-v1';
const ASSETS = [
  '/',
  '/index.html',
  // Thêm các file CSS/JS khác của cậu vào đây
];

self.addEventListener('install', (e) => {
  e.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(ASSETS))
  );
});

self.addEventListener('fetch', (e) => {
  e.respondWith(
    caches.match(e.request).then((res) => res || fetch(e.request))
  );
});