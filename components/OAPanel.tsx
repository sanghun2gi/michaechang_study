"use client";

import { useState } from "react";
import { DraftResult, Evidence, OASimulationResult } from "@/lib/types";
import { TagBadge } from "./TagBadge";

const RISK_LABEL: Record<string, string> = {
  GREEN: "낮음",
  YELLOW: "중간",
  RED: "높음",
};

export function OAPanel({
  draft,
  evidence,
}: {
  draft: DraftResult;
  evidence: Evidence[];
}) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<OASimulationResult | null>(null);

  async function generate() {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch("/api/oa", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          claims: draft.specification.claims,
          evidence,
        }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error ?? "요청 실패");
      setResult(data as OASimulationResult);
    } catch (err) {
      setError(err instanceof Error ? err.message : "오류");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="space-y-5">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-base font-bold">가상 거절이유 OA (STEP 21)</h2>
          <p className="mt-1 text-xs text-slate-500">
            현재 청구항과 등록된 선행기술({evidence.length}건)로 예상 거절이유를 생성합니다.
            진보성 거절에는 결합 동기가 포함됩니다.
          </p>
        </div>
        <button
          onClick={generate}
          disabled={loading}
          className="shrink-0 rounded-md bg-brand px-4 py-2 text-sm font-semibold text-white hover:bg-brand-dark disabled:opacity-50"
        >
          {loading ? "생성 중…" : "가상 OA 생성"}
        </button>
      </div>

      {error && <p className="rounded bg-red-50 p-2 text-sm text-red-700">{error}</p>}

      {result && (
        <>
          <div className="flex items-center gap-3 rounded-lg border border-slate-200 bg-white p-4">
            <span className="text-sm font-semibold text-slate-600">종합 거절 위험</span>
            <TagBadge tag={result.overallRisk} />
            <span className="text-xs text-slate-400">
              ({RISK_LABEL[result.overallRisk]})
            </span>
          </div>

          {result.rejections.map((r, i) => (
            <div key={i} className="rounded-lg border border-slate-200 bg-white p-4">
              <div className="mb-2 flex items-center gap-2">
                <span className="rounded bg-slate-800 px-2 py-0.5 text-xs font-semibold text-white">
                  {r.type}
                </span>
                <span className="text-sm font-medium">{r.targetClaims}</span>
              </div>
              {r.citedEvidence.length > 0 && (
                <p className="mb-2 text-xs text-slate-500">
                  인용: {r.citedEvidence.join(", ")}
                </p>
              )}
              <p className="text-sm leading-relaxed">{r.reasoning}</p>
              {r.combinationMotivation && (
                <p className="mt-2 rounded bg-amber-50 p-2 text-xs text-amber-800">
                  <strong>결합 동기:</strong> {r.combinationMotivation}
                </p>
              )}
              <p className="mt-2 rounded bg-blue-50 p-2 text-xs text-blue-800">
                <strong>대응 방향:</strong> {r.rebuttalHint}
              </p>
            </div>
          ))}
        </>
      )}
    </div>
  );
}
