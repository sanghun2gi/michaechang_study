# AI 특허출원 대시보드 (MVP · 1차 스프린트)

발명 아이디어를 입력하면 **등록 가능성 진단 + 명세서·청구항 초안 + 할루시네이션 검증**을
생성하는 SaaS의 1차 스프린트 MVP입니다. 설계 문서: [`docs/AI_patent_app_product_and_dev_plan.md`](docs/AI_patent_app_product_and_dev_plan.md)

> ⚖️ 본 서비스는 출원 준비를 돕는 초안·진단·참고 도구입니다. 특허등록을 보장하지 않으며,
> 변리사·변호사의 법률 자문을 대체하지 않습니다.

## 구현 범위 (문서 B-3 1차 스프린트)

| # | 기능 | WORKFLOW | 위치 |
|---|------|----------|------|
| 1 | 프로젝트 세팅 (Next.js + TS + Tailwind + Prisma) | — | 루트 |
| 2 | 발명 입력 폼 + 구조화 카드 | STEP 1 / 3 | `components/InventionForm.tsx`, `lib/server/draft.ts` |
| 3 | 명세서·청구항 초안 생성 (서버 AI 호출) | STEP 18 | `lib/server/draft.ts`, `app/api/draft/route.ts` |
| 4 | 할루시네이션 검증 (GREEN/YELLOW/RED) | STEP 19 | `lib/server/draft.ts`, `components/TagBadge.tsx` |
| 5 | Provenance Ledger 기록 래퍼 | STEP 0B | `lib/server/ledger.ts` |
| 6 | 법적 경계 문구 전역 표시 | A-1 | `components/LegalBanner.tsx` |

## 아키텍처 원칙 (CLAUDE.md 절대규칙)

- **AI 호출은 전부 서버에서만** — `app/api/draft/route.ts` → `lib/server/*`. 키는 클라이언트로 나가지 않습니다.
- **모든 AI 판단은 원장에 기록** — `withLedger()` 래퍼가 STEP3/18/19 호출을 감쌉니다.
- **법적 문구 전역** — `LegalBanner`가 `layout.tsx`에 고정되어 모든 화면에 노출됩니다.

## 실행

```bash
npm install
cp .env.example .env        # ANTHROPIC_API_KEY 입력 (선택)
npx prisma generate
npm run dev                 # http://localhost:3000
```

- `ANTHROPIC_API_KEY`가 **있으면** 실제 Claude API로 초안·검증을 생성합니다.
- **없으면** 규칙 기반 데모 폴백(`lib/server/fallback.ts`)으로 동작하여 키 없이도 흐름을 확인할 수 있습니다.
- `DATABASE_URL`이 없으면 원장은 인메모리로 기록됩니다(데모용). 운영 시 `npx prisma db push`로 PostgreSQL 연결.

## 다음 단계 (문서 B-3 2차 스프린트)

Evidence DB · All Elements Matrix · 용어사전/안티센던트 · Claim Ladder · 가상 OA · 전문가 리뷰·승인 게이트.
