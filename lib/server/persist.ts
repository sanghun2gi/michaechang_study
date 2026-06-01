// Prisma 영속화 헬퍼 — Evidence, ClaimLadder, OASimulation, ReviewApproval, EffectData, EligibilityGate
// DB 미설정 시 호출이 오면 no-op으로 처리하고 에러를 던지지 않는다.
import "server-only";
import {
  Evidence,
  MatrixRow,
  ClaimLadderResult,
  OASimulationResult,
  ReviewApproval,
  EffectDataResult,
  EligibilityResult,
} from "../types";

function hasDb() {
  return Boolean(process.env.DATABASE_URL);
}

async function db() {
  const { prisma } = await import("./prisma");
  return prisma;
}

// ── Evidence ─────────────────────────────────────────────────

export async function upsertEvidence(
  inventionId: string,
  items: Evidence[]
): Promise<void> {
  if (!hasDb()) return;
  const p = await db();
  // 기존 Evidence를 삭제 후 재삽입 (수동 입력은 소량)
  await p.evidence.deleteMany({ where: { inventionId } });
  await p.evidence.createMany({
    data: items.map((e) => ({
      id: e.id,
      inventionId,
      title: e.title,
      source: e.source,
      pubDate: e.pubDate,
      summary: e.summary,
      origin: e.origin ?? "manual",
    })),
    skipDuplicates: true,
  });
}

export async function loadEvidence(inventionId: string): Promise<Evidence[]> {
  if (!hasDb()) return [];
  const p = await db();
  const rows = await p.evidence.findMany({ where: { inventionId } });
  return rows.map((r) => ({
    id: r.id,
    title: r.title,
    source: r.source,
    pubDate: r.pubDate,
    summary: r.summary,
    origin: r.origin as Evidence["origin"],
  }));
}

// ── ClaimLadder ───────────────────────────────────────────────

export async function saveClaimLadder(
  inventionId: string,
  result: ClaimLadderResult
): Promise<void> {
  if (!hasDb()) return;
  const p = await db();
  await p.claimLadder.upsert({
    where: { inventionId },
    create: {
      inventionId,
      rungs: JSON.stringify(result.rungs),
      fallbacks: JSON.stringify(result.fallbackElements),
    },
    update: {
      rungs: JSON.stringify(result.rungs),
      fallbacks: JSON.stringify(result.fallbackElements),
    },
  });
}

// ── OASimulation ──────────────────────────────────────────────

export async function saveOA(
  inventionId: string,
  result: OASimulationResult
): Promise<void> {
  if (!hasDb()) return;
  const p = await db();
  await p.oASimulation.upsert({
    where: { inventionId },
    create: {
      inventionId,
      rejections: JSON.stringify(result.rejections),
      overallRisk: result.overallRisk,
    },
    update: {
      rejections: JSON.stringify(result.rejections),
      overallRisk: result.overallRisk,
    },
  });
}

// ── ReviewApproval ────────────────────────────────────────────

export async function saveApproval(
  inventionId: string,
  approval: ReviewApproval
): Promise<void> {
  if (!hasDb()) return;
  const p = await db();
  await p.reviewApproval.upsert({
    where: { inventionId },
    create: {
      inventionId,
      status: approval.status,
      reviewer: approval.reviewer,
      comment: approval.comment,
      decidedAt: approval.decidedAt ? new Date(approval.decidedAt) : null,
    },
    update: {
      status: approval.status,
      reviewer: approval.reviewer,
      comment: approval.comment,
      decidedAt: approval.decidedAt ? new Date(approval.decidedAt) : null,
    },
  });
}

// ── EffectData ────────────────────────────────────────────────

export async function saveEffectData(
  inventionId: string,
  result: EffectDataResult
): Promise<void> {
  if (!hasDb()) return;
  const p = await db();
  await p.effectData.upsert({
    where: { inventionId },
    create: {
      inventionId,
      entries: JSON.stringify(result.entries),
      overallQuality: result.overallQuality,
    },
    update: {
      entries: JSON.stringify(result.entries),
      overallQuality: result.overallQuality,
    },
  });
}

// ── EligibilityGate ───────────────────────────────────────────

export async function saveEligibility(
  inventionId: string,
  result: EligibilityResult
): Promise<void> {
  if (!hasDb()) return;
  const p = await db();
  await p.eligibilityGate.upsert({
    where: { inventionId },
    create: {
      inventionId,
      checks: JSON.stringify(result.checks),
      verdict: result.verdict,
    },
    update: {
      checks: JSON.stringify(result.checks),
      verdict: result.verdict,
    },
  });
}

// ── AllElementsMatrix ─────────────────────────────────────────
// 별도 테이블 없이 Specification.verification JSON에 함께 저장하는 가벼운 방식.
// 추후 별도 테이블로 분리 가능.
export async function saveMatrix(
  inventionId: string,
  matrix: MatrixRow[]
): Promise<void> {
  if (!hasDb()) return;
  // matrix를 Specification의 부가 필드로 저장 (별도 컬럼 없음 → update 사용)
  const p = await db();
  try {
    await p.specification.update({
      where: { inventionId },
      data: { verification: JSON.stringify({ matrix }) },
    });
  } catch {
    // Specification 미존재 시 무시
  }
}
