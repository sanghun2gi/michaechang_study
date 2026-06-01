// Provenance Ledger 래퍼 (문서 절대규칙 #2)
// 모든 AI 판단 함수는 이 래퍼를 통해 근거를 기록한다.
// DATABASE_URL 미설정 시 인메모리 저장(데모용)으로 폴백한다.

import "server-only";

export interface LedgerEntry {
  step: string;
  action: string;
  model: string;
  inputSummary: string;
  outputSummary: string;
  organizationId?: string;
  inventionId?: string;
}

interface StoredLedger extends LedgerEntry {
  id: string;
  createdAt: string;
}

// 데모 폴백용 인메모리 저장소
const memoryLedger: StoredLedger[] = [];

function hasDatabase(): boolean {
  return Boolean(process.env.DATABASE_URL);
}

/**
 * AI 판단 1건을 원장에 기록하고 레코드 id를 반환한다.
 * DB가 있으면 Prisma로, 없으면 인메모리로 기록한다.
 */
export async function recordLedger(entry: LedgerEntry): Promise<string> {
  if (hasDatabase()) {
    try {
      // 동적 import: DB 미사용 데모 환경에서 Prisma 의존성 회피
      const { prisma } = await import("./prisma");
      const rec = await prisma.ledgerRecord.create({ data: entry });
      return rec.id;
    } catch (err) {
      console.error("[ledger] DB 기록 실패, 인메모리로 폴백:", err);
    }
  }
  const id = `mem_${memoryLedger.length + 1}_${Date.now()}`;
  memoryLedger.push({ ...entry, id, createdAt: new Date().toISOString() });
  return id;
}

/**
 * AI 호출을 원장 기록으로 감싸는 헬퍼.
 * fn 실행 결과와 함께 ledgerId를 반환한다.
 */
export async function withLedger<T>(
  meta: Omit<LedgerEntry, "outputSummary">,
  fn: () => Promise<{ result: T; outputSummary: string }>
): Promise<{ result: T; ledgerId: string }> {
  const { result, outputSummary } = await fn();
  const ledgerId = await recordLedger({ ...meta, outputSummary });
  return { result, ledgerId };
}

export function getMemoryLedger(): StoredLedger[] {
  return [...memoryLedger];
}
