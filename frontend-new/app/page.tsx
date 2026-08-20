"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

const exampleQueries = [
  "Analyze transaction performance and identify risks",
  "Analyze customer activity and inactive customers",
  "Analyze loan performance and repayment risks",
  "Analyze credit card utilization and opportunities",
];

export default function Home() {
  const router = useRouter();

  const [query, setQuery] = useState("");
  const [error, setError] = useState("");

  function generateAnalysis() {
    const cleanQuery = query.trim();

    if (!cleanQuery) {
      setError("Please enter a banking analytics query.");
      return;
    }

    setError("");

    router.push(`/report?query=${encodeURIComponent(cleanQuery)}`);
  }

  function handleExampleQuery(example: string) {
    setQuery(example);
    setError("");
  }

  function focusQuery() {
    const queryInput = document.getElementById("banking-query-input");

    if (queryInput) {
      queryInput.focus();

      queryInput.scrollIntoView({
        behavior: "smooth",
        block: "center",
      });
    }
  }

  function openAIInsights() {
    setQuery(
      "Analyze banking performance and identify key risks, opportunities and recommendations"
    );

    setError("");

    focusQuery();
  }

  function openVisualIntelligence() {
    setQuery(
      "Analyze transaction performance and provide visual analytics"
    );

    setError("");

    focusQuery();
  }

  return (
    <main className="premium-background min-h-screen text-white">
      {/* Animated background */}
      <div className="purple-glow purple-glow-one" />
      <div className="purple-glow purple-glow-two" />
      <div className="purple-glow purple-glow-three" />
      <div className="premium-grid" />

      {/* HEADER */}
      <header className="relative z-10 border-b border-violet-500/10 bg-[#0b0614]/75 backdrop-blur-xl">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-5 lg:px-8">
        <div>
      <div className="rounded-full border border-violet-400/20 bg-violet-950/30 px-8 py-4 backdrop-blur-md shadow-[0_0_35px_rgba(139,92,246,0.12)]">
  <p className="text-sm font-bold tracking-[0.35em] text-violet-400">
    BANKING ANALYTICS
  </p>

  <h1 className="mt-2 text-2xl font-extrabold tracking-tight text-white sm:text-3xl lg:text-4xl">
    Banking AI Reporting Platform
  </h1>
</div>
</div>
      
        </div>
      </header>

      {/* MAIN CONTENT */}
      <div className="relative z-10 mx-auto max-w-7xl px-6 py-16 lg:px-8">
        {/* HERO */}
        <section className="text-center">
          <div className="mx-auto max-w-4xl">
            <div className="mx-auto inline-flex items-center gap-2 rounded-full border border-violet-400/20 bg-violet-950/30 px-4 py-2 text-xs font-medium text-violet-300 backdrop-blur-md">
              <span className="h-2 w-2 animate-pulse rounded-full bg-violet-400" />
              REAL-TIME BANKING INTELLIGENCE
            </div>

            <h2 className="mt-7 text-4xl font-bold tracking-tight text-white sm:text-6xl">
              Ask your banking data
              <span className="block bg-gradient-to-r from-violet-300 via-purple-400 to-fuchsia-400 bg-clip-text text-transparent">
                anything.
              </span>
            </h2>

            <p className="mx-auto mt-6 max-w-2xl text-base leading-7 text-violet-100/55 sm:text-lg">
              Explore your banking data using natural language and generate
              intelligent business reports, insights and visual analytics.
            </p>
          </div>
        </section>

        {/* QUERY BOX */}
        <section className="mx-auto mt-12 max-w-4xl">
          <div className="premium-glass premium-border search-glow rounded-3xl p-3">
            <div className="flex flex-col gap-3 sm:flex-row">
              <input
                id="banking-query-input"
                type="text"
                value={query}
                onChange={(event) => {
                  setQuery(event.target.value);
                  setError("");
                }}
                onKeyDown={(event) => {
                  if (event.key === "Enter") {
                    generateAnalysis();
                  }
                }}
                placeholder="Ask a question about your banking data..."
                className="min-h-16 flex-1 rounded-2xl border border-violet-400/10 bg-[#0a0512]/90 px-5 text-base text-white outline-none transition placeholder:text-violet-100/30 focus:border-violet-400/40"
              />

              <button
                type="button"
                onClick={generateAnalysis}
                className="min-h-16 rounded-2xl bg-gradient-to-r from-violet-700 via-purple-700 to-fuchsia-700 px-8 text-sm font-semibold text-white shadow-lg shadow-purple-950/40 transition hover:scale-[1.01] hover:from-violet-600 hover:via-purple-600 hover:to-fuchsia-600"
              >
                Generate Analysis
              </button>
            </div>
          </div>

          {error && (
            <div className="mt-4 rounded-2xl border border-red-500/20 bg-red-950/20 px-5 py-4 text-sm text-red-300">
              {error}
            </div>
          )}
        </section>

        {/* EXAMPLES */}
        <section className="mx-auto mt-8 max-w-5xl">
          <div className="text-center">
            <p className="mb-4 text-xs font-medium uppercase tracking-[0.2em] text-violet-100/35">
              Try an example
            </p>

            <div className="flex flex-wrap justify-center gap-3">
              {exampleQueries.map((example) => (
                <button
                  key={example}
                  type="button"
                  onClick={() => handleExampleQuery(example)}
                  className="rounded-full border border-violet-400/10 bg-[#12091d]/70 px-4 py-2.5 text-xs text-violet-100/55 backdrop-blur-md transition hover:border-violet-400/30 hover:bg-violet-950/40 hover:text-violet-200"
                >
                  {example}
                </button>
              ))}
            </div>
          </div>
        </section>

        
      </div>
    </main>
  );
}