export interface ShapeStats {
  contour_count: number;
  stroke_bbox: number[];
  fill_ratio: number;
  aspect_ratio: number;
}

export interface DetectionResult {
  object_type: string;
  confidence: number;
  suggested_style: string;
  suggested_colors: string[];
  suggested_animations: string[];
  scene_description: string;
  source: "gemini" | "mock";
}

export interface AnalyzeResponse {
  shape_stats: ShapeStats;
  detection: DetectionResult;
  illustration_svg: string;
  animation_svg: string;
}
