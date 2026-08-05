"use client";

import { useMemo, useState } from "react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { StatCard } from "@/components/ui/stat-card";
import { Textarea } from "@/components/ui/textarea";

const SAMPLE_ESSAY = `As a young student, I have always believed in the power of curiosity and resilience. Throughout my academic journey, I have approached every challenge with determination, learning not only from success but also from setbacks. My interest in computer science grew from a desire to understand how technology can solve meaningful problems in society. I have spent countless hours building projects, collaborating with peers, and exploring new ideas that push me beyond my comfort zone. Each experience has strengthened my commitment to creating innovative solutions that improve lives.`;

export function EssayAnalyzer() {
  const [essayText, setEssayText] = useState(SAMPLE_ESSAY);
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState<{
    prediction: string;
    confidence: number;
    summary: string;
    style: string;
    originality: string;
  } | null>(null);

  const wordCount = useMemo(() => {
    const trimmed = essayText.trim();
    if (!trimmed) return 0;
    return trimmed.split(/\s+/).length;
  }, [essayText]);

  const charCount = essayText.length;

  const handleAnalyze = () => {
    setIsLoading(true);

    setTimeout(() => {
      setResult({
        prediction: "Likely Human Written",
        confidence: 92,
        summary:
          "The essay demonstrates strong personal voice, contextual depth, and coherent narrative structure associated with authentic student writing.",
        style: "Academic and reflective",
        originality: "Strong personal framing",
      });
      setIsLoading(false);
    }, 1400);
  };

  return (
    <div className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
      <div className="grid gap-6 lg:grid-cols-[1.5fr_0.9fr]">
        <section className="rounded-3xl border border-white/10 bg-slate-900/80 p-4 shadow-[0_0_30px_rgba(15,23,42,0.8)] backdrop-blur-xl sm:p-6">
          <div className="mb-4 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
            <div>
              <p className="text-xs uppercase tracking-[0.22em] text-cyan-300">Essay Input</p>
              <h2 className="mt-2 text-2xl font-semibold text-white">Admissions essay analysis</h2>
            </div>
            <div className="flex items-center gap-3 text-sm text-slate-300">
              <span>Characters: {charCount}</span>
              <span className="text-slate-500">•</span>
              <span>Words: {wordCount}</span>
            </div>
          </div>

          <Textarea
            value={essayText}
            onChange={(event) => setEssayText(event.target.value)}
            placeholder="Paste the essay text here..."
            aria-label="Essay input"
          />

          <div className="mt-5 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
            <div className="flex flex-wrap items-center gap-2 text-xs text-slate-400">
              <Badge tone="info">AI risk screening</Badge>
              <Badge tone="success">Structured analysis</Badge>
            </div>

            <Button onClick={handleAnalyze} loading={isLoading} className="w-full sm:w-auto">
              {isLoading ? "Analyzing..." : "Analyze Essay"}
            </Button>
          </div>
        </section>

        <aside className="rounded-3xl border border-cyan-500/20 bg-gradient-to-br from-cyan-500/10 via-slate-900 to-violet-500/10 p-4 shadow-[0_0_30px_rgba(34,211,238,0.15)] backdrop-blur-xl sm:p-6">
          <p className="text-xs uppercase tracking-[0.22em] text-cyan-300">Overall prediction</p>
          <div className="mt-4 flex items-center justify-between gap-4">
            <div>
              <div className="text-3xl font-bold text-white">
                {result ? result.prediction : "Pending"}
              </div>
              <p className="mt-2 text-sm text-slate-300">Confidence score</p>
            </div>
            <div className="flex h-20 w-20 items-center justify-center rounded-full border border-cyan-400/30 bg-slate-900/70 text-xl font-bold text-cyan-300">
              {result ? `${result.confidence}%` : "--"}
            </div>
          </div>

          <div className="mt-6 rounded-2xl border border-white/10 bg-slate-950/50 p-4">
            <div className="mb-2 flex items-center justify-between">
              <span className="text-sm text-slate-300">Confidence</span>
              <span className="text-sm font-medium text-white">
                {result ? `${result.confidence}%` : "0%"}
              </span>
            </div>
            <div className="h-2.5 w-full overflow-hidden rounded-full bg-slate-800">
              <div
                className="h-full rounded-full bg-gradient-to-r from-cyan-400 via-violet-500 to-emerald-400 transition-all duration-500"
                style={{ width: `${result ? result.confidence : 0}%` }}
              />
            </div>
          </div>

          <div className="mt-6 space-y-3">
            <div className="rounded-2xl border border-white/10 bg-slate-950/40 p-3">
              <p className="text-xs uppercase tracking-[0.18em] text-slate-400">Summary</p>
              <p className="mt-2 text-sm leading-6 text-slate-200">
                {result ? result.summary : "Submit an essay to review detection signals."}
              </p>
            </div>
            <div className="rounded-2xl border border-white/10 bg-slate-950/40 p-3">
              <p className="text-xs uppercase tracking-[0.18em] text-slate-400">Style signal</p>
              <p className="mt-2 text-sm text-slate-200">
                {result ? result.style : "Waiting for analysis"}
              </p>
            </div>
          </div>
        </aside>
      </div>

      <section className="mt-8 grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        <StatCard label="Language" value="Academic" detail="Consistent tone and structure" tone="cyan" />
        <StatCard label="Originality" value={result ? result.originality : "Evaluating"} detail="Identity signals" tone="purple" />
        <StatCard label="Complexity" value="Balanced" detail="Sentence variety and flow" tone="amber" />
        <StatCard label="Risk" value={result ? "Low" : "Pending"} detail="AI generation likelihood" tone="emerald" />
      </section>

      <section className="mt-8 rounded-3xl border border-white/10 bg-slate-900/80 p-4 shadow-[0_0_24px_rgba(15,23,42,0.85)] backdrop-blur-xl sm:p-6">
        <div className="mb-5 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <p className="text-xs uppercase tracking-[0.22em] text-violet-300">Highlighted Essay</p>
            <h3 className="mt-2 text-2xl font-semibold text-white">Text view</h3>
          </div>
          <Badge tone={result ? "success" : "info"}>{result ? "Result ready" : "Awaiting analysis"}</Badge>
        </div>

        <div className="rounded-2xl border border-white/10 bg-slate-950/60 p-4">
          <p className="whitespace-pre-wrap leading-8 text-slate-200">
            {essayText.split(/\s+/).map((word, index) => {
              const normalized = word.toLowerCase();
              let toneClass = "";

              if (normalized.includes("experience") || normalized.includes("journey") || normalized.includes("passion")) {
                toneClass = "bg-cyan-500/20 text-cyan-200 ring-1 ring-cyan-500/30";
              } else if (normalized.includes("technology") || normalized.includes("society") || normalized.includes("innovative")) {
                toneClass = "bg-violet-500/20 text-violet-200 ring-1 ring-violet-500/30";
              } else if (normalized.includes("challenge") || normalized.includes("resilience") || normalized.includes("commitment")) {
                toneClass = "bg-emerald-500/20 text-emerald-200 ring-1 ring-emerald-500/30";
              }

              return (
                <span key={`${word}-${index}`} className={`rounded px-1 py-0.5 ${toneClass}`}>
                  {word}{" "}
                </span>
              );
            })}
          </p>
        </div>
      </section>
    </div>
  );
}
