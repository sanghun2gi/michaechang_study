/goal `E:\worldtechRnD\Pro_phd_data\rinex\Daily`의 실제 CORS RINEX 명목 30초 자료를 읽기 전용으로 전수 감사하고, 파일에서 확인되는 실제 기간(사용자 설명상 예상 2021~2026년)에 대해 GNSS 전파교란 **후보**를 탐색·반증·외부검증하는 재현가능한 연구 시스템을 완성하라. `analysis_cutoff_utc = min(configured_end_utc, latest_valid_observation_epoch)`로 고정하고, 2026년이 완전년도임이 입증되지 않으면 반드시 `2026 YTD`로 표기하라. 아래의 모든 단계·테스트·과학적 제한·산출물·완료 게이트를 충족하여 전체 실제기간 분석과 한국어 최종보고서 생성까지 계속하라. 경로 접근이나 자원 부족으로 전체 실행이 불가능할 때만 검증된 최대 단계, 정확한 중단 사유, 실측 처리량, 안전한 재개 명령과 다음 완료조건을 남기고 멈춰라.

# CORS RINEX 30초 GNSS 전파교란 분석 실행 프롬프트

## V7.1 — 병렬 실행 + 미규정 사례·세션·실측 반영판

> **버전 계보**: V6(규모실행·과학검증·국제표준 정합 보강판)의 모든 조항을 계승하고, V7에서 **역할이 다른 여러 워커 프로세스의 병렬 실행 계약(39~41절)**을, V7.1에서 **미규정 사례·실행 세션·실측 반영 계약(42~44절)**을 추가한 판이다. V6·V7의 과학적 제한, 증거등급 상한, 블라인드 격리, 누출방지, 원시자료 보호 조항은 어느 것도 완화되지 않았다. 파일명과 문서 버전을 **V7.1**로 일치시키며 설정의 `contract_version: 'V7.1'`으로 이 문서를 식별한다.

> **워커가 1개일 때**: 39~41절은 `parallel_execution.max_total_workers: 1`로 두면 그대로 직렬 실행이 된다. 그래도 작업 큐·배리어·샤딩 키·`worker_id` 기록은 유지한다. 나중에 워커를 늘릴 때 코드와 산출물 구조를 바꾸지 않아도 되게 하기 위함이다.

> **V7.1의 전제**: 어떤 계약도 실제 데이터의 모든 사례를 미리 규정할 수 없다. 그래서 이 개정은 조항을 늘리는 대신 **규칙이 없는 상황을 만났을 때의 규칙(42절)**, **실행 컨텍스트가 끊길 때의 규칙(43절)**, **사전 감사에서 드러난 이 자료의 실제 특성(44절)** 을 추가한다. 계약에 없는 상황에서 조용히 임의 처리하는 것이 이 프로젝트의 가장 큰 재현성 위험이다.

이 문서는 계획서가 아니라 **실제 코드 작성, 실제 데이터 감사, 시험, R1→R5 규모 확장, 후보 반증, 외부검증, 최종보고서 생성까지 수행하게 하는 프로젝트 실행 계약**이다.

### 이번 개정(V7.1)에서 보강된 사항

1. **미규정 사례 처리 계약(42절)**: 계약에 규칙이 없는 상황에서 멈추지도 임의로 정하지도 말고, `docs/UNSPECIFIED_CASES.csv`에 기록하고 **보수적 기본값**(제외 대신 격리, 추정 대신 `unassessable`, 병합 대신 분리, 승격 대신 보류)을 적용한 뒤 계속한다. 같은 사례가 누적되면 그 자체가 계약 개정 요청이다.
2. **에이전트 세션 계약(43절)**: 실행 컨텍스트가 바뀌어도 판단이 유실되지 않도록 `session_id` 기록, 세션 시작 시 필수 읽기, 세션 종료 시 판단 기록 의무, 불변 조항 상시 주입, **세션 안에서 `blind_status`를 바꾸지 않는 규칙**을 둔다.
3. **관측 세션(자정) 경계 계약(44.1절)**: 일 단위 파일 경계에서 arc·모호도·clock이 재초기화되는 물리적 효과를 데이터 파이프라인 이상과 분리해 다루고, **파일·세션 단위 중심화를 금지**하며 자정 인접 사건 비율을 별도 보고한다.
4. **canonical 파일 선택 규칙(44.2절)**: 같은 station-day에 형식이 다른 파일이 공존할 때 무엇을 쓸지 정의한다. 사전 감사에서 실제로 확인된 사례다.
5. **항법자료 병합 계약(44.3절)**: 다수 nav 파일의 중복 ephemeris 제거, health·age 필터, 충돌 시 처리.
6. **관측소 코호트 정책(44.4절)**: 관측소 수가 늘어난 자료에서 연도 비교를 고정 코호트와 전체 중 무엇으로 할지 확정하고 둘 다 보고한다.
7. **위성군 coverage regime(44.5절)**: 가용 위성군이 늘어난 시점을 regime 경계로 삼아 '위성 수 급락' 검출기의 연도별 민감도 차이를 통제한다.
8. **분석집합 동결과 신규 자료(44.6절)**: 실행 중 자료가 늘어나도 동결된 기준선·blind freeze를 오염시키지 않고 새 run으로 분리한다.
9. **위성×epoch 저장 전략(44.7절)**: 수십억 행을 전량 저장하지 않고 스트리밍 누산기 + 사건창 전량 + 정상 층화표본으로 처리한다.
10. **후보율 가드·처리량 게이트(44.8절)**: 후보율이 기대 범위를 벗어나면 임계값을 조용히 조정하지 말고 중단·원인규명한다. 전체 예상 소요가 상한을 넘으면 다음 규모로 진입하지 않고 병목을 먼저 고친다.
11. **수동검토 표본·캐시·로그 운영(44.9~44.10절)**: 후보가 많을 때의 층화표본 규칙, 해제 캐시 수명·용량 상한, 로그 폭증 방지.

이 개정은 새로운 과학적 요구를 추가하지 않는다. 기존 조항이 다루지 못한 **실행 중 판단 공백**을 메우는 것이 전부이며, 과학적 제한·증거등급 상한·누출방지·원시자료 보호는 그대로다.

### 이전 개정(V7)에서 보강된 사항

목적은 하나다. **역할이 다른 여러 프로세스(워커)가 이 계약의 작업을 나누어 동시에 수행해도 결과가 직렬 실행과 동일해야 한다.** 병렬화는 속도 최적화이며, 어떤 경우에도 과학적 제한·게이트·블라인드 격리보다 앞설 수 없다.

1. **실행 DAG와 병렬화 축 정의**: 각 단계의 작업 단위(shard key), 병렬 가능 여부, 선행 의존성, 하드 배리어를 표로 고정한다. → 39.1~39.3절
2. **작업 큐와 pull 모델 워커**: `queue/tasks.*`에 원자적 상태 전이(pending→leased→done/failed/poison)를 두고, 워커가 자기 역할에 맞는 task를 가져간다. → 39.4절
3. **워커 역할 계약**: `orchestrator`, `W_INV`, `W_QC`, `W_EXT`, `W_FEAT`, `W_BASE`, `W_DET`, `W_NET`, `W_FALS`, `W_VAL`, `W_FIG`, `W_REP`의 책임·쓰기 범위·병렬도를 분리한다. → 39.5절
4. **샤드·워커 수 불변성**: shard 배정은 내용 해시 기반으로 하고, `--shards N`과 `--workers M`을 바꿔도 ID와 수치가 같아야 한다. → 39.6절, 41.2절
5. **경계(halo) 처리 계약**: 창 특징·ROTI arc·StationEvent·NetworkEvent가 일자·시간블록 경계에서 잘리지 않도록 패딩과 재병합 reduce를 강제한다. → 39.7절
6. **분산 집계 규칙**: count·sum은 합산하되 median·MAD·분위수는 2-pass 또는 스케치로만 결합하고 오차를 검증한다. 기준선(단계 5)의 병렬화 핵심이다. → 39.8절
7. **하드 배리어 3종**: (B1) 인벤토리·품질 완료 전 특징 확대 금지, (B2) 기준선 동결 전 탐지 금지, (B3) blind freeze 전 공식 사건자료 사용 금지. 배리어 통과는 orchestrator만 선언한다. → 39.3절
8. **블라인드 워커 격리**: `W_VAL`은 별도 프로세스·별도 출력경로로 실행하고, 블라인드 워커와 큐·캐시·산출물을 공유하지 않는다. → 39.5절, 22.6절
9. **자원 예산과 backpressure**: 단계별 CPU/IO 바운드 특성, 워커당 peak RSS, 디스크 여유 기반 lease 중단, 외부 다운로드 single-flight. → 39.9절
10. **실패 격리**: task 단위 재시도·poison 격리로 한 파일이 전체 실행을 멈추지 않게 하고, 격리 목록을 보고서에 명시한다. → 39.10절
11. **역할별 실행 런북**: 데이터 처리 병렬(프로세스)과 구현 작업 병렬(모듈 분담)을 분리한 구체적 실행 순서와 명령. → 40절
12. **병렬 실행 검증·성능 계약**: shard/worker 불변성 시험, 배리어 위반 탐지, 경계 사건 시험, 스케일 효율 실측. → 41절
13. **협업 안전장치 최소본**: `worker_id` provenance, 리스 기반 단일 writer, 승격(promotion), 생산자와 다른 검토자에 의한 후보 판정. → 39.4·39.11절, 30절, 34절

병렬화 때문에 결과가 달라지면 그것은 성능 문제가 아니라 **정확성 결함**이다. 재현되지 않으면 워커 수를 1로 낮추고 원인을 찾은 뒤 다시 확장한다.

### 이전 개정(V6)에서 보강된 사항

국제 측지·항법 학술지(GPS Solutions, Journal of Geodesy, IEEE T-AES/T-GRS) 게재 및 국제기구(ICAO, ITU, IGS) 권고 부합을 목표로 다음을 본문 각 해당 단계에 통합했다.

1. **국제기구 표준 용어 정합**: ICAO Doc 9849 / Annex 10의 RFI 보고·대응 용어와 정합하되, 30초 RINEX로 narrowband·barrage·chirp 파형을 직접 식별하지 말고 `band-selective observation pattern`, `multi-band observation pattern`, `temporally unresolved`로 제한한다. ITU-R M.1901은 RNSS 관련 권고 안내, M.1902/M.1903/M.1905는 대역별 보호기준 문맥으로 정확히 구분한다. → 단계 9, 23절, 최종 산출물
2. **우주기상·자연 교란 분리 고도화 (Solar Cycle 25 대응)**: ROTI, IGS GIM, Kp/Dst 지수 자동 수집·대조와 `space_weather_alert` 플래그. → 단계 3, 단계 4, 21.3절
3. **주파수대역별·위성군별 차분 분석**: L1/E1 vs L2 vs L5/E5a Tracking Ratio, CDMA(GPS) vs FDMA(GLONASS) 간섭 내성 차이 피처. → 신설 4.5절
4. **외부 검증 데이터원의 국제적 확장**: NOTAM, NAVAREA XI 항행경보, AIS 위치이상 집계, ICAO EUR/NAT 사건기록. → 단계 8, 22.2절
5. **공간 통계 정량화**: Moran's I / Geary's C, 순열 p-value, 거리–동조성·semivariogram, 최대연결거리·고립 관측소 민감도. → 단계 7, 20.6절 연계
6. **설정 계약 확장**: `space_weather`, `frequency_profiling`, `spatial_statistics`, `external_validation_sources` 블록. → 14절
7. **추가 보완(검토 과정에서 식별)**: (a) 확장 외부출처의 `source_tier`·`advisory_or_confirmed` 구분과 "advisory 단독 출처로 E4 금지" 규칙, (b) Kp 3시간·Dst 1시간 해상도 및 GLONASS FDMA bias·ROTI≠S4 등 신규 지표 자체의 한계 명문화, (c) 대역차분 피처의 독립 특징군 중복 계상 금지와 인벤토리 확인 관측코드 조건, (d) 공간 가중행렬 민감도·순열검정·다중검정 보정 요구, (e) 학술지 제출 대비 표준 용어 정합표(`reports/13`)와 데이터·코드 가용성 서술(`reports/14`) 산출물. → 각 해당 절
8. **RINEX 2↔3/4 조화 계약**: 3자리 관측코드·추적 속성·실제 주파수를 기준선 키에 포함하고, RINEX 2에서 유일하게 복원할 수 없는 추적모드는 `legacy_ambiguous`로 격리한다. → 4.2절, 16.2~16.3절, 19절
9. **ROTI·공간통계·GLONASS 안정성 계약**: 연속 arc·LLI·cycle slip·coverage를 통과한 ROTI만 사용하고, 섬·연안 관측소에 대한 최대연결거리·고립노드 정책과 시간 유효 GLONASS FDMA channel fallback을 강제한다. → 3.1절, 4.5절, 7단계, 14절
10. **SCI 논문 3편·박사논문 집필 지원 계약**: 논문별 독립 RQ·primary endpoint·claim ID·중복 공개를 강제하고 R4/R5 후 `Publication Viability Gate`에서 논문별 생존·병합 여부를 결정한다. → 38절
11. **(V6 신규) 위성군 coverage 정합**: 한국 상공 가시성이 높은 QZSS(J)와 SBAS(S, KASS 포함)의 관측 존재를 인벤토리에서 확인하고 포함/제외 정책을 설정으로 명시한다. → 단계 1, 4.5절, 14절
12. **(V6 신규) 대역 해석 함정 명문화**: BDS B1I(1561.098 MHz)≠B1C/L1(1575.42 MHz) 별칭 금지의 본문 규정, L2 semi-codeless(L2W) 추적 특성으로 인한 대역차분 오해석 방지. → 4.5절, 단계 11
13. **(V6 신규) 귀속(attribution) 금지 계약**: 송신원 위치뿐 아니라 행위자·국가·기관 귀속도 이 자료로 불가능함을 과학적 제한과 금지 표현에 명시. → 과학적 제한, 31.4절
14. **(V6 신규) 수신기 간섭완화 마스킹 제한**: AGC·notch filter 등 수신기 내부 완화기능이 약한 간섭을 관측에서 은폐할 수 있다는 검출한계(위음성) 명문화. → 과학적 제한, SCIENTIFIC_LIMITATIONS
15. **(V6 신규) matched control 우주기상 매칭**: 대조구간 선정 조건에 유사 지자기 활동 수준을 추가해 Solar Cycle 25 혼란변수를 대조 설계에서도 통제. → 22.3절
16. **(V6 신규) 좌표 기준계 확인**: 관측소 좌표의 datum/기준계(ITRF 실현·국가기준계) 확인과 불일치 기록. → 단계 3

