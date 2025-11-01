import apiClient from "@/api/client"
import type {
  QuestionCreate,
  QuestionCreateResponse,
  QuestionResponse,
} from "@/api/types"

/**
 * Get all questions
 */
export async function getAllQuestions(): Promise<QuestionResponse[]> {
  const { data } = await apiClient.get<QuestionResponse[]>("/question/")
  return data
}

/**
 * Create a new question
 */
export async function createQuestion(payload: QuestionCreate): Promise<QuestionCreateResponse> {
  const { data } = await apiClient.post<QuestionCreateResponse>("/question/", payload)
  return data
}

/**
 * Get a specific question
 */
export async function getQuestionById(question_id: number): Promise<QuestionResponse> {
  const { data } = await apiClient.get<QuestionResponse>(`/question/${question_id}`)
  return data
}

/**
 * Delete a question
 */
export async function deleteQuestion(question_id: number): Promise<void> {
  await apiClient.delete(`/question/${question_id}`)
}
