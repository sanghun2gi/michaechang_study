"use client";

import { useState } from "react";
import { InventionInput, EffectEntry, EffectDataResult, EffectQuality } from "@/lib/types";

const QUALITY_STYLE: Record<EffectQuality, { cls: string; label: string }> = {
  VERIFIED: { cls: "bg-green-100 text-green-800 border-green-300", label: "VERIFIED · 정량 근거 충분" },
  PARTIAL: { cls: "bg-amber-100 text-amber-800 border-amber-300", label: "PARTIAL · 일부 미확인" },
  UNVERIFIED: { cls: "bg-red-100 text-red-800 border-red-300", label: "UNVERIFIED · 근거 없음" },
};

const EMPTY_ENTRY: EffectEntry = {
  effectName: "",
  metric: "",
  baseline: "",
  inventionValue: "",
  source: "",
  note: "",
};

export function EffectDataPanel({ invention }: { invention: InventionInput }) {
  const [entries, setEntries] = useState<EffectEntry[]>([{ ...EMPTY_ENTRY }]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<EffectDataResult | null>(null);

  function updateEntry(i: number, field: keyof EffectEntry, value: string) {
    setEntries((prev) => prev.map((e, idx) => (idx === i ? { ...e, [field]: value } : e)));
  }
  function addRow() {
    setEntries((prev) => [...prev, { ...EMPTY_ENTRY }]);
  }
  function removeRow(i: number) {
    setEntries((prev) => prev.filter((_, idx) => idx !== i));
  }

  async function analyze() {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch("/api/effect", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ invention, userEntries: entries.filter((e) => e.effectName.trim()) }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error ?? "요청 실패");
      setResult(data as EffectDataResult);
    } catch (err) {
      setError(err instanceof Error ? err.message : "오류");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="space-y-5">
      <div className="flex items-start justify-between">
        <div>
          <h2 className="text-base font-bold">효과데이터 프로토콜 (3차 스프린트)</h2>
          <p className="mt-1 text-xs text-slate-500">
            발명 효과의 정량 근거를 입력하면 AI가 빈 필드를 보완하고 품질을 평가합니다.
            입력 없이 분석하면 AI가 효과 항목을 제안합니다.
          </p>
        </div>
        <button
          onClick={analyze}
          disabled={loading}
          className="shrink-0 rounded-md bg-brand px-4 py-2 text-sm font-semibold text-white hover:bg-brand-dark disabled:opacity-50"
        >
          {loading ? "분석 중…" : "AI 분석·보완"}
        </button>
      </div>

      {/* 입력 테이블 */}
      <div className="overflow-x-auto rounded-lg border border-slate-200 bg-white">
        <table className="min-w-full text-xs">
          <thead>
            <tr className="border-b bg-slate-50">
              {["효과명", "측정 지표", "종래기술 값", "발명 값", "출처", "메모", ""].map((h) => (
                <th key={h} className="p-2 text-left font-semibold text-slate-600">
                  {h}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {entries.map((e, i) => (
              <tr key={i} className="border-b last:border-0">
                {(
                  ["effectName", "metric", "baseline", "inventionValue", "source", "note"] as const
                ).map((f) => (
                  <td key={f} className="p-1">
                    <input
                      className="w-full rounded border border-slate-200 p-1 text-xs focus:border-brand focus:outline-none"
                      value={e[f]}
                      onChange={(ev) => updateEntry(i, f, ev.target.value)}
                      placeholder={
                        f === "effectName" ? "효과명" :
                        f === "metric" ? "지표 (예: ms)" :
                        f === "baseline" ? "종래 값" :
                        f === "inventionValue" ? "발명 값" :
                        f === "source" ? "출처" : "메모"
                      }
                    />
                  </td>
                ))}
                <td className="p-1 text-center">
                  <button onClick={() => removeRow(i)} className="text-red-500 hover:text-red-700">
                    ✕
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        <button
          onClick={addRow}
          className="w-full p-2 text-xs text-brand hover:bg-slate-50"
        >
          + 효과 항목 추가
        </button>
      </div>

      {error && <p className="rounded bg-red-50 p-2 text-sm text-red-700">{error}</p>}

      {result && (
        <div className="space-y-3">
          <div className="flex items-center gap-3 rounded-lg border border-slate-200 bg-white p-4">
            <span className="text-sm font-semibold text-slate-600">효과데이터 품질</span>
            <span
              className={`rounded border px-2 py-0.5 text-xs font-semibold ${QUALITY_STYLE[result.overallQuality].cls}`}
            >
              {QUALITY_STYLE[result.overallQuality].label}
            </span>
          </div>
          <div className="overflow-x-auto rounded-lg border border-slate-200 bg-white">
            <table className="min-w-full text-xs">
              <thead>
                <tr className="border-b bg-slate-50">
                  {["효과명", "측정 지표", "종래기술", "발명", "출처", "메모"].map((h) => (
                    <th key={h} className="p-2 text-left font-semibold text-slate-600">{h}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {result.entries.map((e, i) => (
                  <tr key={i} className="border-b last:border-0">
                    <td className="p-2 font-medium">{e.effectName}</td>
                    <td className="p-2 text-slate-600">{e.metric}</td>
                    <td className="p-2 text-slate-600">{e.baseline}</td>
                    <td className="p-2 font-medium text-green-700">{e.inventionValue}</td>
                    <td className="p-2 text-slate-500">{e.source}</td>
                    <td className="p-2 text-slate-400">{e.note}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}
