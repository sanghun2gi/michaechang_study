// 가상 거절이유 생성 (STEP 21) — 진보성 거절 시 결합 동기 포함
import "server-only";
import { complete, parseJson, hasAnthropic, MODEL } from "./anthropic";
import { withLedger } from "./ledger";
import {
  Evidence,
  Rejection,
  HallucinationTag,
  OASimulationResult,
} from "../types";
import { fallbackOA } from "./fallback";

function overallRisk(rejections: Rejection[]): HallucinationTag {
  const hasNovelty = rejections.some((r) => r.type === "신규성");
  if (hasNovelty) return "RED";
  if (rejections.length >= 2) return "YELLOW";
  return rejections.length ? "YELLOW" : "GREEN";
}

export async function simulateOA(params: {
  claims: string;
  evidence: Evidence[];
}): Promise<OASimulationResult> {
  const { claims, evidence } = params;

  const { result, ledgerId } = await withLedger<Rejection[]>(
    {
      step: "STEP21",
      action: "가상 거절이유(OA) 생성",
      model: MODEL,
      inputSummary: `선행기술 ${evidence.length}건 대비`,
    },
    async () => {
      if (!hasAnthropic()) {
        const result = fallbackOA(claims, evidence);
        return { result, outputSummary: `폴백: ${result.length}개 거절` };
      }
      const text = await complete({
        system:
          "너는 특허 심사관 시뮬레이터다. 청구항과 선행기술(Evidence) 목록을 받아 " +
          "예상되는 거절이유(OA)를 생성한다. 진보성 거절에는 반드시 '결합 동기(combinationMotivation)'를 " +
          "구체적으로 제시한다(왜 통상의 기술자가 인용문헌을 결합하겠는가). " +
          '신규성/진보성/기재불비/성립성 중 해당되는 것만. JSON만 출력: ' +
          '{"rejections": [{"type": "신규성"|"진보성"|"기재불비"|"성립성", "targetClaims": string, ' +
          '"citedEvidence": string[], "combinationMotivation": string, "reasoning": string, "rebuttalHint": string}]}. ' +
          "Evidence가 없으면 기재불비/성립성 위주로 보수적으로 평가하고 지어내지 말 것.",
        user: JSON.stringify({ claims, evidence }),
        maxTokens: 2500,
      });
      const parsed = parseJson<{ rejections: Rejection[] }>(text);
      return {
        result: parsed.rejections,
        outputSummary: `${parsed.rejections.length}개 거절이유`,
      };
    }
  );

  return {
    rejections: result,
    overallRisk: overallRisk(result),
    ledgerIds: [ledgerId],
  };
}
