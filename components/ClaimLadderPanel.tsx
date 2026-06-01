"use client";

import { useState } from "react";
import {
  InventionInput,
  DraftResult,
  ClaimLadderResult,
  ClaimRung,
} from "@/lib/types";
import { checkAntecedents } from "@/lib/antecedent";

const SCOPE_STYLE: Record<ClaimRung["scope"], string> = {
  broad: "border-blue-300 bg-blue-50",
  medium: "border-violet-300 bg-violet-50",
  narrow: "border-slate-300 bg-slate-50",
};

export function ClaimLadderPanel({
  invention,
  draft,
}: {
  invention: InventionInput;
  draft: DraftResult;
}) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<ClaimLadderResult | null>(null);

  // STEP 16: 현재 명세서 청구항에 대한 룰 기반 안티센던트 검사
  const antecedentIssues = checkAntecedents(draft.specification.claims);

  async function generate() {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch("/api/claim-ladder", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          invention,
          structureCard: draft.structureCard,
        }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error ?? "요청 실패");
      setResult(data as ClaimLadderResult);
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
          <h2 className="text-base font-bold">Claim Ladder + Fallback (STEP 14/15)</h2>
          <p className="mt-1 text-xs text-slate-500">
            넓은 권리범위 → 좁은 범위로 청구항을 단계화하고, 거절 대응용 Fallback 요소를 제시합니다.
          </p>
        </div>
        <button
          onClick={generate}
          disabled={loading}
          className="shrink-0 rounded-md bg-brand px-4 py-2 text-sm font-semibold text-white hover:bg-brand-dark disabled:opacity-50"
        >
          {loading ? "생성 중…" : "사다리 생성"}
        </button>
      </div>

      {/* STEP 16: 안티센던트 검사 결과 */}
      <div className="rounded-lg border border-slate-200 bg-white p-4">
        <h3 className="mb-2 text-sm font-bold">
          용어·선행사(안티센던트) 검사 (STEP 16)
        </h3>
        {antecedentIssues.length === 0 ? (
          <p className="text-sm text-green-700">현 청구항에서 선행사 누락이 발견되지 않았습니다.</p>
        ) : (
          <ul className="space-y-1 text-sm text-amber-700">
            {antecedentIssues.map((iss, i) => (
              <li key={i}>
                ⚠️ [{iss.claim}] {iss.message}
              </li>
            ))}
          </ul>
        )}
      </div>

      {error && <p className="rounded bg-red-50 p-2 text-sm text-red-700">{error}</p>}

      {result && (
        <>
          <div className="space-y-3">
            {result.rungs.map((r) => (
              <div
                key={r.level}
                className={`rounded-lg border p-4 ${SCOPE_STYLE[r.scope]}`}
              >
                <div className="mb-1 flex items-center gap-2 text-xs font-semibold uppercase text-slate-500">
                  Level {r.level} · {r.scope}
                </div>
                <p className="text-sm leading-relaxed">{r.text}</p>
                <p className="mt-2 text-xs text-slate-500">{r.rationale}</p>
              </div>
            ))}
          </div>

          <div className="rounded-lg border border-slate-200 bg-white p-4">
            <h3 className="mb-3 text-sm font-bold">Fallback Elements (STEP 15)</h3>
            <ul className="space-y-2 text-sm">
              {result.fallbackElements.map((f, i) => (
                <li key={i} className="rounded border border-slate-100 p-2">
                  <span className="font-medium">{f.element}</span>
                  <span className="text-slate-500"> — {f.effect}</span>
                </li>
              ))}
            </ul>
          </div>
        </>
      )}
    </div>
  );
}
