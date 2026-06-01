// 선행기술 검색 서비스 (KIPRIS / Google Patents 연동 + 폴백)
// 실제 API 키가 없는 환경에서는 모의 결과를 반환해 흐름을 보여준다.
import "server-only";
import { SearchHit } from "../types";

// ── KIPRIS Open API ───────────────────────────────────────────
// 한국 특허청 KIPRIS Plus: https://plus.kipris.or.kr/
// 환경변수: KIPRIS_API_KEY
// 엔드포인트: 특허실용신안 키워드 검색 (PatentKeywordSearch)
async function searchKipris(query: string, maxResults = 5): Promise<SearchHit[]> {
  const key = process.env.KIPRIS_API_KEY;
  if (!key) return [];

  try {
    const params = new URLSearchParams({
      query,
      pageNo: "1",
      numOfRows: String(maxResults),
      ServiceKey: key,
      type: "patent",
    });
    const url = `https://plus.kipris.or.kr/kipo-api/kipi/patUtiModInfoSearchSevice/getWordSearch?${params}`;
    const res = await fetch(url, { next: { revalidate: 3600 } });
    if (!res.ok) return [];

    const text = await res.text();
    // KIPRIS XML 파싱 (간략)
    const items = [...text.matchAll(/<item>([\s\S]*?)<\/item>/g)];
    return items.map((m): SearchHit => {
      const get = (tag: string) =>
        m[1].match(new RegExp(`<${tag}>(.*?)<\/${tag}>`))?.[1]?.trim() ?? "";
      return {
        title: get("inventionTitle") || get("title"),
        source: `KR${get("applicationNumber") || get("publicationNumber")}`,
        pubDate: get("openDate") || get("applicationDate"),
        summary: get("abstractContent") || get("summary") || "(초록 없음)",
        origin: "kipris",
      };
    });
  } catch {
    return [];
  }
}

// ── Google Patents (SerpAPI 또는 직접 스크레이핑 대신 Suggest API) ──
// 완전한 연동은 SerpAPI(유료) 또는 Google Patents API가 필요.
// 여기서는 Google Scholar/Patents 검색 URL 생성 + 제한적 파싱을 제공한다.
// 환경변수: SERPAPI_KEY (선택)
async function searchGoogle(query: string, maxResults = 5): Promise<SearchHit[]> {
  const key = process.env.SERPAPI_KEY;
  if (!key) return [];

  try {
    const params = new URLSearchParams({
      engine: "google_patents",
      q: query,
      num: String(maxResults),
      api_key: key,
    });
    const res = await fetch(`https://serpapi.com/search?${params}`, {
      next: { revalidate: 3600 },
    });
    if (!res.ok) return [];

    const json = (await res.json()) as {
      organic_results?: Array<{
        title?: string;
        patent_id?: string;
        publication_date?: string;
        snippet?: string;
      }>;
    };
    return (json.organic_results ?? []).slice(0, maxResults).map((r): SearchHit => ({
      title: r.title ?? "(제목 없음)",
      source: r.patent_id ?? "Google Patents",
      pubDate: r.publication_date ?? "",
      summary: r.snippet ?? "(요약 없음)",
      origin: "google",
    }));
  } catch {
    return [];
  }
}

// ── 데모 폴백 ────────────────────────────────────────────────
function demoResults(query: string): SearchHit[] {
  return [
    {
      title: `[데모] ${query} 관련 선행특허 A`,
      source: "KR10-2019-0000001",
      pubDate: "2019-01-15",
      summary: `[데모] ${query}의 기본 구성을 개시하는 선행 문헌. KIPRIS_API_KEY 환경변수를 설정하면 실제 결과가 나옵니다.`,
      origin: "kipris",
    },
    {
      title: `[데모] ${query} 개선 방법`,
      source: "US20200000001A1",
      pubDate: "2020-06-20",
      summary: `[데모] ${query}의 효율 개선 기법을 다루는 미국 특허. SERPAPI_KEY 설정 시 Google Patents 실검색됩니다.`,
      origin: "google",
    },
  ];
}

/**
 * 키워드로 KIPRIS·Google Patents를 병렬 검색하고 결과를 합친다.
 * 두 API 모두 키가 없으면 데모 폴백을 반환한다.
 */
export async function searchPriorArt(
  query: string,
  maxEach = 5
): Promise<SearchHit[]> {
  const [kiprisHits, googleHits] = await Promise.all([
    searchKipris(query, maxEach),
    searchGoogle(query, maxEach),
  ]);

  const combined = [...kiprisHits, ...googleHits];
  return combined.length ? combined : demoResults(query);
}
