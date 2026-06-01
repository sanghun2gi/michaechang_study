// POST /api/search — 선행기술 키워드 검색 (KIPRIS + Google Patents)
import { NextRequest, NextResponse } from "next/server";
import { z } from "zod";
import { searchPriorArt } from "@/lib/server/search";

const Schema = z.object({
  query: z.string().min(1, "검색어를 입력하세요"),
  maxEach: z.number().min(1).max(10).optional(),
});

export async function POST(req: NextRequest) {
  const parsed = Schema.safeParse(await req.json().catch(() => null));
  if (!parsed.success) {
    return NextResponse.json(
      { error: parsed.error.issues[0]?.message ?? "입력 오류" },
      { status: 422 }
    );
  }
  try {
    const hits = await searchPriorArt(parsed.data.query, parsed.data.maxEach);
    return NextResponse.json({ hits });
  } catch (err) {
    console.error("[api/search]", err);
    return NextResponse.json({ error: "검색 실패" }, { status: 500 });
  }
}
