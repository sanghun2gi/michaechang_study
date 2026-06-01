// POST /api/claim-ladder — 발명 + 구조화 카드로 Claim Ladder/Fallback 생성 (STEP 14/15)
import { NextRequest, NextResponse } from "next/server";
import { z } from "zod";
import { generateClaimLadder } from "@/lib/server/claimLadder";

const Schema = z.object({
  invention: z.object({
    title: z.string().min(1),
    field: z.string().min(1),
    problem: z.string().min(1),
    solution: z.string().min(1),
    effect: z.string().min(1),
    keyFeatures: z.string().min(1),
  }),
  structureCard: z.object({
    components: z.array(z.string()),
    problemSolutionMap: z.array(
      z.object({ problem: z.string(), solution: z.string() })
    ),
    noveltyPoints: z.array(z.string()),
  }),
});

export async function POST(req: NextRequest) {
  const parsed = Schema.safeParse(await req.json().catch(() => null));
  if (!parsed.success) {
    return NextResponse.json({ error: "입력 형식 오류" }, { status: 422 });
  }
  try {
    const result = await generateClaimLadder(
      parsed.data.invention,
      parsed.data.structureCard
    );
    return NextResponse.json(result);
  } catch (err) {
    console.error("[api/claim-ladder]", err);
    return NextResponse.json({ error: "생성 실패" }, { status: 500 });
  }
}
