"use client";

import { useState } from "react";
import { Evidence, SearchHit } from "@/lib/types";

// STEP 6: 선행기술 Evidence DB — 수동 입력 + KIPRIS/Google Patents 검색
export function EvidenceDB({
  evidence,
  setEvidence,
}: {
  evidence: Evidence[];
  setEvidence: (e: Evidence[]) => void;
}) {
  const [tab, setTab] = useState<"manual" | "search">("manual");
  const [draft, setDraft] = useState<Omit<Evidence, "id">>({
    title: "",
    source: "",
    pubDate: "",
    summary: "",
  });
  const [query, setQuery] = useState("");
  const [searching, setSearching] = useState(false);
  const [hits, setHits] = useState<SearchHit[]>([]);
  const [searchError, setSearchError] = useState<string | null>(null);

  function add(item?: Omit<Evidence, "id">) {
    const src = item ?? draft;
    if (!src.title.trim()) return;
    setEvidence([
      ...evidence,
      { ...src, id: `ev_${Date.now()}_${Math.random().toString(36).slice(2)}` },
    ]);
    if (!item) setDraft({ title: "", source: "", pubDate: "", summary: "" });
  }

  function remove(id: string) {
    setEvidence(evidence.filter((e) => e.id !== id));
  }

  async function search() {
    if (!query.trim()) return;
    setSearching(true);
    setSearchError(null);
    setHits([]);
    try {
      const res = await fetch("/api/search", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error);
      setHits(data.hits as SearchHit[]);
    } catch (err) {
      setSearchError(err instanceof Error ? err.message : "검색 실패");
    } finally {
      setSearching(false);
    }
  }

  function addHit(hit: SearchHit) {
    add({
      title: hit.title,
      source: hit.source,
      pubDate: hit.pubDate,
      summary: hit.summary,
      origin: hit.origin,
    } as Omit<Evidence, "id">);
  }

  const alreadyAdded = (source: string) =>
    evidence.some((e) => e.source === source);

  return (
    <div className="space-y-5">
      <div className="flex items-start justify-between">
        <div>
          <h2 className="text-base font-bold">선행기술 Evidence DB (STEP 6)</h2>
          <p className="mt-1 text-xs text-slate-500">
            수동 입력 또는 KIPRIS·Google Patents 검색으로 선행기술을 추가하세요.
            All Elements Matrix와 가상 OA가 이 목록을 사용합니다.
          </p>
        </div>
        <span className="rounded-full bg-slate-100 px-3 py-1 text-xs font-semibold text-slate-600">
          {evidence.length}건
        </span>
      </div>

      {/* 탭 */}
      <div className="flex gap-2">
        {(["manual", "search"] as const).map((t) => (
          <button
            key={t}
            onClick={() => setTab(t)}
            className={`rounded-md px-3 py-1.5 text-xs font-medium ${
              tab === t
                ? "bg-brand text-white"
                : "bg-slate-100 text-slate-600 hover:bg-slate-200"
            }`}
          >
            {t === "manual" ? "수동 입력" : "🔍 KIPRIS·Google 검색"}
          </button>
        ))}
      </div>

      {tab === "manual" && (
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
            onClick={() => add()}
            className="rounded-md bg-brand py-2 text-sm font-semibold text-white hover:bg-brand-dark sm:col-span-2"
          >
            선행기술 추가
          </button>
        </div>
      )}

      {tab === "search" && (
        <div className="space-y-3 rounded-lg border border-slate-200 bg-white p-4">
          <p className="text-xs text-amber-700">
            ⚠️ KIPRIS_API_KEY 또는 SERPAPI_KEY 환경변수가 없으면 데모 결과가 반환됩니다.
          </p>
          <div className="flex gap-2">
            <input
              className="flex-1 rounded border border-slate-300 p-2 text-sm"
              placeholder="검색 키워드 (예: 접이식 태양광 충전기)"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && search()}
            />
            <button
              onClick={search}
              disabled={searching}
              className="rounded-md bg-brand px-4 py-2 text-sm font-semibold text-white hover:bg-brand-dark disabled:opacity-50"
            >
              {searching ? "검색 중…" : "검색"}
            </button>
          </div>
          {searchError && (
            <p className="text-sm text-red-600">{searchError}</p>
          )}
          {hits.length > 0 && (
            <ul className="space-y-2">
              {hits.map((h, i) => (
                <li
                  key={i}
                  className="flex items-start justify-between gap-3 rounded border border-slate-100 p-3"
                >
                  <div className="text-sm">
                    <div className="flex items-center gap-2">
                      <p className="font-semibold">{h.title}</p>
                      <span className="rounded bg-slate-100 px-1.5 py-0.5 text-xs text-slate-500">
                        {h.origin === "kipris" ? "KIPRIS" : "Google"}
                      </span>
                    </div>
                    <p className="text-xs text-slate-500">
                      {h.source} · {h.pubDate}
                    </p>
                    <p className="mt-1 text-xs text-slate-600">{h.summary}</p>
                  </div>
                  <button
                    onClick={() => addHit(h)}
                    disabled={alreadyAdded(h.source)}
                    className="shrink-0 rounded bg-green-600 px-2 py-1 text-xs font-semibold text-white hover:bg-green-700 disabled:bg-slate-300 disabled:text-slate-500"
                  >
                    {alreadyAdded(h.source) ? "추가됨" : "추가"}
                  </button>
                </li>
              ))}
            </ul>
          )}
        </div>
      )}

      {/* 등록된 목록 */}
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
                <div className="flex items-center gap-2">
                  <p className="font-semibold">{e.title}</p>
                  {e.origin && e.origin !== "manual" && (
                    <span className="rounded bg-blue-100 px-1.5 py-0.5 text-xs text-blue-700">
                      {e.origin === "kipris" ? "KIPRIS" : "Google"}
                    </span>
                  )}
                </div>
                <p className="text-xs text-slate-500">
                  {e.source || "출처 미기재"} · {e.pubDate || "공개일 미기재"}
                </p>
                {e.summary && (
                  <p className="mt-1 text-xs text-slate-600">{e.summary}</p>
                )}
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
