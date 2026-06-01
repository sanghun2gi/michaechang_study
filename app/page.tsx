import { InventionForm } from "@/components/InventionForm";

export default function Home() {
  return (
    <div className="space-y-8">
      <section>
        <h1 className="text-2xl font-bold tracking-tight">
          발명 아이디어 → 진단 · 명세서/청구항 초안 · 할루시네이션 검증
        </h1>
        <p className="mt-2 text-sm text-slate-500">
          발명 정보를 입력하면 구조화 카드(STEP 3) → 명세서·청구항 초안(STEP 18) →
          할루시네이션 검증(STEP 19)을 순서대로 생성합니다. 모든 AI 판단은 원장에 기록됩니다.
        </p>
      </section>
      <InventionForm />
    </div>
  );
}
