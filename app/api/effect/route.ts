// POST /api/effect — 효과데이터 분석·보완 (STEP EFFECT)
import { NextRequest, NextResponse } from "next/server";
import { z } from "zod";
import { analyzeEffectData } from "@/lib/server/effectData";
import { saveEffectData } from "@/lib/server/persist";

const EntrySchema = z.object({
  effectName: z.string(),
  metric: z.string(),
  baseline: z.string(),
  inventionValue: z.string(),
  source: z.string(),
  note: z.string(),
});

const Schema = z.object({
  inventionId: z.string().optional(),
  invention: z.object({
    title: z.string().min(1),
    field: z.string().min(1),
    problem: z.string().min(1),
    solution: z.string().min(1),
    effect: z.string().min(1),
    keyFeatures: z.string().min(1),
  }),
  userEntries: z.array(EntrySchema).default([]),
});

export async function POST(req: NextRequest) {
  const parsed = Schema.safeParse(await req.json().catch(() => null));
  if (!parsed.success) {
    return NextResponse.json({ error: "입력 형식 오류" }, { status: 422 });
  }
  try {
    const result = await analyzeEffectData(
      parsed.data.invention,
      parsed.data.userEntries
    );
    if (parsed.data.inventionId) {
      await saveEffectData(parsed.data.inventionId, result);
    }
    return NextResponse.json(result);
  } catch (err) {
    console.error("[api/effect]", err);
    return NextResponse.json({ error: "분석 실패" }, { status: 500 });
  }
}
