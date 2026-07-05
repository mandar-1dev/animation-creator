import { useRef, useState, useEffect, forwardRef, useImperativeHandle } from "react";

export interface DrawingCanvasHandle {
  exportPNG: () => string;
  clear: () => void;
}

interface Props {
  strokeColor?: string;
  strokeWidth?: number;
}

const DrawingCanvas = forwardRef<DrawingCanvasHandle, Props>(
  ({ strokeColor = "#e2e8f0", strokeWidth = 4 }, ref) => {
    const canvasRef = useRef<HTMLCanvasElement>(null);
    const drawing = useRef(false);
    const last = useRef<{ x: number; y: number } | null>(null);
    const [empty, setEmpty] = useState(true);

    useEffect(() => {
      const canvas = canvasRef.current;
      if (!canvas) return;
      const ctx = canvas.getContext("2d");
      if (!ctx) return;
      ctx.lineCap = "round";
      ctx.lineJoin = "round";
    }, []);

    useImperativeHandle(ref, () => ({
      exportPNG: () => canvasRef.current?.toDataURL("image/png") || "",
      clear: () => {
        const canvas = canvasRef.current;
        const ctx = canvas?.getContext("2d");
        if (canvas && ctx) ctx.clearRect(0, 0, canvas.width, canvas.height);
        setEmpty(true);
      },
    }));

    const getPos = (e: React.PointerEvent<HTMLCanvasElement>) => {
      const rect = canvasRef.current!.getBoundingClientRect();
      return {
        x: ((e.clientX - rect.left) / rect.width) * 400,
        y: ((e.clientY - rect.top) / rect.height) * 400,
      };
    };

    const start = (e: React.PointerEvent<HTMLCanvasElement>) => {
      drawing.current = true;
      last.current = getPos(e);
      setEmpty(false);
    };

    const move = (e: React.PointerEvent<HTMLCanvasElement>) => {
      if (!drawing.current) return;
      const ctx = canvasRef.current?.getContext("2d");
      if (!ctx || !last.current) return;
      const pos = getPos(e);
      ctx.strokeStyle = strokeColor;
      ctx.lineWidth = strokeWidth;
      ctx.beginPath();
      ctx.moveTo(last.current.x, last.current.y);
      ctx.lineTo(pos.x, pos.y);
      ctx.stroke();
      last.current = pos;
    };

    const end = () => {
      drawing.current = false;
      last.current = null;
    };

    return (
      <div className="relative w-full aspect-square max-w-[400px] mx-auto rounded-xl border border-studio-border bg-[#0d1420] shadow-[0_0_40px_rgba(56,189,248,0.08)] overflow-hidden">
        {empty && (
          <div className="absolute inset-0 flex items-center justify-center pointer-events-none text-slate-600 text-sm text-center px-6">
            Draw here — stick figure, sun, house, tree, car…
          </div>
        )}
        <canvas
          ref={canvasRef}
          width={400}
          height={400}
          className="w-full h-full touch-none cursor-crosshair"
          onPointerDown={start}
          onPointerMove={move}
          onPointerUp={end}
          onPointerLeave={end}
        />
      </div>
    );
  }
);

export default DrawingCanvas;
