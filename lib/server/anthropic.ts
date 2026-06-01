// Anthropic API 클라이언트 (서버 사이드 전용 — 문서 절대규칙 #1)
// 키가 없으면 hasAnthropic()=false 로 폴백 동작을 유도한다.
import "server-only";
import Anthropic from "@anthropic-ai/sdk";

export const MODEL = "claude-sonnet-4-6";

export function hasAnthropic(): boolean {
  return Boolean(process.env.ANTHROPIC_API_KEY);
}

let client: Anthropic | null = null;

function getClient(): Anthropic {
  if (!client) {
    client = new Anthropic({ apiKey: process.env.ANTHROPIC_API_KEY });
  }
  return client;
}

/**
 * 단일 텍스트 응답을 받는 헬퍼. JSON 응답을 유도할 때 system으로 형식을 강제한다.
 */
export async function complete(params: {
  system: string;
  user: string;
  maxTokens?: number;
}): Promise<string> {
  const msg = await getClient().messages.create({
    model: MODEL,
    max_tokens: params.maxTokens ?? 2000,
    system: params.system,
    messages: [{ role: "user", content: params.user }],
  });
  const block = msg.content.find((b) => b.type === "text");
  return block && block.type === "text" ? block.text : "";
}

/** 모델 응답에서 JSON 블록을 안전하게 파싱한다. */
export function parseJson<T>(text: string): T {
  const fenced = text.match(/```(?:json)?\s*([\s\S]*?)```/);
  const raw = fenced ? fenced[1] : text;
  const start = raw.indexOf("{");
  const end = raw.lastIndexOf("}");
  if (start === -1 || end === -1) {
    throw new Error("JSON 파싱 실패: 객체를 찾을 수 없음");
  }
  return JSON.parse(raw.slice(start, end + 1)) as T;
}
