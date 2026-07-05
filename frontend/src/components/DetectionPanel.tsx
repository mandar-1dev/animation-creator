import type { DetectionResult } from "../types";

export default function DetectionPanel({ detection }: { detection: DetectionResult | null }) {
  if (!detection) {
    return (
      <div className="text-slate-500 text-sm">
        Draw something and click <span className="text-studio-cyan">Analyze</span> to see AI detection results.
      </div>
    );
  }

  return (
    <div className="space-y-3 text-sm">
      <div className="flex items-center justify-between">
        <span className="text-slate-400">Detected Object</span>
        <span className="text-studio-cyan font-semibold capitalize">{detection.object_type}</span>
      </div>
      <div className="flex items-center justify-between">
        <span className="text-slate-400">Confidence</span>
        <span>{Math.round(detection.confidence * 100)}%</span>
      </div>
      <div className="flex items-center justify-between">
        <span className="text-slate-400">Style</span>
        <span className="text-studio-purple">{detection.suggested_style}</span>
      </div>
      <div>
        <span className="text-slate-400 block mb-1">Animations</span>
        <div className="flex flex-wrap gap-1.5">
          {detection.suggested_animations.map((a) => (
            <span key={a} className="px-2 py-0.5 rounded-full bg-studio-cyan/10 border border-studio-cyan/30 text-studio-cyan text-xs">
              {a}
            </span>
          ))}
        </div>
      </div>
      <div>
        <span className="text-slate-400 block mb-1">Palette</span>
        <div className="flex gap-1.5">
          {detection.suggested_colors.map((c) => (
            <div key={c} className="w-6 h-6 rounded border border-studio-border" style={{ background: c }} title={c} />
          ))}
        </div>
      </div>
      <p className="text-slate-500 italic pt-1 border-t border-studio-border">{detection.scene_description}</p>
      <p className="text-xs text-slate-600">
        Source: {detection.source === "gemini" ? "Gemini Vision" : "Rule-based fallback (add GEMINI_API_KEY for real AI analysis)"}
      </p>
    </div>
  );
}
