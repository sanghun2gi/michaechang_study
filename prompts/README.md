# CORS RINEX 30초 GNSS 전파교란 분석 실행 프롬프트

- `CORS_RINEX30S_GNSS_interference_V7_multi_author.md` — 현재 판(V7). V6 계약을 그대로 계승하고 **여러 명의 작성자(사람 연구자 + 코딩 에이전트)가 동시에 실행**할 수 있도록 협업 계약을 추가했다.

## V6 → V7 변경 요약

과학 분석 절차(단계 0~11, 12~38절)는 삭제·완화 없이 유지했고, 다음이 추가·수정되었다.

| 위치 | 변경 |
|---|---|
| 문서 머리말 | 버전 V7, 1인 작업(`solo_mode`) 최소 적용 규칙, V7 개정 요약 13항 |
| 명령 우선순위 | 3순위에 「다중 작성자 무결성」 추가 (개인 진도보다 우선) |
| 역할 | 단일 수석 연구자 → `author_id`/`blind_status`/역할군 9종, 생산자·승인자 겸직 금지 |
| 작업·안전 원칙 | 6항 확장(리스 없는 쓰기 금지) + 11~14항 신설(등록·supersede·방화벽·자기승인 금지) |
| 프로젝트 구조 / 13절 | `config/authors.yaml`, `config/overrides/`, `coordination/`, `locks/`, `runs/`, `shared/`, `AUTHORS.md` |
| 14절 설정 | `collaboration:` 블록(리스·승격·이중검토·방화벽·override 거버넌스), `contract_version: 'V7'` |
| 15.1절 | 협업 원장 6종 추가, `PHASE_HANDOFF.md`에 소유자·검토자·리스·인수인계 필드 |
| 22.6절(신설) | 작성자 수준 블라인드 방화벽, 위반 시 `blind_integrity=compromised` 처리 |
| 27절 | partition manifest에 `author_id`·리스·승격 필드, 리스 기반 잠금·시계오차 규칙, 작성자 독립 결정성 |
| 28.10절(신설) | 동시성·교차 작성자 재현·방화벽·승격 검증 시험 |
| 29절 | `claim/release/claims/lock-status/promote/review/sync-status/verify-collab`, `--author` 필수 |
| 30절 | 후보표·검토표에 생산자/검토자/조정자, 이중검토 비율과 검토자 간 일치도 보고 |
| 32.1절 | claim registry에 `author_id`·`verified_by_author_id`·supersede 열 |
| 33절 | `AUTHOR_REGISTRY.csv`, `COLLABORATION_PROTOCOL.md`, `CONTRACT_OWNERS.csv`, 분석자 자유도 한계 4항 |
| 34절 | 게이트별 구현자·승인자 분리 의무, 불가 시 `deferred_review` |
| 36·37절, 최종 산출물 | 협업 체크리스트, 응답 항목 22~27, `reports/16_collaboration_and_integrity.md` |
| 39절(신설) | 다중 작성자 협업 계약 12개 소절(등록·청구·리스·충돌·승격·원장·방화벽·이중검토·설정·병렬화 축·인수인계·금지사항) |
| 40절(신설) | 공동저자권·CRediT 기여표·저자 순서·AI 도구 공개·분쟁·가용성 책임 |
| 41절(신설) | 계약 문서 자체의 공동 개정 절차·버전/해시 규칙·축약 금지 |
| 실행을 시작하라 | 작성자 확정·작업 청구를 1~2번으로, 종료 시 리스 해제·인수인계를 마지막 단계로 |

## 새 작성자가 처음 할 일

1. `config/authors.yaml`에 `author_id`·역할·`blind_status` 등록 (에이전트는 `operated_by` 필수)
2. `coordination/WORK_CLAIMS.csv`에서 남은 범위를 청구하고 리스 획득
3. `runs/<run_id>__<author_id>/`에서 작업, 게이트·검토 통과 후 승격
4. 종료 시 리스 해제 + `PHASE_HANDOFF.md`·`coordination/HANDOFF_LOG.md` 기록
