// 공유 타입 정의 (클라이언트/서버 공통)

export interface InventionInput {
  title: string;
  field: string;
  problem: string;
  solution: string;
  effect: string;
  keyFeatures: string;
}

export interface StructureCard {
  components: string[]; // 구성요소
  problemSolutionMap: { problem: string; solution: string }[];
  noveltyPoints: string[]; // 신규성 추정 포인트
}

export type HallucinationTag = "GREEN" | "YELLOW" | "RED";

export interface VerificationItem {
  claimText: string; // 검증 대상 문장
  tag: HallucinationTag;
  reason: string; // 태깅 근거
}

export interface SpecificationDraft {
  background: string;
  summary: string;
  detailed: string;
  claims: string;
}

export interface DraftResult {
  structureCard: StructureCard;
  specification: SpecificationDraft;
  verification: VerificationItem[];
  overallTag: HallucinationTag;
  ledgerIds: string[];
}
