// API 키가 없을 때 데모가 동작하도록 하는 규칙 기반 폴백.
// 실제 AI 산출물이 아님을 분명히 하기 위해 모든 결과에 [데모] 표시를 남긴다.
import "server-only";
import {
  InventionInput,
  StructureCard,
  SpecificationDraft,
  VerificationItem,
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
