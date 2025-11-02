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
  console.log(payload)
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
 * Get a specific question
 */
export async function getQuestionType(question_id: number): Promise<any> {
  const { data } = await apiClient.get(`/question/type/${question_id}`)
  return data
}

/**
 * Delete a question
 */
export async function deleteQuestion(question_id: number): Promise<void> {
  await apiClient.delete(`/question/${question_id}`)
}

/**
 * Delete a question
 */
export async function getQuestionInformation(
  question_id: number
): Promise<QuestionInformation> {
  const { data } = await apiClient.get<QuestionInformation>(
    `/question/answer-counter/${question_id}`
  )
  return data
}