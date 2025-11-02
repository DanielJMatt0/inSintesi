import apiClient from "./client"
import type {Team, CreateTeamBody, UpdateTeamBody, User} from "@/api/types.ts";

/**
 * List all teams belonging to the current user.
 */
export async function listTeams(): Promise<Team[]> {
    const { data } = await apiClient.get<Team[]>("/team/")
    return data
}

/**
 * Create a new team.
 */
export async function createTeam(body: CreateTeamBody): Promise<Team> {
    const { data } = await apiClient.post("/team/", body)
    return data
}

/**
 * Retrieve a specific team by its ID.
 */
export async function getTeam(teamId: number): Promise<Team> {
    const { data } = await apiClient.get(`/team/${teamId}`)
    return data
}

/**
 * Update an existing team.
 */
export async function updateTeam(
    teamId: number,
    body: UpdateTeamBody
): Promise<Team> {
    const { data } = await apiClient.put(`/team/${teamId}`, body)
    return data
}

/**
 * Delete a team by its ID.
 */
export async function deleteTeam(teamId: number): Promise<void> {
    await apiClient.delete(`/team/${teamId}`)
}

/**
 * List all users from a specific team (owned by the logged-in team lead).
 */
export async function listUsersFromTeam(teamId: number): Promise<User[]> {
    const { data } = await apiClient.get(`/user/team/${teamId}`)
    return data
}

export async function assignUsersToTeam(id: number, users_ids: number[]) {
    const response = await apiClient.put(`/team/${id}`, { users_ids })
    return response.data
}