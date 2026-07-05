from fastapi import APIRouter, HTTPException, Body
from pydantic import BaseModel

from app.vision.preprocess import decode_base64_image, analyze_strokes, encode_preview_png
from app.ai.gemini_client import analyze_sketch
from app.ai.illustration_generator import generate_illustration_svg
from app.ai.animation_planner import build_animated_svg
from app.models.schemas import AnalyzeResponse, AnimatePromptRequest
from app.core.config import get_settings

router = APIRouter()


class SketchPayload(BaseModel):
    image: str  # data URL from the canvas


@router.get("/health")
def health():
    settings = get_settings()
    return {"status": "ok", "mock_mode": settings.mock_mode}


@router.post("/analyze-sketch", response_model=AnalyzeResponse)
def analyze(payload: SketchPayload = Body(...)):
    if not payload.image:
        raise HTTPException(400, "No image data provided")

    try:
        bgr = decode_base64_image(payload.image)
    except Exception as exc:
        raise HTTPException(400, f"Could not decode image: {exc}")

    stats = analyze_strokes(bgr)
    if stats.fill_ratio == 0.0:
        raise HTTPException(422, "Canvas looks empty - draw something first")

    preview_bytes = encode_preview_png(bgr)
    detection = analyze_sketch(preview_bytes, stats)
    illustration_svg = generate_illustration_svg(detection.object_type, detection.suggested_colors)
    animated_svg = build_animated_svg(illustration_svg, detection.suggested_animations)

    return AnalyzeResponse(
        shape_stats=stats,
        detection=detection,
        illustration_svg=illustration_svg,
        animation_svg=animated_svg,
    )


@router.post("/animate-prompt")
def animate_with_prompt(req: AnimatePromptRequest):
    """Re-animate an already-detected object with a free-text instruction,
    e.g. 'make it dance' / 'add rain'. Maps the instruction to the closest
    entries in the animation library (rule-based; Gemini refinement can be
    layered in later)."""
    from app.ai.illustration_generator import generate_illustration_svg
    from app.ai.animation_planner import ALIASES, ANIMATION_LIBRARY

    text = req.instruction.lower()
    matched = [key for key in ANIMATION_LIBRARY if key.replace("_", " ") in text]
    for phrase, key in ALIASES.items():
        if phrase in text:
            matched.append(key)
    if not matched:
        matched = ["float"]

    illustration_svg = generate_illustration_svg(req.object_type, ["#38bdf8", "#a855f7", "#0f172a", "#f8fafc"])
    animated_svg = build_animated_svg(illustration_svg, matched)
    return {"animation_svg": animated_svg, "applied_animations": matched}
