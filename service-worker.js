const CACHE_NAME = 'noteme-v1';
const STATIC_ASSETS = [
  '/',
  '/index.html',
  '/app.min.js',
  '/style.min.css',
  '/icons/icon-192.png',
  '/icons/icon-512.png'
];

// 安装时缓存核心资源
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(STATIC_ASSETS);
    }).then(() => {
      return self.skipWaiting();
    })
  );
});

// 激活时清理旧缓存
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames
          .filter((name) => name !== CACHE_NAME)
          .map((name) => caches.delete(name))
      );
    }).then(() => {
      return self.clients.claim();
    })
  );
});

// 网络优先的缓存策略
self.addEventListener('fetch', (event) => {
  const { request } = event;

  // 跳过非 GET 请求和 chrome-extension 请求
  if (request.method !== 'GET' || request.url.startsWith('chrome-extension://')) {
    return;
  }

  event.respondWith(
    fetch(request)
      .then((networkResponse) => {
        // 成功获取网络响应，更新缓存
        if (networkResponse && networkResponse.status === 200) {
          const responseClone = networkResponse.clone();
          caches.open(CACHE_NAME).then((cache) => {
            cache.put(request, responseClone);
          });
        }
        return networkResponse;
      })
      .catch(() => {
        // 网络失败，回退到缓存
        return caches.match(request).then((cachedResponse) => {
          if (cachedResponse) {
            return cachedResponse;
          }
          // 缓存也没有，返回离线页面或空响应
          return new Response('Offline', {
            status: 503,
            statusText: 'Service Unavailable',
            headers: { 'Content-Type': 'text/plain' }
          });
        });
      })
  );
});
