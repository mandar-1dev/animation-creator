import { useRef, useState } from "react";
import { motion } from "framer-motion";
import DrawingCanvas, { type DrawingCanvasHandle } from "./components/DrawingCanvas";
import AnimationPreview from "./components/AnimationPreview";
import DetectionPanel from "./components/DetectionPanel";
import { analyzeSketch, animateWithPrompt } from "./services/api";
import type { AnalyzeResponse } from "./types";

export default function App() {
  const canvasRef = useRef<DrawingCanvasHandle>(null);
  const [result, setResult] = useState<AnalyzeResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [prompt, setPrompt] = useState("");

  const handleAnalyze = async () => {
    setLoading(true);
    setError("");
    try {
      const dataUrl = canvasRef.current?.exportPNG() || "";
      const res = await analyzeSketch(dataUrl);
      setResult(res);
    } catch (e: any) {
      setError(e?.response?.data?.detail || "Something went wrong. Is the backend running?");
    } finally {
      setLoading(false);
    }
  };

  const handleClear = () => {
    canvasRef.current?.clear();
    setResult(null);
    setError("");
  };

  const handlePromptEdit = async () => {
    if (!result || !prompt.trim()) return;
    setLoading(true);
    try {
      const res = await animateWithPrompt(result.detection.object_type, result.detection.suggested_style, prompt);
      setResult({ ...result, animation_svg: res.animation_svg });
    } catch {
      setError("Could not update animation");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen px-4 py-8 md:px-10">
      <header className="max-w-6xl mx-auto mb-10 flex items-center justify-between">
        <div>
          <h1 className="text-2xl md:text-3xl font-bold tracking-tight">
            <span className="text-studio-cyan">AI</span> Animation Creator
          </h1>
          <p className="text-slate-500 text-sm mt-1">Sketch it. AI understands it. AI animates it.</p>
        </div>
        <div className="text-xs text-slate-600 border border-studio-border rounded-full px-3 py-1">
          Sketch-to-Animation Engine v0.1
        </div>
      </header>

      <main className="max-w-6xl mx-auto grid md:grid-cols-2 gap-8">
        <section>
          <h2 className="text-sm uppercase tracking-widest text-slate-500 mb-3">Canvas</h2>
          <DrawingCanvas ref={canvasRef} />
          <div className="flex gap-3 mt-4 max-w-[400px] mx-auto">
            <motion.button
              whileTap={{ scale: 0.96 }}
              onClick={handleAnalyze}
              disabled={loading}
              className="flex-1 bg-studio-cyan/90 hover:bg-studio-cyan text-slate-900 font-semibold py-2.5 rounded-lg disabled:opacity-50"
            >
              {loading ? "Analyzing…" : "Analyze & Animate"}
            </motion.button>
            <button
              onClick={handleClear}
              className="px-4 py-2.5 rounded-lg border border-studio-border text-slate-400 hover:text-white hover:border-slate-500"
            >
              Clear
            </button>
          </div>
          {error && <p className="text-red-400 text-sm mt-3 text-center">{error}</p>}
        </section>

        <section>
          <h2 className="text-sm uppercase tracking-widest text-slate-500 mb-3">AI Illustration + Animation</h2>
          <AnimationPreview svg={result?.animation_svg || ""} />

          {result && (
            <div className="max-w-[400px] mx-auto mt-4 flex gap-2">
              <input
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                placeholder="e.g. make it wave, add rain..."
                className="flex-1 bg-[#0d1420] border border-studio-border rounded-lg px-3 py-2 text-sm outline-none focus:border-studio-cyan"
              />
              <button
                onClick={handlePromptEdit}
                className="px-4 py-2 rounded-lg bg-studio-purple/80 hover:bg-studio-purple text-white text-sm"
              >
                Apply
              </button>
            </div>
          )}

          <div className="mt-6 bg-studio-panel/60 border border-studio-border rounded-xl p-4">
            <DetectionPanel detection={result?.detection || null} />
          </div>
        </section>
      </main>
    </div>
  );
}
