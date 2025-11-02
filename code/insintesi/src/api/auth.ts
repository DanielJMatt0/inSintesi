import apiClient from "./client";
import type { AuthResponse } from "./types";

/**
 * Login (matching the FastAPI OAuth2 form style)
 */
export async function login(username: string, password: string): Promise<AuthResponse> {
  const params = new URLSearchParams();
  params.append("username", username);
  params.append("password", password);

  const { data } = await apiClient.post<AuthResponse>("/auth/token", params, {
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
  });
  return data;
}

/**
 * Refresh the access token using a refresh token
 */
export async function refreshToken(refresh_token: string): Promise<AuthResponse> {
  const params = new URLSearchParams();
  params.append("refresh_token", refresh_token);

  const { data } = await apiClient.post<AuthResponse>("/auth/refresh-token", params, {
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
  });
  return data;
}

/**
 * Register a new team leader
 */
export async function registerTeamLead(payload: {
  name: string
  lastname: string
  email: string
  password: string
}): Promise<TeamLeadOut> {
  const { data } = await apiClient.post<TeamLeadOut>("/auth/register", payload, {
    headers: { "Content-Type": "application/json" },
  })
  return data
}