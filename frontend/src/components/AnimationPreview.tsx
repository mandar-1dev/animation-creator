interface Props {
  svg: string;
}

export default function AnimationPreview({ svg }: Props) {
  if (!svg) {
    return (
      <div className="w-full aspect-square max-w-[400px] mx-auto rounded-xl border border-studio-border bg-[#0d1420] flex items-center justify-center text-slate-600 text-sm">
        AI illustration + animation will appear here
      </div>
    );
  }
  return (
    <div
      className="w-full aspect-square max-w-[400px] mx-auto rounded-xl border border-studio-border bg-[#0d1420] shadow-[0_0_40px_rgba(168,85,247,0.1)] overflow-hidden [&_svg]:w-full [&_svg]:h-full"
      dangerouslySetInnerHTML={{ __html: svg }}
    />
  );
}
