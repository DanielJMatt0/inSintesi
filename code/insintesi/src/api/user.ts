import apiClient from "./client"
import type {
    CreateUserBody,
    UpdateUserBody,
    User
} from "./types.ts";


/**
 * List all users for the current logged-in user.
 */
export async function listUsers(): Promise<User[]> {
    const { data } = await apiClient.get("/user/")
    return data
}

/**
 * Create a new user.
 */
export async function createUser(body: CreateUserBody): Promise<User> {
    const { data } = await apiClient.post("/user/", body)
    return data
}

/**
 * Get a single user by its ID.
 */
export async function getUser(userId: number): Promise<User> {
    const { data } = await apiClient.get(`/user/${userId}`)
    return data
}

/**
 * Update an existing user by its ID.
 */
export async function updateUser(
    userId: number,
    body: UpdateUserBody
): Promise<User> {
    const { data } = await apiClient.put(`/user/${userId}`, body)
    return data
}

/**
 * Delete a user by its ID.
 */
export async function deleteUser(userId: number): Promise<void> {
    await apiClient.delete(`/user/${userId}`)
}
