// Claim Ladder 생성 (STEP 14) + Fallback Elements (STEP 15)
import "server-only";
import { complete, parseJson, hasAnthropic, MODEL } from "./anthropic";
import { withLedger } from "./ledger";
import {
  InventionInput,
  StructureCard,
  ClaimRung,
  FallbackElement,
  ClaimLadderResult,
} from "../types";
import { fallbackClaimLadder } from "./fallback";

export async function generateClaimLadder(
  inv: InventionInput,
  card: StructureCard
): Promise<ClaimLadderResult> {
  const { result, ledgerId } = await withLedger<{
    rungs: ClaimRung[];
    fallbackElements: FallbackElement[];
  }>(
    {
      step: "STEP14",
      action: "Claim Ladder + Fallback Elements 생성",
      model: MODEL,
      inputSummary: `${inv.title} / 구성요소 ${card.components.length}개`,
    },
    async () => {
      if (!hasAnthropic()) {
        const result = fallbackClaimLadder(inv, card);
        return { result, outputSummary: `폴백: ${result.rungs.length}단 사다리` };
      }
      const text = await complete({
        system:
          "너는 특허 청구항 전략 보조 도구다. 발명과 구조화 카드를 받아 Claim Ladder를 만든다. " +
          "가장 넓은 권리범위(level 1, broad)에서 점점 한정을 추가해 좁은 범위(narrow)까지 3~4단계로 사다리를 구성한다. " +
          "또한 거절 대응용 Fallback Elements(추가 한정 후보)를 제시한다. " +
          'JSON만 출력: {"rungs": [{"level": number, "scope": "broad"|"medium"|"narrow", "text": string, "rationale": string}], ' +
          '"fallbackElements": [{"element": string, "effect": string}]}. ' +
          "입력에 없는 기술요소를 지어내지 말 것.",
        user: JSON.stringify({ invention: inv, structureCard: card }),
        maxTokens: 2500,
      });
      const result = parseJson<{
        rungs: ClaimRung[];
        fallbackElements: FallbackElement[];
      }>(text);
      return {
        result,
        outputSummary: `${result.rungs.length}단 사다리, fallback ${result.fallbackElements.length}개`,
      };
    }
  );

  return { ...result, ledgerIds: [ledgerId] };
}
