"use client";

import { useMemo } from "react";
import { InventionInput, DraftResult, EligibilityVerdict } from "@/lib/types";
import { checkEligibility } from "@/lib/eligibility";

const VERDICT_STYLE: Record<EligibilityVerdict, { cls: string; label: string }> = {
  ELIGIBLE: { cls: "bg-green-100 text-green-800 border-green-300", label: "적격 가능성 높음" },
  BORDERLINE: { cls: "bg-amber-100 text-amber-800 border-amber-300", label: "경계선 — 변리사 검토 필요" },
  INELIGIBLE: { cls: "bg-red-100 text-red-800 border-red-300", label: "부적격 위험 — 보완 필요" },
};

const RESULT_ICON = { PASS: "✅", FAIL: "❌", WARN: "⚠️" } as const;

// SW·AI 적격성 체크는 룰 기반이므로 발명 정보가 바뀔 때마다 즉시 재계산한다.
export function EligibilityPanel({
  invention,
  draft,
}: {
  invention: InventionInput;
  draft: DraftResult;
}) {
  const result = useMemo(
    () =>
      checkEligibility({
        title: invention.title,
        field: invention.field,
        solution: invention.solution,
        keyFeatures: invention.keyFeatures,
        claims: draft.specification.claims,
      }),
    [invention, draft]
  );

  return (
    <div className="space-y-5">
      <div>
        <h2 className="text-base font-bold">SW·AI 특허적격성 Gate (3차 스프린트)</h2>
        <p className="mt-1 text-xs text-slate-500">
          한국 특허청 SW·AI 심사지침 기반 간이 체크리스트입니다.
          입력 정보가 바뀌면 자동으로 재평가됩니다. 룰 기반 판단이며 변리사 최종 검토가 필요합니다.
        </p>
      </div>

      <div className="flex items-center gap-3 rounded-lg border border-slate-200 bg-white p-4">
        <span className="text-sm font-semibold text-slate-600">종합 판정</span>
        <span
          className={`rounded border px-2 py-0.5 text-xs font-semibold ${VERDICT_STYLE[result.verdict].cls}`}
        >
          {VERDICT_STYLE[result.verdict].label}
        </span>
        <span className="text-xs text-slate-500">{result.summary}</span>
      </div>

      <ul className="space-y-2">
        {result.checks.map((c) => (
          <li
            key={c.checkId}
            className="rounded-lg border border-slate-200 bg-white p-4"
          >
            <div className="flex items-center gap-2">
              <span className="text-base">{RESULT_ICON[c.result]}</span>
              <span className="text-sm font-medium">{c.label}</span>
              <span className="ml-auto text-xs font-semibold text-slate-400">{c.checkId}</span>
            </div>
            <p className="mt-1 text-xs text-slate-500">{c.reason}</p>
          </li>
        ))}
      </ul>
    </div>
  );
}
