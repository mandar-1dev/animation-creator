import axios from "axios";
import type { AnalyzeResponse } from "../types";

const API_BASE = import.meta.env.VITE_API_URL || "http://localhost:8123/api";

export async function analyzeSketch(imageDataUrl: string): Promise<AnalyzeResponse> {
  const { data } = await axios.post<AnalyzeResponse>(`${API_BASE}/analyze-sketch`, {
    image: imageDataUrl,
  });
  return data;
}

export async function animateWithPrompt(objectType: string, style: string, instruction: string) {
  const { data } = await axios.post(`${API_BASE}/animate-prompt`, {
    object_type: objectType,
    style,
    instruction,
  });
  return data as { animation_svg: string; applied_animations: string[] };
}

export async function checkHealth() {
  const { data } = await axios.get(`${API_BASE}/health`);
  return data as { status: string; mock_mode: boolean };
}
