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
