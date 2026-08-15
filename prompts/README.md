# CORS RINEX 30초 GNSS 전파교란 분석 실행 프롬프트

- `CORS_RINEX30S_GNSS_interference_V7_parallel.md` — 현재 판(V7). V6 계약을 그대로 계승하고, **이 계약의 작업을 역할이 다른 여러 워커 프로세스가 나누어 동시에 수행**할 수 있도록 병렬 실행 계약(39~41절)을 추가했다.

## 핵심 설계

- **병렬화 축 3가지**: 데이터 병렬(station×day 파티션) / 역할 병렬(독립 단계 동시 실행) / 구현 병렬(모듈 분담)
- **하드 배리어 3개**: B1 인벤토리·품질 완료 → B2 기준선 동결 → B3 blind freeze. 통과 선언은 orchestrator만.
- **pull 모델 작업 큐**: `queue/`에 결정적 `task_id`, 원자적 상태 전이, 리스·heartbeat, 재시도·poison 격리
- **워커 12역할**: `orchestrator`, `W_INV`, `W_QC`, `W_EXT`, `W_FEAT`, `W_BASE`, `W_DET`, `W_NET`, `W_FALS`, `W_VAL`(unblinded, 별도 프로세스), `W_FIG`, `W_REP`(항상 1개)
- **불변성**: `--shards N`·`--workers M`을 바꿔도 산출물 해시 동일. 다르면 성능 문제가 아니라 정확성 결함.

## 병렬화하면 결과가 달라지는 지점 (단일 워커 강제)

기준선·임계값 확정, blind freeze, NetworkEvent 병합·clustering 최종 실행, 공간 가중행렬 선택과 다중검정 보정 범위, claim registry·보고서 수치 확정.

## 반드시 처리해야 하는 두 가지 함정

1. **경계(halo)**: 일자·시간블록으로 자르면 창 특징·ROTI arc·StationEvent·NetworkEvent가 경계에서 잘린다. → 읽기 패딩 + 자기 구간만 쓰기 + 단일 reduce 재병합(`boundary_open` → `boundary_merged`)
2. **분산 집계**: count·sum은 합산되지만 median·MAD·분위수는 파티션별로 구해 평균낼 수 없다. → 2-pass 또는 병합 가능한 스케치(t-digest 등) + 정확값 대비 오차 보고

## V6 → V7 변경 위치

| 위치 | 변경 |
|---|---|
| 머리말 | 버전 V7, 워커 1개일 때의 최소 적용, V7 개정 요약 13항 |
| 명령 우선순위 | 병렬화를 5순위로 명시(배리어·불변성이 우선) |
| 역할 | `worker_id`/`role`/`shard`/`blind_status` 선언, 동시 실행 프로세스는 단일 역할 |
| 작업·안전 원칙 | 6항(단일 writer) 확장 + 11~14항(provenance·파티션 소유·배리어·backpressure) |
| 프로젝트 구조 / 13절 | `queue/`, `locks/`, `runs/<run_id>__<worker_id>/`, `validation_unblinded/`, `WORKER_STATUS.md` |
| 14절 설정 | `parallel_execution:` 블록(역할별 워커 상한·샤딩·큐·배리어·halo·집계·자원·격리) |
| 15.1절 | `WORKER_STATUS.md`, 큐 상태 기반 재개, handoff에 배리어·task 통계 |
| 22.6절(신설) | 블라인드 워커 프로세스 격리(`W_VAL` 별도 프로세스·별도 경로·B3 이후 생성) |
| 27절 | manifest에 `worker_id`/`task_id`/`shard_*`, 리스 기반 잠금, 샤드·워커 수 무관 결정성 |
| 28.10절(신설) | 병렬 실행 시험(불변성·큐 원자성·배리어·경계·집계 근사·격리·backpressure) |
| 29절 | `plan`, `worker --role`, `queue status`, `barrier declare`, `reduce`, `promote`, `requeue` |
| 30·32·33·34절 | 후보·claim에 워커 provenance, `PARALLEL_EXECUTION_PLAN.md`, 게이트 선언 주체 |
| 36·37절, 최종 산출물 | 병렬 실행 체크리스트, 응답 항목 22~27, `reports/16_parallel_execution_report.md` |
| 39절(신설) | 병렬화 축·단계별 shard key 표·배리어·작업 큐·역할 정의·결정성·halo·분산 집계·자원·실패 격리·승격·금지사항 |
| 40절(신설) | 실행 런북 — 40.1 데이터 처리 병렬(명령 순서), 40.2 구현 작업 병렬(인터페이스 동결 → 모듈 소유권 → 병합 순서), 40.3 최소 구성과 확장 |
| 41절(신설) | 검증·성능 계약 — 직렬로 정확성 확보 후 R3에서 병렬 도입, 불변성·경계·집계 시험, 스케일 효율 실측 |
| 실행을 시작하라 | R1·R2는 워커 1개 직렬, R3에서 큐·배리어·샤딩 도입, 불변성 통과 후에만 워커 증설 |
