import { EssayAnalyzer } from "@/components/features/essay-analyzer";
import { Header } from "@/components/layout/header";

export default function HomePage() {
  return (
    <main className="min-h-screen bg-slate-950 text-white">
      <div className="absolute inset-0 -z-10 bg-[radial-gradient(circle_at_top,_rgba(34,211,238,0.15),_transparent_30%),radial-gradient(circle_at_right,_rgba(168,85,247,0.15),_transparent_30%),linear-gradient(to_bottom,_#020817,_#0f172a)]" />
      <Header />
      <EssayAnalyzer />
    </main>
  );
}
