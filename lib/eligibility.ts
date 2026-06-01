// SW·AI 특허적격성 Gate — 룰 기반 체크리스트 (서버/클라이언트 공용)
// 한국 특허청 심사기준(2023 SW·AI 특허 심사지침) 기반 간이 체크.
// AI 호출 없이 입력 텍스트 분석만으로 즉각 판단.

import { EligibilityCheckItem, EligibilityVerdict, EligibilityResult } from "./types";

const SW_AI_KEYWORDS = [
  "소프트웨어", "프로그램", "알고리즘", "인공지능", "머신러닝", "딥러닝",
  "신경망", "AI", "machine learning", "neural network", "software", "app",
  "애플리케이션", "모델", "학습", "추론", "분류", "예측", "데이터 처리",
];

function containsAny(text: string, keywords: string[]) {
  const lower = text.toLowerCase();
  return keywords.some((k) => lower.includes(k.toLowerCase()));
}

export function checkEligibility(params: {
  title: string;
  field: string;
  solution: string;
  keyFeatures: string;
  claims?: string;
}): EligibilityResult {
  const { title, field, solution, keyFeatures, claims = "" } = params;
  const allText = [title, field, solution, keyFeatures, claims].join(" ");

  const checks: EligibilityCheckItem[] = [];

  // C1: SW/AI 발명 해당 여부
  const isSWAI = containsAny(allText, SW_AI_KEYWORDS);
  checks.push({
    checkId: "C1",
    label: "SW·AI 발명 해당 여부",
    result: isSWAI ? "PASS" : "WARN",
    reason: isSWAI
      ? "발명 내용에 소프트웨어·AI 관련 요소가 확인됩니다."
      : "SW·AI 키워드가 뚜렷하지 않습니다. 하드웨어 발명은 이 게이트가 적용되지 않습니다.",
  });

  // C2: 기술적 수단(하드웨어/시스템) 결합 여부
  const hwKeywords = ["장치", "시스템", "서버", "회로", "모듈", "센서", "프로세서", "메모리", "device", "system", "hardware"];
  const hasHW = containsAny(allText, hwKeywords);
  checks.push({
    checkId: "C2",
    label: "기술적 수단(하드웨어) 결합 여부",
    result: hasHW ? "PASS" : "WARN",
    reason: hasHW
      ? "하드웨어·시스템 구성 요소가 포함되어 있습니다."
      : "순수 소프트웨어 방법으로 보입니다. 하드웨어 결합을 명시하면 적격성이 강화됩니다.",
  });

  // C3: 자연법칙·추상 아이디어만인지
  const abstractKeywords = ["금융방법", "비즈니스방법", "사업방법", "영업방법", "수학적"];
  const isAbstract = containsAny(allText, abstractKeywords);
  checks.push({
    checkId: "C3",
    label: "순수 추상 아이디어·비즈니스방법 여부",
    result: isAbstract ? "FAIL" : "PASS",
    reason: isAbstract
      ? "비즈니스방법 또는 수학적 방법으로 해석될 수 있습니다. 기술적 효과를 명확히 기재하세요."
      : "순수 추상 아이디어로 분류될 명확한 지표가 없습니다.",
  });

  // C4: 발명의 효과·기술적 과제 기재 여부
  const hasSolution = solution.trim().length > 20;
  checks.push({
    checkId: "C4",
    label: "기술적 과제·효과 명시 여부",
    result: hasSolution ? "PASS" : "WARN",
    reason: hasSolution
      ? "해결 수단이 충분히 기재되어 있습니다."
      : "해결 수단이 너무 짧습니다. 구체적인 기술 구성과 효과를 보완하세요.",
  });

  // C5: 청구항 내 컴퓨터·하드웨어 매체 기재
  const claimHW = claims.trim() && containsAny(claims, ["컴퓨터", "processor", "장치", "시스템", "기록매체"]);
  if (claims.trim()) {
    checks.push({
      checkId: "C5",
      label: "청구항 내 컴퓨터/장치 구성 기재",
      result: claimHW ? "PASS" : "WARN",
      reason: claimHW
        ? "청구항에 컴퓨터·장치 구성이 포함되어 있습니다."
        : "청구항에 컴퓨터·하드웨어 매체를 명시하면 특허적격성이 강화됩니다.",
    });
  }

  // 종합 판정
  const fails = checks.filter((c) => c.result === "FAIL").length;
  const warns = checks.filter((c) => c.result === "WARN").length;

  let verdict: EligibilityVerdict;
  let summary: string;
  if (fails > 0) {
    verdict = "INELIGIBLE";
    summary = "특허적격성 부적합 의심 항목이 있습니다. 청구항 및 명세서를 보완하세요.";
  } else if (warns >= 2) {
    verdict = "BORDERLINE";
    summary = "주의 항목이 다수입니다. 변리사 검토로 적격성 보강을 권장합니다.";
  } else {
    verdict = "ELIGIBLE";
    summary = "기본 적격성 체크를 통과했습니다. 변리사 최종 검토를 받으세요.";
  }

  return { checks, verdict, summary, ledgerIds: [] };
}
