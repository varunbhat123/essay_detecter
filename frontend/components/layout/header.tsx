export function Header() {
  return (
    <header className="sticky top-0 z-20 border-b border-white/10 bg-slate-950/80 backdrop-blur-xl">
      <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-4 sm:px-6 lg:px-8">
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-br from-cyan-500 to-violet-500 text-lg font-bold text-white shadow-lg shadow-cyan-500/20">
            AI
          </div>
          <div>
            <p className="text-xs uppercase tracking-[0.2em] text-cyan-300">Essay Intelligence</p>
            <h1 className="text-lg font-semibold text-white">AI Essay Detector</h1>
          </div>
        </div>

        <div className="hidden items-center gap-2 rounded-full border border-white/10 bg-slate-900/80 px-3 py-2 text-sm text-slate-300 md:flex">
          <span className="h-2.5 w-2.5 rounded-full bg-emerald-400 shadow-[0_0_12px_rgba(52,211,153,0.8)]" />
          Ready for analysis
        </div>
      </div>
    </header>
  );
}
