"""
Real OpenCV pipeline: base64 PNG from the canvas -> grayscale -> blur ->
edge detection -> contour extraction -> basic shape statistics.

These stats are cheap, deterministic, and don't need any API key. They're
fed to Gemini (or the mock fallback) as extra context, and also used
standalone as a sanity check that a real drawing was received.
"""
import base64
import io
import cv2
import numpy as np
from PIL import Image

from app.models.schemas import ShapeStats


def decode_base64_image(data_url: str) -> np.ndarray:
    """Accepts a data URL (data:image/png;base64,....) or raw base64."""
    if "," in data_url:
        data_url = data_url.split(",", 1)[1]
    raw = base64.b64decode(data_url)
    img = Image.open(io.BytesIO(raw)).convert("RGBA")

    # Composite onto white background (canvas exports transparent PNGs)
    bg = Image.new("RGBA", img.size, (255, 255, 255, 255))
    composited = Image.alpha_composite(bg, img).convert("RGB")
    return cv2.cvtColor(np.array(composited), cv2.COLOR_RGB2BGR)


def analyze_strokes(bgr_image: np.ndarray) -> ShapeStats:
    gray = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 40, 120)

    contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    # Bounding box of all ink
    thresh = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)[1]
    ys, xs = np.where(thresh > 0)
    if len(xs) == 0:
        bbox = [0, 0, bgr_image.shape[1], bgr_image.shape[0]]
        fill_ratio = 0.0
    else:
        x, y, w, h = int(xs.min()), int(ys.min()), int(xs.max() - xs.min()), int(ys.max() - ys.min())
        bbox = [x, y, max(w, 1), max(h, 1)]
        fill_ratio = float(thresh.sum() / 255) / (bgr_image.shape[0] * bgr_image.shape[1])

    aspect = bbox[2] / bbox[3] if bbox[3] else 1.0

    return ShapeStats(
        contour_count=len(contours),
        stroke_bbox=bbox,
        fill_ratio=round(fill_ratio, 4),
        aspect_ratio=round(aspect, 3),
    )


def encode_preview_png(bgr_image: np.ndarray) -> bytes:
    ok, buf = cv2.imencode(".png", bgr_image)
    if not ok:
        raise ValueError("Could not encode preview image")
    return buf.tobytes()
