// STEP 16: 용어사전 + 안티센던트(선행사 기재) 검사 — 룰 기반, 즉효.
// "상기 X"가 나오기 전에 X가 먼저 도입되었는지 청구항 단위로 검사한다.
// 서버/클라이언트 공용 (AI 호출 없음).
import { AntecedentIssue } from "./types";

// 청구항 텍스트를 "【청구항 N】" 또는 "청구항 N" 기준으로 분할
function splitClaims(claims: string): { id: string; body: string }[] {
  const parts = claims.split(/【?청구항\s*(\d+)】?/);
  const result: { id: string; body: string }[] = [];
  // parts: ["", "1", body1, "2", body2, ...]
  for (let i = 1; i < parts.length; i += 2) {
    result.push({ id: `청구항 ${parts[i]}`, body: parts[i + 1] ?? "" });
  }
  if (result.length === 0) {
    result.push({ id: "청구항", body: claims });
  }
  return result;
}

// "상기 OOO" 패턴에서 명사구를 추출
function extractAnaphora(body: string): string[] {
  const matches = [...body.matchAll(/상기\s+([가-힣A-Za-z0-9]+(?:\s+[가-힣A-Za-z0-9]+){0,2})/g)];
  return matches.map((m) => m[1].trim());
}

export function checkAntecedents(claims: string): AntecedentIssue[] {
  const issues: AntecedentIssue[] = [];
  const claimList = splitClaims(claims);

  for (const claim of claimList) {
    const anaphora = extractAnaphora(claim.body);
    for (const term of anaphora) {
      // "상기 term"의 첫 등장 위치
      const anaphoraIdx = claim.body.indexOf(`상기 ${term}`);
      // term이 "상기" 없이 먼저 도입되었는지
      const beforeText = claim.body.slice(0, anaphoraIdx);
      const introduced = beforeText.includes(term);
      if (!introduced) {
        issues.push({
          term,
          claim: claim.id,
          message: `'상기 ${term}'의 선행사가 같은 청구항 내 앞부분에 도입되지 않았습니다.`,
        });
      }
    }
  }
  return issues;
}
