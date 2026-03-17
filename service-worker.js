// ChennaiOpp Service Worker
// Enables offline support and faster loading

const CACHE_NAME = 'chennaiopp-v1';
const CACHED_URLS = [
  '/app.html',
  '/manifest.json',
];

// Install — cache important files
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => {
      console.log('ChennaiOpp: Caching app files');
      return cache.addAll(CACHED_URLS);
    })
  );
});

// Activate — clean old caches
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames
          .filter(name => name !== CACHE_NAME)
          .map(name => caches.delete(name))
      );
    })
  );
});

// Fetch — serve from cache, fallback to network
self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request).then(response => {
      // Return cached version or fetch from network
      return response || fetch(event.request);
    }).catch(() => {
      // If offline and not cached, show offline page
      return caches.match('/app.html');
    })
  );
});

// Push notifications
self.addEventListener('push', event => {
  const data = event.data ? event.data.json() : {};
  const title = data.title || 'New Opportunity in Chennai!';
  const options = {
    body: data.body || 'A new educational opportunity is available. Tap to view!',
    icon: '/icon-192.png',
    badge: '/icon-192.png',
    vibrate: [100, 50, 100],
    data: { url: data.url || '/app.html' }
  };

  event.waitUntil(
    self.registration.showNotification(title, options)
  );
});

// Notification click — open app
self.addEventListener('notificationclick', event => {
  event.notification.close();
  event.waitUntil(
    clients.openWindow(event.notification.data.url)
  );
});
