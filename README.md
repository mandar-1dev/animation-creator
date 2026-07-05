# AI Animation Creator

**Sketch-to-AI Animation System** — draw a rough sketch, and the app identifies what it is, redraws it as clean vector art, and animates it in real time.

```
You draw  →  OpenCV analyzes strokes  →  Gemini Vision identifies the object
→  procedural SVG illustrator redraws it  →  CSS animation engine brings it to life
```

Built with FastAPI (Python) + React/TypeScript, containerized with Docker.

---

## Stack

| Layer | Tech |
|---|---|
| Backend | FastAPI, OpenCV, Google Gemini API |
| Frontend | React, TypeScript, Vite, TailwindCSS, Framer Motion |
| Illustration | Procedural SVG templates (18 object types) |
| Animation | CSS keyframe engine, mapped from Gemini's suggestions |
| Deployment | Docker, Docker Compose |

---

## Prerequisites

- Docker Desktop **or** Python 3.11+ and Node 20+ installed locally
- A free [Gemini API key](https://aistudio.google.com/apikey)

---

## Run with Docker (recommended)

1. Clone and enter the project:
   ```bash
   git clone https://github.com/mandar-1dev/animation-creator.git
   cd animation-creator
   ```

2. Create a `.env` file in the project root (same folder as `docker-compose.yml`):
   ```
   GEMINI_API_KEY=your_actual_key_here
   ```

3. Build and start:
   ```bash
   docker compose up --build
   ```

4. Open the app:
   - Frontend → http://localhost:5173
   - Backend API docs → http://localhost:8123/docs

5. Verify Gemini is actually connected (not running in fallback mode):
   ```bash
   curl http://localhost:8123/api/health
   ```
   Should return `{"status":"ok","mock_mode":false}`. If `mock_mode` is `true`, your `.env` isn't being picked up — check it's named exactly `.env` (no `.txt`) and sits next to `docker-compose.yml`.

**Stop the app:**
```bash
docker compose down
```

**Restart after the first build** (no need to rebuild every time):
```bash
docker compose up
```

---

## Run locally without Docker

**Backend**
```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
cp .env.example .env      # Windows: copy .env.example .env
# edit .env -> GEMINI_API_KEY=your_key_here

uvicorn app.main:app --reload --port 8123
```

**Frontend** (new terminal)
```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173.

---

## How it works

1. **Draw** on the canvas (mouse, touch, or stylus)
2. Click **Analyze & Animate**
3. **Backend pipeline** (`/api/analyze-sketch`):
   - OpenCV: grayscale → blur → Canny edge detection → contours → bounding box / fill ratio / aspect ratio
   - Gemini Vision: sketch + shape stats → object type, confidence, style, color palette, suggested animations
   - Procedural SVG generator redraws the object using Gemini's palette
   - CSS animation engine wires up motion (walk, wave, blink, fly, flow, launch, etc.) based on Gemini's suggestions
4. **Prompt editing**: type something like `"make it dance"` or `"add rain"` and hit Apply to re-animate without redrawing

Supported objects: human, tree, mountain, sun, moon, house, car, airplane, bird, river, flower, cloud, castle, robot, rocket, dragon, cat, dog, road.

---

## Mock mode

Without a Gemini key, `/api/analyze-sketch` still works end-to-end using a rule-based fallback (bounding-box aspect ratio + contour count), so the full pipeline is testable before you wire in a key. Check `detection.source` in any response — `"gemini"` means real AI analysis, `"mock"` means fallback.

---

## Project structure

```
animation-creator/
├── backend/
│   ├── app/
│   │   ├── main.py                        FastAPI entry point
│   │   ├── core/config.py                 Settings, mock-mode detection
│   │   ├── vision/preprocess.py           OpenCV sketch analysis
│   │   ├── ai/gemini_client.py             Gemini Vision + rule-based fallback
│   │   ├── ai/illustration_generator.py    Procedural SVG templates
│   │   ├── ai/animation_planner.py         CSS keyframe animation engine
│   │   ├── api/routes.py                   /api/analyze-sketch, /api/animate-prompt, /api/health
│   │   └── models/schemas.py               Pydantic request/response models
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── components/DrawingCanvas.tsx
│   │   ├── components/AnimationPreview.tsx
│   │   ├── components/DetectionPanel.tsx
│   │   ├── services/api.ts
│   │   └── App.tsx
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml
└── README.md
```

---

## API reference

| Endpoint | Method | Description |
|---|---|---|
| `/api/health` | GET | Server status + whether Gemini key is loaded |
| `/api/analyze-sketch` | POST | Send a base64 PNG, get back detection + illustration + animation |
| `/api/animate-prompt` | POST | Re-animate a detected object from free-text instruction |

Full interactive docs at `/docs` once the backend is running.

---

## Roadmap

- [ ] Real image-gen API (Gemini image models or Stable Diffusion) in place of procedural SVG
- [ ] Manim-based frame rendering for true MP4/GIF/MOV export
- [ ] Redis + Celery for async render jobs
- [ ] Multi-object "story mode" — combine several detected objects into one animated scene
- [ ] Voice input via Web Speech API

---

## Security note

`GEMINI_API_KEY` is read from `.env`, which is git-ignored by default. Never commit this file or paste your key into chats, issues, or commit messages — leaked keys get auto-revoked by Google within minutes.