각 보강 항목에도 기존의 과학적 제한 원칙이 동일하게 적용된다. 특히 새 지표(ROTI, Moran's I, Tracking Ratio)의 임계값은 모두 `configured` 상태이며 실제 데이터 교정 전에는 과학적 사실이 아니다.

아래 전체 내용을 Codex 또는 동등한 코딩 에이전트에게 제공한다. 일부 예시 코드나 파일럿 계획만 제시하고 멈추지 말고, 각 Phase의 완료 게이트를 통과하면서 안전하게 가능한 최대 규모까지 실행한다.

## 명령 우선순위

충돌하는 요구가 있으면 다음 순서를 따른다.

1. 원시자료와 사용자 파일 보호, 접근권한, 보안
2. 관측된 사실과 추정의 분리, 과학적 제한, 허위 수치 금지
3. Phase 완료 게이트, 재현성, 누출 방지, 검증 계약, **배리어와 샤드 불변성**
4. 전체 규모 실행과 산출물 완성
5. 병렬화와 성능 최적화, 표현 개선

병렬 실행은 5순위다. 배리어를 앞당기거나 기준선을 워커별로 따로 만들어 속도를 얻지 마라. 병렬 실행 결과가 직렬 실행과 다르면 병렬 실행을 멈추고 원인을 먼저 해결한다.

다음 상태어를 실행로그와 보고서에서 일관되게 사용한다.

- `observed`: 실제 파일·실행·1차 출처에서 확인
- `derived`: 관측값으로 계산되며 입력과 산식으로 재현 가능
- `configured`: 설정 후보값이며 보편적 임계값이 아님
- `assumed`: 확인 전 작업 가정
- `unavailable`: 필요한 자료가 없거나 접근 불가
- `unassessable`: 자료는 있으나 해당 주장을 판정할 증거가 부족

경로, 2021~2026년, 30초 간격은 사용자가 알려준 시작점이다. 헤더와 실제 epoch로 확인하기 전에는 `observed`로 승격하지 마라.

---

# 역할

당신은 GNSS 측지·항법, CORS 망 분석, RINEX 2/3/4, GNSS 신호품질 관리, 전파간섭 탐지, 시계열 이상탐지와 재현가능 연구 소프트웨어에 숙련된 수석 연구자이자 데이터 엔지니어다.

이 계약의 작업은 **역할이 다른 여러 워커 프로세스가 나누어 동시에 수행**한다. 실행을 시작할 때 자신이 어떤 워커로 도는지 확정하고 모든 산출물에 기록하라.

```text
worker_id            # 예: w_feat_03 (역할_일련번호)
role                 # orchestrator | W_INV | W_QC | W_EXT | W_FEAT | W_BASE |
                     # W_DET | W_NET | W_FALS | W_VAL | W_FIG | W_REP
shard_index/shard_count
blind_status         # blinded | unblinded (W_VAL만 unblinded)
run_id, host_id, pid
leased_task_ids
```

한 사람 또는 한 에이전트가 여러 역할을 순차로 수행할 수 있으나, **동시에 도는 프로세스는 하나의 역할만 맡는다.** 역할별 책임·쓰기 범위·병렬도는 39.5절에 있다. 워커를 1개만 쓸 때도 같은 구조로 실행한다.

다음 로컬 폴더의 실제 파일을 직접 감사하고, 2021년부터 2026년까지 수집된 것으로 알려진 CORS RINEX 30초 자료를 분석하여 GNSS 전파교란 의심 사건을 탐색·검증하는 재현가능한 분석 시스템을 구축하고 실제 자료에 실행하라.

- 원시자료 폴더: `E:\worldtechRnD\Pro_phd_data\rinex\Daily`
- 분석 결과 폴더: `E:\worldtechRnD\Pro_phd_data\rinex\analysis_30s_interference`
- 분석 대상 기간: 파일에서 확인되는 실제 최초 시각부터 실제 최종 시각까지. 2021~2026년이라는 설명을 그대로 믿지 말고 헤더와 관측 epoch로 검증한다.
- 기본 보고 언어: 한국어
- 시간 표기: UTC와 한국표준시(KST, UTC+9)를 함께 표기한다.
- 한글 그림 글꼴: Windows에서 사용 가능하면 `맑은 고딕`; 사용할 수 없으면 대체 글꼴과 이유를 실행기록에 남긴다.

# 최종 목표

단순히 RINEX 파일을 요약하는 데서 멈추지 말고 다음을 모두 완성하라.

1. 원시자료의 실제 기간, 관측소, RINEX 버전, 파일 형식, 표본간격, 위성군, 관측코드, 압축형식, 중복·결측·손상 여부를 전수 감사한다.
2. C/N0 또는 SNR, 관측 위성 수, 관측 공백, LLI, cycle slip, 코드·반송파·Doppler 일관성, 정적 CORS 위치·시계 잔차 등 실제로 이용 가능한 관측량을 추출한다.
3. 위성 고도각, 관측소·수신기·안테나 변경, 일변화·계절성, 다중경로, 전리층·우주기상, 파일·통신 장애 같은 혼란변수를 통제한다.
4. 단일 관측소 이상과 여러 관측소에서 동시에 발생하는 공간적 공통 이상을 분리한다.
5. 공식 사건정보를 보지 않는 블라인드 탐지와, 정부·ICAO 등 공식 사건시간을 이용한 외부검증을 엄격히 분리한다.
6. 각 후보 사건에 대해 재밍 유사, 스푸핑 유사, 비의도성 RFI 가능, 장비·환경·자료 이상 가능, 판정 유보 중 하나로 제한적으로 분류하고 대안 설명을 함께 제시한다.
7. 전체 코드, 설정, 테스트, 중간 산출물, 후보 사건표, 사건별 근거 그림, 최종 한국어 보고서를 작성해 다른 연구자가 재실행할 수 있게 한다.

# 가장 중요한 과학적 제한

이 제한은 어떤 이유로도 완화하거나 숨기지 마라.

- RINEX 관측자료는 RF 스펙트럼 또는 수신기 내부 진단자료가 아니다. 이 자료만으로 방해신호의 전력, J/S, 중심주파수, 대역폭, 변조방식, 방향, 송신원 위치를 직접 측정했다고 주장하지 마라.
- **행위자·국가·기관 귀속(attribution)은 이 자료로 불가능하다.** 송신원 위치뿐 아니라 특정 국가·조직·시설을 원인 주체로 지목하거나 암시하지 마라. 공식기관이 귀속을 발표한 사건을 인용할 때도 `당국 발표에 따르면`으로 한정하고 본 분석의 결론으로 승격하지 마라.
- **수신기 내부 간섭완화 기능(AGC 조정, notch/adaptive filter, 다중상관기 완화 등)은 약하거나 완화 가능한 간섭을 관측값에서 은폐할 수 있다.** 따라서 이 분석의 미탐지는 `간섭 부재`의 증거가 아니라 `이 관측체계에서 관측되지 않음`이다. 수신기 기종·펌웨어별 완화능력 차이가 관측소 간 반응 차이의 대안 설명일 수 있음을 반증·해석 단계에서 고려하라.
- 30초 표본은 30초보다 짧은 사건을 놓치거나 한두 epoch로만 남길 수 있다. 시작·종료시각과 지속시간의 해상도 한계를 모든 사건표와 보고서에 명시하라.
- RINEX의 `Sxx` 관측값과 1~9 SSI는 동일한 것이 아니다. 헤더의 `SIGNAL STRENGTH UNIT`, 관측코드, RINEX 버전을 확인한 뒤 단위를 해석하라. `Sxx`가 없을 때 SSI를 임의로 dB-Hz의 연속값처럼 사용하지 마라.
- LLI bit 0은 이전 관측 이후 loss of lock 및 cycle slip 가능성을, bit 1은 half-cycle ambiguity 가능성을 나타내지만, LLI 증가만으로 전파교란을 확정하지 마라.
- 단일 관측소의 파일 공백, 위성 수 감소 또는 SNR 저하만으로 재밍이라고 결론내리지 마라. 수신기 장애, 저장·통신 장애, 안테나 또는 펌웨어 변경, 주변 장애물, 기상과 다중경로를 먼저 검토하라.
- 고정 CORS의 30초 RINEX만으로 정교한 스푸핑 확정은 특히 어렵다. 상관기 왜곡, AGC, 원시 IQ, 다중 peak, 수신기 내부 PVT·clock diagnostic가 없으므로 결과 명칭은 원칙적으로 `스푸핑과 양립 가능한 이상(spoofing-compatible anomaly)`으로 제한한다.
- RINEX 2의 2자리 관측코드는 RINEX 3/4의 추적 속성을 유일하게 복원하지 못할 수 있다. 수신기·펌웨어·변환기 근거 없이 `S1`을 `S1C`, `S1W`, `S1X` 중 하나로 임의 매핑하지 마라.
- `C1C`/`C1W`는 의사거리, `S1C`/`S1W`는 신호강도 관측값이다. 관측 family가 다른 코드를 하나의 기준선으로 비교하지 마라. `X`의 추적 의미도 위성군별로 다르므로 일반화하지 마라.
- IGS GIM은 30초 국지 사건의 직접 검증 센서가 아니라 광역 전리층 배경 자료다. 또한 1차 전리층 코드·반송파 지연의 `f^-2` 관계를 C/N0 저하·tracking loss·scintillation 진폭에 직접 적용하지 마라.
- `전파교란 확정`은 RINEX 이상만으로 부여하지 마라. 공식기관의 동일 시공간 사건기록, 독립 RF 센서 또는 통제실험 같은 외부 증거가 있어야 한다.
- 이상탐지 모델의 높은 점수는 원인 규명이 아니다. 모든 후보에 관측 근거, 반증, 대안 설명, 데이터 품질과 불확실성을 기록하라.
- 관측소, 날짜, 수치, 파일 수, 성능지표, 사건을 추정하거나 만들어내지 마라. 실제 파일 또는 출처로 확인하지 못한 항목은 `확인 필요` 또는 `자료 없음`으로 기록하라.

# 작업 및 안전 원칙

1. `Daily` 폴더와 그 아래 모든 원시파일은 읽기 전용으로 취급한다. 이름변경, 이동, 압축해제 덮어쓰기, 수정, 삭제를 금지한다.
2. 생성물은 모두 별도 결과 폴더에 쓴다. 임시 압축해제 파일은 결과 폴더의 `cache`에 두고 원본과 SHA-256 또는 파일 크기·수정시각의 연결관계를 기록한다.
3. 기존 코드·보고서·결과가 있으면 완성되었다고 가정하지 말고 먼저 감사한다. 검증된 부분은 최대한 재사용하되, 검증되지 않은 결과는 새 결과와 분리한다.
4. 전체 파일을 메모리에 한꺼번에 적재하지 마라. 헤더 전수조사 후 일자·관측소 단위 스트리밍 또는 청크 처리와 Parquet 파티션을 사용한다.
5. 긴 실행은 재시작 가능하고 멱등적이어야 한다. 이미 정상 완료된 파티션은 해시와 설정이 같을 때 건너뛰고, 실패한 파티션만 다시 실행한다.
6. 서로 다른 워커·에이전트·프로세스가 같은 산출물을 동시에 수정하지 않도록 한다. 하나의 파티션에는 하나의 writer만 둔다(39.4절 작업 큐와 리스). 읽기는 잠금 없이 자유롭다.
7. 분석을 시작하기 전에 사용 가능한 디스크, CPU, RAM을 기록하고 예상 임시공간과 출력용량을 계산한다. 여유공간이 안전마진을 충족하지 못하면 원시자료를 건드리지 말고 축소 실행 및 필요한 공간을 보고한다.
8. 광범위한 질문을 먼저 던지고 멈추지 마라. 실제 폴더를 먼저 읽기 전용으로 감사하고 합리적인 기본값으로 파일럿을 완성하라. 경로 접근 불가, 암호화 파일, 필수 권한 부족처럼 실제로 진행 불가능한 경우에만 정확한 오류와 필요한 조치를 보고한다.
9. 작업 중 `PROGRESS.md`, `DECISIONS.md`, `SURPRISES.md`, `RUN_LOG.md`를 계속 갱신한다. 중단되더라도 이 네 파일과 설정만으로 재개할 수 있어야 한다.
10. `TODO`, 빈 함수, 가짜 데이터, 임시 성공처리로 완료를 선언하지 마라.
11. 모든 실행은 `worker_id`·`role`·`run_id`를 기록한다. 어떤 산출물이 어떤 워커·샤드에서 나왔는지 추적할 수 없으면 신뢰하지 않는다.
12. 워커는 자신이 lease한 task의 출력 경로에만 쓴다. 타인의 파티션은 읽기만 하고 조용히 재계산해 덮어쓰지 않는다.
13. 배리어(39.3절)를 워커가 스스로 넘지 않는다. 통과 선언은 orchestrator만 한다.
14. 병렬 실행 중 자원 부족·디스크 포화가 발생하면 새 task lease를 멈추고 진행 중 task를 정상 종료시킨다. 강제 종료로 부분 산출물을 남기지 마라.
15. **계약에 규칙이 없는 상황을 만나면 임의로 정하지 말고 42절을 적용한다.** 기록 없이 내린 임시 판단은 이 프로젝트에서 가장 흔한 재현성 결함이다.
16. 세션(실행 컨텍스트)이 끊길 조짐이 있으면 모듈을 반쪽 구현하지 말고, 원자적 작업을 마무리·시험한 뒤 43절의 인계 기록을 남기고 깨끗한 경계에서 멈춘다.

# 프로젝트 구조

결과 폴더 아래에 최소한 다음 구조를 만든다. 실제 필요에 따라 하위파일을 추가할 수 있으나 역할을 바꾸지 마라.

    analysis_30s_interference/
      README.md
      pyproject.toml 또는 requirements-lock.txt
      config/
        analysis.yaml
        official_events_template.csv
      src/
        rinex_interference/
      tests/
      scripts/
      inventory/
      cache/
      data_quality/
      features/
      baselines/
      candidates/
      validation/
      figures/
      reports/
      logs/
      queue/
      locks/
      runs/
      PROGRESS.md
      DECISIONS.md
      SURPRISES.md
      RUN_LOG.md
      run_manifest.json

# 단계 0 — 환경·기존 자산 감사

작업 폴더와 상위 폴더에서 `AGENTS.md`, `CLAUDE.md`, `README`, 기존 분석 코드, 환경파일, 연구문서, 사건목록, 관측소 메타데이터를 찾고 적용 범위를 확인한다. 기존 사용자 변경사항을 보존한다.

Python 버전과 패키지 상태를 확인한다. 우선 고려 도구는 `georinex`, `xarray`, `numpy`, `pandas`, `pyarrow`, `scipy`, `statsmodels`, `scikit-learn`, `ruptures`, `matplotlib`, `seaborn`, `plotly`, `pyproj`이다. 실제 필요 없는 패키지는 설치하지 않는다. RINEX 점검·변환에는 사용 가능할 경우 GFZRNX와 Hatanaka 압축도구를 이용하되, 외부 실행파일이 없으면 Python 기반 대체경로를 구현한다. 도구 버전과 라이선스를 기록한다.

기존 연구 자산을 다음 세 부류로 목록화하라.

- 검증되어 그대로 재사용 가능한 것
- 재현 또는 수정 후 사용할 것
- 현재 연구와 무관하거나 근거가 부족해 제외할 것

산출물:

- `inventory/project_inventory.csv`
- `reports/00_existing_asset_audit.md`
- `logs/environment.txt`
- 초기 `run_manifest.json`

# 단계 1 — 헤더 중심 전수 인벤토리

먼저 모든 파일을 재귀적으로 열거하되 전체 관측본문은 읽지 않는다. `.rnx`, `.obs`, `.nav`, RINEX 2의 연도 접미 파일, `.crx`, `.d`, `.gz`, `.Z`, `.zip` 등 실제 확장자를 식별한다. 파일명만으로 유형을 확정하지 말고 헤더로 관측·항법·기상·미지원 파일을 판별한다.

각 파일에 대해 가능한 범위에서 다음을 기록한다.

- 절대경로가 아닌 원시자료 루트 기준 상대경로
- 파일 크기, 수정시각, 압축방식, 읽기 성공 여부, 오류유형
- RINEX 버전과 파일 유형
- marker/station 식별자와 표준화된 관측소 ID
- `TIME OF FIRST OBS`, `TIME OF LAST OBS`, time system, `INTERVAL`
- 실제 첫 epoch와 마지막 epoch의 표본 확인값
- receiver type/version, antenna type, approximate XYZ, antenna delta
- GNSS별 관측코드와 C/L/D/S 계열 보유 여부
- **위성군 식별자 전수 확인**: G/R/E/C 외에 J(QZSS), S(SBAS), I(NavIC) 관측의 존재 여부와 관측코드. 한국 관측소는 QZSS 가시성이 높고 KASS(한국형 SBAS) 운용 이후 SBAS 관측이 기록될 수 있다. 존재가 확인된 위성군은 14절 `constellations` 정책에 따라 분석 포함/제외를 결정하고, 제외하더라도 인벤토리에는 보유 사실을 기록한다.
- 파일명에서 읽은 연도·DOY와 헤더·epoch의 일치 여부
- 예상 epoch 수, 실제 epoch 수, 완전성, 중복 epoch, 역전시각, 30초 이외 간격
- 완전 중복, 내용이 다른 경로 중복, 잘린 파일, 손상 파일, 0 byte 파일

2021~2026 각 연도를 완전한 1년이라고 가정하지 마라. `analysis_cutoff_utc = min(configured_end_utc, latest_valid_observation_epoch)`를 manifest에 고정하고, 완전년도가 아닌 2026년은 YTD로 표기한다. 분석 실행시각 이후이거나 configured end를 넘는 epoch는 시계·파일 오류 후보로 격리하고 별도 검토 전에 분석 기간을 늘리는 근거로 사용하지 않는다. 연간 비교는 동일 DOY 범위 또는 유효 station-day/observation-hour로 노출량을 표준화한다.

전수 해시가 지나치게 비싸면 1차 인벤토리에서는 크기·수정시각·빠른 표본해시를 사용하고, 중복 의심파일과 분석에 실제 사용한 파일에는 SHA-256을 계산한다. 선택 기준을 기록한다.

산출물:

- `inventory/rinex_file_inventory.parquet`
- `inventory/rinex_file_inventory.csv`
- `inventory/station_year_coverage.csv`
- `inventory/observation_code_matrix.csv`
- `inventory/duplicate_and_corrupt_files.csv`
- `reports/01_data_inventory_report.md`

# 단계 2 — 데이터 품질 게이트와 분석 가능성 판정

관측소×일자 단위로 다음 품질지표를 계산한다.

- 30초 기준 예상 epoch 대비 관측률
- 가장 긴 공백, 공백 수, 비정상 간격 수
- GNSS별·신호별 유효 관측률
- 위성 수 분포와 급락 횟수
- S 관측값 또는 SSI 보유 여부와 단위 신뢰도
- LLI 보유 여부, bit별 건수
- dual-frequency 조합 가능 여부
- code/carrier/Doppler 보유 여부
- 항법파일 또는 정밀궤도에 의한 위성 고도각·방위각·SPP 계산 가능 여부
- 수신기·안테나·펌웨어·관측코드·좌표 변경 여부

다음 품질등급을 사용하되 임계값은 `analysis.yaml`에 두고 데이터 분포에 대한 민감도분석을 수행한다.

- Q0: 읽기 불가 또는 핵심 시각정보 불명
- Q1: 대규모 결측·불규칙 간격으로 사건분석 부적합
- Q2: 제한된 특징만 사용 가능
- Q3: 주요 SNR·tracking 특징 분석 가능
- Q4: 다중주파수·고도각 보정·잔차 분석까지 가능

Q0~Q1 파일은 삭제하거나 억지 보정하지 말고 제외 이유를 남긴다. SNR이 없는 관측소는 별도 특징세트로 처리하며 SNR을 추정 생성하지 않는다.

산출물:

- `data_quality/station_day_quality.parquet`
- `data_quality/metadata_change_points.csv`
- `reports/02_data_quality_and_feasibility.md`
- `reports/03_feature_availability_by_station.md`

# 단계 3 — 항법자료와 시간·좌표 표준화

로컬 항법 RINEX, BRDC, SP3, CLK 파일의 존재를 먼저 확인한다. 필요한 날짜의 항법자료가 없으면 다음 순서로 처리한다.

1. SNR·위성 수·LLI·관측공백처럼 궤도 없이 계산 가능한 분석은 계속한다.
2. 고도각 보정, geometry-free 조합 또는 정적 위치 잔차에 필요한 입력을 `reports/missing_inputs.md`에 기록한다.
3. 인터넷과 다운로드가 허용되는 실행환경이면 IGS/CDDIS 등 공식 저장소에서 필요한 최소 BRDC 파일만 받아 `cache/external`에 저장하고 URL, 취득시각, 파일해시를 기록한다. 비공식 출처는 사용하지 않는다.
4. 다운로드할 수 없으면 해당 특징은 `not_computed`로 남기고 대체 특징과 증거감소를 보고한다.

## 3.1 GLONASS FDMA channel 시간 유효 해결

GLONASS FDMA 파장 및 이중주파수 조합에 필요한 channel number `k`를 다음 우선순위로 해결한다.

1. 해당 관측 RINEX 헤더의 `GLONASS SLOT / FRQ #`
2. 동일 시점의 로컬 GLONASS 항법자료
3. IGS MGEX metadata의 시간 유효 `SATELLITE/PRN`과 `SATELLITE/FREQUENCY_CHANNEL` 조합
4. 미해결

PRN만을 key로 하는 현재 시점 정적 룩업을 금지한다. `SVN`, `PRN/slot`, `channel`, `valid_from_utc`, `valid_to_utc`, `source_url`, `source_version`, `retrieved_at_utc`, `sha256`를 갖는 스냅숈을 `cache/external/glonass_channels_YYYYMMDD.json` 또는 Parquet으로 보존한다. 사건 epoch가 유효기간에 포함되는 레코드만 조인하고 소스 우선순위·충돌·결측을 기록한다.

channel을 해결하지 못하면 가정값을 대입하지 말고 GLONASS의 파장 의존 특징·TEC 조합만 `not_computed` 처리한다. 위성 수, 신호강도, gap 등 channel 비의존 특징은 계속 산출하고 `feature_unavailable_reason=glonass_channel_unresolved`를 남긴다.

## 3.2 우주기상·전리층 참조자료 수집 (Solar Cycle 25 대응)

2024년 분석구간은 Solar Cycle 25 태양 극대기 발표 기간과 겹치며, 2025~2026년은 높은 활동이 지속될 수 있지만 전체를 기계적으로 `극대기`로 라벨하지 마라. 대규모 지자기 폭풍(예: 2024년 5월 G5급)과 전리층 교란이 다중 위성 tracking·lock에 영향을 줄 수 있으므로, 사건별 공식 지수와 실제 RINEX 관측을 대조한다.

- 지자기 지수: Kp(GFZ Potsdam 공식), Dst(Kyoto WDC), 가능하면 NOAA SWPC 경보 이력. provisional/definitive 버전 구분과 취득시각을 기록한다.
- 전리층 지도: IGS GIM(최종/신속) IONEX 파일. 필요한 최소 날짜만 `cache/external`에 저장하고 URL·해시를 남긴다.
- ROTI: 별도 다운로드가 아니라 본 자료의 30초 이중주파수 위상차분으로 직접 계산한다(4.5절). GIM·지수는 대조용이다.

다음 제한을 반드시 기록한다.

- Kp는 3시간, Dst는 1시간 해상도다. 30초 사건의 시각과 직접 비교할 수 없으며 기간 플래그로만 사용한다.
- IGS GIM은 광역·저해상도 배경자료이므로 30초 국지 사건의 시작·종료 시각이나 원인을 직접 확정하는 근거로 쓰지 않는다.
- 지수가 낮다는 이유로 국지 scintillation을 배제하지 말고, 높다는 이유로 인위적 교란을 자동 배제하지 마라(21.3절 원칙 동일).
- 우주기상 지수·GIM은 공식 사건정보가 아닌 공개 물리자료이므로 블라인드 트랙 A에서 사용해도 누출이 아니다. 단, 사용 여부와 버전을 `DECISIONS.md`와 threshold provenance에 남긴다.
- 자료를 받을 수 없으면 `space_weather_reference: unavailable`로 기록하고 해당 반증 단계는 `untestable`로 처리한다.

RINEX 헤더의 time system을 읽어 GPS time, UTC, GLONASS time, BDT, GST를 혼동하지 마라. 내부 기준시각을 명시적으로 하나로 통일하고, leap second 처리를 검증한 뒤 UTC와 KST 표시열을 생성한다. 단순히 모든 원시시각에 9시간을 더하지 마라.

관측소 XYZ는 헤더와 외부 station metadata를 비교한다. 좌표의 datum/기준계(ITRF 실현 연도·epoch 또는 국가기준계)를 확인하고, 헤더와 외부 metadata의 기준계가 다르면 변환 근거를 기록하거나 `datum_unverified`로 표기한다. 알려진 고정좌표가 없으면 헤더 좌표를 사용하되 정밀도 제한을 기록한다. 좌표나 안테나·수신기 변경일은 정상 기준선 분할점으로 사용한다.

# 단계 4 — 재현가능한 특징 추출

원시 관측값을 그대로 보존하지 않는 요약특징이라도 원본 파일, station, epoch, satellite, constellation, signal code로 역추적할 수 있게 provenance 열을 둔다. 대용량 테이블은 CSV 한 파일이 아니라 연도/관측소/일자 기준 Parquet 파티션으로 저장한다.

## 4.1 관측가용성·tracking 특징

- epoch별 전체 및 GNSS별 관측 위성 수
- GNSS·주파수대·관측코드별 유효 관측 수와 결측률
- 새로 소실된 위성과 재획득 위성 수
- 30초 초과 gap, 동시 다중위성 소실률, lock 지속시간
- LLI bit 0과 bit 1을 분리하고, bit 2 이상은 해당 RINEX 버전·위성군·신호의 공식 의미를 확인해 raw bit와 해석을 별도 보존한다. bit 2를 loss-of-lock와 자동 합산하지 않는다.
- 가능한 경우 geometry-free phase, Melbourne–Wübbena 또는 동등한 이중주파수 조합에 의한 cycle-slip 후보

LLI, 조합검출, 관측공백은 서로 다른 검출기로 유지하고 하나를 다른 것의 정답으로 사용하지 마라.

## 4.2 신호강도 특징

`Sxx`가 있고 단위가 dB-Hz로 확인되는 신호는 `station×receiver×firmware×antenna/radome×RINEX major×constellation×exact 3-character observation code×actual frequency×metadata regime`별로 분리한다. 신호강도는 `S1C` vs `S1W`처럼 같은 S family 내에서 비교하고, `C1C` vs `C1W`는 별도 의사거리 family로 다룬다. 서로 다른 수신기·펌웨어·관측 family·정확 관측코드의 절대수준을 바로 합치지 마라.

RINEX 2의 `S1`, `S2`를 RINEX 3/4의 특정 추적속성으로 변환할 때는 수신기·펌웨어·변환기 문서로 유일하게 확인되는 경우만 canonical code를 부여한다. 나머지는 `tracking_attribute=U`, `mapping_status=legacy_ambiguous`로 격리하고 RINEX 3/4 exact-code 기준선에 편입하지 않는다. 추적모드 차이가 특정 dB-Hz 단차를 만든다는 수치는 수신기별 실증 전에 고정하지 말고 `literature_candidate` 또는 `dataset_calibrated`로만 사용한다.

- epoch별 median, lower quantiles, MAD, IQR
- 전 epoch 대비 변화량과 5·10·30분 강건 변화량
- 동시에 하락한 위성의 비율
- 고도각 구간별 정상 기대값 대비 residual
- 동일 주파수대에 속하는 여러 위성군의 공통 하락도
- 특정 위성만의 하락과 관측소 전체 공통 하락의 분리

위성 고도각을 계산할 수 있으면 station×receiver-regime×constellation×exact-observation-code×actual-frequency×elevation-bin 단위의 정상 기준을 만든다. 가능하면 주간·계절 효과를 강건 회귀 또는 분위수 기준으로 보정한다. 고도각을 계산할 수 없으면 같은 위성·유사 local sidereal time 또는 과거 동일 시간대 기준을 보조적으로 사용하되 한계를 명시한다.

## 4.3 코드·반송파·Doppler·위치 특징

실제 관측코드가 허용하는 범위에서 다음을 계산한다.

- code-minus-carrier의 변화와 점프
- dual-frequency ionosphere-free 및 geometry-free 조합의 변화
- Doppler와 연속 carrier phase 차분의 부호·단위 정합성을 검증한 뒤 불일치 residual
- 정적 CORS 알려진 좌표를 고정 또는 기준으로 한 pseudorange residual
- SPP 또는 사용 가능한 해법의 위치 오차, 수신기 clock bias/drift, 잔차 RMS, 가용성
- GNSS별 해와 다중 GNSS 해의 불일치

물리단위, 파장, GLONASS FDMA 채널, cycle 단위와 meter 단위를 명시적으로 처리한다. 단위 테스트 없이 조합식을 전체 자료에 적용하지 마라.

## 4.4 일·관측소 요약 및 원시 증거 링크

각 특징을 epoch, 5분, 30분, 일 단위로 요약하되 사건검출용 epoch/짧은 창 자료를 보존한다. 각 후보 사건이 어떤 원본 파일과 epoch에서 나왔는지 추적 가능한 `source_refs`를 만든다.

산출물:

- `features/epoch_features/`
- `features/window_features/`
- `features/station_day_summary/`
- `reports/04_feature_dictionary.md`
- `reports/05_feature_extraction_validation.md`

## 4.5 주파수대역·위성군 차분 특징 (Inter-Frequency / Inter-Constellation)

인위적 교란은 특정 타깃 주파수(주로 L1/E1 1575.42 MHz, L2 1227.60 MHz, L5/E5a 1176.45 MHz)에 집중되는 경향이 있다. 실제 인벤토리에서 확인된 관측코드가 허용하는 범위에서만 다음을 계산한다. L5/E5a 관측이 없는 관측소·기간에 해당 특징을 추정 생성하지 마라.

대역 정의·해석에서 다음 함정을 금지한다(설정의 `forbid_cross_constellation_band_alias`와 동일 원칙).

- **BDS B1I(1561.098 MHz)를 L1/E1/B1C(1575.42 MHz)와 같은 대역으로 별칭하지 마라.** B1I 이상과 L1 이상은 별도 대역 관측으로 기록하고, 실제 명목 주파수(`nominal_frequency_hz`)를 대역 그룹의 키로 사용한다.
- **GPS L2W(semi-codeless) 추적은 저고도·저SNR에서 원래 취약하다.** L2W 소실·저하를 곧바로 `L2 대역 표적 간섭`의 증거로 해석하지 마라. 가능한 경우 L2C(L2L/L2S/L2X)와 L2W를 분리 집계하고, L2W만의 저하는 추적방식 취약성 대안설명을 먼저 검토한다.
- **QZSS(J)는 L1/L5 계열 주파수를 공유하므로 대역차분 분석에 포함할 수 있으나 위성군은 별도로 유지한다.** 고궤도 준천정 특성상 고도각 분포가 GPS와 다르므로 기준선을 혼합하지 마라. SBAS(S, KASS 포함)는 측위 관측 특성이 달라 기본 제외하되, L1/L5 신호 존재 자체는 대역 영향 범위의 보조 참고로 기록할 수 있다.

- **대역별 Tracking Ratio**: 동일 위성·동일 epoch에서 대역별 유효 추적 비율 $TR_{L1}$, $TR_{L2}$, $TR_{L5}$를 계산하고, L1만 소실되고 L2/L5는 유지되는 협대역형 패턴과 전 대역 동시 소실(광대역/Barrage형) 패턴을 비율 지표로 분리한다.
- **대역별 SNR 하락 불균형**: 고도각 보정 residual 기준으로 대역 간 하락 격차(예: ΔL1−ΔL5)를 산출한다.
- **위성군 간 취약성 차이**: GPS(CDMA)와 GLONASS(FDMA)의 간섭 내성 차이를 다중 검출기 피처로 사용한다. GLONASS FDMA는 위성별 채널 주파수가 다르므로 채널번호를 명시적으로 처리하고, GLONASS 위성 간 반응 차이 자체를 협대역 가설의 보조 지표로 활용할 수 있다.
- **ROTI**: 이중주파수 위상의 geometry-free 조합으로 ROT를 계산하고 5분 창의 표준편차(TECU/min)로 ROTI를 산출한다. 단, 하나의 연속 arc에서 유효 위상 epoch `N_epoch ≥ 8`, 유효 ROT 차분 `N_ROT ≥ 7`, window coverage `≥ 0.80`, epoch 간격 `≤ nominal interval`(시계 허용오차 제외)를 모두 만족하고 두 주파수 중 어느 한 쪽에도 LLI·cycle slip·비정상 phase jump가 없을 때만 유효값으로 계산한다. 5분 창의 양 끝점 포함 규칙, `n_epochs_expected`, `n_rot_expected`, 결측 이유를 저장한다. `N_epoch` 7/8/9와 coverage 0.7/0.8/0.9를 민감도 분석하고, 8과 0.80은 교정 전 `configured`다. GLONASS는 FDMA channel과 bias 문제 때문에 기본 제외하되 3.1절의 channel·검증 게이트를 통과한 경우만 별도 민감도 경로에서 사용한다.

ROTI 사건 대표값은 단일 slip에 취약한 `max`를 주지표로 쓰지 말고 `median`, `Q90`, `valid_roti_fraction`, `high_roti_satellite_fraction`, `roti_spatial_coherence`를 보고한다.

해석 규칙:

- 대역선택적 저하 + 낮은 ROTI + 정온한 지자기 지수 조합은 협대역 인위적 간섭 가설을 지지하는 **보조** 증거일 뿐 확정이 아니다.
- 전 대역·전 위성군 저하 + 높은 ROTI + `space_weather_alert` 기간 조합은 전리층·우주기상 가설의 우선 검토를 요구한다.
- 두 지표가 상충하면 `conflicting_evidence`로 남기고 어느 쪽으로도 강제하지 마라.

# 단계 5 — 정상 기준선 구축

정상 기준선은 전체기간 평균 하나로 만들지 마라. 다음 계층을 반영한다.

- 관측소
- 수신기·안테나·펌웨어와 관측코드가 동일한 metadata regime
- 위성군과 주파수대·signal code
- 위성 고도각 또는 그 대체조건
- 시간대, 계절, 필요한 경우 요일

각 특징의 강건 표준화는 원칙적으로 다음 형태를 사용한다.

    robust_z = (x - baseline_median) / max(1.4826 * baseline_MAD, empirical_scale_floor)

`empirical_scale_floor`는 임의 epsilon이 아니라 feature 측정 분해능, 수신기·관측코드 기준군의 안정 표본, 정상 holdout으로 교정하고 provenance와 민감도를 남긴다. MAD가 0이거나 표본이 부족하면 IQR, 경험적 분위수 또는 19절의 계층적 fallback을 사용하고 fallback 수준을 열로 남긴다. 합리적 floor를 정의할 수 없으면 해당 z-score를 결측 처리한다. 미래 데이터로 과거 기준선을 학습하는 누수를 방지한다. 기준선 구간과 검출 구간을 시간순으로 분리하고, 공식 사건정보는 블라인드 기준선 학습에 사용하지 않는다.

수신기·안테나·펌웨어·관측코드 변경 전후를 같은 분포로 강제 결합하지 마라. 변경점 주변의 안정화 기간은 민감도분석 대상으로 둔다.

산출물:

- `baselines/baseline_parameters.parquet`
- `baselines/baseline_regimes.csv`
- `reports/06_baseline_method_and_leakage_control.md`

# 단계 6 — 다중 검출기 이상탐지

하나의 모델 점수로 결론내리지 말고 최소 다음 독립 특징군을 사용한다.

1. signal-strength family: 고도각 보정 SNR/CN0 공통 하락 또는 비정상 공통 상승
2. tracking family: 위성 수 급락, 동시 소실, 재획득, LLI와 cycle slip 증가
3. measurement-consistency family: 코드·반송파·Doppler 조합과 잔차 이상
4. solution family: 정적 위치, clock bias/drift, SPP 잔차·가용성 이상
5. availability family: epoch gap과 파일 완전성 이상

4.5절의 대역별 Tracking Ratio·SNR 불균형·CDMA/FDMA 차이는 signal-strength family와 tracking family 내부의 세부 피처로 사용하되, 독립 특징군 수를 부풀리는 별도 family로 중복 계상하지 마라. ROTI는 검출기가 아니라 21.3절 반증·분류 단계의 대조 지표로 사용한다.

강건 임계값, change-point detection, isolation forest 같은 비지도 방법을 비교할 수 있으나 모델 복잡도가 물리적 해석을 대신하지 않게 한다. 모든 임계값과 seed를 설정파일에 둔다. 여러 관측소·신호·시간을 동시에 검사하는 다중검정 문제를 고려하여 FDR 또는 경험적 false-alarm rate를 보고한다.

후보 생성 규칙은 최소 두 개의 독립 특징군이 같은 시간창에서 이상일 때를 기본으로 하되, 자료가 제한된 관측소는 별도 규칙과 낮은 증거등급을 사용한다. 인접한 후보 window를 사건으로 병합하는 최대 간격은 설정값으로 두고 5분, 10분 등 대안값에 대한 민감도를 확인한다.

# 단계 7 — 다중 관측소 시공간 동조성

GNSS 전파교란 판단의 핵심은 단일 수신기 이상과 공간적으로 일관된 공통 이상을 구분하는 것이다.

- epoch 또는 짧은 window별로 동시에 이상인 관측소 수와 비율을 계산한다.
- 관측소 간 거리와 후보 시작시각 차이를 계산한다.
- 동일 GNSS·주파수대·feature family에서의 동시성을 우선 평가한다.
- 단일 관측소 → 인접 관측소 → 광역 관측소로 이어지는 시간·거리 패턴을 조사한다.
- 단일 위성 이상은 위성·궤도·데이터 문제를 우선 검토하고, 여러 위성에서 동시에 나타나는 관측소 중심 패턴과 구분한다.
- 전국 동시 파일 공백은 전파교란보다 중앙 수집·변환·배포 장애 가능성을 먼저 검토한다.
- 공간군집 결과에 영향을 주는 관측소 밀도 차이를 통제한다.

단순히 "동시 이상 관측소 수"를 세는 데서 멈추지 말고 다음 공간 통계 계량화를 수행한다.

- **공간 자기상관**: 이상 강도(예: 관측소별 robust z 요약)에 대해 Moran's I 또는 Geary's C를 계산하고 순열검정으로 p-value를 산출한다. 가중행렬 후보에 `k-NN + maximum-distance cutoff`, 거리 밴드, `1/d`/`1/d^2`(최소거리 floor 포함), adaptive kernel, Delaunay 인접성을 포함하고 최소 3개 대안을 비교한다. 80 km는 고정 표준이 아니라 50/80/120 km 민감도 후보로만 두며, 실제 관측소 간격 분포·연결성·섬 관측소 영향을 보고 선택한다. 관측소 밀도 편중이 큰 망에서는 가중행렬 선택이 결과를 좌우할 수 있음을 명시한다.
- **고립 관측소 정책**: 최대연결거리로 이웃이 없어진 서해·동해 도서 관측소를 먼 내륙 관측소와 자동 연결하지 마라. `spatial_isolate=true`로 기록하고 해당 가중행렬의 Moran's I에서 제외하되, 제외 station과 유효 network coverage를 보고한다. 가중행렬별 연결 성분, 고립노드 수, 최대·중앙 연결거리를 저장한다.
- **거리–동조성 관계**: 출발점이 없는 `C/N0 공간 기울기`를 송신원 감쇠로 해석하지 마라. 관측소 쌍별 이상 동조성·시계열 상관과 거리의 관계, 거리 bin별 semivariance, 연결성 감소를 기술통계로 보고한다. 지형·차폐·관측소 밀도를 물리적 자유공간 감쇠로 바꾸지 마라.
- 다수 사건에 걸쳐 반복 계산하므로 공간통계 p-value에도 다중검정 보정(24.4절 규칙)을 적용한다.

전파원 위치를 직접 추정했다고 표현하지 마라. 충분한 관측소별 강도감쇠와 시간정보가 없으면 지도에는 `이상 관측망 범위`만 표시한다. Moran's I가 유의하다는 사실도 송신원 존재·위치의 증거가 아니라 공간군집의 증거일 뿐이다.

산출물:

- `candidates/station_window_anomalies.parquet`
- `candidates/network_candidate_events.csv`
- `candidates/event_station_membership.csv`
- `candidates/spatial_statistics.csv`
- `figures/network/`
- `reports/07_network_coherence_analysis.md`

# 단계 8 — 블라인드 탐지와 공식 사건 외부검증 분리

분석을 두 트랙으로 분리한다.

## 트랙 A: 블라인드 탐지

정부·ICAO 사건일을 보지 않고 정상 기준선과 이상후보를 고정한다. 후보의 생성시각, 사용한 코드 버전, 설정 해시를 기록해 사후 변경을 막는다.

## 트랙 B: 알려진 사건 재현과 외부검증

공식 사건정보가 제공되어 있거나 공식 원문에서 확보할 수 있을 때만 다음 스키마로 정리한다.

    event_id, source_agency, source_title, source_url, document_date,
    start_utc, end_utc, area_text, geometry_or_bbox, event_type,
    primary_source, access_date, notes

공식 사건 후보는 `config/official_events.csv`에 두고, 파일이 없으면 `official_events_template.csv`만 생성한다. 언론기사는 후보 탐색에만 사용할 수 있으며 최종 외부검증 근거는 정부, 군·항공·해양 당국, ICAO, ITU 등 1차 출처 원문으로 역추적한다. 출처가 불명확한 시간·지역을 추정해 채우지 마라.

국내 정부 발표 외에 다음 국제 공신력 데이터원을 접근 가능한 범위에서 크로스 체크 대상으로 확장한다. 각 출처의 증거 성격 차이를 반드시 구분한다.

- **항공 NOTAM**: GNSS 전파교란 관련 발행 NOTAM 아카이브 대조. NOTAM은 실제 간섭 확인기록이 아니라 예방적 경보일 수 있으므로 `advisory` 성격으로 표기하고, NOTAM 단독으로 E4 승격 근거로 쓰지 마라.
- **해양 항행경보(NAVAREA XI)**: 국립해양조사원 및 NAVAREA XI 조정국(일본 해상보안청) 발행 GPS 수신장애 항행경보 매칭.
- **AIS 위치이상 집계**: 서해·동해안 인근 선박의 AIS 기반 GPS 이상 집계 보고서와 시공간 중첩 비교. AIS 위치이상은 AIS 장비 자체 문제·수신망 문제로도 발생하므로 GNSS 교란의 직접 증거로 단정하지 말고 독립 관측자료 후보로만 취급한다.
- **대한민국·ICAO APAC 출처 우선**: 대한민국 CORS 외부검증은 국내 공식기관, 항공교통본부, 해양·항행경보, ICAO APAC 관련 자료를 먼저 확인한다. ICAO EUR/NAT 등 타 권역 기록은 방법·용어·비교 맥락으로 사용하되, 한국 사건의 직접 외부정답으로 쓰지 않는다.

이 확장 출처들도 22.2절의 공식 사건표 스키마로 정규화하고 `source_tier`(정부 1차 발표 / 국제기구 기록 / 항행·항공 경보 / 집계·2차 보고)를 구분해 기록한다. 서로 다른 출처가 같은 원사건을 재보고한 경우 독립증거로 중복 계상하지 마라.

다음을 별도로 계산한다.

- 공식 사건시간과 RINEX 후보시간의 중첩
- 공식 영향지역과 관측소 위치의 공간 중첩 또는 거리
- 사건일 전후의 동일 시각 matched-control 날짜 비교
- 같은 관측소의 비사건일 false alarm
- 알려진 사건 leave-one-event-out 평가
- 관측소 leave-one-station-out 일반화
- Precision, Recall, PR-AUC, ROC-AUC는 진짜 양성·음성 정의가 정당할 때만 산출

공식 사건이 관측망 범위 밖이거나 시간·영역이 모호하면 검출 실패로 단정하지 말고 평가불가로 처리한다. 공식 사건과 겹친다는 이유만으로 같은 원인이라고 확정하지 마라.

산출물:

- `validation/official_events_normalized.csv`
- `validation/blind_vs_official_overlap.csv`
- `validation/matched_controls.csv`
- `reports/08_external_validation.md`

# 단계 9 — 사건 분류와 증거등급

각 사건에 대해 다음 원인유형을 하나의 확정 라벨이 아니라 순위가 있는 가설로 기록한다.

- `jamming_like`: 여러 위성에서 동시 SNR 하락, tracking loss, 위성 수 감소, LLI/cycle slip 증가와 회복이 같은 주파수대 또는 여러 대역에 일관됨
- `spoofing_compatible`: 고정국 위치·clock·pseudorange/carrier/Doppler 일관성의 구조적 이상이 있으나 RINEX만으로 확정 불가
- `unintentional_rfi_possible`: 특정 대역의 반복적·국지적 이상이 있으나 고의성 증거 없음
- `receiver_or_site_issue`: 한 관측소에 국한되고 metadata change, 전원·저장·통신, 안테나, 주변환경 설명이 더 타당함
- `satellite_or_product_issue`: 같은 위성에서 여러 지역 관측소가 비슷하게 이상하며 관측소 중심 패턴이 아님
- `ionosphere_or_space_weather_possible`: 다중주파수 조합과 공간범위가 전리층 교란 설명과 더 양립함
- `data_pipeline_issue`: 파일 경계, 압축·변환·수집 장애 패턴과 일치함
- `indeterminate`: 증거가 부족하거나 가설이 경합함

`jamming_like` 또는 `unintentional_rfi_possible`로 분류된 후보에는 ICAO Doc 9849 및 Annex 10의 RFI 유형 구분과 정합하도록 다음 **보조 가설 필드**를 추가한다. 이는 30초 RINEX 간접지표(4.5절 대역차분·위성군차분)로 추정한 가설이며 스펙트럼 측정이 아니다.

- `rfi_observation_pattern`: `band_selective`(특정 대역 관측치만 선택적 악화) / `multi_band_common`(다중 대역 공통 악화) / `temporally_unresolved`(30초 표본으로 시간구조 판별 불가) / `unassessable`. narrowband·barrage·chirp는 스펙트럼/RF 센서 없이 라벨로 부여하지 않는다.
- `rfi_intent_hypothesis`: `intentional_possible` / `unintentional_possible`(산업·인접대역 유출, 예: L-band Satcom·5G Sub-6 스퓨리어스) / `unassessable`. 의도성은 RINEX만으로 판정 근거가 거의 없으므로 공식 사건기록과 정합할 때만 `intentional_possible`을 사용한다.

보고서 서술은 ITU-R M.1901을 RNSS 관련 권고 안내로, ITU-R M.1902(1 215–1 300 MHz)·M.1903(1 559–1 610 MHz)·M.1905(1 164–1 215 MHz)를 대역별 보호기준 문맥으로 구분하고, IGS 품질관리 용어와 정합한다. Report ITU-R M.2458은 RNSS 응용 보고서이며 보호기준 근거로 대체하지 마라. RINEX 관측은 해당 보호기준 위반 여부를 직접 측정하지 못한다.

증거등급은 다음과 같이 제한한다.

- E0: 분석 불가 또는 자료 부족
- E1: 단일 지표 이상
- E2: 한 관측소에서 두 개 이상 독립 특징군이 일치
- E3: 서로 다른 복수 관측소에서 유사한 신호·대역·특징 패턴의 시공간 동조성이 확인됨. 한 관측소의 multi-band 일치만으로는 E3이 아니다.
- E4: E3에 더해 독립된 발생확인 공식 1차 출처 또는 별도 센서가 동일 시공간에서 정합함. advisory·NOTAM·NAVAREA의 단순 중첩은 단독 E4 근거가 아니다.
- E5: 독립 RF 측정 또는 통제실험으로 원인이 직접 확인됨

RINEX 단독 분석은 원칙적으로 E3을 넘지 않는다. 공식 사건자료와 정합하면 E4까지 가능하지만, 공식 사건의 세부 시공간 근거가 충분한지 별도 평가한다.

최종 판정표에는 최소 다음 열을 포함한다.

    candidate_id, start_utc, end_utc, start_kst, end_kst,
    duration_seconds_observed, timing_uncertainty_seconds,
    stations, station_count, affected_constellations, affected_bands,
    signal_strength_score, tracking_score, measurement_score,
    solution_score, availability_score, spatial_coherence_score,
    primary_hypothesis, competing_hypotheses, evidence_grade,
    rfi_observation_pattern, rfi_intent_hypothesis,
    band_discrepancy_ratio, roti_median_tecu_min, roti_q90_tecu_min,
    valid_roti_fraction, high_roti_satellite_fraction, space_weather_flag,
    morans_i, morans_i_pvalue, spatial_coherence_distance_slope,
    official_event_overlap, official_source_tier,
    data_quality_grade, source_refs,
    limitations, manual_review_status

# 단계 10 — 파일럿에서 전체기간으로 단계적 확대

전체 6년을 처음부터 한 번에 돌리지 마라.

1. 전수 헤더 인벤토리를 먼저 완료한다.
2. 실제 파일에서 대표 관측소와 날짜를 선택한 소규모 파일럿으로 parser, 단위, 시간, 특징과 그림을 검증한다. 정상일과 이상 가능일을 모두 포함하되 선택 근거를 기록한다.
3. 파일럿의 테스트와 수동검토가 통과하면 10개 안팎의 관측소·여러 계절로 확대한다. 정확한 관측소 수는 실제 인벤토리와 자원을 근거로 정한다.
4. 처리시간·메모리·출력용량을 추정한 뒤 전체 관측소·전체 실제기간으로 확대한다.
5. 각 단계에서 동일 설정의 재실행 결과가 같고, 실패 후 재개가 되는지 검증한다.

전체 실행이 매우 오래 걸리더라도 파일럿 결과만 전체결과처럼 보고하지 마라. `pilot`, `expanded`, `full` 실행범위를 모든 표와 그림에 명시한다.

# 단계 11 — 테스트와 품질보증

최소 다음 테스트를 작성하고 실행한다.

- RINEX 2/3/4 헤더 및 관측파일 식별 테스트
- gzip, Hatanaka, Unix `.Z` 등 실제 보유 압축형식 테스트
- 30초 epoch 수, 날짜경계, 윤년, DOY, leap second와 UTC/KST 변환 테스트
- RINEX 관측코드별 C/L/D/S 매핑 테스트
- LLI bit 해석 테스트
- GPS·Galileo·BDS·GLONASS의 주파수·파장 및 GLONASS FDMA 처리 테스트
- BDS B1I(1561.098 MHz)와 B1C/L1(1575.42 MHz)의 대역 분리 테스트(`forbid_cross_constellation_band_alias` 검증)
- GPS L2C 계열과 L2W(semi-codeless)의 분리 집계 테스트
- QZSS(J)·SBAS(S) 위성 식별과 포함/제외 정책 분기 테스트
- GPST·BDT 등 시간계 오프셋 변환 테스트
- 인위적으로 삽입한 gap, SNR 공통하락, cycle slip, clock jump를 탐지하는 synthetic unit test
- 정상 synthetic data의 false alarm 테스트
- 동일 입력·설정·seed의 결정적 재실행 테스트
- 한 일자 실패 후 resume 테스트
- 2~3개 실제 원본파일에 대한 수동 독립검산
- 가능하면 GFZRNX 등 독립 도구의 통계와 parser 결과 교차검증

합성자료는 코드 검증용일 뿐 실제 사건 근거에 섞지 마라.

완료 기준:

- 테스트가 모두 통과하거나, 통과하지 못한 테스트와 영향이 최종보고서에 명시됨
- 인벤토리의 파일 수와 처리·제외·실패 파일 수가 정확히 reconciliation됨
- 후보 사건에서 원본파일과 epoch까지 역추적 가능함
- 원시자료가 수정되지 않았음이 확인됨
- 전체 실행범위와 미완료 범위가 명확함
- 모든 핵심 표와 그림이 동일 설정으로 재생성됨

# 사건별 시각화

각 상위 후보 사건에 대해 최소 다음 그림을 생성한다.

1. UTC/KST 이중표기 사건 타임라인
2. 관측소별 위성 수, 고도각 보정 SNR residual, LLI/cycle slip, gap, 위치·clock residual 패널
3. GNSS·주파수대별 비교 패널
4. 사건 관측소와 비사건 대조 관측소 비교
5. 관측소 지도와 시공간 동조성
6. 사건 전·중·후 분포 비교

축, 단위, 표본간격, smoothing window, 데이터 품질등급과 분석범위를 그림에 적는다. 지도를 그릴 때 실제 송신원 위치로 오해될 표시를 하지 마라.

# 최종 산출물

다음을 빠짐없이 만든다.

- `reports/09_candidate_event_catalog.csv`
- `reports/09_candidate_event_catalog.md`
- `reports/10_final_scientific_report.md`
- `reports/11_reproducibility_report.md`
- `reports/12_limitations_and_next_data.md`
- `reports/13_standards_terminology_alignment.md` — 본 분석의 분류·용어와 ICAO Doc 9849/Annex 10, ITU-R M.1901·M.1902·M.1903·M.1905, IGS 품질관리 용어의 대응표. 각 대응이 `일치` / `부분 대응` / `본 자료로 판정 불가` 중 무엇인지 명시
- `reports/14_data_and_code_availability.md` — 학술지 제출 대비 데이터·코드 가용성 서술 초안. 원시자료 접근제한, 공개 가능한 파생산출물 범위, 잠금 의존성·설정·해시로 재현 가능함을 기술 (실제 아카이빙·DOI 발급은 수행하지 말고 필요 절차만 기록)
- `reports/15_evaluation_protocol_and_results.md` — calibration/holdout, block bootstrap, matched control, multiple testing, 지표별 분모·CI·ground-truth 한계
- `reports/16_parallel_execution_report.md` — 실행 DAG와 배리어 이력, 역할별 워커 수와 task 통계, shard/worker 불변성 시험 결과, 경계 재병합 통계, 분산 집계 근사 오차, 워커 수별 처리량·병목·자원 사용, poison task와 그 영향
- `reports/manual_review_queue.csv`
- `figures/` 아래 사건별 PNG와 전체 요약 그림
- 실행 가능한 CLI 또는 스크립트
- `README.md`의 설치·파일럿·전체실행·재개·보고서 재생성 명령
- 잠긴 의존성 파일, 설정파일, 로그, manifest, 테스트 결과

최종 과학보고서는 다음 순서로 작성한다.

1. 한 페이지 핵심결론
2. 자료의 실제 범위와 품질
3. 30초 RINEX로 가능한 것과 불가능한 것
4. 분석방법과 혼란변수 통제
5. 블라인드 후보 결과
6. 다중관측소 시공간 결과
7. 공식 사건 외부검증 결과
8. 재밍 유사·스푸핑 유사·비교란 이상 분류
9. false positive·false negative·민감도분석
10. 박사논문에서 주장 가능한 범위
11. 2024~2026년 1초 RINEX와 저가형 수신기 자료로 이어질 후속검증 설계

마지막 후속검증 설계에는 동일 사건에 대해 `실제 30초 자료`, `1초 자료`, `1초→30초 다운샘플 자료`를 비교하여 시간해상도 효과와 데이터 도메인 차이를 분리하는 방법을 포함하라. 그러나 현재 30초 분석 결과에 1초 자료의 결과가 존재하는 것처럼 섞지 마라.

# 완료 시 응답 형식

작업을 마치면 채팅에는 장황한 과정이 아니라 다음만 간결히 보고한다.

1. 실제 분석한 기간·관측소·파일 수
2. 성공·제외·실패 파일 수와 핵심 데이터 품질
3. 후보 사건 수와 증거등급별 개수
4. 공식 사건과 중첩된 후보 수
5. 가장 강한 후보 5건의 시각·관측소·가설·증거등급·핵심 근거
6. 확정할 수 없는 사항과 그 이유
7. 최종보고서, 사건목록, 재현방법, 로그의 경로
8. 전체기간 실행 완료 여부와 남은 작업
9. 병렬 실행 구성(역할별 워커 수·shard 수)과 큐에 남은 task, 다음 재개 명령

경로에 접근하지 못했거나 실제 분석을 완료하지 못했으면 `분석 완료`라고 말하지 마라. 생성한 코드와 파일럿만 있다면 그 범위를 정확히 밝힌다.

# 참고해야 할 1차 규격·방법 자료

구현 중 해석이 불명확할 때에는 다음 원문을 우선 확인하고, 사용한 버전과 접근일을 보고서에 남긴다.

- IGS/RTCM RINEX 4.02: https://files.igs.org/pub/data/format/rinex_4.02.pdf
- IGS RINEX Working Group: https://igs.org/wg/rinex/
- IGS MGEX 시간 유효 위성 PRN·GLONASS frequency-channel metadata: https://igs.org/mgex/metadata
- IGS daily 30-second data 설명: https://igs.org/data/
- GFZRNX 공식 사용자 안내서: https://gnss.git-pages.gfz-potsdam.de/gfzrnx/
- SWEPOS CORS 망 기반 SNR 전파간섭 탐지 연구: https://doi.org/10.1515/jogs-2022-0157
- 다중 수신기 pseudorange 기반 spoofing network monitoring 연구: https://doi.org/10.3390/s16101677
- ICAO Doc 9849 (GNSS Manual) 및 Annex 10 Vol. I: RFI 유형·보고 체계 용어 정합용
- ITU-R Recommendation M.1901: RNSS 관련 권고 안내 문서, https://www.itu.int/rec/R-REC-M.1901/en
- ITU-R M.1902: 1 215–1 300 MHz RNSS 보호기준, https://www.itu.int/rec/R-REC-M.1902/en
- ITU-R M.1903: 1 559–1 610 MHz RNSS 보호기준, https://www.itu.int/rec/R-REC-M.1903/en
- ITU-R M.1905: 1 164–1 215 MHz RNSS 보호기준, https://www.itu.int/rec/R-REC-M.1905/en
- Report ITU-R M.2458: RNSS 응용 보고서. 보호기준 문서로 인용하지 말 것, https://www.itu.int/pub/R-REP-M.2458
- IGS 데이터·품질관리 문서 및 ANTEX 안테나 모델: https://igs.org/formats-and-standards/
- ROTI 정의 원문: Pi et al. (1997), Monitoring of global ionospheric irregularities using the worldwide GPS network, https://doi.org/10.1029/97GL02273
- IGS GIM(IONEX): https://www.igs.org/products/ . 지자기 지수 출처는 GFZ Kp, Kyoto WDC Dst, NOAA SWPC를 우선하고 접근일·버전을 기록

이 자료를 인용했다는 이유만으로 그 연구의 임계값을 현재 CORS 자료에 그대로 적용하지 마라. 실제 운영기관, 수신기, 관측코드, 관측소 환경과 정상분포에서 임계값을 다시 검증한다.

---

# 규모실행·병렬실행 운영 계약 (V6 계승, V7 확장)

아래 조항은 앞의 과학 분석 절차를 실제 대규모 프로젝트로 완성하기 위한 추가 요구다. 12~38절은 V6에서 계승했고 39~41절이 V7의 다중 워커 병렬 실행 계약이다. 앞 절과 중복되면 더 엄격한 조항을 따른다.

# 12. CORS 고정망 분석 단위와 안정적 ID

모바일 NMEA 분석의 `Pass`, `Route`, `Hotspot`을 사용하지 마라. CORS는 고정관측망이므로 다음 계층을 사용한다.

```text
RawFile
  └─ Observation
      └─ Epoch
          └─ StationWindow
              └─ StationEvent
                  └─ NetworkEvent
                      └─ EventFamily
```

## 12.1 단위 정의

- `RawFile`: 원시 또는 압축 RINEX 파일 하나. 내용 중복 시에도 파일 개체는 보존하고 duplicate group에 연결한다.
- `Observation`: station, epoch, satellite, observation code의 측정 한 건이다.
- `Epoch`: 한 관측소의 한 시각 관측 집합이다.
- `StationWindow`: 설정된 시간창에서 특징을 집계한 단위다. 창 길이는 실제 interval의 정수배로 정한다.
- `StationEvent`: 같은 관측소에서 시간적으로 연결되고 유사한 특징근거가 유지되는 이상구간이다.
- `NetworkEvent`: 허용 시차 안에 여러 관측소에서 유사한 signal/constellation/feature pattern으로 관측된 사건 묶음이다.
- `EventFamily`: 공식 사건 또는 반복패턴에 연결된 NetworkEvent 집합이다. 자동으로 동일 원인이라고 간주하지 않는다.
- `MetadataRegime`: 수신기, 펌웨어, 안테나, radome, 좌표, interval, 관측코드 구성이 안정적인 기간이다.
- `DataAvailabilityInterval`: 관측소 자료가 정상적으로 기대되는 운영기간이다.
- `AffectedObservationFootprint`: 이상이 관측된 관측소·시간 범위다. 간섭원 위치가 아니다.

## 12.2 안정적 식별자

식별자는 재실행, worker 수, 파일열거 순서, chunk 크기에 관계없이 같아야 한다.

```text
file_id          = hash(relative_path, size, content_fingerprint)
station_id       = canonical marker/network ID
regime_id        = hash(station_id, effective_from, metadata_signature)
epoch_id         = hash(station_id, canonical_epoch_time)
window_id        = hash(station_id, window_start, window_size, config_hash)
station_event_id = hash(station_id, start_bin, end_bin, event_rule_version)
network_event_id = hash(sorted_station_event_ids, clustering_rule_version)
run_id           = timestamp + short(config_hash) + short(code_hash)
```

절대경로, 프로세스 순서 또는 임의 UUID만으로 영구 ID를 만들지 마라.

# 13. 확장 프로젝트 구조

앞 절의 기본 구조를 다음과 같이 확장한다.

```text
analysis_30s_interference/
├─ README.md
├─ pyproject.toml
├─ uv.lock 또는 requirements-lock.txt
├─ .gitignore
├─ config/
│  ├─ analysis.yaml
│  ├─ paths.example.yaml
│  ├─ thresholds.yaml
│  ├─ official_events_template.csv
│  └─ logging.yaml
├─ src/rinex_interference/
│  ├─ __init__.py
│  ├─ cli.py
│  ├─ config.py
│  ├─ provenance.py
│  ├─ inventory.py
│  ├─ compression.py
│  ├─ rinex_header.py
│  ├─ rinex_reader.py
│  ├─ schemas.py
│  ├─ time_systems.py
│  ├─ station_metadata.py
│  ├─ orbit_geometry.py
│  ├─ quality.py
│  ├─ features/
│  │  ├─ signal.py
│  │  ├─ tracking.py
│  │  ├─ phase.py
│  │  ├─ code_doppler.py
│  │  ├─ positioning.py
│  │  └─ availability.py
│  ├─ baseline.py
│  ├─ anomaly.py
│  ├─ station_events.py
│  ├─ network_events.py
│  ├─ confounders.py
│  ├─ official_validation.py
│  ├─ evaluation.py
│  ├─ reporting.py
│  └─ plotting.py
├─ scripts/
│  ├─ run_r1_smoke.ps1
│  ├─ run_r2_station_day.ps1
│  ├─ run_r3_pilot.ps1
│  ├─ run_r4_representative.ps1
│  ├─ run_r5_full.ps1
│  └─ verify_outputs.ps1
├─ tests/
│  ├─ fixtures/
│  ├─ golden/
│  ├─ unit/
│  ├─ integration/
│  └─ scale/
├─ inventory/
├─ cache/
├─ canonical/
├─ data_quality/
├─ metadata/
├─ geometry/
├─ features/
├─ baselines/
├─ candidates/
├─ validation/
├─ evaluation/
├─ figures/
├─ reports/
├─ logs/
├─ checkpoints/
├─ manifests/
│  ├─ partitions/
│  └─ promotions.csv
├─ queue/
│  ├─ tasks.sqlite 또는 tasks/            # 작업 큐(39.4절)
│  ├─ barriers.json                       # 배리어 상태(39.3절)
│  └─ poison/                             # 격리된 실패 task
├─ locks/                                 # <scope_hash>.lock, 원자적 생성
├─ runs/<run_id>__<worker_id>/            # 워커별 임시·부분 산출물
├─ validation_unblinded/                  # W_VAL 전용 출력(블라인드 워커 접근 금지)
├─ docs/
├─ PROGRESS.md
├─ PHASE_HANDOFF.md
├─ WORKER_STATUS.md
├─ DECISIONS.md
├─ SURPRISES.md
└─ RUN_LOG.md
```

`paths.example.yaml`만 저장소에 공개 가능하게 두고 실제 절대경로는 별도 로컬 설정 또는 환경변수로 주입한다. 표와 보고서에는 원시루트 기준 상대경로만 기록한다.

워커는 `runs/<run_id>__<worker_id>/`에 부분 산출물을 만들고, 완료·검증된 파티션만 공식 경로(`features/`, `candidates/` 등)로 원자적 이동(승격)한다. 승격되지 않은 개인 산출물을 보고서 수치로 쓰지 마라.

# 14. 설정 계약

모든 조정 가능한 값은 소스코드가 아니라 설정에 둔다. 아래 값은 시작 후보이며 실제 데이터 교정 전에는 과학적 사실이 아니다.

```yaml
project:
  name: cors_rinex_30s_interference    # resume 동일성 유지를 위해 버전을 이름에 넣지 않는다
  contract_version: 'V7.1'
  timezone_report: Asia/Seoul
  language: ko

parallel_execution:
  enabled: true
  max_total_workers: auto_bounded        # min(CPU-2, RAM/worker_peak_rss, IO 한계)
  role_worker_limits:                    # 역할별 동시 인스턴스 상한(실측 후 조정)
    W_INV: 6
    W_QC: 6
    W_EXT: 2                             # 외부 다운로드는 소수·single-flight
    W_FEAT: 8
    W_BASE: 4
    W_DET: 8
    W_NET: 2                             # 시간블록 단위, 경계 재병합 필요
    W_FALS: 4
    W_VAL: 1                             # unblinded, 별도 프로세스
    W_FIG: 4
    W_REP: 1
  shard:
    key_policy: content_hash_of_shard_key   # 파일 열거 순서 의존 금지
    default_shards: 16
    invariance_test_shards: [1, 4, 16]
  queue:
    backend: sqlite_wal                  # 또는 원자적 rename 기반 디렉터리 큐
    location_must_be_local_disk: true    # 네트워크 공유의 잠금 semantics 신뢰 금지
    lease_seconds_default: 3600
    heartbeat_seconds: 60
    stale_lease_grace_seconds: 900
    max_attempts: 3
    backoff_seconds: [30, 120, 600]
    poison_policy: isolate_and_continue
  barriers:
    b1_inventory_quality_complete: required
    b2_baseline_frozen: required
    b3_blind_freeze_before_official: required
    declared_by_role: orchestrator
  halo:
    window_feature_padding_seconds: 900  # windows.sizes_seconds 최대값 이상
    roti_arc_padding_seconds: 1800
    event_merge_padding_seconds: 600
    network_block_padding_seconds: 120   # >= network_alignment_tolerance_seconds
  aggregation:
    additive_stats: [count, sum, sum_sq, min, max, histogram_bins]
    order_statistics_policy: two_pass_or_sketch
    sketch_method: t_digest              # 또는 kll, fixed_bin_histogram
    sketch_accuracy_check: required      # 정확값 대비 오차 보고
  resources:
    worker_peak_rss_mb_budget: configured
    min_free_disk_gb_to_lease: configured
    io_bound_stages: [inventory, parse, decompress]
    cpu_bound_stages: [features, roti, detection, spatial_statistics]
    decompress_cache_single_flight: true
  isolation:
    unblinded_roles: [W_VAL]
    unblinded_output_root: validation_unblinded
    forbid_shared_queue_with_blinded_roles: true

unspecified_cases:                       # 42절
  policy: record_conservative_default_and_continue
  register_path: docs/UNSPECIFIED_CASES.csv
  escalation_count: 20                   # 같은 case_id가 이 수를 넘으면 계약 개정 요청
  conservative_defaults:
    - quarantine_never_delete
    - unassessable_never_estimate
    - split_never_merge
    - hold_never_promote
  block_final_numbers_until_resolved: true

session:                                 # 43절 — 에이전트 실행 컨텍스트
  require_session_id: true
  must_read_on_start:
    - docs/runbook/00_invariants_and_goal.md
    - PHASE_HANDOFF.md
    - docs/IMPLEMENTATION_STATUS.md
    - DECISIONS.md
    - docs/UNSPECIFIED_CASES.csv
  always_in_context:                     # 축약·생략 금지
    - scientific_limitations
    - evidence_grade_caps
    - blind_isolation_rules
    - raw_data_protection
  blind_status_fixed_within_session: true
  stop_at_clean_boundary: true
  record_decisions_before_exit: true

observation_session:                     # 44.1절 — GNSS 관측 세션(일 단위 파일)
  file_is_session_default: true
  stitch_across_day_boundary: true
  max_stitch_gap_seconds: 60
  stitch_break_on: [receiver_reset, clock_step, coordinate_jump, obs_code_change, time_reversal]
  forbid_per_file_or_session_centering: true
  midnight_window_seconds: 300
  report_boundary_adjacent_event_fraction: true

canonical_file_selection:                # 44.2절
  priority:
    - higher_rinex_version
    - larger_valid_epoch_count
    - wider_observation_span
    - more_observation_codes
    - later_mtime
  content_equality_keys: [epoch_count, first_epoch, last_epoch, observation_code_set]
  on_tie: quarantine_and_report
  never_delete_alternatives: true

navigation_merge:                        # 44.3절
  source_priority: [sp3_clk, local_broadcast_nav, external_brdc]
  dedupe_key: [constellation, prn, toe_or_toc, iode_or_iodc]
  exclude_unhealthy: true
  max_ephemeris_age_hours: 4
  on_conflict: keep_all_and_record_selection

station_cohort:                          # 44.4절
  primary: fixed_cohort_present_in_all_analysis_years
  secondary: all_available_with_exposure_normalization
  report_both: true
  freeze_before_evaluation: true

constellation_coverage_regime:           # 44.5절
  new_constellation_starts_new_regime: true
  min_stable_days_to_close_regime: 7

reprocessing:                            # 44.6절
  analysis_set_frozen_by: analysis_cutoff_utc
  new_data_policy: new_run_id_never_extend_frozen_baseline
  rebaseline_requires: [orchestrator_approval, documented_scope, superseded_claims]

satellite_obs_retention:                 # 44.7절
  mode: events_plus_sample               # full | events_plus_sample | sample_only
  event_window_seconds: 1800
  normal_sample_fraction: 0.01
  sample_strata: [station_id, regime_id, constellation, elevation_bin, season]
  full_mode_requires_free_disk_multiple: 3

candidate_rate_guard:                    # 44.8절
  expected_alert_rate_per_valid_station_day: [0.0001, 0.05]   # configured
  action_outside_range: stop_and_diagnose_never_silently_retune

runtime_guard:
  max_full_run_hours: 96                 # configured
  measure_at: [r1, r2, r3]
  action_if_exceeded: fix_bottleneck_before_next_scale

manual_review:                           # 44.9절
  full_review_max_candidates: 200
  stratify_by: [evidence_grade, station_id, month, primary_hypothesis]
  sample_seed: 20260330
  report_sampling_fraction: true

cache_policy:                            # 44.10절
  decompressed_ttl_minutes: 30
  delete_on_task_success: true
  max_cache_gb: configured
  stop_lease_below_free_gb: configured

log_policy:
  per_file_level: warning_and_above
  success_goes_to_manifest_not_log: true
  max_log_gb: configured

constellations:
  include: [G, R, E, C]                # 기본 분석 대상
  qzss_policy: include_if_observed_separate_baseline   # J: 관측 확인 시 별도 기준선으로 포함
  sbas_policy: record_presence_exclude_from_detection  # S(KASS 포함): 존재 기록, 검출 제외
  navic_policy: record_presence_only

analysis_period:
  configured_start_utc: '2021-01-01T00:00:00Z'
  configured_end_utc: '2026-12-31T23:59:59Z'
  cutoff_policy: min_configured_end_and_latest_valid_epoch
  incomplete_calendar_year_label: YTD
  annual_comparison_policy: equal_doy_or_exposure_normalized

paths:
  raw_root: 'E:\worldtechRnD\Pro_phd_data\rinex\Daily'
  output_root: 'E:\worldtechRnD\Pro_phd_data\rinex\analysis_30s_interference'

inventory:
  recursive: true
  compute_full_sha256: false
  fingerprint_head_tail_bytes: 1048576
  verify_first_last_epoch: true

processing:
  expected_interval_seconds: 30
  interval_tolerance_seconds: 0.5
  batch_rows: 250000
  max_workers: auto_bounded
  atomic_write: true
  resume: true
  overwrite: false

retention:
  persist_all_observations: false
  persist_epoch_summary: true
  persist_event_windows: true
  event_padding_minutes: 30
  normal_sample_fraction: 0.01
  daily_accumulators: true

geometry:
  min_elevation_deg_candidate: 15
  elevation_bins_deg: [0, 5, 10, 15, 20, 30, 45, 60, 90]
  azimuth_bins_deg: 30
  product_preference: [sp3, broadcast_nav, unavailable]

baseline:
  method: robust_hierarchical
  training_policy: pseudo_prospective
  group_key_fields: [station_id, regime_id, receiver_type, receiver_version, antenna_type, rinex_major_version, constellation, obs_family, exact_observation_code, nominal_frequency_hz, elevation_bin]
  isolate_legacy_ambiguous_tracking: true
  min_epochs_per_cell: 200
  rolling_days_candidate: 28
  exclude_candidate_buffer_hours: 12
  mad_floor_policy: empirical_by_group

windows:
  sizes_seconds: [30, 60, 120, 300, 900]
  station_event_gap_seconds: 60
  network_alignment_tolerance_seconds: 60

evaluation:
  block_bootstrap_unit: station_day
  bootstrap_replicates: 1000
  multiple_testing: benjamini_hochberg
  random_seed: 20260330

official_validation:
  enabled: false
  blind_results_frozen_first: true
  time_tolerance_minutes_candidates: [1, 5, 15, 30]
  spatial_zone_policy: configured_and_sensitivity_tested

space_weather:
  enable_filter: true
  kp_source: gfz_potsdam
  dst_source: kyoto_wdc
  kp_threshold: 5.0
  dst_threshold_nt: -50.0
  roti_window_minutes: 5
  roti_threshold_tecu_min: 0.5
  roti_constellations: [GPS, GAL, BDS]   # GLONASS FDMA 제외가 기본
  roti_min_continuous_epochs: 8
  roti_min_rot_samples: 7
  roti_min_window_coverage: 0.80
  roti_require_single_arc: true
  roti_reject_lli_or_cycle_slip: true
  roti_max_gap_seconds: 30
  roti_sensitivity_epochs: [7, 8, 9]
  roti_sensitivity_coverage: [0.70, 0.80, 0.90]
  roti_primary_summaries: [median, q90, valid_fraction, high_satellite_fraction, spatial_coherence]
  gim_source: igs_final_then_rapid
  gim_role: broad_context_only
  index_version_policy: record_provisional_or_definitive
  flag_name: space_weather_alert
  auto_exclude: false                    # 자동 제외 금지, 검증 강화만

frequency_profiling:
  analyze_band_discrepancy: true
  group_key_fields: [constellation, exact_observation_code, nominal_frequency_hz]
  forbid_cross_constellation_band_alias: true
  require_inventory_confirmed_codes: true
  compare_cdma_vs_fdma: true

glonass_frequency_channel:
  source_priority: [rinex_observation_header, local_navigation, igs_mgex_time_valid_metadata]
  require_validity_interval_match: true
  forbid_static_prn_only_lookup: true
  unresolved_policy: disable_wavelength_dependent_glonass_features
  snapshot_path_pattern: cache/external/glonass_channels_YYYYMMDD.json

spatial_statistics:
  calculate_morans_i: true
  spatial_weight_candidates:
    - {method: knn_with_distance_cap, k: 4, max_distance_km: 50}
    - {method: knn_with_distance_cap, k: 6, max_distance_km: 80}
    - {method: knn_with_distance_cap, k: 8, max_distance_km: 120}
    - {method: distance_band, cutoff_policy: station_spacing_quantiles}
    - {method: inverse_distance, power: 1, minimum_distance_floor_km: configured}
    - {method: inverse_distance, power: 2, minimum_distance_floor_km: configured}
    - {method: adaptive_kernel, kernel: gaussian}
    - {method: delaunay_neighbors}
  isolated_station_policy: exclude_and_report_never_force_connect
  record_graph_diagnostics: true
  permutation_replicates: 999
  pairwise_coherence_distance_analysis: true
  semivariogram_analysis: descriptive_only
  source_free_decay_model_forbidden: true

external_validation_sources:
  - KOREAN_GOVERNMENT_PRIMARY
  - ICAO_APAC
  - NOTAM
  - NAVAREA_XI
  - AIS_ANOMALY_REPORTS
  - ICAO_EUR_NAT_INCIDENTS
  - LOCAL_GOVERNMENT_ALERTS
```

`space_weather.kp_threshold`, `dst_threshold_nt`, `roti_threshold_tecu_min`, 공간 가중행렬 후보를 포함한 위 값은 모두 `configured` 상태의 시작 후보다. `auto_exclude: false` 원칙을 지켜라. `space_weather_alert` 기간의 후보는 자동 탈락시키지 말고 21.3절 반증 단계를 강화 적용한 뒤 상태를 남긴다.

설정의 후보값을 바꾸면 변경이유, 영향범위, 이전·새 config hash를 `DECISIONS.md`에 남긴다.

# 15. 장기 실행 통제와 Phase handoff

## 15.1 진행 파일

실행 시작 즉시 만들고 매 의미 있는 단계마다 갱신한다.

- `PROGRESS.md`: 완료·진행·대기 작업, 실측 범위, 마지막 성공 checkpoint
- `PHASE_HANDOFF.md`: 현재 Phase, 게이트 결과, 실패항목, 다음 정확한 명령
- `DECISIONS.md`: 선택, 근거, 대안, 영향, 되돌리는 방법
- `SURPRISES.md`: 예상과 다른 데이터·성능·품질 발견
- `RUN_LOG.md`: 실행시각, 명령, run ID, `worker_id`·`role`·shard, 종료코드, 산출물
- `WORKER_STATUS.md`: 현재 살아 있는 워커, 역할, lease 중인 task, 마지막 heartbeat, 처리량, 배리어 상태
- `docs/IMPLEMENTATION_STATUS.md`: Phase별 구현 상태, 구현 파일, 실행 명령, 시험 결과, 실자료 검증 범위, 남은 차단요인, `descoped_to_future_work`
- `docs/UNSPECIFIED_CASES.csv`: 계약에 규칙이 없어 임시 처리한 사례와 그 영향(42절)
- `docs/SESSION_LOG.csv`: 세션별 시작·종료, 읽은 문서, 내린 판단, 남긴 인계(43절)

`queue/`의 task 상태와 `WORKER_STATUS.md`만으로 "지금 무엇이 돌고 있고 무엇이 남았는지"를 알 수 있어야 한다. 워커가 모두 죽어도 큐와 partition manifest로 재개할 수 있어야 한다.

`PHASE_HANDOFF.md` 최소 항목:

```text
phase_id
status: not_started | running | passed | failed | blocked
input_scope
config_hash
code_hash
started_at_utc
finished_at_utc
measured_runtime_seconds
measured_peak_rss_mb
measured_input_bytes
measured_output_bytes
gate_checks
failed_checks
last_valid_checkpoint
exact_resume_command
next_phase_entry_condition
barrier_state              # B1/B2/B3 통과 여부와 선언시각
tasks_total/done/failed/poison
active_workers_by_role
measured_throughput_per_worker
```

## 15.2 완료 게이트 원칙

- 산출물이 존재한다는 이유만으로 Phase를 통과시키지 않는다.
- schema, row count reconciliation, 오류율, provenance, 시험, 자원 사용을 함께 확인한다.
- 게이트 실패 상태에서 다음 대규모 단계로 자동 진입하지 않는다.
- 중단 후 재개가 되는지 R2 이전에 실제 시험한다.
- 빈 파일, 빈 표, 오류를 삼킨 실행을 성공으로 기록하지 않는다.

## 15.3 placeholder 금지

소스와 문서에서 다음을 검사한다.

```text
TODO
FIXME
NotImplementedError
빈 pass 구현
production path의 mock result
temporary success
dummy candidate
실제 결과처럼 보이는 hard-coded 수치
```

시험 fixture의 의도적인 더미값은 fixture 경로와 주석 안에서만 허용한다.

## 15.4 Context budget·모듈화 실행 계약

이 문서 전체를 한 번의 코딩 turn에서 모두 구현하려 하지 마라. P0에서 원본 계약을 변경하지 않고 다음 실행용 모듈을 생성한다.

```text
docs/runbook/
  00_invariants_and_goal.md
  01_inventory_and_quality.md
  02_rinex_harmonization.md
  03_features_and_roti.md
  04_baseline_and_detection.md
  05_spatial_and_network_events.md
  06_falsification_and_external_validation.md
  07_evaluation_and_claims.md
  08_scale_and_recovery.md
  09_publication_viability.md
```

각 Phase는 `00_invariants_and_goal.md`, 해당 Phase 모듈, `PHASE_HANDOFF.md`, 현재 config/schema만 주 실행 컨텍스트로 사용한다. 이전 Phase의 장황한 로그를 재주입하지 말고 claim ID·artifact path·config/code hash·gate 결과로 연결한다. 모듈화 과정에서 본 문서의 과학적 제한·안전·증거등급·누출방지 원칙을 축약·삭제하지 마라.

# 16. 세부 데이터 계약

## 16.1 전수 파일 인벤토리

`inventory/rinex_file_inventory.parquet`에 최소 다음 열을 저장한다.

```text
file_id
relative_path
filename
extension_chain
size_bytes
mtime_utc
compression_type
fingerprint_method
content_fingerprint
duplicate_group_id
rinex_version
rinex_file_type
satellite_system_declared
marker_name_raw
marker_number_raw
station_id_filename
station_id_header
station_id_canonical
station_id_conflict
receiver_number
receiver_type
receiver_version
antenna_number
antenna_type
approx_x_m
approx_y_m
approx_z_m
antenna_delta_h_m
antenna_delta_e_m
antenna_delta_n_m
interval_header_s
time_first_header_raw
time_last_header_raw
time_system_header
first_epoch_observed_raw
last_epoch_observed_raw
first_epoch_canonical
last_epoch_canonical
obs_types_signature
obs_type_count
signal_strength_unit
header_complete
parse_status
parse_error_class
parse_error_message_short
```

헤더 first/last와 실제 first/last epoch를 비교한다. 하루 2,880 epoch를 무조건 기대하지 말고 실제 span, 실제 interval, partial day, duplicate epoch, time-system boundary를 반영해 expected count를 계산한다.

중복은 다음 단계로 분류한다.

1. 동일 content hash
2. 동일 station/time span/obs signature이지만 압축만 다름
3. 겹치지만 서로 보완적인 파일
4. 동일 epoch에 값이 충돌하는 파일

중복 원본을 삭제하지 말고 canonical selection rule, excluded file ID, 근거를 manifest에 남긴다.

## 16.2 MetadataRegime

다음 중 하나가 실질적으로 바뀌면 regime 후보를 만든다.

- receiver serial/type/firmware
- antenna serial/type/radome
- approximate XYZ 또는 antenna delta
- interval
- RINEX major version
- constellation coverage
- raw observation code signature과 exact 3-character observation code/tracking attribute coverage
- RINEX 2→3/4 mapping status·mapping confidence·legacy ambiguity 구성
- signal strength unit
- 장기간 gap 뒤 운영 재개

오타와 실제 변경은 station log, 전후 다수 헤더, 좌표 차이, 변화 지속성으로 구분한다.

```text
regime_id
station_id
effective_start
effective_end
receiver_signature
antenna_signature
coordinate_signature
observation_signature
raw_observation_signature
canonical_observation_signature
tracking_attribute_signature
mapping_status_signature
interval_signature
evidence_file_ids
change_reason
confidence
manual_review_status
```

## 16.3 Canonical observation

```text
run_id
file_id
station_id
regime_id
epoch_time_raw
time_system_raw
epoch_time_utc
epoch_time_gpst
epoch_flag
receiver_clock_offset_s
satellite_id
constellation
prn
source_obs_code_raw
canonical_obs_code
obs_family
frequency_band
nominal_frequency_hz
tracking_code
tracking_attribute_known
mapping_method
mapping_status
mapping_confidence
mapping_evidence
value
unit_interpreted
unit_confidence
lli_raw
lli_loss_of_lock
lli_half_cycle
ssi_raw
parse_quality_flags
source_row_reference
```

장기 전체자료에서 이 표를 무조건 전량 영구저장하지 마라. 전체기간은 epoch summary와 daily accumulator를 보존하고, full observation은 R1/R2, 사건 전후 padding, 강건한 정상 표본에 우선 보존한다.

## 16.4 Epoch summary

```text
station_id
regime_id
epoch_time_utc
epoch_time_gpst
source_file_ids
interval_from_previous_s
epoch_flag
satellites_observed_total
satellites_by_constellation
signals_observed_total
valid_signal_strength_count
signal_strength_median
signal_strength_iqr
lli_count
loss_of_lock_count
half_cycle_count
phase_valid_count
code_valid_count
doppler_valid_count
duplicate_observation_count
parse_warning_count
availability_state
```

## 16.5 Window feature

```text
window_id
station_id
regime_id
window_start_utc
window_end_utc
window_size_s
constellation
signal_group
feature_name
feature_family
feature_value
feature_unit
expected_value
residual
robust_z
coverage_fraction
n_epochs_expected
n_epochs_observed
n_satellites
geometry_available
quality_flags
baseline_id
```

## 16.6 StationEvent

```text
station_event_id
station_id
regime_id
observed_start_utc
observed_end_utc
start_uncertainty_s
end_uncertainty_s
duration_observed_s
window_sizes_contributing
feature_families_triggered
primary_signals
constellations_affected
satellites_affected_count
satellites_visible_count
signal_drop_effect
tracking_drop_effect
slip_effect
position_effect
clock_effect
data_quality_flags
pre_recovery_contrast
post_recovery_contrast
raw_evidence_refs
baseline_refs
station_score
initial_label
initial_evidence_grade
```

## 16.7 NetworkEvent

```text
network_event_id
observed_start_utc
observed_end_utc
time_uncertainty_s
station_event_ids
stations_affected
stations_available
station_fraction_affected
station_geometry_summary
affected_observation_footprint
constellations_affected
bands_affected
satellite_commonality
station_commonality
network_coherence_score
lag_summary
data_pipeline_score
satellite_product_score
receiver_site_score
ionosphere_score
rfi_like_score
alternative_explanations
evidence_grade
classification
manual_review_status
```

# 17. 시간·관측소 정규화 검증

## 17.1 시간체계

GPST, UTC, GLONASS time, GST, BDT, QZSS time, 미상체계를 구분한다. 원시 timestamp와 선언체계를 보존한 뒤 canonical time으로 변환한다. leap second table 버전과 출처를 manifest에 기록한다.

필수시험:

- 알려진 leap-second 경계
- 일·연도 경계
- GPS week/day와 calendar round-trip
- BDT/GST/GLONASS 변환
- naive/aware datetime 혼용 방지
- UTC와 KST 보고값 round-trip

시간체계가 불명확하면 station 단독 품질분석은 할 수 있지만 network 동시성 분석에는 사용하지 않는다.

## 17.2 관측소 ID

- filename ID, `MARKER NAME`, `MARKER NUMBER`, station log ID를 별도 보존한다.
- 대소문자·국가코드·monument code를 임의로 소실하지 않는다.
- ID conflict를 자동 병합하지 말고 mapping table과 근거를 만든다.
- 좌표 근접성만으로 동일 관측소라고 결론내리지 않는다.

# 18. 특징군 의존성과 검열 처리

같은 원자료에서 파생된 여러 통계를 독립 증거로 중복계상하지 마라. `docs/DEPENDENCY_GRAPH.md`에 raw observation→feature→family score→event→claim 연결을 기록한다.

## 18.1 Signal family

- satellite/signal S값
- epoch median, trimmed mean, lower quantile, IQR
- constellation/band별 signal median과 coverage
- elevation-conditioned expected signal
- observed minus expected residual
- station-common residual component
- satellite-common residual component
- network-common residual component
- abrupt drop, sustained depression, recovery slope
- multi-band common vs selective attenuation
- group-calibrated lower-tail fraction

고도각 기준모형 후보:

```text
robust spline(elevation)
station/regime/signal별 smooth model
elevation × azimuth sector robust table
hierarchical median/MAD fallback
```

표본이 부족할 때 fallback 수준과 evidence coverage를 열로 남긴다.

## 18.2 Tracking family

- observed satellite 대비 geometrically expected satellite
- signal tracks per satellite
- simultaneous track loss
- reacquisition count와 관측된 duration
- constellation/band별 dropout ratio
- common-drop ratio
- observed-but-S-missing와 fully missing 구분
- total tracking loss 구간의 censoring-aware 지표

약한 위성이 탈락하면 남은 위성의 S 중앙값이 오를 수 있다. `관측된 S 분포`와 `추적 탈락`을 함께 보고하고, 탈락한 위성의 S를 0으로 대체하지 않는다.

## 18.3 Phase/lock family

- LLI loss-of-lock와 half-cycle을 분리
- phase arc break
- geometry-free phase jump
- Melbourne–Wübbena jump
- time-differenced phase residual
- 방법 간 cycle-slip consensus
- 다수 위성 동시 slip
- 단일 위성의 관측망 공통 slip

주파수·파장·신호조합을 constellation별로 검증한다. GLONASS FDMA channel이 필요한 계산에서 channel을 생략하지 않는다.

## 18.4 Code/phase/Doppler consistency family

- code-minus-carrier trend
- code-carrier divergence
- Doppler-integrated phase consistency
- time-differenced pseudorange residual
- inter-frequency divergence
- constellation common clock 제거 후 불일치

sampling interval, 단위, 부호정의를 산식에 명시한다. 구성할 수 없는 조합은 0이 아니라 결측이다.

## 18.5 Position/clock family

- static ENU residual
- horizontal/vertical robust z
- SPP residual RMS
- receiver clock step/drift proxy
- constellation-subset solution disagreement
- geometry-conditioned solution loss

정밀모델·제품이 부족한데 PPP라고 부르지 마라. 구현 수준에 맞게 `SPP diagnostic` 또는 `position residual diagnostic`로 표기한다.

## 18.6 Availability/recorder family

- unexpected epoch gap
- all-observation loss
- file reset boundary
- header/observation transition
- receiver clock reset
- epoch special event
- network ingestion synchronized gap

이 family는 RF-like score와 분리해 운영·자료 장애의 우선 분류에 사용한다.

# 19. 기준선 오염·누출 방지

기준선 group key의 기본 후보는 다음과 같다. 특히 RINEX 3/4는 3자리 관측코드와 tracking attribute를 분리 기준으로 사용한다. RINEX 2의 비유일 매핑은 동일 group에 편입하지 않는다.

```text
station_id
metadata_regime
receiver_type
receiver_firmware
antenna_radome
rinex_major_version
constellation
observation_family
exact_observation_code
nominal_frequency_hz
tracking_attribute_or_legacy_unknown
elevation_bin
azimuth_sector_if_supported
time_of_day_bin
season_or_day_of_year_bin
```

- 평가 사건과 주변 exclusion buffer를 학습 기준선에 넣지 않는다.
- retrospective 양방향 기준선과 pseudo-prospective 과거→미래 기준선을 분리한다.
- 공식 사건은 blind baseline과 threshold selection에 사용하지 않는다.
- 관측소·날짜를 행 단위로 무작위 섞지 않는다.
- 장비변경을 하나의 기준선이 흡수하지 않게 한다.

기본 강건값 후보:

```text
center = median(x)
scale = 1.4826 × MAD(x)
z_robust = (x - center) / max(scale, scale_floor)
```

MAD가 0이라고 임의의 작은 epsilon으로 큰 z를 만들지 마라. fallback 순서를 설정한다.

1. 동일 station/regime/signal의 인접 elevation bin
2. 동일 station/regime/band
3. 동일 receiver/antenna class의 안정 관측소
4. feature-specific empirical floor
5. baseline unavailable

fallback 단계별 사용률과 정상 holdout 분포를 보고한다. 변화점은 자동으로 장비변경이라고 확정하지 말고 헤더·station log·지속성을 확인한다.

# 20. StationEvent와 NetworkEvent 생성 규칙

## 20.1 탐지 순서

1. 단변량 robust residual과 변화점
2. feature family별 score
3. 규칙 기반 evidence composition
4. 비지도 모델은 보조순위화
5. 시간 연결과 최소근거를 적용한 StationEvent
6. 망 공통성과 위성 선택성을 적용한 NetworkEvent

Isolation Forest, LOF, autoencoder의 높은 점수는 원인 규명이 아니다. 모델 입력에 official event ID, 사건시각, 수동 label이 누출되지 않게 한다.

## 20.2 StationEvent

- 인접 anomalous window를 설정된 gap tolerance로 연결한다.
- 낮은 coverage로 끊긴 구간을 자동 정상으로 간주하지 않는다.
- 시작·종료는 `observed_first_abnormal_epoch`, `observed_last_abnormal_epoch`, `time_uncertainty_s`로 보고한다.
- 사건 전·후 recovery contrast를 계산한다.
- 한 epoch·한 family만의 사건은 높은 등급으로 올리지 않는다.
- file boundary, receiver reset과 겹치면 quality branch에서 먼저 검토한다.
- 여러 window 길이 중 유리한 것만 고르지 말고 사전 선택규칙과 sensitivity를 기록한다.

## 20.3 세 관점의 망 분해

### Station-centric

한 관측소에서 많은 위성·신호가 동시에 악화되는가?

### Satellite-centric

한 위성·signal이 넓은 관측망에서 동시에 악화되는가?

### Network-centric

여러 관측소에서 다수 위성 또는 동일 band의 이상이 시간적으로 일치하는가?

해석 우선순위:

```text
단일 station × 다수 satellite        → receiver/site/local RFI 비교
다수 station × 단일 satellite        → satellite/product 우선
인접 다수 station × 다수 satellite  → regional/common RF-like 가능성 상승
전국 다수 station × 완전 gap         → pipeline/time/product 우선
동일 band 선택적 악화                 → band-specific RFI 검토
동일 constellation만 악화            → product/time/receiver support 비교
```

이 표는 확정 규칙이 아니라 반증 우선순위다.

## 20.4 NetworkEvent clustering

- StationEvent의 시간 overlap 또는 허용 lag를 사용한다.
- station 거리, network adjacency, 공식 영향권은 서로 다른 공간정의로 보존한다.
- 거리 임계값을 보편값으로 하드코딩하지 않는다.
- 시간 tolerance와 공간 threshold 민감도를 시험한다.
- feature family, constellation, affected band의 유사도를 사용한다.
- 한 긴 사건이 서로 무관한 사건을 이어붙이는 chaining을 방지한다.
- `stations_available`을 분모로 하며 전체 등록 station 수를 기계적으로 쓰지 않는다.

## 20.5 시간지연 해석

- cross-correlation은 30초 sampling과 결측을 고려한다.
- lag를 간섭원 이동, 전파속도, 방향으로 변환하지 않는다.
- station clock과 ingestion delay를 먼저 확인한다.
- 1 epoch 차이는 30초 해상도 범위의 불확실성으로 보고한다.

## 20.6 Spatial Zone

공식 사건이 source area/coordinate를 제공할 때에만 다음 zone을 구성할 수 있다.

```text
Zone A: source-defined affected/core region
Zone B: near comparison region
Zone C: far in-network control
Zone D: external or unaffected control
```

경계를 설정파일에 두고 여러 대안 경계로 민감도를 확인한다. 공식 출처가 말한 위치와 RINEX affected footprint를 혼동하지 않는다.

# 21. 반증 엔진

모든 상위 후보는 다음 대안설명을 체계적으로 검토한다. 반증되어 탈락한 후보도 `docs/FALSIFICATION_LOG.md`에 남긴다.

## 21.1 수신기·안테나·현장

- metadata regime 변경 전후
- receiver reboot/reset/clock step
- antenna/radome/firmware 변경
- station coordinate/antenna height 변경
- 동일 sidereal time 또는 동일 azimuth sector 반복
- 낮은 elevation 위주 저하
- 특정 station의 장기 기준선 이동
- 주변 차폐·공사·수목·다중경로 가능성

## 21.2 위성·항법제품

- 단일 satellite의 광역 공통 이상
- broadcast health와 ephemeris age
- SP3/CLK/BRDC 공백·불연속
- constellation clock/time issue
- satellite maneuver/known anomaly
- 먼 control station의 동일 satellite

## 21.3 전리층·우주기상

- geometry-free 또는 TEC-like 지표
- **ROTI**: 후보 시간창의 관측소별·위성별 ROTI(4.5절)와 정상 기준선 대비 상승 여부
- **IGS GIM 대조**: 후보 시각·지역의 GIM TEC 및 그 변화율와의 광역 배경 정합성. GIM의 격자·시간 해상도와 final/rapid 버전을 기록하고 30초 국지 사건의 직접 근거로 쓰지 않는다.
- **지자기 지수 필터**: Kp ≥ 5 또는 Dst ≤ −50 nT(설정값) 구간의 `space_weather_alert` 플래그. 플래그 기간의 후보는 자동 제외가 아니라 반증 검토를 강화하고, 결과를 `softly_explained` 또는 `conflicting_evidence`로 명시적으로 남긴다
- 광역성, local time, geomagnetic latitude
- 주파수 의존성과 constellation 공통성: `f^-2`는 1차 전리층 코드·반송파 지연의 분산성 서명에 적용한다. geometry-free 위상/코드 조합이 이 관계와 정합하는지 검사하되, C/N0 저하·tracking loss·scintillation 진폭이 동일한 `f^-2`를 따른다고 가정하지 마라.
- 공식 space-weather index의 시간해상도 제한(Kp 3시간, Dst 1시간)
- scintillation monitor 부재라는 제한
- 관측소 간 반응 차이의 대안설명으로서 수신기 기종·펌웨어별 내부 간섭완화 능력 차이(regime 정보와 교차 검토)

우주기상 index가 높다는 이유로 자동 제외하지 말고, 낮다는 이유로 local scintillation을 불가능하다고 단정하지 않는다. ROTI 상승과 대역 선택적 저하가 동시에 관측되는 등 지표가 상충하면 어느 한쪽 가설로 강제하지 말고 `conflicting_evidence`로 기록한다.

## 21.4 기상

- 강수·적설·태풍·착빙 가능성
- station-specific 자료 coverage
- 기상자료 시간·공간 해상도
- S값·안테나·다중경로 변화와 일관성

## 21.5 Data pipeline

- 전국 또는 서버 그룹의 동일시각 gap
- file rollover, compression, ingest 재시작
- header와 실제 epoch 불일치
- station log 운영중단
- parser bug 또는 unsupported observation
- 시간변환 오류가 만든 가짜 동시성

## 21.6 반증 상태

```text
hard_refuted
softly_explained
not_refuted
untestable
conflicting_evidence
```

`untestable`은 긍정증거가 아니다. 후보 funnel에 각 단계의 수를 기록한다.

```text
raw_anomalous_windows
station_events
after_data_quality_filter
after_receiver_site_review
after_satellite_product_review
after_ionosphere_weather_review
network_events
officially_concordant_events
final_reportable_candidates
```

# 22. Blind discovery와 공식 사건 replay 격리

## 22.1 Track A — Blind discovery

- 공식 사건 날짜·시각·영향권을 feature, baseline, threshold, 후보생성에 사용하지 않는다.
- candidate table, config hash, code hash를 먼저 freeze한다.
- freeze artifact의 timestamp와 SHA-256을 기록한다.

## 22.2 Track B — Official-event replay

- 정부, ICAO, 항공·해양·통신 당국 등 1차 source를 우선한다.
- exact time, source timezone, time precision, affected area, source wording을 보존한다.
- 날짜만 알려진 사건은 하루 전체 positive label이 아니다.
- `interference`, `disruption`, `jamming`이라는 원문 표현을 임의로 강화하지 않는다.
- 같은 원문을 재인용한 여러 기사를 독립증거로 세지 않는다.

공식 사건표:

```text
official_event_id
source_organization
source_document_title
source_document_id
source_url
publication_time
event_start_raw
event_end_raw
source_timezone
event_start_utc
event_end_utc
time_precision
affected_area_raw
affected_area_geometry_or_description
event_term_raw
event_type_normalized
source_tier
advisory_or_confirmed
confidence_in_extraction
accessed_at
notes
```

`source_tier`는 정부 1차 발표 / 국제기구 기록(ICAO EUR/NAT 등) / 항행·항공 경보(NOTAM, NAVAREA XI) / 집계·2차 보고(AIS 이상 집계 등)를 구분한다. `advisory_or_confirmed`는 해당 문서가 예방적 경보인지 실제 발생 확인기록인지 원문 표현대로 구분하며, `advisory` 단독 출처는 E4 승격의 충분조건이 아니다.

## 22.3 Track C — Matched negative controls

정상 대조구간은 사전에 다음을 맞춘다.

- station availability
- time of day와 season
- satellite geometry
- metadata regime
- data-quality gate
- **유사 지자기 활동 수준**: Kp 범주(예: 정온/활동/폭풍) 또는 `space_weather_alert` 상태가 사건구간과 유사한 날을 우선 선택한다. 매칭이 불가능하면 우주기상 상태 차이를 대조 한계로 기록한다
- official event buffer와 비중첩

공식 사건이 보고되지 않았다는 사실은 실제 RF 이상이 없었다는 완전한 보증이 아니다.

## 22.4 비교 결과 상태

```text
hit
partial_temporal_match
partial_spatial_match
weak_feature_match
miss
unassessable_no_station_coverage
unassessable_data_quality
unassessable_time_precision
```

miss를 숨기지 말고 sampling, station coverage, 품질, feature coverage를 분석한다.

## 22.5 누출검사

- official event file load 전에 blind artifact hash가 있는가?
- source event ID가 baseline/model feature에 들어갔는가?
- threshold가 official-event 성능만 최대화하도록 선택됐는가?
- 공식사건 주변이 정상학습에 들어갔는가?
- Track A와 Track B 성능표현을 혼합했는가?

## 22.6 블라인드 워커 프로세스 격리

병렬 실행에서 누출은 코드뿐 아니라 **프로세스 구성**으로도 발생한다.

- `W_VAL`(공식 사건 정규화·replay)은 별도 프로세스로 실행하고 출력은 `validation_unblinded/`에만 쓴다. 블라인드 워커는 이 경로를 읽지 않는다.
- 블라인드 워커와 `W_VAL`은 같은 작업 큐를 공유하지 않는다. task 이름·shard key에 공식 사건 시각·지역이 드러나지 않게 한다(`official_event_id`만 사용).
- 배리어 B3(blind freeze) 이전에는 `W_VAL` task를 큐에 넣지 않는다. orchestrator가 freeze manifest 해시를 기록한 뒤에만 생성한다.
- 하나의 에이전트·사람이 두 역할을 순차 수행해야 한다면, 블라인드 산출물을 먼저 동결·해시한 뒤에만 공식 자료를 열람하고 그 순서를 `RUN_LOG.md` 시각으로 증명한다. 이는 프로세스 분리보다 약한 통제이므로 보고서에 명시한다.
- 격리 위반이 확인되면 해당 산출물에 `blind_integrity=compromised`를 남기고 영향 범위를 재실행하거나 증거등급을 강등한다. 은폐하지 마라.

# 23. 증거등급 적용 규칙

앞 절의 E0~E5를 다음처럼 엄격히 적용한다.

- E0: 자료 부족, 시간 불명, 품질실패 또는 핵심 특징 coverage 부족
- E1: 한 station에서 한 feature family만 이상
- E2: 한 station에서 서로 의존성이 낮은 2개 이상 family가 일관
- E3: 서로 다른 복수 station에서 시간·패턴·반증 결과가 일관. 한 station의 multi-band 일치만으로는 E2 상한이다.
- E4: E3와 독립된 발생확인 공식 1차 출처 또는 별도 센서의 정확한 동일 시공간 일치. advisory 중첩만으로는 E4를 부여하지 않는다.
- E5: 직접 RF 측정 또는 통제실험으로 원인 확인

30초 CORS RINEX 단독은 E3을 넘지 않는다. 공식 외부사건을 정확히 연결하면 E4까지 가능하다. E5는 이번 자료만으로 부여하지 않는다.

## 23.1 Jamming-like 최소논리

다음은 후보논리이며 데이터 교정 없는 고정 임계값이 아니다.

- 다수 위성·신호의 동시 signal/tracking 악화
- elevation/azimuth 기대 대비 station-common drop
- phase/lock 또는 position/clock의 일관된 추가 이상
- 관측 가능한 abrupt onset과 recovery
- pipeline/receiver reset만으로 설명되지 않음
- 가능하면 여러 인접 station의 시공간 coherence

## 23.2 Spoofing-compatible 최소논리

SNR 저하나 위성 수 감소만으로 spoofing label을 주지 않는다.

- static position의 비물리적 coherent displacement
- receiver clock의 coherent anomaly
- constellation subset solution disagreement
- code/phase/Doppler consistency 이상
- tracking은 유지되지만 여러 위성 측정이 공통방향으로 왜곡

correlator/IQ/독립 clock이 없으므로 확정하지 않는다. jamming-like와 spoofing-compatible을 하나의 positive label로 합치지 않는다.

# 24. 평가·불확실성 계약

## 24.1 분할

행 단위 무작위 분할을 금지하고 목적에 맞게 다음을 사용한다.

- leave-station-out
- leave-day/week-block-out
- leave-metadata-regime-out
- pseudo-prospective past→future
- blind freeze→official replay

## 24.2 Ground truth가 부족할 때

- empirical alert rate per valid station-day
- event rate per valid observation day
- manual-review yield
- threshold에 따른 candidate stability
- station concentration
- matched-control exceedance rate
- official-event concordance
- feature-family agreement
- falsification survival rate

## 24.3 방어 가능한 official truth가 있을 때만

- event-level sensitivity proxy
- first observed anomaly까지의 시간과 30초 불확실성
- station-level affected fraction
- matched-control false-positive proxy

## 24.4 통계 규칙

- station epoch를 독립 표본으로 취급하지 않는다.
- station-day 또는 방어 가능한 block 단위 bootstrap을 사용한다.
- 여러 station/window/feature 탐색에는 다중검정을 고려한다.
- p-value만으로 사건을 선정하지 않는다.
- effect size, coverage, uncertainty를 같이 보고한다.
- threshold 선택과 최종평가에 같은 자료를 사용하지 않는다.
- sensitivity 결과 중 유리한 값만 선택하지 않는다.

산출물:

- `evaluation/split_manifest.parquet`
- `evaluation/normal_holdout_metrics.parquet`
- `evaluation/official_event_results.parquet`
- `evaluation/threshold_sensitivity.parquet`
- `evaluation/bootstrap_intervals.parquet`
- `reports/15_evaluation_protocol_and_results.md`

# 25. 규모실행 Runbook R1→R5

사용자가 알려준 2021~2026년 범위를 완전년도로 가정하거나 즉시 전체 실행하지 마라. 헤더·실제 epoch로 확인한 `analysis_cutoff_utc`까지 아래 게이트를 순서대로 통과하고, 부분 연도는 YTD로 보고한다.

## R1 — 단일 파일 smoke test

선정:

- 대표 정상 observation 파일 1개
- 가능하면 실제 RINEX version/압축형식별 추가 1개
- 손상 또는 미지원 파일 1개를 negative test로 포함

확인:

- 헤더와 실제 first/last epoch
- 관측코드·단위·time system
- canonical row와 epoch summary
- 기하 또는 geometry-unavailable 경로
- peak RSS와 처리시간
- atomic write와 동일설정 재실행 skip

R1 통과 전 R2로 가지 않는다.

## R2 — 단일 StationDay end-to-end

- 정상일 1개와 가능한 경우 known/problem day 1개
- inventory→parse→quality→feature→baseline fallback→event→report 전 경로
- 후보에서 원시 epoch까지 drill-down
- 강제 중단 후 resume 시험
- golden output 생성

## R3 — 소규모 망·기간 파일럿

실제 인벤토리를 보고 범위를 선택한다. 시작 후보:

- 3~10 station
- 1개월 또는 계절이 다른 여러 주
- 서로 다른 receiver/antenna regime
- 정상기간, 품질문제기간, 가능한 사건기간
- official replay가 있으면 blind freeze 후 known day와 matched control

검사:

- station/network event rate
- candidate explosion
- baseline coverage와 fallback
- NetworkEvent chaining
- data-pipeline false event
- 실측 GB/h, files/h, station-days/h
- peak RSS, output/input ratio, cache growth

## R4 — 대표 연도 또는 대표 지역

선정근거:

- 계절 전체
- station 밀도와 장비 다양성
- 정상·품질문제 기간
- 가능한 공식사건 기간
- full run의 5~20% 또는 실측으로 방어 가능한 비율

R4에서 schema, feature set, threshold selection policy, config를 동결한다. R5 결과를 보고 임계값을 계속 바꾸지 않는다.

## R5 — 확인된 전체기간·전체망

- 실제 header/epoch에서 확인된 최초~최종 기간
- 지원 가능한 전체 station/regime
- 실패 partition 자동 재시도와 unresolved 목록
- 월/연도 checkpoint
- 중간 resource forecast 갱신
- 종료 후 manifest reconciliation

## 25.1 단계별 필수 실행기록

```text
scope_definition
input_files
input_bytes
station_days_attempted
station_days_succeeded
station_days_failed
runtime_seconds
throughput_gb_per_hour
files_per_hour
peak_rss_mb
output_bytes
cache_bytes
candidate_windows
station_events
network_events
warnings_by_class
config_hash
code_hash
```

## 25.2 전체 소요시간 산정

R3/R4 실측값으로만 계산한다.

```text
estimated_runtime = remaining_input_bytes / measured_effective_throughput
```

압축률, file당 overhead, station heterogeneity, retry를 반영한 하한·중앙·상한을 보고한다. NMEA 등 다른 프로젝트 처리량을 가져오지 않는다.

## 25.3 R5 진입 게이트

- R1~R4 pass
- schema freeze
- config freeze
- baseline/leakage audit pass
- candidate rate sanity pass
- 예상 disk + 안전마진 확보
- resume/atomic write test pass
- retention policy 확정
- 예상 완료시간과 운영방식 기록

# 26. 자원예산·저장정책·중단조건

## 26.1 메모리

- 전체 file inventory와 소형 metadata 외에 전 관측을 RAM에 올리지 않는다.
- `worker 수 × file expansion × batch memory` 상한을 산정한다.
- 단계별 peak RSS를 실측한다.
- OS page cache와 process RSS를 구분한다.
- 메모리 압박으로 swap thrashing이 생기면 worker/batch를 줄인다.

## 26.2 디스크

영구보존 우선순위:

1. inventory와 provenance
2. epoch summary
3. station/network event와 padding raw evidence
4. baseline accumulator와 parameter
5. 정상 stratified sample
6. 재생성 가능한 full-observation cache

`persist_all_observations=false`가 기본이다. 전량 observation 저장이 연구질문에 필수라면 R3 실측 후 disk budget을 계산해 명시적으로 켠다.

## 26.3 Descope 순서

1. 불필요한 full-observation 중간저장 중지
2. interactive figure와 비핵심 고해상도 출력 축소
3. 정상 raw-evidence 표본률 축소
4. 병렬 worker 축소
5. 비핵심 model/window 축소
6. 대표범위까지만 실행하고 R5 blocked 보고

inventory, provenance, quality, baseline, falsification을 생략해 속도를 맞추지 않는다.

## 26.4 즉시 중단조건

- 원시자료에 쓰기가 발생하려는 경우
- output disk 안전마진 미달
- 시간변환 미검증으로 망 동시성 신뢰 불가
- parser silent loss 또는 row reconciliation 실패
- schema drift로 기존 partition과 혼합 위험
- config/code hash 없이 resume하려는 경우
- candidate rate가 `candidate_rate_guard` 범위를 벗어나고 원인 미확인 (임계값 조정으로 대응 금지)
- 전체 예상 소요가 `runtime_guard.max_full_run_hours`를 초과하는데 병목 개선 없이 다음 규모로 진입하려는 경우
- 해제 캐시가 `cache_policy` 상한을 넘어 계속 증가하는 경우
- 미규정 사례가 `unspecified_cases.escalation_count`를 넘었는데 규칙 확정 없이 최종 수치를 만들려는 경우
- official-event leakage 발견
- 기존 사용자 변경과 충돌

중단은 `blocked`로 기록하고 정확한 원인, 마지막 valid checkpoint, 필요한 조치, 재개명령을 남긴다.

# 27. Atomic write·checkpoint·resume

## 27.1 Partition manifest

```text
partition_key
input_file_ids
input_fingerprints
config_hash
code_hash
schema_version
started_at
completed_at
row_counts
quality_counts
output_files
output_hashes
status
error_class
retry_count
worker_id
role
shard_index
shard_count
lease_id
lease_expiry_utc
task_id
promoted_from_run_id
```

## 27.2 재개 규칙

- input fingerprint, config hash, code hash, schema version이 모두 같고 output hash가 유효할 때만 skip한다.
- partial `.tmp`는 성공 산출물이 아니다.
- checksum mismatch는 해당 partition만 격리·재실행한다.
- 동일 partition의 동시 write를 리스 기반 lock으로 막는다. 리스는 `worker_id`, `role`, `run_id`, `host`, `pid`, `heartbeat_at_utc`, `lease_expiry_utc`를 포함한다.
- stale lock 판단기준(`stale_lease_grace_seconds`)과 강제해제·재할당 이력을 남긴다. heartbeat가 살아 있는 리스는 회수하지 않는다.
- 죽은 워커의 부분 산출물(`.tmp`)은 삭제하지 말고 격리한 뒤 task를 재할당한다.
- 다른 워커가 완료한 partition은 input fingerprint·config·code·schema·output hash가 모두 일치할 때만 재사용하고, 재사용 사실을 provenance에 남긴다.
- retryable/non-retryable error를 구분한다.

## 27.3 결정성

- random seed를 설정·기록한다.
- unordered file iteration에 의존하지 않는다.
- floating aggregation tolerance를 명시한다.
- worker 수와 chunk 크기가 event ID를 바꾸지 않아야 한다.
- 중단·resume 결과가 uninterrupted run과 동일해야 한다.
- `worker_id`, `role`, host, shard 배정, task 처리 순서, lease 시각은 ID와 수치에 영향을 주지 않는다. provenance 열에만 나타난다.
- `--shards N`, `--workers M`을 바꿔도 산출물이 동일해야 한다(41.2절 불변성 시험). shard 배정은 내용 해시 기반으로만 계산한다.
- 부동소수 합산 순서에 의존하는 집계는 금지한다. 결합 순서와 무관한 방식(정렬된 축약, Kahan 합산, 고정 bin 히스토그램)을 쓰고 허용 tolerance를 명시한다.

# 28. 상세 시험 계약

## 28.1 RINEX·압축 단위시험

- RINEX 2/3/4 header
- long/short filename mismatch
- `.gz`, Hatanaka, 실제 보유 `.Z`
- mixed constellation
- observation-code continuation
- missing `END OF HEADER`
- truncated final epoch
- 파일 확장자와 header file type 불일치

## 28.2 시간 단위시험

- GPS/UTC leap second
- GLONASS/GST/BDT 변환
- day/year boundary
- leap year DOY
- UTC/KST 병기
- unknown/ambiguous time system

## 28.3 관측 단위시험

- missing vs observed zero
- LLI bit별 parsing
- SSI parsing
- S observation unit confidence
- duplicate epoch/observation
- special epoch flag
- clock offset
- RINEX 2 observation mapping provenance

## 28.4 기하 단위시험

- known elevation/azimuth
- below-horizon handling
- missing ephemeris
- ephemeris age/health
- product boundary
- GLONASS channel-dependent wavelength

## 28.5 특징 단위시험

- signal drop
- censored tracking loss
- cycle slip
- Doppler-phase consistency
- metadata regime boundary
- robust z with MAD zero
- baseline fallback
- missing geometry

## 28.6 사건 단위시험

- temporal merge/split
- gap with missing coverage
- stable event ID
- NetworkEvent chaining 방지
- station availability denominator
- one-satellite network anomaly
- file-boundary pipeline issue

## 28.7 합성 시나리오

각 시나리오의 기대 family, label branch, 반증상태를 고정한다.

1. 정상 elevation-dependent S curve
2. 한 station의 모든 satellite signal drop + tracking loss
3. 한 satellite의 전국 공통 이상
4. receiver reset과 파일경계
5. 전국 동시 data-pipeline gap
6. 특정 azimuth/elevation sector 반복 다중경로
7. metadata change 후 장기 S offset
8. 광역 전리층 유사 주파수 의존 이상
9. band-selective local RFI-like anomaly
10. 10초 사건을 30초 sampling했을 때 miss/alias
11. spoofing-compatible static position/clock drift
12. missing을 0으로 잘못 채운 가짜 drop 방지
13. official event의 baseline 누출 탐지
14. chunk boundary의 StationEvent
15. NetworkEvent 중 station availability 변화

## 28.8 Integration/Golden/Scale 시험

- fixture inventory→final report end-to-end
- R1 실제파일 end-to-end
- 압축/비압축 동일내용 동등성
- forced interruption 뒤 resume
- config 변경 시 cache invalidation
- schema 변경 시 unsafe merge 차단
- blind freeze before official replay
- chunk 크기 0.5×/1×/2× 결과 동등성
- worker 1개/다수 결과 동등성

Golden output:

- inventory 핵심행
- epoch summary
- feature row
- StationEvent
- NetworkEvent
- candidate evidence JSON
- 보고서 핵심표

run ID, 임시경로 같은 비결정 field만 명시적으로 normalize한다.

## 28.9 정적검사

- `pytest`
- `ruff check`
- `ruff format --check` 또는 동등 formatter
- 적용한 type checker
- placeholder scan
- Markdown link/table sanity
- code fence pair
- schema contract

시험 수를 부풀리지 말고 pass/fail/skip과 skip 이유를 보고한다.

## 28.10 병렬 실행 시험

- shard 불변성: `--shards 1/4/16`의 산출물 해시 동일(provenance 열 제외)
- worker 불변성: `--workers 1`과 `--workers N`의 산출물 해시 동일
- 큐 원자성: 두 워커가 같은 task를 동시에 lease할 때 정확히 하나만 성공
- 리스 만료 후 재할당, heartbeat 유지 중 회수 차단, 죽은 워커의 `.tmp` 격리
- 배리어: B2 이전 탐지 task가 leasable 되지 않는지, B3 이전 `W_VAL` task가 생성되지 않는지
- 경계 사건: 자정·시간블록 경계를 걸치는 StationEvent·NetworkEvent·ROTI arc가 패딩·재병합 후 직렬 실행과 동일한지
- 분산 집계: 스케치 기반 median·MAD·분위수와 정확값의 오차가 허용 범위인지
- 부동소수 결합 순서 무관성: 축약 순서를 바꿔도 tolerance 안에서 동일한지
- 실패 격리: poison task가 있어도 나머지 shard가 완료되는지
- backpressure: 디스크 여유 임계 이하에서 신규 lease가 중단되는지
- 블라인드 격리: 블라인드 워커가 `validation_unblinded/`를 읽거나 `W_VAL` task를 lease하려 할 때 차단되는지

# 29. CLI 계약

사용자가 Phase별 또는 전체 실행을 재현할 수 있게 한다.

```powershell
python -m rinex_interference.cli doctor --config config/analysis.yaml
python -m rinex_interference.cli audit-assets --config config/analysis.yaml
python -m rinex_interference.cli inventory --config config/analysis.yaml
python -m rinex_interference.cli build-metadata --config config/analysis.yaml
python -m rinex_interference.cli parse --config config/analysis.yaml --scope r1
python -m rinex_interference.cli quality --config config/analysis.yaml --scope r2
python -m rinex_interference.cli geometry --config config/analysis.yaml --scope r2
python -m rinex_interference.cli features --config config/analysis.yaml --scope r2
python -m rinex_interference.cli baselines --config config/analysis.yaml --scope r3
python -m rinex_interference.cli detect --config config/analysis.yaml --track blind --scope r3
python -m rinex_interference.cli freeze-blind --config config/analysis.yaml
python -m rinex_interference.cli validate-official --config config/analysis.yaml
python -m rinex_interference.cli evaluate --config config/analysis.yaml
python -m rinex_interference.cli report --config config/analysis.yaml
python -m rinex_interference.cli run --config config/analysis.yaml --scale r4
python -m rinex_interference.cli resume --run-id <RUN_ID>
python -m rinex_interference.cli verify --run-id <RUN_ID>
```

병렬 실행 명령:

```powershell
# 1) 오케스트레이터: 계획 수립과 큐 생성
python -m rinex_interference.cli plan --config config/analysis.yaml --scale r3 --shards 16
python -m rinex_interference.cli queue status --config config/analysis.yaml
python -m rinex_interference.cli barrier status
python -m rinex_interference.cli barrier declare --name b2_baseline_frozen --evidence <MANIFEST_HASH>

# 2) 워커: 역할을 지정해 큐에서 task를 가져간다(pull 모델)
python -m rinex_interference.cli worker --role W_FEAT --workers 6 --config config/analysis.yaml
python -m rinex_interference.cli worker --role W_DET --shard 3/16 --once

# 3) 축약·승격·회수
python -m rinex_interference.cli reduce --stage network_events --config config/analysis.yaml
python -m rinex_interference.cli promote --run-id <RUN_ID> --stage features
python -m rinex_interference.cli requeue --status failed --max-attempts 3
python -m rinex_interference.cli queue poison-list
```

모든 해당 명령은 `--dry-run`, `--log-level`, `--workers`, `--station`, `--start`, `--end`를 지원한다. `--force`는 명시적이어야 하며 원본에는 적용할 수 없다.

병렬 실행 명령의 추가 규칙:

- `worker`는 `--role`을 반드시 요구하고, 역할에 허용되지 않은 stage의 task는 lease하지 않는다.
- `worker`는 `--workers`(프로세스 내 동시 실행 수)와 `--shard i/N`(외부에서 분할)을 함께 지원하되, 어느 조합에서도 결과가 같아야 한다.
- 배리어가 닫혀 있으면 해당 stage의 task는 큐에서 leasable 상태가 되지 않는다. 워커가 배리어를 우회하는 옵션은 제공하지 않는다.
- `doctor`는 큐 백엔드의 원자성, 큐 위치(로컬 디스크 여부), 호스트 시계 오차, 워커당 RAM 예산, 디스크 여유, 압축 해제 캐시 경합을 점검한다.
- 종료코드는 정상 0, data/config/resource/internal error 외에 `queue_empty`, `barrier_blocked`, `lease_lost`를 구분한다.

`--dry-run`은 input 수, 예상 작업, cache hit, 예상 output 공간을 표시하고 분석산출물은 쓰지 않는다. 정상 종료 0과 data/config/resource/internal error 종료코드를 구분한다.

# 30. 후보 Evidence Bundle 계약

각 최종 후보에 기계와 사람이 모두 검토할 수 있는 JSON bundle을 만든다.

```json
{
  "network_event_id": "<stable_id>",
  "classification": "jamming_like_anomaly",
  "evidence_grade": "E3",
  "observed_time": {
    "start_utc": "<observed>",
    "end_utc": "<observed>",
    "start_kst": "<derived>",
    "end_kst": "<derived>",
    "uncertainty_seconds": "<derived_from_sampling>"
  },
  "coverage": {
    "stations_available": "<observed>",
    "stations_affected": "<derived>",
    "satellites_observed": "<observed>",
    "feature_coverage": "<derived>"
  },
  "feature_families": [],
  "affected_observation_footprint": {},
  "raw_evidence_refs": [],
  "baseline_refs": [],
  "alternative_explanations": [],
  "falsification_results": [],
  "official_event_links": [],
  "limitations": [],
  "claim_ids": []
}
```

위 문자열은 schema 예시이며 실제 값이 아니다. 최종 후보표에는 다음을 포함한다.

```text
network_event_id
classification
evidence_grade
observed_start_utc
observed_end_utc
observed_start_kst
observed_end_kst
time_uncertainty_s
stations_affected
stations_available
station_fraction_affected
constellations_affected
bands_affected
feature_families
network_coherence_score
primary_alternative_explanation
falsification_survival_status
official_match_status
official_event_ids
data_quality_status
review_status
evidence_bundle_path
produced_by_worker_id
reviewed_by
boundary_merged            # 일자·시간블록 경계에서 재병합된 사건인지
```

수동 검토표:

```text
reviewer_id
review_timestamp
candidate_id
data_visible_to_reviewer
blind_or_unblinded
classification_before
classification_after
evidence_grade_before
evidence_grade_after
hard_refutation
soft_explanation
uncertainty
notes
```

검토자가 official event를 보았는지 반드시 기록한다.

# 31. 시각화 추가 계약

모든 그림에 time zone, sampling interval, station 수, coverage, 단위, event ID, source scope를 표시한다.

## 31.1 품질 그림

- year×station availability heatmap
- RINEX version/interval/obs-code timeline
- metadata regime timeline
- station-day completeness 분포
- S-value coverage와 unit confidence
- gap duration과 동시성 분포

## 31.2 기준선 그림

- signal/elevation curve by representative signal/regime
- residual distribution과 robust scale
- time-of-day/seasonal residual
- baseline coverage/fallback level
- metadata change 전후

## 31.3 후보 그림

- 사건 전후 station별 multi-panel time series
- constellation/band별 signal/tracking/phase
- satellite×time heatmap
- station×time heatmap
- available station 대비 affected station map
- elevation/azimuth distribution
- 유효한 position/clock diagnostic
- alternative-explanation comparison
- official time/zone overlay는 unblinded figure에만 추가

## 31.4 금지 표현

- 지도에 source location을 추정한 듯한 marker를 놓지 않는다.
- 그림·캡션·주석에서 특정 국가·조직·시설을 원인 주체로 지목하거나 암시하지 않는다. 공식 발표 인용은 출처를 명시한 인용 형식으로만 표기한다.
- missing을 0 색상으로 그리지 않는다.
- 후보별 color scale을 임의 변경해 효과를 과장하지 않는다.
- station 수가 다른 비교에 count만 쓰지 말고 fraction도 병기한다.
- UTC/KST를 축과 제목에 명시한다.
- 한글 font가 깨지지 않는지 실제 render를 확인한다.

# 32. Claim Registry·임계값·출처

## 32.1 `docs/CLAIM_REGISTRY.csv`

```text
claim_id
claim_text_ko
claim_type
status
value
unit
population_scope
time_scope
source_artifact
source_rows_or_query
source_document
calculation_method
config_hash
code_hash
verified_at
review_notes
run_id
worker_id
shard_count
supersedes_claim_id
superseded_by_claim_id
```

`claim_type`:

```text
observed
derived
external
assumption
limitation
```

`status`:

```text
proposed
archive_reported
verified
rejected
superseded
unverified
```

파일 수, station 수, 기간, 결측률, candidate 수, 처리량도 claim이다. 보고서의 핵심 숫자는 claim ID에서 source table 또는 계산 query로 역추적돼야 한다. 재실행 결과가 달라지면 이전 claim을 삭제하지 말고 supersede한다.

## 32.2 `docs/THRESHOLD_TRACEABILITY.md`

```text
threshold_name
value
unit
direction
origin
source_reference
calibration_scope
calibration_period
holdout_period
group_key
sensitivity_range
selected_before_final_evaluation
config_path
status
```

origin:

```text
theoretical_reference
rinex_standard_semantics
literature_candidate
receiver_documented
dataset_calibrated
operational_candidate
```

문헌의 3 dB, 6 dB 같은 값을 본 수신기·30초 aggregation·signal·elevation 조건에서 검증하지 않고 확정값으로 쓰지 않는다.

## 32.3 `docs/SOURCE_REGISTER.md`

```text
source_id
organization_or_authors
title
version_or_date
url_or_local_path
accessed_at
document_type
relevant_section
claim_or_threshold_used
applicability_to_this_data
limitations
```

우선순위:

1. RINEX/IGS/수신기 제조사 공식문서
2. 정부·ICAO 등 사건 1차 원문
3. peer-reviewed 연구
4. 공식 운영기관 metadata
5. 2차 기사·블로그는 탐색 보조

# 33. 필수 연구 문서

## `docs/METHODOLOGY.md`

다음을 재구현 가능한 수준으로 쓴다.

- 분석단위와 안정적 ID
- time normalization
- station mapping과 metadata regime
- observation code와 unit
- quality policy
- orbit/geometry
- feature definition
- baseline/fallback
- StationEvent/NetworkEvent
- falsification
- official validation
- evaluation/statistics

## `docs/DATA_DICTIONARY.md`

모든 table/column의 type, unit, null 의미, key, 허용범위, provenance를 기록한다.

## `docs/SCIENTIFIC_LIMITATIONS.md`

최소 다음을 포함한다.

- 30초 sampling과 짧은 사건 누락
- RF spectrum/IQ/AGC/correlator 부재
- S observation/SSI의 수신기별 의미
- tracking-loss selection bias
- elevation·multipath·site environment
- receiver/antenna/firmware regime
- ionosphere·space weather confounding
- orbit product와 time-system 오류
- data-pipeline synchronized gap
- station distribution과 spatial coverage
- affected footprint ≠ source location
- official event 목록의 불완전성과 보고편향
- ground truth 부족과 metric 제한
- observational study의 인과 제한
- Kp/Dst의 3시간·1시간 해상도와 30초 사건 시각의 비교 한계
- ROTI가 진폭 scintillation(S4)의 직접 측정이 아니라는 점과 GLONASS FDMA bias 제한
- NOTAM·항행경보의 advisory 성격과 실제 발생 확인기록의 구분
- AIS 위치이상의 GNSS 외 원인(AIS 장비·수신망) 가능성
- 공간통계(Moran's I 등)의 가중행렬·관측소 밀도·도서 고립노드 민감성과 거리–동조성·semivariogram의 기술통계 한계
- RINEX 2 관측코드에서 RINEX 3/4 tracking attribute를 유일하게 복원하지 못하는 legacy ambiguity
- IGS GIM의 광역·저해상도 배경자료 한계와 30초 국지 사건 직접 판정 불가
- `f^-2` 전리층 지연 관계를 C/N0·tracking loss·scintillation 진폭에 직접 적용할 수 없는 한계
- 대역차분 지표의 관측코드 coverage 의존성(L5/E5a 미보유 관측소·기간)
- 수신기 내부 간섭완화(AGC·notch·adaptive filter)에 의한 약한 간섭 은폐 가능성과 미탐지≠부재의 원칙
- L2W semi-codeless 추적 취약성과 대역 표적 간섭 해석의 혼동 위험
- BDS B1I≠B1C/L1 주파수 차이와 대역 별칭 오류 위험
- 행위자·국가·기관 귀속(attribution) 불가와 공식 발표 인용의 한정 표기
- affected footprint ≠ source ≠ actor
- 분산 집계에서 median·MAD·분위수를 스케치로 근사했을 때의 오차와 그 검증 범위
- 일자·시간블록 경계에서 잘린 사건의 재병합 규칙이 지속시간·사건 수 통계에 주는 영향
- 워커 수·샤드 수·실행환경 차이에 의한 수치 미세편차 가능성과 불변성 시험으로 확인한 범위

## `docs/EVALUATION_PROTOCOL.md`

- calibration/holdout split
- pseudo-prospective policy
- blind freeze
- official replay
- matched controls
- block bootstrap
- multiple testing
- synthetic injection
- manual review
- sensitivity analysis

## `docs/FALSIFICATION_LOG.md`

후보별 모든 반증시도, 입력자료, 결과, reviewer, 상태를 남긴다.

## `docs/CORRECTIONS.md`

잘못된 판단을 삭제하지 말고 시각, 원판단, 근거, 수정, 영향산출물과 함께 기록한다.

## `docs/DEPENDENCY_GRAPH.md`

raw observation→feature→score→event→claim의 의존관계를 기록한다. 각 노드에 병렬 단위(shard key), 배리어, 축약(reduce) 지점을 함께 표기한다.

## `docs/PARALLEL_EXECUTION_PLAN.md`

39~41절을 이 프로젝트의 실제 자원·경로에 맞게 구체화한다. 단계별 shard key와 예상 task 수, 역할별 워커 수, 배리어 순서, 경계 패딩 값, 축약 지점, 실측 처리량과 병목, 재개 절차를 적는다. 워커 수를 바꿀 때 이 문서를 갱신한다.

# 34. Phase별 승인표

| Gate | 필수 산출물 | 핵심 검증 | 실패 시 행동 |
|---|---|---|---|
| P0 | 환경·기존자산 감사 | 원본/결과 분리, 자원·버전 | 규칙·경로 해결 전 중단 |
| P1 | 전수 인벤토리 | file/byte 조정, 실제 기간 | 실패파일 분류 후 재감사 |
| P2 | time/station/regime | time round-trip, ID conflict | 망 동시성 분석 금지 |
| P3 | canonical parser | row reconciliation, bounded memory | parser 수정 후 R1 반복 |
| P4 | data quality | gap/duplicate/coverage | 후보생성 전 품질정책 수정 |
| P5 | geometry/product | golden geometry, coverage | 독립특징만 진행 |
| P6 | feature | 산식·단위·결측·합성시험 | 잘못된 family 비활성화 |
| P7 | baseline | leakage·fallback·holdout | 기준선 재학습 |
| P8 | StationEvent | alert rate·stable ID | threshold/aggregation 감사 |
| P9 | NetworkEvent | satellite/station/pipeline 분해 | clustering 수정 |
| P10 | falsification | 모든 후보 반증상태 | final candidate 금지 |
| P11 | official replay | blind freeze·source provenance | 검증결과 분리/무효화 |
| P12 | evaluation | CI·분모·leakage audit | 성능주장 금지 |
| R5 | full scale | manifest reconciliation | 실패 partition과 재개 보고 |

각 게이트에 `declared_by`(orchestrator), `evidence_links`, `barrier_state`, `worker_summary`(역할별 task 수·실패·poison)를 기록한다. 게이트 판정과 배리어 선언은 orchestrator 역할만 수행하고, 자신이 생산한 후보의 최종 판정은 생산 워커를 운영한 주체가 단독으로 하지 않는다. 불가피하면 `deferred_review`로 표기하고 증거등급 상한을 낮춘다.

# 35. 1초 RINEX·차량 NMEA 선택적 후속검증

이번 기본분석은 30초 CORS다. 다른 자료가 있어도 기본 pipeline을 오염시키지 말고 별도 validation adapter로 연결한다.

## 35.1 CORS 1초 자료

사용자가 알려준 2024~2026년 범위는 실제 파일로 확인한다. 동일 사건에서 세 가지를 비교한다.

```text
A: native 30s CORS
B: native 1s CORS
C: native 1s를 동일규칙으로 30s downsample
```

이를 통해 temporal-resolution effect와 receiver/station/domain effect를 분리한다. 1초 자료는 onset/offset, 짧은 burst, satellite-specific response, slip/reacquisition을 보강할 수 있다. 30초에서 보이지 않은 10초 사건은 sampling limit 가능성을 명시한다.

## 35.2 차량 NMEA

사용자가 알려준 1초, 2017~2026년 범위는 실제 파일로 확인한다. CORS raw observation과 NMEA sentence를 직접 같은 척도로 합치지 마라. 비교 가능한 aggregate만 사용한다.

- valid satellite count change
- standardized signal-strength degradation
- tracking/fix availability
- 동일 UTC/KST window
- coarse affected-observation footprint

NMEA `Pass/Hotspot`과 CORS `StationEvent/NetworkEvent`는 별도 domain ID다.

```text
network_event_id_30s
station_event_id_1s
nmea_event_id
time_overlap
spatial_relation
comparable_feature_family
direction_agreement
resolution_effect
domain_effect_possible
concordance_status
limitations
```

추가자료가 없으면 `not_available_not_required`로 기록하고 30초 분석 완료를 막지 않는다.

# 36. 최종 완료 체크리스트

## 자료·안전

- [ ] 원시자료를 변경하지 않았다.
- [ ] 원시/결과 경로가 분리되었다.
- [ ] 전수 file 수와 byte를 조정했다.
- [ ] 실제 기간과 interval을 확인했다.
- [ ] 모든 실패파일을 기록했다.
- [ ] duplicate를 삭제하지 않고 canonical rule로 처리했다.

## RINEX·시간·Metadata

- [ ] version/type/observation code를 header로 확인했다.
- [ ] S observation과 SSI를 구분했다.
- [ ] exact 3-character observation code·tracking attribute·actual frequency를 기준선 key에 반영했다.
- [ ] RINEX 2의 비유일 3/4 매핑을 `legacy_ambiguous`로 격리하고 mapping provenance를 남겼다.
- [ ] time system과 leap second를 검증했다.
- [ ] station ID conflict를 해결 또는 보류했다.
- [ ] receiver/antenna/firmware regime을 만들었다.
- [ ] QZSS(J)·SBAS(S)·NavIC(I) 관측 존재를 확인하고 포함/제외 정책을 기록했다.
- [ ] 좌표 datum/기준계를 확인했거나 `datum_unverified`로 표기했다.

## Parser·Quality

- [ ] bounded streaming이다.
- [ ] missing과 zero를 구분한다.
- [ ] row/epoch reconciliation을 통과했다.
- [ ] chunk invariance를 통과했다.
- [ ] resume equivalence를 통과했다.
- [ ] data-pipeline gap branch가 작동한다.

## Feature·Baseline

- [ ] feature별 unit·formula·missing policy가 있다.
- [ ] 가능한 범위에서 elevation/geometry를 통제했다.
- [ ] regime을 넘는 무효 비교가 없다.
- [ ] baseline fallback coverage를 보고했다.
- [ ] leakage audit를 통과했다.
- [ ] tracking-loss selection bias를 처리했다.
- [ ] ROTI는 연속 arc, `N_epoch`, `N_ROT`, coverage, LLI/cycle-slip 게이트를 통과한 값만 사용했다.
- [ ] GLONASS channel을 header→local navigation→time-valid IGS metadata 순으로 해결했고 미해결 특징을 강등 처리했다.

## Event·Falsification

- [ ] StationEvent/NetworkEvent ID가 안정적이다.
- [ ] station availability를 분모로 쓴다.
- [ ] satellite-centric anomaly를 분리했다.
- [ ] receiver/site 가능성을 검토했다.
- [ ] ionosphere/weather 가능성을 검토했다.
- [ ] ROTI·GIM·Kp/Dst 대조를 수행하고 `space_weather_alert` 기간을 자동 제외하지 않았다.
- [ ] 대역차분·위성군차분 지표를 인벤토리 확인 관측코드 범위에서만 계산했다.
- [ ] RFI는 `band_selective`/`multi_band_common`/`temporally_unresolved` 관측패턴으로만 기록하고 narrowband·barrage·chirp 파형을 스펙트럼 측정 없이 부여하지 않았다.
- [ ] Moran's I 순열 p-value와 가중행렬 민감도를 보고했다.
- [ ] 최대연결거리로 생긴 도서·연안 고립 관측소를 먼 관측소와 강제 연결하지 않고 제외·coverage를 보고했다.
- [ ] 거리–동조성·semivariogram을 기술통계로만 보고하고 송신원 추정으로 표현하지 않았다.
- [ ] data pipeline anomaly를 분리했다.
- [ ] 모든 후보에 falsification status가 있다.
- [ ] footprint를 source location이라 하지 않았다.
- [ ] 행위자·국가·기관 귀속을 어디에도 쓰지 않았고 공식 발표 인용은 한정 표기했다.
- [ ] L2W 단독 저하를 대역 표적 간섭으로 해석하지 않았고 B1I/B1C 대역을 별칭하지 않았다.
- [ ] 미탐지를 간섭 부재로 서술하지 않았다(수신기 완화 마스킹 제한 반영).

## External validation·Evaluation

- [ ] blind 결과를 먼저 freeze했다.
- [ ] official source provenance가 완전하다.
- [ ] NOTAM·NAVAREA XI·AIS·ICAO 기록의 `source_tier`와 advisory/confirmed를 구분했다.
- [ ] advisory 단독 출처로 E4를 부여하지 않았다.
- [ ] matched controls를 정의했다(우주기상 상태 매칭 또는 그 한계 기록 포함).
- [ ] miss/partial/unassessable을 보고했다.
- [ ] 방어 불가능한 precision/recall을 쓰지 않았다.
- [ ] block CI와 multiple testing을 고려했다.

## Test·Scale

- [ ] unit/integration/golden test가 통과했다.
- [ ] synthetic scenario가 기대 branch로 간다.
- [ ] placeholder scan이 통과했다.
- [ ] R1→R4를 순서대로 통과했다.
- [ ] R5 전 schema/config를 동결했다.
- [ ] 실측 GB/h, peak RSS, output ratio가 있다.
- [ ] full completion 또는 정확한 blocked/resume 상태다.

## 병렬 실행

- [ ] 단계별 shard key·병렬도·의존성·배리어가 `docs/PARALLEL_EXECUTION_PLAN.md`에 있다.
- [ ] 배리어 B1·B2·B3가 orchestrator 선언으로만 통과되었다.
- [ ] shard 수 1/4/16과 worker 수 1/N의 결과가 동일했다(불변성 시험).
- [ ] 경계 패딩과 재병합 reduce가 적용되었고 경계 사건 시험이 통과했다.
- [ ] median·MAD·분위수의 분산 집계 방식과 근사 오차를 보고했다.
- [ ] 모든 partition에 `worker_id`·`task_id`·`shard_index`가 기록되었다.
- [ ] 리스 없는 쓰기, 타 워커 파티션 덮어쓰기가 없었다.
- [ ] 실패 task 재시도·poison 격리 목록과 그 영향 범위를 보고했다.
- [ ] `W_VAL`이 별도 프로세스·별도 경로로 격리 실행되었다.
- [ ] 워커 수별 실측 처리량·peak RSS·디스크 사용과 병목을 기록했다.

## 미규정 사례·세션·자료 특이사항

- [ ] 계약에 규칙이 없던 사례를 모두 `docs/UNSPECIFIED_CASES.csv`에 기록하고 보수적 기본값을 적용했다.
- [ ] 누적 임계를 넘은 미규정 사례는 규칙으로 확정했거나 최종 수치에서 제외했다.
- [ ] 모든 산출물에 `session_id`가 있고, 세션 시작 시 필수 문서를 읽은 기록이 있다.
- [ ] 한 세션 안에서 `blind_status`를 바꾸지 않았다.
- [ ] 세션 종료 시 그 세션에서 내린 판단이 `DECISIONS.md`에 남았다.
- [ ] 파일·세션 단위 중심화를 사용하지 않았고, 자정 인접 사건 비율을 보고했다.
- [ ] 자정 경계를 걸친 arc·사건을 규칙대로 연결하거나 분리하고 그 근거를 남겼다.
- [ ] 같은 station-day의 중복·이형 파일에 canonical 선택 규칙을 적용하고 대안을 보존했다.
- [ ] 항법자료의 중복 ephemeris·health·age 필터를 적용하고 선택 근거를 기록했다.
- [ ] 연도 비교를 고정 코호트와 전체 두 가지로 보고했다.
- [ ] 위성군 확대 시점을 regime 경계로 처리했다.
- [ ] 실행 중 추가된 자료를 동결된 분석집합에 섞지 않았다.
- [ ] 위성×epoch 행을 전량 저장하지 않았고, 표본 통계를 전량 통계처럼 보고하지 않았다.
- [ ] 후보율이 기대 범위 안이었거나, 벗어난 경우 원인을 규명했다(임계값 조정 아님).
- [ ] 수동검토를 전수로 못 했다면 층화표본 규칙과 표본 비율을 보고했다.

## Report

- [ ] claim registry와 source register가 있다.
- [ ] threshold provenance가 있다.
- [ ] candidate casebook이 있다.
- [ ] scientific limitations가 본문에 있다.
- [ ] 실제 수치만 사용했다.
- [ ] 한국어 figure가 깨지지 않는다.
- [ ] 38절 Publication Viability Gate를 수행했고, viable/conditionally viable로 판정된 논문에 한해 outline·claims_map·figures/paper·chapter_map을 작성했다. 이 항목의 보류는 R5 데이터 파이프라인 완료를 무효화하지 않는다.

# 37. 최종 응답 확장 형식

앞의 완료 응답 형식을 다음 순서로 확장한다.

1. 실행결론: 완료/부분완료/blocked
2. 원시자료 보존 확인
3. 실제 기간·station·file·byte·RINEX·interval
4. 기존자산 재사용/수정/폐기 결정
5. Phase P0~P12와 R1~R5 상태
6. 구현기능과 주요파일
7. 데이터품질과 제외·제한범위
8. metadata regime과 관측가능성
9. feature·baseline·threshold와 출처상태
10. parser 검산, pytest, lint, golden, chunk/resume 결과
11. 실측 처리량, peak RSS, disk/output, 전체 예상과 실제시간
12. blind candidate funnel
13. StationEvent→NetworkEvent 집계
14. 후보별 증거등급·반증·대안설명
15. official-event hit/partial/miss/unassessable
16. 정상 holdout alert rate와 CI
17. 주요 figure/table/evidence bundle 위치
18. claim/source registry 상태
19. 실패·미완료·untestable 항목
20. 30초 자료의 과학적 제한
21. Publication Viability Gate 판정과 논문별 viable/conditional/merge/not-supported 상태, 작성된 근거 패키지
22. 병렬 실행 구성: 역할별 워커 수, shard 수, 총 task 수와 완료·실패·poison 수
23. 배리어 B1/B2/B3 통과 시각과 근거, 경계 재병합 사건 수
24. 워커 수별 실측 처리량·스케일 효율·병목 단계와 자원 상한
25. shard/worker 불변성 시험 결과와 분산 집계 근사 오차
26. 다음 정확한 resume 명령(큐 상태 기준)과 남은 task 범위
27. 미규정 사례 건수·유형과 그것이 결론에 준 영향
28. 세션 수·인계 기록 상태와 이번 세션에서 확정한 판단
29. 자정 경계 사건 비율, canonical 선택·격리 파일 수, 코호트별 비교 결과
30. 1초/RF 후속검증 명령

각 숫자는 전수·표본·추정 중 무엇인지 표시하고 claim ID 또는 산출물에 연결한다.

# 38. SCI 논문 3편·박사논문 집필 지원 계약

이 분석의 산출물은 SCI(E)급 학술지 논문 최대 3편과 박사학위논문의 근거자료 후보가 된다. 3편은 사전 확정 목표가 아니며, R4/R5·외부검증·claim audit 후 `Publication Viability Gate`를 통과한 논문만 독립 원고로 구성한다. 분석 단계에서 아래 요구를 함께 충족해, 집필 시 산출물을 재가공 없이 인용·재현할 수 있게 하라. 단, 다음 원칙이 우선한다.

- **결과가 논문 구성을 결정한다.** 아래 논문 분해는 시작 가설이며, 실제 데이터 결과가 지지하지 않으면 구성을 조정하고 그 이유를 `DECISIONS.md`에 남긴다. 논문 편수를 맞추기 위해 결과를 부풀리거나 동일 결과를 중복 게재 형태(salami slicing)로 쪼개지 마라. 각 논문의 독립적 기여와 데이터·결과 중복 범위를 명시적으로 구분한다.
- **논문 산출물은 파이프라인 완료 게이트가 아니다.** P0~P12·R1~R5의 완료는 논문 3편 생성 여부와 분리한다. 분석 결과가 부족하면 논문을 병합·보류·미지원하고도 연구 파이프라인은 완료될 수 있다.
- **본문 전체의 과학적 제한·증거등급·claim registry 규칙은 논문 초안에도 동일하게 적용된다.** 논문용이라는 이유로 표현을 강화하지 마라.
- 에이전트는 논문 완성 원고를 대필하는 것이 아니라, 심사에 방어 가능한 **집필 가능 상태의 근거 패키지**(outline, 결과표, 그림, claim 매핑, 재현 명령)를 만든다.

## 38.1 논문 분해 시작 가설

```text
Paper A — 데이터·방법론 논문
  RQ-A: 이종 수신기·RINEX 버전·메타데이터 변화가 존재하는 국가 CORS 장기자료에서
        전파교란 후보 탐지의 관측 가능성과 무결성 체계를 어떻게 구성할 수 있는가?
  주제: 국가 CORS 망 다년(실확인 기간) 30초 RINEX의 대규모 무결성 감사,
        품질 게이트, 재현가능 간섭탐지 파이프라인 설계
  후보 저널군: GPS Solutions / Journal of Geodesy 계열. 저널명은 설계 강제조건이 아님
  primary endpoint: 품질게이트 통과율, regime/code coverage, 파이프라인 재현성·처리 무결성
  핵심 산출물: 단계 0~5, 품질등급 분포, 파이프라인 검증(R1~R5), 처리량 실측

Paper B — 탐지·망 동조성 논문
  RQ-B: 30초 자료에서 다중 특징군과 공간 동조성을 결합했을 때 경험적
        오경보 대리지표와 후보사건 안정성이 얼마나 개선되는가?
  주제: 다중 검출기 + 공간통계(Moran's I, 거리–동조성, semivariogram) 기반
        블라인드 NetworkEvent 탐지와 empirical alert/false-alarm proxy
  후보 저널군: IEEE T-AES / GPS Solutions 계열. 저널명은 설계 강제조건이 아님
  primary endpoint: valid station-day당 alert rate, matched-control exceedance, threshold·weight-matrix candidate stability
  핵심 산출물: 단계 6~7, 20절, 24절 통계, 대역차분(4.5절), funnel

Paper C — 외부검증·사례 논문
  RQ-C: 태양활동·전리층 교란과 외부에 보고된 인위적 전파교란 의심사건을 어느 범위까지
        물리적으로 분리할 수 있으며 외부검증의 한계는 무엇인가?
  주제: 발생확인 공식 사건과 advisory·NOTAM·NAVAREA XI·AIS를 분리한 replay,
        ROTI/GIM/지자기 지수 대조, 대표 사건 심층 사례분석
  후보 저널군: NAVIGATION / GPS Solutions 계열. 저널명은 설계 강제조건이 아님
  primary endpoint: official-event concordance, matched-control 대비, 증거등급·반증 생존율·검증불가율
  핵심 산출물: 단계 8~9, 21~23절, evidence bundle, 표준 정합표(reports/13)

박사논문 — 위 3편을 포괄하는 통합 서사
  서론·문헌연구 → 자료·방법(Paper A) → 탐지(Paper B)
  → 검증·사례(Paper C) → 종합토의·한계·후속(1초/RF) → 결론
```

각 논문의 novelty 후보(예: 다년·전국망 규모, 30초 자료 한계의 정직한 정량화, blind/official 격리 프로토콜, 국제 외부자료 다중 tier 검증)는 `configured` 가설로 두고 문헌 확인 후 확정한다.

## 38.2 논문별 필수 요소

세 논문 후보 각각에 대해 다음을 산출한다. 각 `outline.md` 첫 부분에 `primary_RQ`, `primary_endpoint`, `unique_claim_ids`, `shared_methods`, `shared_dataset_scope`, `overlap_disclosure`, `publication_viability`를 필수로 둔다.

- `manuscripts/paper_{A,B,C}/outline.md`: IMRaD 구조 개요, 절별 핵심 주장, 사용할 표·그림 목록
- `manuscripts/paper_{A,B,C}/claims_map.csv`: 논문 주장 ↔ `docs/CLAIM_REGISTRY.csv`의 claim ID ↔ 산출물 경로 ↔ 증거등급. **claim registry에 없는 주장을 논문 개요에 쓰지 마라.**
- `manuscripts/paper_{A,B,C}/contributions.md`: 기여 3~5개, 각 기여가 기존 연구 대비 무엇이 다른지, 그리고 어떤 결과가 그 기여를 지지하는지
- `manuscripts/paper_{A,B,C}/limitations_section_draft.md`: `SCIENTIFIC_LIMITATIONS.md`에서 해당 논문 범위의 제한을 발췌·서술
- `manuscripts/CROSS_PAPER_OVERLAP_MATRIX.md`: 데이터 기간·station·feature·figure/table·primary endpoint·claim ID 중복과 차별성, 공유 방법 인용계획
- `manuscripts/PUBLICATION_VIABILITY.md`: 논문별 `viable | conditionally_viable | merge_recommended | not_supported` 판정과 근거
- 데이터·코드 가용성 문안(reports/14 재사용)과 재현 명령

## 38.3 문헌 위치화(related work) 규칙

- 비교 대상 문헌군: CORS/SNR 기반 간섭탐지, 수신기망 spoofing 모니터링, ROTI·scintillation, 항공 GNSS RFI 보고 분석, 공간통계 응용. 실제 접근·확인한 문헌만 `docs/SOURCE_REGISTER.md`에 등재한다.
- **존재를 확인하지 않은 인용을 만들지 마라.** 서지정보(저자, 연도, 저널, DOI)를 확인할 수 없으면 `확인 필요`로 남긴다.
- 가능하면 기존 방법(예: 고정 임계 SNR 하락 탐지) 1개 이상을 동일 자료의 서브셋에 재구현해 정량 비교(baseline comparison)하고, 재구현의 충실도 한계를 명시한다. 재구현이 불가능하면 비교 불가 사유를 기록한다.

## 38.4 저널 수준 그림·표 규격

한국어 보고서 그림과 별도로 논문용 그림을 `figures/paper/` 아래 생성한다.

- 형식: 벡터(PDF/SVG) 우선 + 600 dpi PNG 병행, 영문 라벨, 저널 1단(약 90 mm)·2단(약 180 mm) 폭 두 버전
- 색각이상 안전 팔레트, 좌표축 단위·시간계(UTC) 명시, 오차막대·CI 표기
- 지도 그림에는 `affected network footprint` 표기 원칙(송신원 오해 금지)을 영문 캡션에도 유지
- 모든 논문 그림은 스크립트로 재생성 가능해야 하며 생성 명령을 그림별로 기록한다

## 38.5 통계 보고 규격

논문 대상 결과표·본문 초안에서 다음을 강제한다.

- p-value 단독 보고 금지: 효과크기 또는 실측 비율 + 신뢰구간(블록 부트스트랩, 24.4절) + 표본 단위(n, station-day 등)를 함께 제시
- 사용 검정·부트스트랩·다중검정 보정 방법과 파라미터를 표 각주 또는 방법절에 명시
- 성능지표(precision/recall 등)는 24.3절 조건을 만족할 때만 사용하고, ground truth 불완전성을 각 표에 명시
- `pilot / expanded / full` 실행범위를 모든 논문 표·그림에 표기

## 38.6 박사논문 매핑 산출물

- `manuscripts/dissertation/chapter_map.md`: 학위논문 장 구조 ↔ 3편 논문 ↔ 보고서·산출물 매핑표, 장별 핵심 주장과 증거등급 상한
- `manuscripts/dissertation/defensible_claims.md`: reports/10의 "박사논문에서 주장 가능한 범위" 절을 확장해, 주장별로 `방어 가능 / 조건부 / 주장 불가`를 심사 질문 예상과 함께 정리
- 후속연구 장 초안: 35절의 1초 RINEX·NMEA·RF 센서 후속검증 설계를 재사용

## 38.7 Publication Viability Gate와 완료 기준

- [ ] R4 이상 분석·통계·반증 결과를 근거로 각 논문을 `viable | conditionally_viable | merge_recommended | not_supported`로 판정했다.
- [ ] viable/conditionally viable 논문만 outline과 claims_map을 완성하고 모든 주장이 claim ID로 역추적된다.
- [ ] 논문 간 결과 중복 범위와 각 논문의 독립 기여가 문서화되었다.
- [ ] 각 논문의 primary RQ·primary endpoint·unique claim과 공유 방법·데이터 범위가 분리되었다.
- [ ] 논문용 영문 벡터 그림이 재생성 스크립트와 함께 존재한다.
- [ ] 통계 보고 규격(효과크기·CI·n·보정방법)이 결과표에 반영되었다.
- [ ] 확인되지 않은 문헌 인용이 없다.
- [ ] dissertation chapter_map과 defensible_claims가 존재한다.
- [ ] 실제 결과가 시작 가설의 논문 구성을 지지하지 않는 경우 병합·보류·미지원 이유가 기록되었다.

이 게이트는 학술 출판 준비 게이트이며 R5 데이터 파이프라인 완료를 막지 않는다. `not_supported`는 연구 실패가 아니라 증거 수준에 맞춘 정상적 결과다.

# 39. 다중 워커 병렬 실행 계약

이 절은 앞의 모든 단계를 **역할이 다른 여러 프로세스가 나누어 동시에 수행**하기 위한 규칙이다. 앞 절과 충돌하면 더 엄격한 조항을 따른다. 병렬화의 목표는 속도이며, 결과는 직렬 실행과 같아야 한다.

## 39.1 병렬화의 3가지 축

1. **데이터 병렬(같은 일을 다른 자료에)**: station×day 파티션처럼 서로 독립인 단위를 나눈다. 이 프로젝트 처리량의 대부분이 여기서 나온다.
2. **역할 병렬(다른 일을 동시에)**: 특징 추출이 도는 동안 다른 워커가 외부 참조자료를 받거나 그림·문서를 만든다. 의존성이 없는 단계에만 적용한다.
3. **구현 병렬(코드 작성 분담)**: 모듈 경계로 나누어 서로 다른 작성자·에이전트가 동시에 구현한다. 40.2절 규칙을 따른다.

세 축을 섞어 쓰되, 의존성과 배리어를 어긴 병렬화는 금지한다.

## 39.2 단계별 작업 단위와 병렬도

아래 표를 `docs/PARALLEL_EXECUTION_PLAN.md`의 시작값으로 쓰고 실측 후 갱신한다. `shard key`는 task를 만드는 단위이며 출력 파티션 키와 일치해야 한다.

| 단계 | shard key(작업 단위) | 담당 역할 | 병렬도 | 선행 조건 | 결합(reduce) |
|---|---|---|---|---|---|
| 0 환경·자산 감사 | 없음 | orchestrator | 1 | — | — |
| 1 헤더 인벤토리 | `file_id` 묶음 | W_INV | 높음(IO 한계) | P0 | 조각 concat → 정렬·중복·해시 검사 |
| 2 품질 게이트 | `station×day` | W_QC | 높음 | P1 전량(B1) | station-day 파티션 concat |
| 3 항법·외부 참조자료 | `날짜` 또는 `product` | W_EXT | 낮음(2~4, single-flight) | P1 | `cache/external` 공유·해시 검증 |
| 3.1 GLONASS 채널 스냅샷 | 스냅샷 1건 | W_EXT | 1 | P3 | — |
| 4 특징 추출 | `station×day`(+halo) | W_FEAT | 최고(CPU 바운드) | B1, P3 | 파티션 독립 저장 |
| 4.5 ROTI·대역차분 | `station×day×arc` | W_FEAT | 최고 | 4와 동일 task 내 | — |
| 5 기준선 | `baseline group_key` | W_BASE | 중간 | **학습구간 특징 전량(배리어)** | 39.8절 분산 집계 |
| 6 이상탐지 | `station×day` | W_DET | 최고 | **B2 기준선 동결** | 후보 window concat |
| 7 망 동조성·공간통계 | `시간블록(day 또는 6h)×전 관측소` | W_NET | 중간 | 해당 시간블록의 P6 전량 | 경계 패딩 후 사건 재병합(단일 reduce) |
| 8 공식 사건 외부검증 | `event_id` | W_VAL | 낮음 | **B3 blind freeze** | 별도 경로, 블라인드 산출물과 미혼합 |
| 9 반증·분류 | `candidate_id` | W_FALS | 높음 | P7 | 후보 카탈로그 concat |
| 시각화 | `candidate_id` 또는 그림 종류 | W_FIG | 높음 | P9 | — |
| 보고서·claim 확정 | 없음 | W_REP | 1 | 전 단계 | 단일 writer |

병렬화하면 결과가 달라지는 작업은 **반드시 단일 워커**로 둔다.

- 기준선 파라미터·임계값 확정, blind freeze
- StationEvent→NetworkEvent 병합 규칙과 clustering의 최종 실행
- 공간 가중행렬 선택과 다중검정 보정 범위 결정
- claim registry 최종 상태와 보고서 수치 확정

## 39.3 하드 배리어

배리어는 orchestrator만 선언하고 `queue/barriers.json`에 근거 해시와 시각을 남긴다. 워커는 배리어를 우회하는 수단을 갖지 않는다.

- **B1 — 인벤토리·품질 완료**: 전수 인벤토리와 품질등급이 끝나기 전에 특징 추출을 파일럿 범위 밖으로 확대하지 않는다. 분석 대상 파일 집합이 확정되지 않은 상태의 대규모 실행은 재작업을 부른다.
- **B2 — 기준선 동결**: 기준선 파라미터가 확정·해시되기 전에 탐지 task를 leasable 상태로 만들지 않는다. 워커마다 다른 기준선을 쓰면 후보가 워커 수에 의존하게 된다.
- **B3 — blind freeze**: 블라인드 후보와 설정·코드 해시가 동결되기 전에 공식 사건자료를 큐·캐시·특징에 들이지 않는다. `W_VAL` task는 B3 이후에만 생성한다.

배리어 통과 조건은 산출물 존재가 아니라 15.2절 게이트 통과다. 배리어를 앞당기려면 계약을 고치고 근거를 남겨야 하며, 실행 중 임의 완화는 금지한다.

## 39.4 작업 큐와 워커 계약

pull 모델을 쓴다. orchestrator가 task를 만들고, 워커가 자기 역할의 leasable task를 가져간다. push 방식으로 워커에 미리 할당하지 마라(불균등·재할당 문제).

```text
task_id                # 결정적: hash(stage, shard_key, config_hash, code_hash, schema_version)
stage
role_required
shard_key
shard_index / shard_count
depends_on_task_ids
barrier_required
status                 # pending | leasable | leased | running | done | failed | poison
lease_owner_worker_id
lease_expiry_utc
heartbeat_at_utc
attempts
error_class
input_refs
output_paths
runtime_seconds
peak_rss_mb
```

- 상태 전이는 원자적이어야 한다. SQLite(WAL) 또는 디렉터리 큐의 원자적 `rename`을 사용하고, **큐는 네트워크 공유가 아닌 로컬 디스크**에 둔다. 원자성을 보장할 수 없으면 `doctor`가 병렬 실행을 차단한다.
- `task_id`는 내용 기반이므로 재실행 시 같은 task는 같은 ID를 갖는다. 이미 `done`이고 출력 해시가 유효하면 다시 실행하지 않는다.
- 워커는 lease 중 `heartbeat_seconds`마다 갱신한다. 만료 후 `stale_lease_grace_seconds`가 지나면 orchestrator가 회수·재할당한다.
- 워커는 자기 task의 `output_paths`에만 쓴다. 완성 전에는 `runs/<run_id>__<worker_id>/`의 `.tmp`에 쓰고 완료 시 원자적으로 이동한다.

## 39.5 역할 정의

| 역할 | 책임 | 쓰기 범위 | blind |
|---|---|---|---|
| `orchestrator` | 계획·큐 생성, 배리어 선언, 게이트 판정, 승격, 자원 조정 | `queue/`, `manifests/`, 진행파일 | blinded |
| `W_INV` | 파일 열거·헤더 인벤토리·압축 판별·해시 | `inventory/` | blinded |
| `W_QC` | 품질지표·등급·metadata regime | `data_quality/`, `metadata/` | blinded |
| `W_EXT` | BRDC/SP3/CLK·IONEX·Kp/Dst·GLONASS 채널 취득 | `cache/external/` | blinded |
| `W_FEAT` | 특징·ROTI·대역차분 추출 | `features/` | blinded |
| `W_BASE` | 기준선 학습·동결 | `baselines/` | blinded |
| `W_DET` | 다중 검출기 이상탐지·StationEvent | `candidates/station_*` | blinded |
| `W_NET` | 망 동조성·공간통계·NetworkEvent | `candidates/network_*`, `candidates/spatial_*` | blinded |
| `W_FALS` | 반증 엔진·분류·증거등급 | `candidates/`, `docs/FALSIFICATION_LOG.md` | blinded |
| `W_VAL` | 공식 사건 정규화·replay·외부검증 | `validation_unblinded/` | **unblinded** |
| `W_FIG` | 그림 생성 | `figures/` | blinded(공식 overlay는 W_VAL 산출물에서만) |
| `W_REP` | 보고서·claim 확정 | `reports/`, `docs/CLAIM_REGISTRY.csv` | 단계별 분리 |

- 동시에 도는 프로세스는 하나의 역할만 맡는다. 한 사람·에이전트가 여러 역할을 순차 수행하는 것은 허용한다.
- 역할별 동시 인스턴스 수는 `role_worker_limits`로 제한하고 실측 후 조정한다.
- `W_REP`는 항상 1개다. 보고서·claim 확정을 병렬로 하지 마라.

## 39.6 샤딩과 결정성

- shard 배정: `shard_index = int(sha256(shard_key_canonical), 16) % shard_count`. 파일 열거 순서·디렉터리 순회 순서에 의존하지 마라.
- `shard_key`는 정규화된 문자열(예: `station=XXXX|date=2023-05-14`)로 만들고 대소문자·구분자를 고정한다.
- shard 수를 바꾸면 task 분할은 달라지지만 **출력 파티션과 내용은 같아야 한다.** 출력 경로에 shard_index를 넣지 마라.
- 난수는 설정 seed에서 파생하되 `seed_for_task = hash(base_seed, task_id)`처럼 task별 결정적으로 만든다. 워커 지역 시각·PID를 seed에 넣지 마라.
- 축약은 정렬된 순서로 수행하고, 부동소수 합산은 결합 순서에 무관한 방식과 tolerance를 명시한다.

## 39.7 경계(halo) 처리

일자·시간블록으로 자르면 경계에 걸친 현상이 잘린다. 다음을 강제한다.

- **창 특징**: 각 파티션은 앞뒤로 `window_feature_padding_seconds`(창 최대 길이 이상)만큼 읽어 계산하고, **쓰기는 자기 구간만** 한다. 읽기 패딩과 쓰기 구간을 혼동하지 마라.
- **ROTI·arc**: 자정 경계를 걸치는 연속 arc는 `roti_arc_padding_seconds`만큼 앞뒤를 포함해 arc 연속성·LLI·coverage 게이트를 판정한다. 경계에서 arc를 강제로 끊어 유효 ROTI를 잃지 마라.
- **StationEvent**: 파티션 경계에 닿은 사건은 `boundary_open=true`로 표시하고, 이웃 파티션 완료 후 단일 reduce에서 병합한다. 병합 결과에 `boundary_merged=true`를 남긴다.
- **NetworkEvent**: 시간블록 병렬 시 블록 경계 ±`network_block_padding_seconds`를 포함해 clustering하고, reduce에서 중복 사건을 안정 ID 기준으로 제거한다.
- 경계 처리 여부는 사건 수·지속시간 통계를 바꾸므로 41.3절 경계 시험으로 직렬 실행과 대조한다.

## 39.8 분산 집계 규칙

기준선(단계 5)과 요약 통계는 파티션별 부분결과를 결합해야 한다.

- **그대로 합산 가능**: count, sum, sum of squares, min, max, 고정 bin 히스토그램, 결측 수
- **직접 결합 불가**: median, MAD, 분위수, robust scale. 다음 중 하나만 쓴다.
  1. **2-pass**: 1차로 고정 bin 히스토그램 또는 후보 분위수를 만들고, 2차로 정확값을 확정한다(정확·느림).
  2. **스케치**: t-digest·KLL 등 병합 가능한 자료구조를 파티션별로 만들고 결합한다(빠름·근사). 이 경우 대표 그룹에서 정확값과의 오차를 측정해 보고한다.
- 어떤 방식을 쓰든 `baseline_median`, `baseline_MAD`, `empirical_scale_floor`의 산출 방식과 근사 오차를 `docs/METHODOLOGY.md`와 `reports/16`에 남긴다.
- 그룹 표본이 `min_epochs_per_cell` 미만이면 19절 계층 fallback을 적용하고 fallback 수준을 열로 남긴다. 병렬화 때문에 부분 표본으로 기준선을 만들지 마라.
- 기준선 학습은 배리어 뒤에서 한 번만 수행하고 결과를 해시·동결한다. 탐지 워커는 동결된 기준선만 읽는다.

## 39.9 자원 예산과 backpressure

- 총 병렬도 = `min(CPU-2, 가용 RAM / 워커당 peak RSS, 저장장치 IO 한계)`. 실측 전에는 보수적으로 시작해 단계별로 올린다.
- 단계 특성이 다르다. 인벤토리·압축 해제는 IO 바운드이므로 워커를 늘려도 디스크 큐가 병목이다. 특징·탐지·공간통계는 CPU 바운드다. 그림 생성은 메모리·폰트 자원을 쓴다. IO 바운드 단계와 CPU 바운드 단계를 겹쳐 돌리면 전체 효율이 올라간다.
- 원시자료가 네트워크·외장 드라이브에 있으면 동시 읽기 수를 별도로 제한하고, 압축 해제 캐시는 로컬 디스크에 둔다.
- 같은 압축 파일을 여러 워커가 동시에 해제하지 않도록 캐시 항목마다 single-flight 잠금을 둔다. 해제본 재사용 정책과 정리 기준을 기록한다.
- 외부 저장소(IGS/CDDIS 등) 다운로드는 `W_EXT` 소수 워커로 제한하고 서버 정책을 존중한다. 병렬 다운로드로 부하를 주지 마라.
- 출력 디스크 여유가 `min_free_disk_gb_to_lease` 아래로 내려가면 신규 lease를 중단하고 26.3절 descope 순서를 적용한다.

## 39.10 실패 격리와 재시도

- task 단위로 재시도한다. `backoff_seconds`로 간격을 두고 `max_attempts` 초과 시 `poison`으로 격리한다.
- poison task는 전체 실행을 멈추지 않는다. 다만 격리 목록과 사유를 `queue/poison/`과 보고서에 남기고, 인벤토리 파일 수 reconciliation에 반영한다.
- retryable(일시적 IO·잠금 경합)과 non-retryable(파일 손상·스키마 위반)을 구분한다. 후자는 즉시 격리한다.
- 워커가 죽으면 리스 만료 후 재할당하고 부분 산출물은 격리한다. 같은 task가 반복 실패하면 워커 수를 줄여 재현한 뒤 원인을 찾는다.
- 한 shard가 계속 실패해 결과가 비어 있는데도 전체를 `완료`로 보고하지 마라.

## 39.11 단일 writer와 승격

- 하나의 출력 파티션에는 하나의 writer만 있다. 리스 없이 공유 경로에 쓰지 않는다.
- 워커는 `runs/<run_id>__<worker_id>/`에 만들고, 스키마·행수·해시 검증 후 공식 경로로 원자적 이동한다. 승격 기록은 `manifests/promotions.csv`에 남긴다.
- 승격되지 않은 부분 산출물을 보고서·표·그림의 수치로 쓰지 마라. 필요하면 `pending`으로 명시한다.
- 여러 워커가 만든 결과를 하나의 표로 합칠 때는 config·code·schema 해시가 모두 같은지 먼저 확인한다. 다르면 합치지 말고 재실행 범위를 정한다.

## 39.12 병렬 실행 금지사항

- 배리어를 넘기 전에 다음 단계 task를 leasable로 만들기
- 워커마다 다른 기준선·임계값·기간으로 만든 결과를 하나의 카탈로그에 합치기
- 파티션 경계에서 패딩 없이 창 특징·ROTI·사건을 계산하기
- median·MAD를 파티션별로 구해 단순 평균하기
- 리스 없이 공유 경로에 쓰거나 타 워커 파티션을 재계산해 덮어쓰기
- 실패 task를 조용히 건너뛰고 전체 완료로 보고하기
- 속도를 위해 `W_VAL`을 블라인드 워커와 같은 프로세스·큐·경로에서 실행하기
- 출력 경로에 `shard_index`를 넣어 shard 수를 바꾸면 결과 경로가 달라지게 만들기

# 40. 역할별 실행 런북

## 40.1 데이터 처리 병렬 런북

R3(소규모 망·기간 파일럿)에서 다음 순서로 검증한 뒤 R4·R5로 확대한다. 워커 수는 실측 자원에 맞춘다.

```powershell
# [0] 오케스트레이터 (단일 프로세스, 계속 유지)
python -m rinex_interference.cli doctor  --config config/analysis.yaml
python -m rinex_interference.cli plan    --config config/analysis.yaml --scale r3 --shards 16

# [1] 인벤토리 — IO 바운드
python -m rinex_interference.cli worker --role W_INV --workers 6
python -m rinex_interference.cli queue status                     # 완료 확인

# [2] 품질 + 외부 참조자료 — 역할 병렬(서로 독립)
python -m rinex_interference.cli worker --role W_QC  --workers 6
python -m rinex_interference.cli worker --role W_EXT --workers 2
python -m rinex_interference.cli barrier declare --name b1_inventory_quality_complete

# [3] 특징·ROTI — CPU 바운드, 최대 병렬
python -m rinex_interference.cli worker --role W_FEAT --workers 8

# [4] 기준선 — 배리어 뒤 단일 소유, group_key 샤딩
python -m rinex_interference.cli worker --role W_BASE --workers 4
python -m rinex_interference.cli barrier declare --name b2_baseline_frozen --evidence <HASH>

# [5] 탐지 → 망 동조성(시간블록) → 경계 재병합
python -m rinex_interference.cli worker --role W_DET --workers 8
python -m rinex_interference.cli worker --role W_NET --workers 2
python -m rinex_interference.cli reduce --stage network_events

# [6] 반증·분류, 그림 — 후보 단위 병렬
python -m rinex_interference.cli worker --role W_FALS --workers 4
python -m rinex_interference.cli worker --role W_FIG  --workers 4

# [7] 블라인드 동결 후에만 외부검증
python -m rinex_interference.cli freeze-blind
python -m rinex_interference.cli barrier declare --name b3_blind_freeze_before_official
python -m rinex_interference.cli worker --role W_VAL --workers 1

# [8] 평가·보고서 — 단일
python -m rinex_interference.cli evaluate
python -m rinex_interference.cli report
```

운영 규칙:

- 각 단계에서 `queue status`로 `pending/leased/failed/poison`을 확인하고, 실패가 남은 채 다음 배리어를 선언하지 않는다.
- 워커는 언제든 추가·제거할 수 있어야 한다. 워커를 늘렸다고 결과가 달라지면 즉시 중단하고 41.2절 시험으로 원인을 찾는다.
- 장시간 실행은 워커별 로그를 분리(`logs/worker_<worker_id>.log`)하고 처리량(task/h, GB/h)을 주기적으로 기록한다.
- 자원이 부족하면 워커 수를 줄이는 것이 먼저이고, 분석 범위 축소(26.3절)는 그다음이다.

## 40.2 구현 작업 병렬 런북

여러 작성자·에이전트가 코드를 동시에 만들 때는 다음 순서를 지킨다. 인터페이스를 먼저 고정하지 않으면 병렬 구현이 재작업으로 끝난다.

1. **인터페이스 동결(직렬, 1인)**: `schemas.py`(테이블·열·타입), `config.py`, 작업 큐 스키마, 안정 ID 규칙, provenance 열. 이것이 끝나기 전에는 병렬 구현을 시작하지 않는다.
2. **골든 픽스처 우선**: 실제 파일 2~3개에서 만든 소형 fixture와 기대 출력(28절 golden)을 먼저 만든다. 각 모듈 담당자는 이 fixture로 자기 모듈을 검증한다.
3. **모듈 단위 소유권**: 파일 경계로 나눈다. 예) A: `compression.py`+`rinex_header.py`+`rinex_reader.py`, B: `time_systems.py`+`station_metadata.py`+`orbit_geometry.py`, C: `features/*`, D: `baseline.py`+`anomaly.py`, E: `network_events.py`+`confounders.py`, F: `evaluation.py`+`reporting.py`+`plotting.py`, G: 큐·CLI·오케스트레이션. 같은 파일을 두 사람이 동시에 고치지 않는다.
4. **공유 파일 규칙**: `schemas.py`·`config.py`·`cli.py`처럼 모두가 건드리는 파일은 변경 전 선점(청구)하고 짧게 끝낸다. 스키마 변경은 소유자 승인 후 일괄 반영한다.
5. **병합 순서**: 하위 의존(파서·시간·기하) → 특징 → 기준선·탐지 → 망·반증 → 평가·보고. 상위 모듈을 먼저 병합해 하위 인터페이스를 강제하지 마라.
6. **각 병합의 완료 조건**: 해당 모듈 단위시험 통과, golden 재생성 결과 동일, placeholder 스캔 통과, 스키마 변경 시 마이그레이션·재실행 범위 기록.
7. **에이전트에게 맡길 때**: 15.4절 모듈 문서 + 해당 모듈의 스키마·fixture·시험만 컨텍스트로 준다. 다른 모듈의 코드를 고치지 말라고 범위를 명시한다.

## 40.3 최소 구성과 확장

- **워커 1개**: `max_total_workers: 1`. 큐·배리어·샤딩은 그대로 두고 순차 실행한다. 이 결과가 모든 불변성 시험의 기준(reference)이 된다.
- **소규모(4~8 코어 1대)**: 위 40.1 런북을 그대로 쓰되 역할별 워커 수를 절반으로 시작한다.
- **여러 대**: 큐를 한 대(또는 신뢰 가능한 DB)에 두고 원시자료 읽기 대역폭을 먼저 측정한다. 파일 접근이 병목이면 노드를 늘려도 처리량이 늘지 않는다. 노드별로 `cache/`는 로컬에 두고 공식 산출물만 공유 저장소에 승격한다.
- 확장 전후로 반드시 41.2절 불변성 시험을 다시 통과시킨다.

# 41. 병렬 실행 검증·성능 계약

## 41.1 검증 순서

병렬화는 R1·R2에서 만들지 말고, 직렬로 정확성을 확보한 뒤 R3에서 도입한다. 순서를 바꾸면 병렬 버그와 과학적 오류가 섞여 원인을 분리할 수 없다.

1. R1·R2: 워커 1개, 큐·배리어 구조만 갖춘 직렬 실행으로 정확성 확보
2. R3: 워커 2~4개로 확장하고 불변성 시험 통과
3. R4: 목표 워커 수로 확장, 처리량·자원 실측, 병목 식별
4. R5: 확정된 구성으로 전체 실행, 실측 기반 소요시간 재산정

## 41.2 불변성 시험

- `--workers 1` 결과를 기준으로 `--workers N`, `--shards 1/4/16` 결과의 내용 해시가 동일(provenance 열 제외)
- 사건 ID·경계 사건 수·후보 수가 워커 수와 무관
- 중단 후 재개 결과가 무중단 실행과 동일
- 실패·재시도가 있었던 실행과 없던 실행의 최종 산출물이 동일
- 불일치가 발견되면 성능 문제로 취급하지 말고 정확성 결함으로 기록·수정한다.

## 41.3 경계·집계 시험

- 자정·시간블록 경계를 걸치는 합성 사건이 직렬 실행과 동일하게 검출·병합되는지
- 경계에 걸친 ROTI arc가 패딩 후 유효값으로 계산되는지
- 스케치 기반 median·MAD와 정확값의 오차가 대표 그룹에서 허용 범위인지
- 축약 순서를 바꿔도 tolerance 안에서 동일한지

## 41.4 성능 측정과 보고

다음을 실측해 `reports/16_parallel_execution_report.md`에 남긴다. 추정값을 실측처럼 쓰지 마라.

```text
role
worker_count
tasks_done / failed / poison
wall_clock_seconds
cpu_seconds
throughput (task/h, station_day/h, GB/h)
peak_rss_mb_per_worker
disk_read_mb_s / disk_write_mb_s
scaling_efficiency (workers=1 대비)
bottleneck_class (cpu | io | memory | lock | external_network)
```

- 워커 수를 늘려도 처리량이 늘지 않는 지점을 찾아 병목을 명시한다. 대개 원시자료 IO 또는 압축 해제다.
- 잠금 경합·큐 지연이 전체 시간의 유의한 비율이면 shard 크기를 키워 task 수를 줄인다(task가 너무 잘면 오버헤드가 커진다).
- 전체 소요시간 산정(25.2절)은 이 실측값으로 갱신한다.

# 42. 미규정 사례 처리 계약

이 계약은 완결될 수 없다. 실제 자료는 항상 조항보다 한 걸음 앞서 있고, 빈틈은 언제나 **계약이 데이터와 처음 만나는 지점**에서 생긴다. 따라서 규칙이 없는 상황 자체를 예외가 아니라 **정상 업무 흐름**으로 다룬다.

## 42.1 기본 행동

계약에 규칙이 없는 상황을 만나면 다음을 모두 수행한다. **멈추지도, 임의로 정하지도 않는다.**

1. `docs/UNSPECIFIED_CASES.csv`에 기록한다.
2. 아래 보수적 기본값 중 해당하는 것을 적용하고 계속 진행한다.
3. 영향을 받는 산출물에 `unspecified_case_ids` 열로 연결한다.
4. 같은 `case_id`가 `escalation_count`를 넘으면 그 자체가 계약 개정 요청이다. orchestrator가 규칙을 확정하기 전까지 그 사례가 포함된 결과를 **최종 수치로 쓰지 않는다.**

## 42.2 보수적 기본값

| 상황 | 하지 말 것 | 할 것 |
|---|---|---|
| 해석 불가 파일·레코드 | 삭제·건너뛰기 | **격리**하고 사유 기록 |
| 판정 근거 부족 | 추정값 생성 | `unassessable` 또는 `not_computed` |
| 같은 것인지 불확실한 두 대상 | 병합 | **분리 유지**하고 관계만 기록 |
| 증거등급·후보 승격 애매 | 상향 | **보류**하고 판단 근거 기록 |
| 단위·의미 불확실한 관측값 | 다른 값으로 환산 | 원값 보존 + `unit_confidence` 강등 |
| 시각 해석 불확실 | 임의 보정 | 격리하고 시간계 확인 전까지 망 동시성 분석 제외 |

## 42.3 `docs/UNSPECIFIED_CASES.csv`

```text
case_id                  # 사례 유형의 안정 ID (내용 기반 해시)
first_seen_at_utc
occurrences
stage / module
input_example            # 파일 상대경로·행·필드 (원시자료를 복사하지 말 것)
why_unspecified          # 어느 절이 이 경우를 다루지 않는지
temporary_handling       # 적용한 보수적 기본값
affected_artifacts
affected_claim_ids
reversal_procedure       # 규칙 확정 시 되돌리는 방법
status                   # open | escalated | ruled | superseded
ruled_by / ruled_at_utc / rule_reference
session_id / worker_id / run_id
```

## 42.4 보고 의무

- 최종 보고서에 미규정 사례 목록과 **그것이 결론에 준 영향**을 반드시 싣는다.
- 미규정 사례가 하나도 없다는 보고는 신뢰하지 않는다. 대개는 기록하지 않은 것이다.
- 규칙이 확정되면 조항을 41절 절차로 개정하고, 기존 임시 처리 결과의 재실행 범위를 명시한다.

# 43. 세션 계약

이 문서에서 **세션**은 두 가지를 뜻하며 절대 혼동하지 않는다.

- **실행 세션(execution session)**: 사람 또는 코딩 에이전트의 한 번의 작업 컨텍스트. 이 절의 대상이다.
- **관측 세션(observation session)**: GNSS 관측 파일 하나가 담는 시간 구간(기본 24시간). 44.1절의 대상이다.

## 43.1 왜 실행 세션이 연구 결과에 영향을 주는가

- 세션은 **기억의 경계**다. 세션 안에서만 존재했던 판단(왜 이 파일을 제외했는지, 왜 이 임계값을 골랐는지)은 세션이 끝나면 사라지고, 다음 세션은 같은 계약을 읽고도 다르게 해석한다.
- 세션은 **분석자 자유도**를 만든다. 세션마다 규칙이 조금씩 바뀌면 사후 튜닝과 구분되지 않는다.
- 세션은 **블라인드 경계**다. 한 세션에서 공식 사건자료를 읽은 뒤 같은 세션에서 기준선을 만지면, 프로세스가 분리되어 있어도 누출은 이미 일어난 것이다.
- 컨텍스트 한계 때문에 계약 전체를 매번 주입할 수 없다. 모듈만 주입하면 **과학적 제한이 빠진 채 실행**될 위험이 생긴다.

## 43.2 세션 시작 의무

새 세션은 다음을 먼저 읽고, 읽었다는 사실을 `docs/SESSION_LOG.csv`에 남긴다.

```text
docs/runbook/00_invariants_and_goal.md   # 불변 조항
PHASE_HANDOFF.md                          # 현재 Phase와 다음 정확한 1개 작업
docs/IMPLEMENTATION_STATUS.md             # 무엇이 구현·검증되었는지
DECISIONS.md                              # 이미 내려진 판단(재논의 금지)
docs/UNSPECIFIED_CASES.csv                # 열린 미규정 사례
```

읽지 않고 시작해 이미 내려진 판단을 뒤집는 것을 금지한다. 판단을 바꿔야 한다면 재논의가 아니라 **supersede 절차**를 따른다.

## 43.3 불변 조항 상시 주입

15.4절 모듈화로 컨텍스트를 나눌 때에도 다음은 **어떤 세션에서도 축약·생략하지 않는다.**

- 가장 중요한 과학적 제한, 금지 표현
- 증거등급 상한(RINEX 단독 E3)
- 블라인드 격리와 누출 방지
- 원시자료 보호
- 42절 미규정 사례 기본 행동

## 43.4 세션 중 규칙

- 한 세션 안에서 `blind_status`를 바꾸지 않는다. 공식 사건자료를 열람해야 하면 **세션을 종료하고 새 세션을 unblinded로 시작**한다.
- 컨텍스트가 부족해질 조짐이 있으면 코드를 축약하거나 여러 모듈을 반쪽 구현하지 않는다. 현재 원자적 작업을 완료·시험한 뒤 깨끗한 경계에서 멈춘다.
- 세션에서 새로 만든 규칙·임계값·예외 처리는 즉시 `DECISIONS.md` 또는 `UNSPECIFIED_CASES.csv`에 쓴다. 세션 종료 시 몰아 쓰지 않는다(잊는다).

## 43.5 세션 종료 의무

```text
session_id
started_at_utc / ended_at_utc
role / blind_status
documents_read
tasks_completed / tasks_left_open
decisions_made              # DECISIONS.md 레코드 ID
unspecified_cases_opened
artifacts_written
next_single_action          # 다음 세션이 할 정확히 하나의 작업
```

`PHASE_HANDOFF.md`와 이 기록만으로 다른 세션이 이어받을 수 있어야 한다. **개인의 기억에만 있는 맥락을 남기지 마라.**

## 43.6 세션과 재현성

- 모든 산출물·claim·결정에 `session_id`를 남기고 `run_id`·`worker_id`와 매핑한다.
- 재실행 결과가 달라졌을 때 "어느 세션의 판단에서 갈라졌는지" 추적할 수 있어야 한다.
- 세션 수와 세션당 작업 범위를 `IMPLEMENTATION_STATUS.md`에 기록해 Phase별 실제 소요를 남긴다.

# 44. 실측 인벤토리 반영 계약

## 44.0 사전 감사에서 확인된 자료 특성

아래는 **사용자가 제공한 사전 감사 결과**이며 상태는 `external`이다. 단계 1에서 이 계약의 방식으로 재확인하기 전에는 `observed`로 승격하지 않는다. 재확인 결과가 다르면 아래 수치가 아니라 재확인 결과를 따른다.

```text
기간            2021-01-01 ~ 2026-05-18 (1,964일, 범위 내 결측 0일) → 2026은 YTD
station-day     175,935
파일            875,789 (station-day당 약 4.98 = obs 1 + nav 약 4)
용량            454.3 GiB (station-day당 약 2.64 MiB)
관측소          79국(2021) → 98국(2026)
압축·형식       거의 전량 .Z (Unix compress), RINEX 2 계열 파일명
형식 예외       10일에서 다른 확장자 혼입(.zip 포함)
파생 규모       station-epoch 약 5.07억, 위성×epoch 약 10~18 G건
```

이 특성에서 곧바로 따라오는 계약이 44.1~44.10이다.

## 44.1 관측 세션(일 경계) 계약

파일 하나를 무조건 독립 세션으로 간주하지 않는다. 자정 경계에서 arc·모호도·수신기 clock이 재초기화되는 것은 **물리적 현상**이며 데이터 파이프라인 이상과 구분해 다룬다.

- 같은 station에서 앞 파일의 마지막 유효 epoch와 다음 파일의 첫 유효 epoch 간격이 `max_stitch_gap_seconds` 이내이고 관측코드 구성·좌표·수신기 metadata가 연속이면 `logical_session_id`로 연결한다.
- 수신기 reset, clock step, 좌표 불연속, 관측코드 변경, 시각 역행이 있으면 새 세션으로 분리하고 `session_break_reason`을 남긴다.
- 연결·분리 근거를 `session_stitch_reason`, `session_stitch_confidence`로 저장한다.
- **파일 단위 또는 세션 단위 중심화(offset 제거)를 금지한다.** 세션 전체에 걸친 장시간 이상이 정상 오프셋으로 흡수되어 사라진다. 기준선은 반드시 5절·19절의 regime 계층으로 만든다.
- 자정 ±`midnight_window_seconds` 안에서 시작·종료한 사건의 비율을 별도로 보고한다. 이 비율이 비정상적으로 높으면 세션 효과를 먼저 의심한다.
- 경계를 걸친 arc는 39.7절 halo로 계산하고, 경계에서 병합된 사건은 `boundary_merged=true`로 표시해 지속시간 분포를 별도 집계한다.

## 44.2 canonical 파일 선택 규칙

같은 station-day에 형식·압축이 다른 파일이 공존하는 사례가 실제로 존재한다(44.0의 형식 예외 10일).

1. `content_equality_keys`로 내용 동등성을 먼저 판정한다. 동등하면 우선순위 목록으로 canonical을 고른다.
2. 동등하지 않으면 **둘 다 격리**하고 `duplicate_group_id`로 묶은 뒤 수동 확인 대상으로 올린다. 임의로 하나를 고르지 않는다.
3. 어떤 경우에도 대안 파일을 삭제·이동하지 않는다(원시자료 보호).
4. 선택 결과와 근거를 `inventory/canonical_selection.csv`에 남기고, 후보 사건의 `source_refs`가 canonical 파일을 가리키게 한다.
5. 우선순위로도 결정되지 않으면 42절 미규정 사례로 기록한다.

## 44.3 항법자료 병합 계약

station-day당 nav 파일이 여러 개 존재한다.

- 위성 위치·고도각 계산의 소스 우선순위는 `navigation_merge.source_priority`를 따르고, 실제 사용한 소스를 epoch·위성 단위로 기록한다.
- 여러 nav의 동일 ephemeris는 `dedupe_key`로 중복 제거한다. 서로 다른 값이 같은 key로 오면 병합하지 말고 둘 다 보존한 뒤 선택 근거를 남긴다.
- health flag가 불량인 레코드는 제외하되 제외 사실을 기록한다. `max_ephemeris_age_hours`를 넘는 외삽은 사용하지 않고 해당 구간을 `geometry_unavailable`로 둔다.
- 항법자료 문제로 고도각을 계산하지 못한 구간을 **정상으로 간주하지 않는다.** 고도각 의존 특징만 `not_computed`로 두고 나머지는 계속 산출한다.

## 44.4 관측소 코호트 정책

관측소 수가 79국에서 98국으로 증가했다. 연도 비교에서 이 변화를 통제하지 않으면 "사건이 늘었다"가 "관측소가 늘었다"와 구분되지 않는다.

- **주 분석은 고정 코호트**(분석 전 기간에 존재한 관측소)로 수행한다.
- **보조 분석은 전체 관측소 + 노출 정규화**(유효 station-day 분모)로 수행한다.
- 두 결과를 모두 보고하고, 결론이 코호트 선택에 따라 달라지면 그 사실을 명시한다.
- 코호트 정의는 평가 이전에 동결한다. 결과를 보고 코호트를 바꾸지 않는다.
- 관측소 신설·폐지·이설(같은 코드, 다른 지점)은 regime 분할이 아니라 **station 분할**로 처리하고 좌표 점프로 감지한다.

## 44.5 위성군 coverage regime

- 한 관측소에서 새 위성군 관측이 시작·중단되면 그 시점을 regime 경계로 삼는다(`min_stable_days_to_close_regime` 이상 안정 후 확정).
- '위성 수 급락' 계열 검출기의 기준선은 반드시 같은 coverage regime 안에서만 만든다. 2021년과 2025년의 위성 수 분포를 하나의 기준선으로 합치지 않는다.
- 대역차분(4.5절) 특징은 인벤토리에서 확인된 관측코드가 존재하는 regime에서만 계산한다. L5/E5a가 없는 구간에서 값을 만들어내지 않는다.

## 44.6 분석집합 동결과 신규 자료

자료는 계속 쌓인다. 실행 중 입력 집합이 커지는 것은 정상 상황이다.

- 분석집합은 `analysis_cutoff_utc`로 동결한다. 동결 이후 추가된 파일은 **현재 run에 포함하지 않는다.**
- 새 자료로 분석하려면 새 `run_id`로 분리하고, 동결된 기준선·blind freeze를 연장하지 않는다.
- 기준선 재학습이 필요하다고 판단되면 orchestrator 승인·범위 문서화·기존 claim supersede를 함께 수행한다.
- 보고서에는 항상 분석집합의 cutoff와 그 시점의 파일 수·용량을 명시한다.

## 44.7 위성×epoch 저장 전략

위성×epoch 레코드는 10~18 G건 규모다. **전량 저장하지 않는다.**

- 고도각·신호강도 기준선은 위성별 행을 저장하지 않고 **스트리밍 누산기**(group_key × constellation × exact code × elevation_bin의 count·합·제곱합·히스토그램 또는 39.8절 스케치)로 만든다.
- epoch 수준 특징(위성 수, 공통 하락 비율, 분위수 등)은 ingest 중에 계산해 epoch 요약 테이블에만 남긴다.
- 위성별 행은 `satellite_obs_retention.mode`에 따라 **사건창 전후 전량 + 정상 구간 층화표본**만 보존한다. detect 이후 사건창을 원문에서 재파싱하는 2-pass를 허용한다.
- `full` 모드는 여유 디스크가 예상 산출량의 3배 이상일 때만, 근거를 기록하고 켠다.
- 무엇이 전량이고 무엇이 표본인지 manifest와 보고서에 명시한다. **표본 통계를 전량 통계처럼 보고하지 않는다.**

## 44.8 후보율 가드와 처리량 게이트

- 유효 station-day당 후보 발생률이 `candidate_rate_guard`의 기대 범위를 벗어나면 **본실행을 진행하지 않는다.** 기준선 오류, 세션 중심화 실수, 품질 게이트 누락, 시간계 오류를 먼저 확인한다.
- 이때 임계값을 조용히 올려 후보 수를 맞추는 것을 금지한다. 원인을 찾아 고치거나 42절로 기록한다.
- R1·R2·R3에서 단위 처리량(station-day/h, GB/h)을 실측하고 전체 예상 소요를 산출한다. 예상 소요가 `runtime_guard.max_full_run_hours`를 넘으면 다음 규모로 진입하지 말고 병목(압축 해제 경로, 파서 핫루프, 저장 전략, dtype)을 먼저 개선한다.
- 25.2절의 소요시간 산정은 이 실측값으로만 한다. 다른 프로젝트의 처리량을 가져오지 않는다.

## 44.9 수동검토 표본 규칙

- 후보가 `manual_review.full_review_max_candidates` 이하이면 전수 검토한다.
- 초과하면 `stratify_by` 기준의 층화표본을 고정 seed로 뽑아 검토하고, **표본 비율과 층별 구성**을 보고한다.
- 전수 검토하지 못한 후보는 `manual_review_status=not_reviewed`로 남기고 증거등급 상한을 낮춘다. 검토하지 않은 후보를 검토한 것처럼 집계하지 않는다.
- 이중검토(39.8절) 비율은 이 표본 위에서 계산한다.

## 44.10 캐시·로그 운영

- 압축 해제본은 처리 후 즉시 삭제한다(`delete_on_task_success`). 전량 해제본을 보관하려 하지 마라. 이 자료는 해제 시 텍스트가 크게 팽창한다.
- 캐시 용량이 상한에 닿으면 신규 task lease를 중단하고 정리 후 재개한다.
- 파일 단위 성공 로그를 텍스트 로그에 남기지 않는다. 성공은 partition manifest에, 로그에는 경고 이상만 남긴다. 875,789개 파일 규모에서는 로그 자체가 자원 문제가 된다.
- 로그 총량 상한을 두고, 초과 시 회전·압축하되 오류 로그는 보존한다.

# 실행을 시작하라

먼저 원시자료 폴더의 접근 가능 여부와 상위 수준의 디렉터리 구조를 읽기 전용으로 확인하고, 기존 지침파일과 기존 연구자산을 감사하라. 그 다음 전수 헤더 인벤토리와 소규모 파일럿을 완성하고 검증한 후, 자원 안전조건을 만족하면 전체 실제기간으로 확장하라. 계획만 제시하고 멈추지 말고 코드 작성, 테스트, 실제 실행, 결과 검증, 보고서 생성까지 계속하라.

즉시 다음 순서로 수행한다.

1. 이번 실행 세션의 `session_id`·역할·`blind_status`를 정하고, 43.2절 필수 문서를 먼저 읽는다(없으면 만든다). 이미 내려진 판단을 다시 논의하지 않는다.
2. 원시자료와 결과경로의 존재·권한을 읽기 전용으로 확인한다.
3. 적용 규칙, Git 상태, 기존 코드·보고서·후보·설정을 감사한다.
4. 환경, 도구, CPU, RAM, disk, 원시자료 저장장치의 읽기 대역폭을 기록한다.
5. 진행파일·`WORKER_STATUS.md`·`UNSPECIFIED_CASES.csv`·초기 manifest를 만든다.
6. Phase 1 헤더 중심 전수 인벤토리를 수행하고, 44.0절의 사전 감사 수치를 재확인한다.
7. 실제 RINEX version·압축·관측코드를 근거로 R1 표본을 선택한다. 형식 예외 파일을 반드시 포함한다.
8. **워커 1개(직렬)로** R1을 end-to-end로 구현·시험하고 모든 게이트와 단위 처리량을 기록한다. 이 결과가 이후 병렬 실행의 기준이다.
9. R2까지 직렬로 통과한 뒤 R3에서 작업 큐·배리어·샤딩을 도입하고 41.2절 불변성 시험과 44.8절 후보율·처리량 게이트를 통과시킨다.
10. gate와 시험이 통과할 때에만 워커 수를 늘리고 R4→R5로 확장한다. 처리량·병목을 실측해 기록한다.
11. blind artifact를 freeze하기 전에 공식 사건정보를 탐지에 사용하지 않는다. `W_VAL`은 B3 이후 별도 세션·별도 프로세스로만 실행한다.
12. 상위 후보에 모든 반증을 수행한 뒤 최종 보고한다.
13. 세션을 끝낼 때 43.5절 인계 기록과 미규정 사례를 남긴다. 다음 세션이 읽을 **정확히 하나의 다음 작업**을 적는다.

광범위한 사전 질문만 던지고 멈추지 마라. 접근 가능한 파일을 먼저 감사하고 안전한 기본값으로 R1까지 진행한다. 실제로 막히는 권한, 경로, 저장공간, 암호화, 손상 문제만 정확한 증거와 필요한 조치와 함께 질문한다.

실제 데이터가 없거나 접근할 수 없으면 station·event·수치를 만들어내지 마라. 구현, synthetic test, input contract까지 완료하고 `blocked` 상태, 필요한 입력, 마지막 valid checkpoint, 정확한 resume 명령을 남긴다.

**후보 수가 줄어드는 것은 실패가 아니다. 자료장애·위성문제·수신기변경·전리층·현장환경으로 설명되는 후보를 제거하고도 남은 사건만 제한된 표현으로 제시하라. 30초 CORS RINEX는 강력한 관측망 증거를 줄 수 있지만 RF 원인을 단독 확정하는 센서는 아니다.**
