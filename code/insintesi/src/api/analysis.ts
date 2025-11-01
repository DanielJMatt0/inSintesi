import apiClient from "./client";
import type { AnalyzeResponse } from "./types";

export async function runAnalysis(questionId: number): Promise<AnalyzeResponse> {
  const { data } = await apiClient.post<AnalyzeResponse>(`/analyze/${questionId}`);
  return data;
}

export async function updateAnalysis(questionId: number): Promise<AnalyzeResponse> {
  const { data } = await apiClient.put<AnalyzeResponse>(`/analyze/${questionId}`);
  return data;
}

export async function getReport(questionId: number): Promise<Record<string, any>> {
  const { data } = await apiClient.get(`/analyze/report/${questionId}`);
  return data;
}

export async function healthCheck(): Promise<any> {
  const { data } = await apiClient.get("/");
  return data;
}
