// 효과데이터 프로토콜 (3차 스프린트)
// 발명 효과의 정량 근거를 구조화하고 품질을 평가한다.
import "server-only";
import { complete, parseJson, hasAnthropic, MODEL } from "./anthropic";
import { withLedger } from "./ledger";
import {
  InventionInput,
  EffectEntry,
  EffectQuality,
  EffectDataResult,
} from "../types";

function judgeQuality(entries: EffectEntry[]): EffectQuality {
  if (!entries.length) return "UNVERIFIED";
  const verified = entries.filter(
    (e) => e.baseline.trim() && e.inventionValue.trim() && e.source.trim()
  ).length;
  if (verified === entries.length) return "VERIFIED";
  if (verified > 0) return "PARTIAL";
  return "UNVERIFIED";
}

export async function analyzeEffectData(
  inv: InventionInput,
  rawUserEntries: EffectEntry[]
): Promise<EffectDataResult> {
  // 사용자가 직접 입력한 항목이 있으면 AI로 보완, 없으면 AI로 제안
  const { result, ledgerId } = await withLedger<EffectEntry[]>(
    {
      step: "EFFECT",
      action: "효과데이터 분석·보완",
      model: MODEL,
      inputSummary: `${inv.title} / 입력 항목 ${rawUserEntries.length}개`,
    },
    async () => {
      if (!hasAnthropic()) {
        const fallback: EffectEntry[] = rawUserEntries.length
          ? rawUserEntries
          : [
              {
                effectName: `[데모] ${inv.effect}`,
                metric: "[데모] 정량 지표 미입력",
                baseline: "[데모] 종래기술 값 필요",
                inventionValue: "[데모] 발명 구현 값 필요",
                source: "[데모] 실험보고서 또는 논문 출처 필요",
                note: "ANTHROPIC_API_KEY 설정 시 AI가 효과 항목을 제안합니다.",
              },
            ];
        return { result: fallback, outputSummary: `${fallback.length}개 항목(폴백)` };
      }
      const text = await complete({
        system:
          "너는 특허 효과데이터 분석 보조 도구다. 발명 정보와 사용자가 이미 입력한 효과 항목을 받는다. " +
          "① 입력 항목이 있으면 빈 필드를 추론으로 보완(모르면 '[확인 필요]'). " +
          "② 입력이 없으면 발명의 핵심 효과 2~3개를 제안한다. " +
          "수치·데이터를 지어내지 말 것. JSON만 출력: " +
          '{"entries": [{"effectName": string, "metric": string, "baseline": string, ' +
          '"inventionValue": string, "source": string, "note": string}]}',
        user: JSON.stringify({ invention: inv, userEntries: rawUserEntries }),
        maxTokens: 1800,
      });
      const parsed = parseJson<{ entries: EffectEntry[] }>(text);
      return {
        result: parsed.entries,
        outputSummary: `${parsed.entries.length}개 항목`,
      };
    }
  );

  return {
    entries: result,
    overallQuality: judgeQuality(result),
    ledgerIds: [ledgerId],
  };
}
