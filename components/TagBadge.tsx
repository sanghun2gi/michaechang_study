import { HallucinationTag } from "@/lib/types";

const STYLES: Record<HallucinationTag, { cls: string; label: string }> = {
  GREEN: { cls: "bg-green-100 text-green-800 border-green-300", label: "GREEN · 근거 충분" },
  YELLOW: { cls: "bg-amber-100 text-amber-800 border-amber-300", label: "YELLOW · 확인 필요" },
  RED: { cls: "bg-red-100 text-red-800 border-red-300", label: "RED · 근거 없음" },
};

export function TagBadge({ tag }: { tag: HallucinationTag }) {
  const s = STYLES[tag];
  return (
    <span className={`inline-block rounded border px-2 py-0.5 text-xs font-semibold ${s.cls}`}>
      {s.label}
    </span>
  );
}
