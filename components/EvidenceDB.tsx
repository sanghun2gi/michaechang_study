"use client";

import { useState } from "react";
import { Evidence } from "@/lib/types";

// STEP 6: 선행기술 수동 입력형 Evidence DB
export function EvidenceDB({
  evidence,
  setEvidence,
}: {
  evidence: Evidence[];
  setEvidence: (e: Evidence[]) => void;
}) {
  const [draft, setDraft] = useState<Omit<Evidence, "id">>({
    title: "",
    source: "",
    pubDate: "",
    summary: "",
  });

  function add() {
    if (!draft.title.trim()) return;
    setEvidence([...evidence, { ...draft, id: `ev_${Date.now()}` }]);
    setDraft({ title: "", source: "", pubDate: "", summary: "" });
  }

  function remove(id: string) {
    setEvidence(evidence.filter((e) => e.id !== id));
  }

  return (
    <div className="space-y-5">
      <div>
        <h2 className="text-base font-bold">선행기술 Evidence DB (STEP 6)</h2>
        <p className="mt-1 text-xs text-slate-500">
          청구항을 평가하려면 선행기술을 먼저 등록하세요. All Elements Matrix와 가상 OA가 이 목록을 사용합니다.
        </p>
      </div>

      <div className="grid gap-3 rounded-lg border border-slate-200 bg-white p-4 sm:grid-cols-2">
        <input
          className="rounded border border-slate-300 p-2 text-sm"
          placeholder="문헌 명칭 *"
          value={draft.title}
          onChange={(e) => setDraft({ ...draft, title: e.target.value })}
        />
        <input
          className="rounded border border-slate-300 p-2 text-sm"
          placeholder="출처 (특허번호/논문/URL)"
          value={draft.source}
          onChange={(e) => setDraft({ ...draft, source: e.target.value })}
        />
        <input
          className="rounded border border-slate-300 p-2 text-sm"
          placeholder="공개일 (예: 2019-03-21)"
          value={draft.pubDate}
          onChange={(e) => setDraft({ ...draft, pubDate: e.target.value })}
        />
        <input
          className="rounded border border-slate-300 p-2 text-sm"
          placeholder="관련 내용 요약"
          value={draft.summary}
          onChange={(e) => setDraft({ ...draft, summary: e.target.value })}
        />
        <button
          onClick={add}
          className="rounded-md bg-brand py-2 text-sm font-semibold text-white hover:bg-brand-dark sm:col-span-2"
        >
          선행기술 추가
        </button>
      </div>

      {evidence.length === 0 ? (
        <p className="text-sm text-slate-400">등록된 선행기술이 없습니다.</p>
      ) : (
        <ul className="space-y-2">
          {evidence.map((e) => (
            <li
              key={e.id}
              className="flex items-start justify-between gap-3 rounded-lg border border-slate-200 bg-white p-3"
            >
              <div className="text-sm">
                <p className="font-semibold">{e.title}</p>
                <p className="text-xs text-slate-500">
                  {e.source || "출처 미기재"} · {e.pubDate || "공개일 미기재"}
                </p>
                {e.summary && <p className="mt-1 text-xs text-slate-600">{e.summary}</p>}
              </div>
              <button
                onClick={() => remove(e.id)}
                className="shrink-0 text-xs text-red-600 hover:underline"
              >
                삭제
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
