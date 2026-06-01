# 프로젝트: AI 특허출원 대시보드

## 무엇
발명 입력 → 등록 가능성 진단 + 명세서/청구항 초안 + 가상 OA를 만드는 SaaS.
상세 설계는 /docs/AI_patent_app_product_and_dev_plan.md 참조.

## 스택
- Next.js 14 App Router + TypeScript
- Tailwind CSS
- Prisma + PostgreSQL
- Anthropic API (서버 사이드 전용)

## 절대 규칙
1. AI API 키·Agent 프롬프트를 클라이언트로 보내지 말 것. 모든 AI 호출은 서버에서.
2. 모든 AI 판단 함수는 LedgerRecord에 근거를 기록할 것 (recordLedger 래퍼 사용).
3. UI 어디에도 "등록 보장 / 법률 자문" 표현 금지. "초안·진단·참고" 로만.
4. 사용자 카드정보를 직접 다루지 말 것. 결제는 Stripe 위탁.
5. 발명정보는 영업비밀 — 테넌트(Organization)별로 데이터 격리.
6. 파일은 기능별 폴더로. 한 파일 300줄 넘으면 분리 제안.

## 코딩 컨벤션
- 타입은 명시적으로. any 금지.
- 서버 로직은 lib/server, API는 app/api/, UI는 components/.
- 커밋은 작게, 기능 단위로.

## 현재 작업 단계
1차 스프린트: 발명 입력 → 초안 생성 → 할루시네이션 검증.
