"""
Calls Gemini Vision to identify the sketched object and plan its
illustration/animation. Falls back to a small rule-based classifier
(using the OpenCV shape stats) when no GEMINI_API_KEY is set, so the
whole app is runnable and demoable before you add your key.
"""
import json
import base64
import google.generativeai as genai

from app.core.config import get_settings
from app.models.schemas import ShapeStats, DetectionResult

SUPPORTED_OBJECTS = [
    "human", "tree", "mountain", "sun", "moon", "house", "car", "airplane",
    "bird", "river", "road", "flower", "cloud", "castle", "robot", "rocket",
    "dragon", "cat", "dog",
]

PROMPT_TEMPLATE = """You are the vision engine of a sketch-to-animation app.
Look at this hand-drawn sketch and respond ONLY with strict JSON, no markdown
fences, matching this schema exactly:

{{
  "object_type": one of {objects},
  "confidence": float 0-1,
  "suggested_style": short style name (e.g. "Cartoon Sketch", "Studio Ghibli Inspired"),
  "suggested_colors": array of 3-5 hex color strings,
  "suggested_animations": array of 2-5 short animation names (e.g. "walk", "blink", "wave"),
  "scene_description": one short sentence describing what the whole scene is doing
}}

Shape stats from OpenCV preprocessing (for extra context): {stats}
"""


def _settings():
    return get_settings()


def analyze_sketch(image_bytes: bytes, stats: ShapeStats) -> DetectionResult:
    settings = _settings()
    if settings.mock_mode:
        return _mock_analyze(stats)

    genai.configure(api_key=settings.gemini_api_key)
    model = genai.GenerativeModel(settings.gemini_model)

    prompt = PROMPT_TEMPLATE.format(objects=SUPPORTED_OBJECTS, stats=stats.model_dump())
    image_part = {"mime_type": "image/png", "data": image_bytes}

    try:
        response = model.generate_content([prompt, image_part])
        text = response.text.strip()
        # Strip accidental markdown fences
        if text.startswith("```"):
            text = text.strip("`")
            text = text.split("\n", 1)[1] if "\n" in text else text
            if text.lower().startswith("json"):
                text = text[4:]
        data = json.loads(text)
        return DetectionResult(
            object_type=data.get("object_type", "unknown"),
            confidence=float(data.get("confidence", 0.5)),
            suggested_style=data.get("suggested_style", "Cartoon Sketch"),
            suggested_colors=data.get("suggested_colors", ["#38bdf8", "#a855f7", "#0f172a"]),
            suggested_animations=data.get("suggested_animations", ["float"]),
            scene_description=data.get("scene_description", ""),
            source="gemini",
        )
    except Exception as exc:  # network / parsing / quota issues
        fallback = _mock_analyze(stats)
        fallback.scene_description = f"(Gemini call failed, used fallback: {exc})"
        return fallback


def _mock_analyze(stats: ShapeStats) -> DetectionResult:
    """Rule-based guess using bounding box aspect ratio + contour density,
    used only when no API key is configured or the API call fails."""
    ar = stats.aspect_ratio
    contours = stats.contour_count

    if ar < 0.6:
        obj, style, anims = "human", "Cartoon Sketch", ["walk", "wave", "blink"]
    elif ar > 2.2:
        obj, style, anims = "river", "Watercolor", ["flow", "ripple"]
    elif contours > 40:
        obj, style, anims = "tree", "Studio Ghibli Inspired", ["leaves_sway", "wind"]
    elif 0.6 <= ar <= 1.3:
        obj, style, anims = "sun", "Minimal", ["glow", "rotate"]
    else:
        obj, style, anims = "house", "Children Book", ["smoke_chimney", "window_glow"]

    return DetectionResult(
        object_type=obj,
        confidence=0.55,
        suggested_style=style,
        suggested_colors=["#38bdf8", "#a855f7", "#f8fafc", "#0f172a"],
        suggested_animations=anims,
        scene_description=f"A simple {obj} scene (mock detection - add GEMINI_API_KEY for real analysis).",
        source="mock",
    )
