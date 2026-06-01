// API 키가 없을 때 데모가 동작하도록 하는 규칙 기반 폴백.
// 실제 AI 산출물이 아님을 분명히 하기 위해 모든 결과에 [데모] 표시를 남긴다.
import "server-only";
import {
  InventionInput,
  StructureCard,
  SpecificationDraft,
  VerificationItem,
  ClaimRung,
  FallbackElement,
  Evidence,
  Rejection,
} from "../types";

function splitFeatures(keyFeatures: string): string[] {
  return keyFeatures
    .split(/[,\n·•]/)
    .map((s) => s.trim())
    .filter(Boolean);
}

export function fallbackStructure(inv: InventionInput): StructureCard {
  const components = splitFeatures(inv.keyFeatures);
  return {
    components: components.length ? components : ["[데모] 구성요소 입력 필요"],
    problemSolutionMap: [{ problem: inv.problem, solution: inv.solution }],
    noveltyPoints: [`[데모] ${inv.title}의 차별점은 변리사 검토 필요`],
  };
}

export function fallbackSpec(
  inv: InventionInput,
  card: StructureCard
): SpecificationDraft {
  const claimsBody = card.components
    .map((c, i) => `  ${i === 0 ? "" : "상기 "}${c}`)
    .join(";\n");
  return {
    background: `[데모 초안] 본 발명은 ${inv.field} 분야에 관한 것이다. 종래기술은 ${inv.problem} 문제가 있었다.`,
    summary: `[데모 초안] 본 발명은 ${inv.solution} 을 통해 상기 과제를 해결하며, ${inv.effect} 의 효과를 가진다.`,
    detailed: `[데모 초안] ${inv.title}\n\n구성요소:\n- ${card.components.join(
      "\n- "
    )}\n\n동작: ${inv.solution}`,
    claims: `【청구항 1】\n${inv.title}로서,\n${claimsBody}\n을 포함하는 ${inv.title}.\n\n【청구항 2】\n제1항에 있어서, ${inv.effect} 를 특징으로 하는 ${inv.title}.`,
  };
}

export function fallbackVerify(
  inv: InventionInput,
  spec: SpecificationDraft
): VerificationItem[] {
  const items: VerificationItem[] = [];
  // 효과에 수치가 있으면 입력 근거 확인 필요(YELLOW)
  const hasNumber = /\d/.test(spec.summary) || /\d/.test(spec.detailed);
  items.push({
    claimText: "청구항 1 (독립항)",
    tag: inv.keyFeatures.trim() ? "GREEN" : "RED",
    reason: inv.keyFeatures.trim()
      ? "[데모] 입력된 핵심 구성요소로 뒷받침됨"
      : "[데모] 핵심 구성요소 입력이 비어 있어 근거 없음",
  });
  items.push({
    claimText: "발명의 효과 기재",
    tag: hasNumber ? "YELLOW" : "GREEN",
    reason: hasNumber
      ? "[데모] 수치 표현은 실험데이터 출처 확인 필요"
      : "[데모] 입력된 효과 범위 내 서술",
  });
  return items;
}

// STEP 14/15 폴백: 구성요소 수를 기준으로 사다리 단계 구성
export function fallbackClaimLadder(
  inv: InventionInput,
  card: StructureCard
): { rungs: ClaimRung[]; fallbackElements: FallbackElement[] } {
  const comps = card.components.length
    ? card.components
    : splitFeatures(inv.keyFeatures);
  const broad = comps.slice(0, Math.max(1, Math.ceil(comps.length / 2)));
  const rungs: ClaimRung[] = [
    {
      level: 1,
      scope: "broad",
      text: `[데모] ${broad.join(", ")} 를 포함하는 ${inv.title}.`,
      rationale: "[데모] 최대 권리범위 — 회피설계가 어렵게 핵심 요소만 한정.",
    },
    {
      level: 2,
      scope: "medium",
      text: `[데모] 제1항에 있어서 ${comps.join(", ")} 를 더 포함하는 ${inv.title}.`,
      rationale: "[데모] 중간 범위 — 선행기술 회피와 권리범위의 균형.",
    },
    {
      level: 3,
      scope: "narrow",
      text: `[데모] 제2항에 있어서 ${inv.solution} 로 동작하는 것을 특징으로 하는 ${inv.title}.`,
      rationale: "[데모] 최협 범위 — 진보성 거절 대비 안전 청구항.",
    },
  ];
  const fallbackElements: FallbackElement[] = comps.slice(0, 3).map((c) => ({
    element: c,
    effect: `[데모] ${c} 한정 추가 시 인용발명과의 차별성 강화`,
  }));
  return { rungs, fallbackElements };
}

// STEP 21 폴백: Evidence 유무에 따라 보수적 거절 생성
export function fallbackOA(claims: string, evidence: Evidence[]): Rejection[] {
  if (!evidence.length) {
    return [
      {
        type: "기재불비",
        targetClaims: "청구항 전체",
        citedEvidence: [],
        combinationMotivation: "",
        reasoning:
          "[데모] 선행기술 미입력 상태 — 신규성/진보성 판단 불가. Evidence DB를 채우세요.",
        rebuttalHint: "[데모] 선행기술 조사 후 재평가 필요.",
      },
    ];
  }
  const titles = evidence.map((e) => e.title);
  const rejections: Rejection[] = [
    {
      type: "진보성",
      targetClaims: "청구항 1",
      citedEvidence: titles.slice(0, 2),
      combinationMotivation:
        "[데모] 두 인용문헌은 동일 기술분야에 속하고 동일 과제를 다루므로 결합 동기가 인정될 수 있음.",
      reasoning:
        "[데모] 인용발명들의 조합으로 청구항 1의 구성에 용이하게 도달 가능하다고 주장될 수 있음.",
      rebuttalHint:
        "[데모] 결합의 곤란성 또는 예측 못한 효과(현저한 효과)를 주장. Fallback Element 추가 한정 검토.",
    },
  ];
  return rejections;
}
