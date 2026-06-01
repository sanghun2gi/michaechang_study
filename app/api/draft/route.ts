// POST /api/draft — 발명 입력을 받아 초안 + 검증 결과를 반환한다.
// AI 호출은 전부 이 서버 핸들러 내부에서만 일어난다 (절대규칙 #1).
import { NextRequest, NextResponse } from "next/server";
import { z } from "zod";
import { generateDraft } from "@/lib/server/draft";

const InventionSchema = z.object({
  title: z.string().min(1, "발명 명칭을 입력하세요"),
  field: z.string().min(1, "기술분야를 입력하세요"),
  problem: z.string().min(1, "해결 과제를 입력하세요"),
  solution: z.string().min(1, "해결 수단을 입력하세요"),
  effect: z.string().min(1, "효과를 입력하세요"),
  keyFeatures: z.string().min(1, "핵심 구성요소를 입력하세요"),
});

export async function POST(req: NextRequest) {
  let body: unknown;
  try {
    body = await req.json();
  } catch {
    return NextResponse.json({ error: "잘못된 요청 형식" }, { status: 400 });
  }

  const parsed = InventionSchema.safeParse(body);
  if (!parsed.success) {
    return NextResponse.json(
      { error: parsed.error.issues.map((i) => i.message).join(", ") },
      { status: 422 }
    );
  }

  try {
    const result = await generateDraft(parsed.data);
    return NextResponse.json(result);
  } catch (err) {
    console.error("[api/draft] 초안 생성 실패:", err);
    return NextResponse.json(
      { error: "초안 생성 중 오류가 발생했습니다." },
      { status: 500 }
    );
  }
}
