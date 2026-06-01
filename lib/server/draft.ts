// 초안 생성 파이프라인 (STEP 3 → 18 → 19)
// DB 스키마 → 서버 로직(AI 호출+원장) 순서. 모든 AI 호출은 ledger로 감싼다.
import "server-only";
import { complete, parseJson, hasAnthropic, MODEL } from "./anthropic";
import { withLedger } from "./ledger";
import {
  InventionInput,
  StructureCard,
  SpecificationDraft,
  VerificationItem,
  HallucinationTag,
  DraftResult,
} from "../types";
import {
  fallbackStructure,
  fallbackSpec,
  fallbackVerify,
} from "./fallback";

const inputSummary = (inv: InventionInput) => `${inv.title} / ${inv.field}`;

// STEP 3: 발명 구조화 카드
async function buildStructureCard(
  inv: InventionInput
): Promise<{ result: StructureCard; ledgerId: string }> {
  return withLedger<StructureCard>(
    {
      step: "STEP3",
      action: "발명 구조화 카드 생성",
      model: MODEL,
      inputSummary: inputSummary(inv),
    },
    async () => {
      if (!hasAnthropic()) {
        const result = fallbackStructure(inv);
        return { result, outputSummary: "폴백: 입력 기반 구조화" };
      }
      const text = await complete({
        system:
          "너는 한국 특허 명세서 보조 도구다. 발명 정보를 구조화 카드로 정리한다. " +
          '반드시 JSON만 출력: {"components": string[], "problemSolutionMap": [{"problem": string, "solution": string}], "noveltyPoints": string[]}. ' +
          "사실을 지어내지 말고 입력 범위 내에서만 정리한다.",
        user: JSON.stringify(inv),
        maxTokens: 1500,
      });
      const result = parseJson<StructureCard>(text);
      return {
        result,
        outputSummary: `구성요소 ${result.components.length}개`,
      };
    }
  );
}

// STEP 18: 명세서/청구항 초안
async function buildSpecification(
  inv: InventionInput,
  card: StructureCard
): Promise<{ result: SpecificationDraft; ledgerId: string }> {
  return withLedger<SpecificationDraft>(
    {
      step: "STEP18",
      action: "명세서/청구항 초안 생성",
      model: MODEL,
      inputSummary: inputSummary(inv),
    },
    async () => {
      if (!hasAnthropic()) {
        const result = fallbackSpec(inv, card);
        return { result, outputSummary: "폴백: 템플릿 초안" };
      }
      const text = await complete({
        system:
          "너는 한국 특허 명세서 초안 작성 보조 도구다. 발명과 구조화 카드를 받아 명세서 초안을 만든다. " +
          '반드시 JSON만 출력: {"background": string, "summary": string, "detailed": string, "claims": string}. ' +
          "claims는 독립항 1개와 종속항 2~3개를 한국 청구항 형식으로. " +
          "입력에 없는 수치/실험데이터를 지어내지 말 것. 모르면 '[확인 필요]'로 표기.",
        user: JSON.stringify({ invention: inv, structureCard: card }),
        maxTokens: 3000,
      });
      const result = parseJson<SpecificationDraft>(text);
      return { result, outputSummary: "명세서 4개 섹션 + 청구항" };
    }
  );
}

// STEP 19: 할루시네이션 검증 (GREEN/YELLOW/RED)
async function verifyDraft(
  inv: InventionInput,
  spec: SpecificationDraft
): Promise<{ result: VerificationItem[]; ledgerId: string }> {
  return withLedger<VerificationItem[]>(
    {
      step: "STEP19",
      action: "할루시네이션 검증",
      model: MODEL,
      inputSummary: inputSummary(inv),
    },
    async () => {
      if (!hasAnthropic()) {
        const result = fallbackVerify(inv, spec);
        return { result, outputSummary: `폴백: ${result.length}개 항목` };
      }
      const text = await complete({
        system:
          "너는 특허 초안 사실검증기다. 명세서 초안의 각 핵심 주장(특히 청구항)이 " +
          "원본 발명 입력으로 뒷받침되는지 검증한다. " +
          'JSON만 출력: {"items": [{"claimText": string, "tag": "GREEN"|"YELLOW"|"RED", "reason": string}]}. ' +
          "GREEN=입력으로 명확히 뒷받침, YELLOW=일부 추론/확인필요, RED=입력에 근거 없음/지어냄 의심.",
        user: JSON.stringify({ invention: inv, specification: spec }),
        maxTokens: 2000,
      });
      const parsed = parseJson<{ items: VerificationItem[] }>(text);
      return {
        result: parsed.items,
        outputSummary: `${parsed.items.length}개 항목 검증`,
      };
    }
  );
}

function overallTag(items: VerificationItem[]): HallucinationTag {
  if (items.some((i) => i.tag === "RED")) return "RED";
  if (items.some((i) => i.tag === "YELLOW")) return "YELLOW";
  return "GREEN";
}

/** 전체 파이프라인 실행: 구조화 → 초안 → 검증 */
export async function generateDraft(inv: InventionInput): Promise<DraftResult> {
  const { result: structureCard, ledgerId: l1 } = await buildStructureCard(inv);
  const { result: specification, ledgerId: l2 } = await buildSpecification(
    inv,
    structureCard
  );
  const { result: verification, ledgerId: l3 } = await verifyDraft(
    inv,
    specification
  );

  return {
    structureCard,
    specification,
    verification,
    overallTag: overallTag(verification),
    ledgerIds: [l1, l2, l3],
  };
}
