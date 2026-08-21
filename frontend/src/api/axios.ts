import axios from "axios";

const API = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "/api",
  headers: {
    "Content-Type": "application/json",
  },
});

API.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("token");
    if (token) {
      config.headers.Authorization = `Token ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// ---- OFFLINE CACHE ----
const CACHE_PREFIX = "mobi_cache_";
const QUEUE_KEY = "mobi_offline_queue";

function cacheGet(url: string, data: any) {
  try {
    localStorage.setItem(CACHE_PREFIX + url, JSON.stringify(data));
  } catch {}
}

function getCached(url: string): any | null {
  try {
    const raw = localStorage.getItem(CACHE_PREFIX + url);
    return raw ? JSON.parse(raw) : null;
  } catch {
    return null;
  }
}

function queueWrite(config: any) {
  try {
    const queue = JSON.parse(localStorage.getItem(QUEUE_KEY) || "[]");
    queue.push({
      url: config.url,
      method: config.method,
      data: config.data,
      headers: config.headers,
      timestamp: Date.now(),
    });
    localStorage.setItem(QUEUE_KEY, JSON.stringify(queue));
  } catch {}
}

async function syncQueue() {
  const queue = JSON.parse(localStorage.getItem(QUEUE_KEY) || "[]");
  if (!queue.length) return;
  const remaining: any[] = [];
  for (const item of queue) {
    try {
      await axios({
        url: item.url.startsWith("http") ? item.url : (import.meta.env.VITE_API_URL || "/api") + item.url,
        method: item.method,
        data: item.data,
        headers: item.headers,
      });
    } catch {
      remaining.push(item);
    }
  }
  localStorage.setItem(QUEUE_KEY, JSON.stringify(remaining));
}

// Listen for reconnection
let wasOffline = !navigator.onLine;
window.addEventListener("online", () => {
  wasOffline = false;
  syncQueue();
});
window.addEventListener("offline", () => {
  wasOffline = true;
});

// Response interceptor: cache GETs, queue writes when offline
API.interceptors.response.use(
  (response) => {
    if (response.config.method === "get") {
      cacheGet(response.config.url || "", response.data);
    }
    return response;
  },
  (error) => {
    const config = error.config;
    if (!navigator.onLine && config && config.method !== "get") {
      queueWrite(config);
      return Promise.resolve({ data: { offline: true, queued: true } });
    }
    if (!navigator.onLine && config && config.method === "get") {
      const cached = getCached(config.url || "");
      if (cached) {
        return Promise.resolve({ data: cached, cached: true });
      }
    }
    return Promise.reject(error);
  }
);

export default API;
