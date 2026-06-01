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

// ── 2차 스프린트 ─────────────────────────────────────────────

// STEP 6: 선행기술 근거 (Evidence DB)
export interface Evidence {
  id: string;
  title: string; // 문헌 명칭
  source: string; // 출처 (특허번호/논문/URL 등)
  pubDate: string; // 공개일 (YYYY-MM-DD, 자유 텍스트 허용)
  summary: string; // 관련 내용 요약
}

// STEP 9: All Elements Matrix — 청구항 구성요소 × 선행기술 커버리지
export type ElementCoverage = "FULL" | "PARTIAL" | "NONE";

export interface MatrixCell {
  evidenceId: string;
  coverage: ElementCoverage;
}

export interface MatrixRow {
  element: string; // 청구항 구성요소
  cells: MatrixCell[]; // 각 Evidence에 대한 커버리지
}

// STEP 14: Claim Ladder — 넓은 권리범위에서 좁은 범위로 단계화
export interface ClaimRung {
  level: number; // 1=가장 넓음
  scope: "broad" | "medium" | "narrow";
  text: string; // 청구항 문장
  rationale: string; // 이 단계의 전략적 의미
}

// STEP 15: Fallback Elements — 거절 시 추가할 한정 요소
export interface FallbackElement {
  element: string; // 한정에 쓸 구성요소/특징
  effect: string; // 추가 시 강화되는 점
}

export interface ClaimLadderResult {
  rungs: ClaimRung[];
  fallbackElements: FallbackElement[];
  ledgerIds: string[];
}

// STEP 21: 가상 거절이유 (OA Simulation)
export type RejectionType = "신규성" | "진보성" | "기재불비" | "성립성";

export interface Rejection {
  type: RejectionType;
  targetClaims: string; // 대상 청구항 (예: "청구항 1, 3")
  citedEvidence: string[]; // 인용 Evidence 제목/번호
  combinationMotivation: string; // 결합 동기 (진보성에 필수)
  reasoning: string; // 거절 논리
  rebuttalHint: string; // 대응 방향 힌트
}

export interface OASimulationResult {
  rejections: Rejection[];
  overallRisk: HallucinationTag; // GREEN=낮음 / YELLOW=중간 / RED=높음
  ledgerIds: string[];
}

// STEP 16: 안티센던트(선행사 기재) 검사 결과 — 룰 기반
export interface AntecedentIssue {
  term: string; // 문제가 된 용어
  claim: string; // 발견된 청구항 식별
  message: string;
}

// STEP 24 / 24B: 전문가 리뷰 + 승인 게이트
export type ApprovalStatus = "PENDING" | "APPROVED" | "REJECTED";

export interface ReviewApproval {
  status: ApprovalStatus;
  reviewer: string;
  comment: string;
  decidedAt: string | null;
}
