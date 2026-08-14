"use client";

import { useMemo, useState } from "react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { StatCard } from "@/components/ui/stat-card";
import { Textarea } from "@/components/ui/textarea";
import { appConfig } from "@/lib/config";

const SAMPLE_ESSAY = `As a young student, I have always believed in the power of curiosity and resilience. Throughout my academic journey, I have approached every challenge with determination, learning not only from success but also from setbacks. My interest in computer science grew from a desire to understand how technology can solve meaningful problems in society. I have spent countless hours building projects, collaborating with peers, and exploring new ideas that push me beyond my comfort zone. Each experience has strengthened my commitment to creating innovative solutions that improve lives.`;

type ExtractedFeatures = {
  perplexity: number;
  burstiness: number;
  vocabulary_diversity: number;
  readability_score: number;
  entropy: number;
  repeated_phrase_ratio: number;
  transition_word_frequency: number;
  sentence_complexity: number;
  lexical_richness: number;
};

type SentenceHighlight = {
  sentence: string;
  score: number;
  confidence: number;
  status: string;
  reasons: string[];
  extracted_features: ExtractedFeatures;
};

type DetectionResponse = {
  overall_score: number;
  prediction: string;
  confidence: number;
  status: string;
  summary: string;
  sentence_highlights: SentenceHighlight[];
};

const featureLabels: Record<string, string> = {
  perplexity: "Perplexity",
  burstiness: "Burstiness",
  vocabulary_diversity: "Vocabulary diversity",
  readability_score: "Readability score",
  entropy: "Entropy",
  repeated_phrase_ratio: "Repeated phrase ratio",
  transition_word_frequency: "Transition word frequency",
  sentence_complexity: "Sentence complexity",
  lexical_richness: "Lexical richness",
};

function getRiskLevel(score: number): "Low" | "Medium" | "High" {
  if (score >= 0.7) return "High";
  if (score >= 0.4) return "Medium";
  return "Low";
}

function formatLikelihood(value: number): string {
  return `${Math.round(value * 100)}%`;
}

function formatStatus(value: string): string {
  const mappedStatus: Record<string, string> = {
    likely_human: "Likely Human",
    likely_ai: "Likely AI",
  };

  return mappedStatus[value] ?? value.replace(/_/g, " ").replace(/\b\w/g, (char) => char.toUpperCase());
}

function formatFeatureValue(value: number | string): string {
  if (typeof value === "number") {
    return Number.isInteger(value) ? String(value) : value.toFixed(4).replace(/0+$/, "").replace(/\.$/, "");
  }

  return value;
}

function getToneClass(status: string): string {
  if (status === "likely_ai") return "bg-rose-500/20 text-rose-200 ring-1 ring-rose-500/30";
  if (status === "suspicious") return "bg-amber-500/20 text-amber-200 ring-1 ring-amber-500/30";
  return "bg-emerald-500/20 text-emerald-200 ring-1 ring-emerald-500/30";
}

