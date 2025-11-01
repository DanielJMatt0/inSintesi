export interface AnalyzeResponse {
  id: string;
  question_type: string;
  topic: string;
  summary?: string | null;
  recommendation?: string | null;
  ai_thought?: string | null;
  created_at?: string | null;
  updated_at?: string | null;
  extra?: Record<string, any> | null;
}

export interface AuthResponse {
  access_token: string;
  refresh_token: string;
}

export interface ValidationError {
  loc: (string | number)[];
  msg: string;
  type: string;
}

// === ANSWER TYPES ===
export interface AnswerResponse {
  id: number
  content: string
  question_id: number
  created_at: string
}

export interface CreateAnswerBody {
  content: string
}

// === QUESTION TYPES ===
export interface QuestionResponse {
  id: number
  content: string
  created_at: string
  updated_at?: string | null
}

export interface QuestionCreate {
  content: string
  team_lead_id: number
  question_type_id: number
  token_type: string
  teams_ids: number[]
  users_ids?: number[] | null
  expires_at?: string | null
}

export interface QuestionCreateResponse {
  question: QuestionResponse
  tokens: string[]
}

export interface QuestionResponse {
  id: number
  content: string
  created_at: string
  updated_at?: string | null
}

export interface Team {
  id: number
  name: string
  members?: number[]
  created_at?: string
  updated_at?: string
}

export interface CreateTeamBody {
  name: string
}

export interface UpdateTeamBody {
  name?: string
}

export interface User {
  id: number
  name: string
  lastname: string
  email: string
  created_at?: string
  updated_at?: string
}

export interface CreateUserBody {
  name: string
  lastname: string
  email: string
}

export interface UpdateUserBody {
  name?: string
  lastname?: string
  email?: string
}