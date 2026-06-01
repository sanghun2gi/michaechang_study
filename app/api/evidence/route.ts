// GET /api/evidence?inventionId=xxx  — DB 로드
// POST /api/evidence                 — 목록 저장(upsert) + 검색 트리거
import { NextRequest, NextResponse } from "next/server";
import { z } from "zod";
import { searchPriorArt } from "@/lib/server/search";
import { upsertEvidence, loadEvidence } from "@/lib/server/persist";
import { Evidence } from "@/lib/types";

const SaveSchema = z.object({
  inventionId: z.string().min(1),
  items: z.array(
    z.object({
      id: z.string(),
      title: z.string(),
      source: z.string(),
      pubDate: z.string(),
      summary: z.string(),
      origin: z.string().optional(),
    })
  ),
});

export async function GET(req: NextRequest) {
  const inventionId = req.nextUrl.searchParams.get("inventionId");
  if (!inventionId) {
    return NextResponse.json({ error: "inventionId 필요" }, { status: 400 });
  }
  const items = await loadEvidence(inventionId);
  return NextResponse.json({ items });
}

export async function POST(req: NextRequest) {
  const parsed = SaveSchema.safeParse(await req.json().catch(() => null));
  if (!parsed.success) {
    return NextResponse.json({ error: "입력 형식 오류" }, { status: 422 });
  }
  const items = parsed.data.items as Evidence[];
  await upsertEvidence(parsed.data.inventionId, items);
  return NextResponse.json({ ok: true, saved: items.length });
}