export function EssayAnalyzer() {
  const [essayText, setEssayText] = useState(SAMPLE_ESSAY);
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState<DetectionResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [expandedFeatures, setExpandedFeatures] = useState<Record<number, boolean>>({});

  const wordCount = useMemo(() => {
    const trimmed = essayText.trim();
    if (!trimmed) return 0;
    return trimmed.split(/\s+/).length;
  }, [essayText]);

  const charCount = essayText.length;

  const handleAnalyze = async () => {
    if (!essayText.trim()) {
      setError("Please enter an essay before analyzing.");
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      const response = await fetch(`${appConfig.apiBaseUrl}/api/detect`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ essay: essayText }),
      });

      if (!response.ok) {
        const payload = await response.json().catch(() => null);
        throw new Error(payload?.detail || "Failed to analyze essay. Please try again.");
      }

      const payload = (await response.json()) as DetectionResponse;

      if (
        typeof payload?.overall_score !== "number" ||
        typeof payload?.prediction !== "string" ||
        typeof payload?.confidence !== "number" ||
        !Array.isArray(payload?.sentence_highlights)
      ) {
        throw new Error("The detection service returned a malformed response.");
      }

      setResult(payload);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unexpected error while analyzing.");
      setResult(null);
    } finally {
      setIsLoading(false);
    }
  };

  const toggleFeatureSection = (index: number) => {
    setExpandedFeatures((current) => ({
      ...current,
      [index]: !current[index],
    }));
  };

  const scorePercent = result ? Math.round(result.overall_score * 100) : 0;
  const riskLevel = result ? getRiskLevel(result.overall_score) : "Low";

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

            <Button onClick={handleAnalyze} loading={isLoading} className="w-full sm:w-auto" disabled={!essayText.trim()}>
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
              {result ? `${Math.round(result.confidence * 100)}%` : "--"}
            </div>
          </div>

          <div className="mt-6 rounded-2xl border border-white/10 bg-slate-950/50 p-4">
            <div className="mb-2 flex items-center justify-between">
              <span className="text-sm text-slate-300">Confidence</span>
              <span className="text-sm font-medium text-white">
                {result ? `${Math.round(result.confidence * 100)}%` : "0%"}
              </span>
            </div>
            <div className="h-2.5 w-full overflow-hidden rounded-full bg-slate-800">
              <div
                className="h-full rounded-full bg-gradient-to-r from-cyan-400 via-violet-500 to-emerald-400 transition-all duration-500"
                style={{ width: `${result ? Math.round(result.confidence * 100) : 0}%` }}
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
              <p className="text-xs uppercase tracking-[0.18em] text-slate-400">Status</p>
              <p className="mt-2 text-sm text-slate-200">
                {result ? result.status : "Waiting for analysis"}
              </p>
            </div>
          </div>
        </aside>
      </div>

      {error ? (
        <div className="mt-6 rounded-3xl border border-rose-500/20 bg-rose-500/10 p-4 text-sm text-rose-100">
          <strong>Error:</strong> {error}
        </div>
      ) : null}

      <section className="mt-8 grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        <StatCard label="Prediction" value={result ? result.prediction : "Pending"} detail="Overall detection result" tone="cyan" />
        <StatCard label="Confidence" value={result ? `${scorePercent}%` : "--"} detail="AI likelihood confidence" tone="purple" />
        <StatCard label="Words" value={String(wordCount)} detail="Essay word count" tone="amber" />
        <StatCard label="Risk" value={result ? riskLevel : "Pending"} detail="AI generation likelihood" tone="emerald" />
      </section>

      <section className="mt-8 rounded-3xl border border-white/10 bg-slate-900/80 p-4 shadow-[0_0_24px_rgba(15,23,42,0.85)] backdrop-blur-xl sm:p-6">
        <div className="mb-5 flex items-center justify-between gap-3">
          <div>
            <p className="text-xs uppercase tracking-[0.22em] text-violet-300">Sentence Analysis</p>
            <h3 className="mt-2 text-2xl font-semibold text-white">Sentence-level breakdown</h3>
          </div>
          <Badge tone={isLoading ? "info" : result ? "success" : "info"}>{isLoading ? "Analyzing..." : result ? "Result ready" : "Awaiting analysis"}</Badge>
        </div>

        {isLoading ? (
          <div className="rounded-2xl border border-white/10 bg-slate-950/60 p-5 text-sm text-slate-300">
            <div className="flex items-center gap-3">
              <span className="h-4 w-4 animate-spin rounded-full border-2 border-cyan-400/30 border-t-cyan-300" />
              Analyzing essay sentences and extracting feature signals...
            </div>
          </div>
        ) : result && result.sentence_highlights.length > 0 ? (
          <div className="space-y-4">
            {result.sentence_highlights.map((highlight, index) => {
              const aiLikelihood = Math.round(highlight.score * 100);
              const isExpanded = expandedFeatures[index];

              return (
                <div key={`sentence-analysis-${index}`} className="rounded-2xl border border-white/10 bg-slate-950/60 p-4">
                  <div className="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
                    <p className="text-base leading-7 text-slate-200">{highlight.sentence}</p>
                    <span className={`inline-flex rounded-full px-2.5 py-1 text-xs font-medium ${getToneClass(highlight.status)}`}>
                      {formatStatus(highlight.status)}
                    </span>
                  </div>

                  <div className="mt-4">
                    <div className="mb-2 flex items-center justify-between gap-3 text-sm text-slate-300">
                      <span>AI likelihood</span>
                      <span className="font-medium text-white">{formatLikelihood(highlight.score)}</span>
                    </div>
                    <div className="h-2.5 w-full overflow-hidden rounded-full bg-slate-800">
                      <div
                        className="h-full rounded-full bg-gradient-to-r from-cyan-400 via-violet-500 to-rose-500 transition-all duration-500"
                        style={{ width: `${Math.min(100, Math.max(aiLikelihood, 0))}%` }}
                      />
                    </div>
                  </div>

                  {highlight.reasons.length > 0 ? (
                    <ul className="mt-4 list-disc space-y-1 pl-5 text-sm text-slate-300">
                      {highlight.reasons.map((reason, reasonIndex) => (
                        <li key={`${highlight.sentence}-${reasonIndex}`}>{reason}</li>
                      ))}
                    </ul>
                  ) : null}

                  <button
                    type="button"
                    onClick={() => toggleFeatureSection(index)}
                    className="mt-4 inline-flex items-center rounded-full border border-cyan-500/30 bg-cyan-500/10 px-3 py-1.5 text-xs font-medium text-cyan-200 transition hover:bg-cyan-500/20"
                  >
                    {isExpanded ? "Hide" : "Show"} Extracted Features
                  </button>

                  {isExpanded ? (
                    <div className="mt-4 rounded-2xl border border-white/10 bg-slate-900/80 p-3">
                      <div className="grid gap-3 sm:grid-cols-2">
                        {Object.entries(highlight.extracted_features).map(([featureKey, value]) => (
                          <div key={`${highlight.sentence}-${featureKey}`} className="rounded-xl border border-white/10 bg-slate-950/60 p-3">
                            <p className="text-[11px] uppercase tracking-[0.16em] text-slate-400">{featureLabels[featureKey] ?? featureKey}</p>
                            <p className="mt-2 text-sm font-medium text-white">{formatFeatureValue(value)}</p>
                          </div>
                        ))}
                      </div>
                    </div>
                  ) : null}
                </div>
              );
            })}
          </div>
        ) : (
          <div className="rounded-2xl border border-white/10 bg-slate-950/60 p-5 text-sm text-slate-300">
            Awaiting analysis
          </div>
        )}
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
          <p className="whitespace-pre-wrap leading-8 text-slate-200 cursor-default">
            {result && result.sentence_highlights.length > 0 ? (
              result.sentence_highlights.map((highlight, index) => {
                let toneClass = "text-slate-200";

                if (highlight.status === "likely_ai") {
                  toneClass = "bg-rose-500/20 text-rose-200 ring-1 ring-rose-500/30";
                } else if (highlight.status === "suspicious") {
                  toneClass = "bg-amber-500/20 text-amber-200 ring-1 ring-amber-500/30";
                } else if (highlight.status === "likely_human") {
                  toneClass = "bg-emerald-500/20 text-emerald-200 ring-1 ring-emerald-500/30";
                }

                return (
                  <span
                    key={`sentence-${index}`}
                    className={`rounded px-1 py-0.5 mx-0.5 transition-colors duration-200 ${toneClass}`}
                    title={`Score: ${highlight.score} | Reasons: ${highlight.reasons.join(", ")}`}
                  >
                    {highlight.sentence}{" "}
                  </span>
                );
              })
            ) : (
              essayText
            )}
          </p>
        </div>
      </section>
    </div>
  );
}
