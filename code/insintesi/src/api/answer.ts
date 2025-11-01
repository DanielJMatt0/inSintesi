import apiClient from "./client"
import type {
  AnswerResponse,
  QuestionResponse,
  CreateAnswerBody,
} from "./types"

/**
 * Retrieve the question associated with a public token (used by respondents).
 */
export async function getQuestionFromToken(
  token: string
): Promise<QuestionResponse> {
  const { data } = await apiClient.get(`/answer/question/${token}`)
  return data
}

/**
 * Send an answer (valid token, not used).
 */
export async function createAnswer(
  token: string,
  content: string
): Promise<AnswerResponse> {
  const payload: CreateAnswerBody = { content }
  const { data } = await apiClient.post(`/answer/${token}`, payload)
  return data
}

/**
 * Get a single response.
 */
export async function getAnswer(answerId: number): Promise<AnswerResponse> {
  const { data } = await apiClient.get(`/answer/${answerId}`)
  return data
}

/**
 * Delete a reply.
 */
export async function deleteAnswer(answerId: number): Promise<void> {
  await apiClient.delete(`/answer/${answerId}`)
}