"use client";

import { useState } from "react";
import { DraftResult, InventionInput } from "@/lib/types";
import { DraftResultView } from "./DraftResultView";

const FIELDS: { key: keyof InventionInput; label: string; placeholder: string; rows?: number }[] = [
  { key: "title", label: "발명의 명칭", placeholder: "예: 접이식 휴대용 태양광 충전기" },
  { key: "field", label: "기술분야", placeholder: "예: 휴대용 전원 / 태양광 발전 장치" },
  { key: "problem", label: "해결하려는 과제", placeholder: "종래기술의 문제점", rows: 3 },
  { key: "solution", label: "해결 수단", placeholder: "어떻게 해결하는가", rows: 3 },
  { key: "effect", label: "효과", placeholder: "발명의 효과", rows: 2 },
  { key: "keyFeatures", label: "핵심 구성요소", placeholder: "쉼표/줄바꿈으로 구분", rows: 3 },
];

const EMPTY: InventionInput = {
  title: "",
  field: "",
  problem: "",
  solution: "",
  effect: "",
  keyFeatures: "",
};

const SAMPLE: InventionInput = {
  title: "접이식 휴대용 태양광 충전기",
  field: "휴대용 전원 공급 장치 및 태양광 발전",
  problem: "기존 휴대용 충전기는 부피가 크고 야외에서 태양광으로 직접 충전이 어려웠다.",
  solution: "다관절 힌지로 접히는 태양광 패널 모듈과 가변 전압 제어 회로를 결합하여 휴대성과 충전 효율을 동시에 확보한다.",
  effect: "휴대 부피를 줄이면서 야외 직접 충전이 가능하다.",
  keyFeatures: "다관절 힌지, 접이식 태양광 패널 모듈, 가변 전압 제어 회로, 휴대용 배터리 팩",
};

export function InventionForm() {
  const [form, setForm] = useState<InventionInput>(EMPTY);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<DraftResult | null>(null);

  const update = (key: keyof InventionInput, value: string) =>
    setForm((f) => ({ ...f, [key]: value }));

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const res = await fetch("/api/draft", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(form),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error ?? "요청 실패");
      setResult(data as DraftResult);
    } catch (err) {
      setError(err instanceof Error ? err.message : "알 수 없는 오류");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="grid gap-8 md:grid-cols-2">
      <form onSubmit={submit} className="space-y-4">
        <div className="flex items-center justify-between">
          <h2 className="text-base font-bold">발명 입력 (STEP 1)</h2>
          <button
            type="button"
            onClick={() => setForm(SAMPLE)}
            className="text-xs text-brand underline"
          >
            샘플 발명 채우기
          </button>
        </div>

        {FIELDS.map((f) => (
          <div key={f.key}>
            <label className="mb-1 block text-sm font-medium text-slate-700">
              {f.label}
            </label>
            {f.rows ? (
              <textarea
                value={form[f.key]}
                onChange={(e) => update(f.key, e.target.value)}
                placeholder={f.placeholder}
                rows={f.rows}
                className="w-full rounded-md border border-slate-300 p-2 text-sm focus:border-brand focus:outline-none focus:ring-1 focus:ring-brand"
              />
            ) : (
              <input
                value={form[f.key]}
                onChange={(e) => update(f.key, e.target.value)}
                placeholder={f.placeholder}
                className="w-full rounded-md border border-slate-300 p-2 text-sm focus:border-brand focus:outline-none focus:ring-1 focus:ring-brand"
              />
            )}
          </div>
        ))}

        {error && (
          <p className="rounded bg-red-50 p-2 text-sm text-red-700">{error}</p>
        )}

        <button
          type="submit"
          disabled={loading}
          className="w-full rounded-md bg-brand py-2.5 text-sm font-semibold text-white hover:bg-brand-dark disabled:opacity-50"
        >
          {loading ? "분석 중… (구조화 → 초안 → 검증)" : "진단 + 초안 생성"}
        </button>
        <p className="text-center text-xs text-slate-400">
          AI 산출물은 초안·참고자료입니다. 변리사 검토 전 단계입니다.
        </p>
      </form>

      <div>
        {result ? (
          <DraftResultView data={result} />
        ) : (
          <div className="flex h-full min-h-[300px] items-center justify-center rounded-lg border border-dashed border-slate-300 text-sm text-slate-400">
            왼쪽에 발명을 입력하면 진단·초안·검증 결과가 여기에 표시됩니다.
          </div>
        )}
      </div>
    </div>
  );
}
