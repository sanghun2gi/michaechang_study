"use client";

import { Evidence, ElementCoverage, MatrixRow } from "@/lib/types";

// STEP 9: All Elements Matrix — 청구항 구성요소 × 선행기술 커버리지
// 구성요소는 구조화 카드(STEP 3)에서 가져오고, 각 셀의 커버리지는 사용자가 지정한다.

const CYCLE: ElementCoverage[] = ["NONE", "PARTIAL", "FULL"];
const STYLE: Record<ElementCoverage, { cls: string; label: string }> = {
  NONE: { cls: "bg-green-100 text-green-700", label: "없음" },
  PARTIAL: { cls: "bg-amber-100 text-amber-700", label: "부분" },
  FULL: { cls: "bg-red-100 text-red-700", label: "전부" },
};

export function AllElementsMatrix({
  components,
  evidence,
  matrix,
  setMatrix,
}: {
  components: string[];
  evidence: Evidence[];
  matrix: MatrixRow[];
  setMatrix: (m: MatrixRow[]) => void;
}) {
  // 구성요소/Evidence 조합으로 매트릭스 동기화 (없는 셀은 NONE)
  function coverage(element: string, evId: string): ElementCoverage {
    const row = matrix.find((r) => r.element === element);
    return row?.cells.find((c) => c.evidenceId === evId)?.coverage ?? "NONE";
  }

  function cycle(element: string, evId: string) {
    const current = coverage(element, evId);
    const next = CYCLE[(CYCLE.indexOf(current) + 1) % CYCLE.length];
    const rows = components.map((el) => {
      const existing = matrix.find((r) => r.element === el);
      const cells = evidence.map((ev) => {
        if (el === element && ev.id === evId) {
          return { evidenceId: ev.id, coverage: next };
        }
        return {
          evidenceId: ev.id,
          coverage:
            existing?.cells.find((c) => c.evidenceId === ev.id)?.coverage ??
            "NONE",
        };
      });
      return { element: el, cells };
    });
    setMatrix(rows);
  }

  // 각 구성요소가 어떤 단일 선행기술에도 FULL로 덮이지 않으면 신규성 유리
  function rowNovelty(element: string): boolean {
    return !evidence.some((ev) => coverage(element, ev.id) === "FULL");
  }

  if (components.length === 0) {
    return <p className="text-sm text-slate-400">먼저 초안을 생성해 구성요소를 확보하세요.</p>;
  }

  return (
    <div className="space-y-4">
      <div>
        <h2 className="text-base font-bold">All Elements Matrix (STEP 9)</h2>
        <p className="mt-1 text-xs text-slate-500">
          셀을 클릭하면 커버리지(없음→부분→전부)가 바뀝니다. 어떤 단일 선행기술도 한 구성요소를
          '전부' 덮지 않으면 신규성에 유리합니다.
        </p>
      </div>

      {evidence.length === 0 ? (
        <p className="text-sm text-slate-400">Evidence DB 탭에서 선행기술을 먼저 등록하세요.</p>
      ) : (
        <div className="overflow-x-auto rounded-lg border border-slate-200 bg-white">
          <table className="min-w-full text-sm">
            <thead>
              <tr className="border-b bg-slate-50">
                <th className="p-3 text-left font-semibold">구성요소</th>
                {evidence.map((ev) => (
                  <th key={ev.id} className="p-3 text-center font-semibold" title={ev.summary}>
                    {ev.title}
                  </th>
                ))}
                <th className="p-3 text-center font-semibold">신규성</th>
              </tr>
            </thead>
            <tbody>
              {components.map((el) => (
                <tr key={el} className="border-b last:border-0">
                  <td className="p-3 font-medium">{el}</td>
                  {evidence.map((ev) => {
                    const cov = coverage(el, ev.id);
                    return (
                      <td key={ev.id} className="p-2 text-center">
                        <button
                          onClick={() => cycle(el, ev.id)}
                          className={`w-16 rounded px-2 py-1 text-xs font-semibold ${STYLE[cov].cls}`}
                        >
                          {STYLE[cov].label}
                        </button>
                      </td>
                    );
                  })}
                  <td className="p-3 text-center text-xs">
                    {rowNovelty(el) ? (
                      <span className="text-green-700">유리</span>
                    ) : (
                      <span className="text-red-700">불리</span>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
