import { defineStore } from "pinia"
import { login, refreshToken } from "@/api/auth"
import type { AuthResponse } from "@/api/types"

export const useAuthStore = defineStore("auth", {
  state: () => ({
    accessToken: localStorage.getItem("accessToken") || "",
    refreshToken: localStorage.getItem("refreshToken") || "",
  }),

  getters: {
    /**
     * True if an access token exists
     */
    isAuthenticated: (state) => !!state.accessToken,
  },

  actions: {
    /**
     * Log in and save the tokens
     */
    async login(username: string, password: string) {
      const data: AuthResponse = await login(username, password)

      this.accessToken = data.access_token
      this.refreshToken = data.refresh_token

      localStorage.setItem("accessToken", this.accessToken)
      localStorage.setItem("refreshToken", this.refreshToken)
    },

    /**
     * Update the access token using the refresh token
     */
    async refreshAccessToken(): Promise<string> {
      if (!this.refreshToken) throw new Error("Missing refresh token")

      const data: AuthResponse = await refreshToken(this.refreshToken)
      this.accessToken = data.access_token
      localStorage.setItem("accessToken", this.accessToken)
      return this.accessToken
    },

    /**
     * Logout
     */
    logout() {
      this.accessToken = ""
      this.refreshToken = ""
      localStorage.removeItem("accessToken")
      localStorage.removeItem("refreshToken")
    },

    /**
     * Check if the user is authenticated (alias getter)
     */
    hasValidToken(): boolean {
      return !!this.accessToken
    },
  },
})
