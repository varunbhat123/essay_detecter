type StatCardProps = {
  label: string;
  value: string;
  detail: string;
  tone?: "cyan" | "purple" | "amber" | "emerald" | "rose";
};

const toneClasses: Record<NonNullable<StatCardProps["tone"]>, string> = {
  cyan: "from-cyan-500/20 to-cyan-500/5 text-cyan-300 ring-cyan-400/30",
  purple: "from-violet-500/20 to-violet-500/5 text-violet-300 ring-violet-400/30",
  amber: "from-amber-500/20 to-amber-500/5 text-amber-300 ring-amber-400/30",
  emerald: "from-emerald-500/20 to-emerald-500/5 text-emerald-300 ring-emerald-400/30",
  rose: "from-rose-500/20 to-rose-500/5 text-rose-300 ring-rose-400/30",
};

export function StatCard({ label, value, detail, tone = "cyan" }: StatCardProps) {
  return (
    <div
      className={`rounded-2xl border border-white/10 bg-gradient-to-br ${toneClasses[tone]} p-4 shadow-lg ring-1 backdrop-blur-sm`}
    >
      <p className="text-xs uppercase tracking-[0.2em] text-slate-400">{label}</p>
      <div className="mt-4 flex items-end justify-between gap-4">
        <span className="text-2xl font-semibold text-white">{value}</span>
      </div>
      <p className="mt-2 text-sm text-slate-300">{detail}</p>
    </div>
  );
}
