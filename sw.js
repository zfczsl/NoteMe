const CACHE_NAME = 'noteme-v13';
const urlsToCache = [
  '/',
  '/daywise.html',
  '/manifest.json',
  '/index.html'
];

// 安装 Service Worker
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(urlsToCache))
      .then(() => self.skipWaiting())
  );
});

// 激活并清理旧缓存
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.filter(name => name !== CACHE_NAME)
          .map(name => caches.delete(name))
      );
    }).then(() => self.clients.claim())
  );
});

// 拦截请求，优先使用缓存
self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => {
        // 缓存有就返回，没有就请求网络
        return response || fetch(event.request);
      })
      .catch(() => {
        // 网络失败时返回离线页面
        if (event.request.mode === 'navigate') {
          return caches.match('/daywise.html');
        }
      })
  );
});
