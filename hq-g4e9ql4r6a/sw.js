// Nidi HQ service worker (2026-11-18): only for the push notifications
// hq-notify sends (a new nidi, the other home in, a payment). No caching.
self.addEventListener('install', function () { self.skipWaiting(); });
self.addEventListener('activate', function (e) { e.waitUntil(self.clients.claim()); });
self.addEventListener('push', function (e) {
  var d = {};
  try { d = e.data ? e.data.json() : {}; } catch (x) { d = { title: e.data ? e.data.text() : 'Nidi HQ' }; }
  e.waitUntil(self.registration.showNotification(d.title || 'Nidi HQ', {
    body: d.body || '',
    tag: d.tag || undefined,
    icon: '/assets/press/nidi-app-icon-1024.png',
    data: { url: d.url || '/hq-g4e9ql4r6a/' }
  }));
});
self.addEventListener('notificationclick', function (e) {
  e.notification.close();
  var url = (e.notification.data && e.notification.data.url) || '/hq-g4e9ql4r6a/';
  e.waitUntil(self.clients.matchAll({ type: 'window', includeUncontrolled: true }).then(function (list) {
    for (var i = 0; i < list.length; i++) { if (list[i].url.indexOf('/hq-g4e9ql4r6a/') >= 0 && 'focus' in list[i]) return list[i].focus(); }
    return self.clients.openWindow(url);
  }));
});
