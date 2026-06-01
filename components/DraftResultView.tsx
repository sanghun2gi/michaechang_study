import { DraftResult } from "@/lib/types";
import { TagBadge } from "./TagBadge";

function Section({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <section className="rounded-lg border border-slate-200 bg-white p-5">
      <h3 className="mb-3 text-sm font-bold text-slate-700">{title}</h3>
      {children}
    </section>
  );
}

export function DraftResultView({ data }: { data: DraftResult }) {
  return (
    <div className="space-y-5">
      <div className="flex items-center gap-3 rounded-lg border border-slate-200 bg-white p-4">
        <span className="text-sm font-semibold text-slate-600">종합 검증 등급</span>
        <TagBadge tag={data.overallTag} />
        <span className="ml-auto text-xs text-slate-400">
          원장 기록 {data.ledgerIds.length}건 · STEP 3/18/19
        </span>
      </div>

      <Section title="🧩 발명 구조화 카드 (STEP 3)">
        <p className="mb-2 text-xs font-semibold text-slate-500">구성요소</p>
        <ul className="mb-3 list-disc pl-5 text-sm">
          {data.structureCard.components.map((c, i) => (
            <li key={i}>{c}</li>
          ))}
        </ul>
        <p className="mb-2 text-xs font-semibold text-slate-500">신규성 포인트</p>
        <ul className="list-disc pl-5 text-sm text-slate-600">
          {data.structureCard.noveltyPoints.map((c, i) => (
            <li key={i}>{c}</li>
          ))}
        </ul>
      </Section>

      <Section title="📄 명세서 초안 (STEP 18)">
        <div className="space-y-3 text-sm">
          <Field label="배경기술" value={data.specification.background} />
          <Field label="발명의 요약" value={data.specification.summary} />
          <Field label="구체적 내용" value={data.specification.detailed} />
        </div>
      </Section>

      <Section title="⚖️ 청구항 초안 (STEP 18)">
        <pre className="whitespace-pre-wrap rounded bg-slate-50 p-3 text-sm leading-relaxed">
          {data.specification.claims}
        </pre>
      </Section>

      <Section title="🔍 할루시네이션 검증 (STEP 19)">
        <ul className="space-y-3">
          {data.verification.map((v, i) => (
            <li key={i} className="rounded border border-slate-100 p-3">
              <div className="mb-1 flex items-center justify-between gap-2">
                <span className="text-sm font-medium">{v.claimText}</span>
                <TagBadge tag={v.tag} />
              </div>
              <p className="text-xs text-slate-500">{v.reason}</p>
            </li>
          ))}
        </ul>
      </Section>
    </div>
  );
}

function Field({ label, value }: { label: string; value: string }) {
  return (
    <div>
      <p className="mb-1 text-xs font-semibold text-slate-500">{label}</p>
      <p className="whitespace-pre-wrap leading-relaxed text-slate-700">{value}</p>
    </div>
  );
}
