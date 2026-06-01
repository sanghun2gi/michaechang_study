import { Workspace } from "@/components/Workspace";

export default function Home() {
  return (
    <div className="space-y-8">
      <section>
        <h1 className="text-2xl font-bold tracking-tight">
          발명 아이디어 → 진단 · 초안 · 선행기술 · Claim Ladder · 가상 OA · 승인
        </h1>
        <p className="mt-2 text-sm text-slate-500">
          탭을 따라 진행하세요: 진단·초안(STEP 1/3/18/19) → 선행기술 DB(STEP 6) →
          All Elements Matrix(STEP 9) → Claim Ladder·안티센던트(STEP 14/15/16) →
          가상 OA(STEP 21) → 전문가 리뷰·승인(STEP 24/24B). 모든 AI 판단은 원장에 기록됩니다.
        </p>
      </section>
      <Workspace />
    </div>
  );
}
