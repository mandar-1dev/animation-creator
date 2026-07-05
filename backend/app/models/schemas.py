from pydantic import BaseModel
from typing import Optional


class ShapeStats(BaseModel):
    contour_count: int
    stroke_bbox: list[int]  # x, y, w, h
    fill_ratio: float
    aspect_ratio: float


class DetectionResult(BaseModel):
    object_type: str
    confidence: float
    suggested_style: str
    suggested_colors: list[str]
    suggested_animations: list[str]
    scene_description: str
    source: str  # "gemini" or "mock"


class AnalyzeResponse(BaseModel):
    shape_stats: ShapeStats
    detection: DetectionResult
    illustration_svg: str
    animation_svg: str


class AnimatePromptRequest(BaseModel):
    object_type: str
    style: str
    instruction: str  # e.g. "make it dance", "add rain"
