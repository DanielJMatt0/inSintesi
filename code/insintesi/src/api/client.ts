import axios from "axios";
import { useAuthStore } from "../stores/authStore";

const apiClient = axios.create({
  baseURL: "http://localhost:8000",
  timeout: 10000,
});

let isRefreshing = false;
let refreshSubscribers: ((token: string) => void)[] = [];

function subscribeTokenRefresh(cb: (token: string) => void) {
  refreshSubscribers.push(cb);
}

function onRefreshed(token: string) {
  refreshSubscribers.forEach((cb) => cb(token));
  refreshSubscribers = [];
}

apiClient.interceptors.request.use((config) => {
  const auth = useAuthStore();
  if (auth.accessToken) {
    config.headers = config.headers || {};
    config.headers.Authorization = `Bearer ${auth.accessToken}`;
  }
  return config;
});

apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const auth = useAuthStore();
    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      if (isRefreshing) {
        return new Promise((resolve) => {
          subscribeTokenRefresh((token) => {
            originalRequest.headers.Authorization = `Bearer ${token}`;
            resolve(apiClient(originalRequest));
          });
        });
      }

      originalRequest._retry = true;
      isRefreshing = true;

      try {
        const newToken = await auth.refreshAccessToken();
        isRefreshing = false;
        onRefreshed(newToken);
        originalRequest.headers.Authorization = `Bearer ${newToken}`;
        return apiClient(originalRequest);
      } catch (err) {
        isRefreshing = false;
        auth.logout();
        return Promise.reject(err);
      }
    }

    return Promise.reject(error);
  }
);

export default apiClient;
