import { defineStore } from "pinia";
import apiClient from "../api/client";
import type { AuthResponse } from "../api/types";

export const useAuthStore = defineStore("auth", {
  state: () => ({
    accessToken: localStorage.getItem("accessToken") || "",
    refreshToken: localStorage.getItem("refreshToken") || "",
  }),

  actions: {
    async login(username: string, password: string) {
      const params = new URLSearchParams();
      params.append("grant_type", "");
      params.append("username", username);
      params.append("password", password);
      params.append("scope", "");
      params.append("client_id", "");
      params.append("client_secret", "");

      const { data } = await apiClient.post<AuthResponse>("/auth/token", params, {
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
      });

      this.accessToken = data.access_token;
      this.refreshToken = data.refresh_token;
      localStorage.setItem("accessToken", this.accessToken);
      localStorage.setItem("refreshToken", this.refreshToken);
    },

    async refreshAccessToken(): Promise<string> {
      const params = new URLSearchParams();
      params.append("refresh_token", this.refreshToken);

      const { data } = await apiClient.post<AuthResponse>("/auth/refresh_token", params, {
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
      });

      this.accessToken = data.access_token;
      localStorage.setItem("accessToken", this.accessToken);
      return this.accessToken;
    },

    logout() {
      this.accessToken = "";
      this.refreshToken = "";
      localStorage.removeItem("accessToken");
      localStorage.removeItem("refreshToken");
    },
  },
});
