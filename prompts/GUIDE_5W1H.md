# CORS RINEX 30초 GNSS 전파교란 분석 프롬프트 — 5W1H 설명서

대상 문서: `prompts/CORS_RINEX30S_GNSS_interference_V7_parallel.md` (V7)

이 설명서는 위 프롬프트를 **처음 보는 사람**이 "이게 무슨 일을 시키는 문서이고, 왜 이렇게 길고 까다로운가"를 이해하도록 쓴 안내서다. 원문은 3,200줄이 넘는 실행 계약이라 처음부터 읽기 어렵다. 여기서는 Why → What → Who → Where → When → How 순서로 풀어 설명하고, 마지막에 자주 하는 오해·용어·본문 위치 색인을 붙였다.

> **한 문장 요약**
> 전국 CORS(상시관측소)에 2021년경부터 쌓인 30초 간격 GNSS 관측파일을 전수 감사해서, **GPS 전파교란이 의심되는 사건 후보를 찾아내고 → 다른 원인일 가능성을 하나씩 반증하고 → 공식 사건기록과 대조한 뒤 → 남은 것만 제한된 표현으로 보고**하는 재현 가능한 분석 시스템을, 코딩 에이전트가 실제로 만들고 실행하게 하는 지시서다.

---

## 0. 5W1H 한 장 요약

| 구분 | 핵심 |
|---|---|
| **Why (왜)** | GNSS 전파교란은 항공·해양·측위에 실제 피해를 준다. 하지만 RF 계측기 없이 관측자료만으로 "재밍이다"라고 말하면 과학적으로 무너진다. 그래서 **탐지보다 반증과 한계 표기를 더 강하게 요구**하는 계약을 만들었다. 최종 용도는 박사학위논문과 SCI 논문의 근거자료다. |
| **What (무엇)** | RINEX 파일 요약이 아니라 **파이프라인 소프트웨어 + 검증시험 + 사건 후보 카탈로그 + 증거 묶음 + 한국어 최종보고서 세트**를 만든다. 주장 강도는 증거등급 E0~E5로 제한하며 RINEX만으로는 원칙적으로 E3을 넘지 못한다. |
| **Who (누가)** | 사람 연구자와 코딩 에이전트가 함께. 실행은 **역할이 다른 12종 워커 프로세스**(orchestrator, W_INV, W_QC, W_EXT, W_FEAT, W_BASE, W_DET, W_NET, W_FALS, W_VAL, W_FIG, W_REP)로 나눠서 병렬 수행한다. |
| **Where (어디서)** | 원시자료 `E:\...\rinex\Daily`(**읽기 전용**), 결과는 `analysis_30s_interference/`에만 기록. 외부 참조자료(IGS·GFZ·Kyoto 등)는 `cache/external`에 URL·해시와 함께 보관. 공간 범위는 한국 CORS 망. |
| **When (언제)** | 분석 대상 기간은 "2021~2026"이라는 **말이 아니라 파일 헤더와 실제 epoch로 확인한 기간**. 실행 순서는 게이트 P0~P12와 규모확장 R1→R5, 그리고 병렬 배리어 B1~B3이 강제한다. |
| **How (어떻게)** | 인벤토리 → 품질게이트 → 시간·좌표 표준화 → 특징추출 → 정상 기준선 → 다중 검출기 이상탐지 → 다중 관측소 공간 동조성 → 블라인드/외부검증 분리 → 반증·분류·증거등급 → 보고서. 각 단계마다 완료 게이트, 재현성 요구, 금지사항이 붙는다. |

---

## 1. WHY — 왜 이런 문서를 만들었는가

### 1.1 현실 문제

GNSS(GPS·GLONASS·Galileo·BeiDou 등) 신호는 지상에 도달할 때 매우 약하다. 그래서 상대적으로 작은 방해전파(재밍)나 위조신호(스푸핑)에도 수신 품질이 무너질 수 있다. 항공기 접근·해상 항행·정밀측위·시각동기가 모두 영향을 받는다. 한국 주변에서도 GPS 수신장애 관련 항행경보·NOTAM이 발행된 사례가 있다.

### 1.2 왜 하필 CORS 30초 RINEX인가

CORS(Continuously Operating Reference Station, 상시관측소)는 다음 장점이 있다.

- **전국에 고정 설치**되어 있고 위치가 알려져 있다 → 위치가 흔들리면 그 자체가 이상신호
- **장기간 연속 축적**되어 있다 → 몇 년치 정상 분포를 만들 수 있다
- **여러 관측소가 동시에 본다** → 한 대의 고장인지 지역 현상인지 구분할 수 있다

이건 "관측망 증거"로서는 강력하다. 단, 결정적 한계가 있다(1.3).

### 1.3 왜 그렇게까지 조심하라고 하는가 — 이 자료로 못 하는 것

프롬프트가 가장 강조하는 부분이며, 문서 전체의 톤을 결정한다.

- RINEX는 **RF 스펙트럼도, 수신기 내부 진단자료도 아니다.** 방해신호의 전력·J/S·중심주파수·대역폭·변조방식·방향·**송신원 위치**를 측정했다고 말할 수 없다.
- **행위자·국가·기관 귀속(attribution)은 불가능하다.** 공식기관이 발표한 귀속을 인용할 때도 "당국 발표에 따르면"으로 한정하고 본 분석의 결론으로 올리지 않는다.
- 수신기 내부의 **간섭완화 기능(AGC·notch filter 등)이 약한 간섭을 관측값에서 지워버릴 수 있다.** 따라서 "안 보였다"는 "간섭이 없었다"가 아니라 "이 관측체계에서는 관측되지 않았다"이다.
- **30초 표본**은 30초보다 짧은 사건을 놓치거나 한두 epoch로만 남긴다. 시작·종료시각과 지속시간에는 항상 해상도 한계가 붙는다.
- 고정 CORS 30초 자료로 **스푸핑을 확정하는 것은 특히 어렵다.** 그래서 결과 명칭을 `spoofing_compatible`(스푸핑과 양립 가능한 이상)로 제한한다.

### 1.4 왜 이렇게 형식이 빡빡한가

이 문서는 사람에게 주는 연구계획서가 아니라 **코딩 에이전트에게 주는 실행 계약**이다. 에이전트(그리고 사람도)는 흔히 이런 실수를 한다.

- 파일을 다 못 읽었는데 "분석 완료"라고 말한다
- 확인하지 않은 관측소 수·기간·성능지표를 그럴듯하게 채운다
- 파일럿 결과를 전체 결과처럼 보고한다
- 이상치를 찾자마자 "재밍 탐지"라고 부른다

그래서 프롬프트는 상태어(`observed`/`derived`/`configured`/`assumed`/`unavailable`/`unassessable`)를 강제하고, 모든 숫자를 claim ID로 역추적하게 하고, 게이트를 통과하지 못하면 다음 단계로 못 가게 막는다. **"후보 수가 줄어드는 것은 실패가 아니다"** 라는 마지막 문장이 이 문서의 철학이다.

### 1.5 최종 용도

- SCI(E)급 논문 최대 3편(방법론 / 탐지·망 동조성 / 외부검증·사례)의 근거자료
- 박사학위논문의 자료·방법·탐지·검증 장
- 다만 논문 편수는 **사전 확정 목표가 아니다.** 결과가 지지하지 않으면 병합·보류하고, 그래도 데이터 파이프라인은 완료로 인정한다(38절).

---

## 2. WHAT — 무엇을 만들고, 무엇을 주장할 수 있는가

### 2.1 만들어야 하는 산출물

| 묶음 | 내용 |
|---|---|
| 코드 | `src/rinex_interference/` — 파서, 시간계, 기하, 품질, 특징, 기준선, 탐지, 망 사건, 반증, 검증, 평가, 보고, 그림 + CLI |
| 설정 | `config/analysis.yaml`(모든 임계값), `thresholds.yaml`, `authors`/`overrides`, 잠긴 의존성 |
| 자료 산출물 | `inventory/`(전수 파일 목록), `data_quality/`, `features/`, `baselines/`, `candidates/`, `validation/`, `evaluation/` (대용량은 Parquet 파티션) |
| 근거 | 후보별 Evidence Bundle(JSON), `figures/` 사건별 그림, `docs/FALSIFICATION_LOG.md` |
| 문서 | `reports/00`~`reports/16`, `docs/METHODOLOGY.md`, `DATA_DICTIONARY.md`, `SCIENTIFIC_LIMITATIONS.md`, `CLAIM_REGISTRY.csv`, `THRESHOLD_TRACEABILITY.md`, `SOURCE_REGISTER.md` 등 |
| 운영 기록 | `PROGRESS.md`, `PHASE_HANDOFF.md`, `DECISIONS.md`, `SURPRISES.md`, `RUN_LOG.md`, `WORKER_STATUS.md`, `run_manifest.json` |

핵심 보고서 몇 개:

- `reports/09_candidate_event_catalog.(csv|md)` — 후보 사건 카탈로그
- `reports/10_final_scientific_report.md` — 한국어 최종 과학보고서
- `reports/12_limitations_and_next_data.md` — 한계와 다음에 필요한 자료
- `reports/15_evaluation_protocol_and_results.md` — 평가 프로토콜·결과
- `reports/16_parallel_execution_report.md` — 병렬 실행·성능 실측 (V7 신설)

### 2.2 분석 단위 계층 (12절)

```
RawFile → Observation → Epoch → StationWindow → StationEvent → NetworkEvent → EventFamily
```

- `StationEvent`: 한 관측소에서 시간적으로 이어지는 이상 구간
- `NetworkEvent`: 허용 시차 안에서 여러 관측소가 비슷한 신호·대역·특징으로 이상한 묶음
- `AffectedObservationFootprint`: 이상이 **관측된** 관측소·시간 범위. **간섭원 위치가 아니다.**

모든 ID는 재실행·워커 수·파일 순서와 무관하게 같아야 한다(안정 ID).

### 2.3 무엇을 주장할 수 있는가 — 증거등급 (9절)

| 등급 | 의미 |
|---|---|
| E0 | 분석 불가·자료 부족 |
| E1 | 단일 지표 이상 |
| E2 | 한 관측소에서 독립 특징군 2개 이상 일치 |
| E3 | **여러 관측소**에서 유사 패턴의 시공간 동조성 확인 |
| E4 | E3 + 독립된 발생확인 공식 1차 출처 또는 별도 센서 정합 |
| E5 | 독립 RF 측정·통제실험으로 원인 직접 확인 |

**RINEX 단독 분석은 원칙적으로 E3을 넘지 않는다.** NOTAM·항행경보 같은 advisory(예방적 경보)의 단순 시간중첩만으로는 E4를 줄 수 없다.

### 2.4 사건 원인 분류 (확정 라벨이 아니라 순위 있는 가설)

`jamming_like`, `spoofing_compatible`, `unintentional_rfi_possible`, `receiver_or_site_issue`, `satellite_or_product_issue`, `ionosphere_or_space_weather_possible`, `data_pipeline_issue`, `indeterminate`

여기에 ICAO 용어와 맞추기 위한 보조 필드가 붙는다.

- `rfi_observation_pattern`: `band_selective` / `multi_band_common` / `temporally_unresolved` / `unassessable`
  → **narrowband·barrage·chirp 같은 파형 이름은 스펙트럼 측정 없이 붙이지 않는다.**
- `rfi_intent_hypothesis`: `intentional_possible` / `unintentional_possible` / `unassessable`

### 2.5 상태어 (문서 전체에서 일관되게 사용)

| 상태어 | 뜻 |
|---|---|
| `observed` | 실제 파일·실행·1차 출처에서 확인됨 |
| `derived` | 관측값으로 계산됨, 입력과 산식으로 재현 가능 |
| `configured` | 설정한 후보값일 뿐 보편적 임계값이 아님 |
| `assumed` | 확인 전 작업 가정 |
| `unavailable` | 자료가 없거나 접근 불가 |
| `unassessable` | 자료는 있으나 판정할 증거가 부족 |

"경로·2021~2026년·30초"조차 처음에는 사용자가 말해준 시작점일 뿐이며, 헤더와 실제 epoch로 확인하기 전에는 `observed`로 승격하지 못한다.

---

## 3. WHO — 누가 수행하는가

### 3.1 사람과 에이전트

프롬프트는 "GNSS 측지·항법, CORS 망 분석, RINEX 2/3/4, 신호품질 관리, 전파간섭 탐지, 이상탐지, 재현가능 연구 소프트웨어에 숙련된 수석 연구자이자 데이터 엔지니어"라는 역할을 에이전트에게 부여한다. 실제로는 사람 연구자가 감독하고, 코딩 에이전트가 구현·실행하며, 여러 프로세스가 나뉘어 돈다.

### 3.2 워커 역할 12종 (V7의 39.5절)

| 역할 | 하는 일 | 쓰는 곳 |
|---|---|---|
| `orchestrator` | 작업계획·큐 생성, **배리어 선언**, 게이트 판정, 승격 | `queue/`, `manifests/` |
| `W_INV` | 파일 열거·헤더 인벤토리·압축 판별·해시 | `inventory/` |
| `W_QC` | 품질지표·등급·metadata regime | `data_quality/`, `metadata/` |
| `W_EXT` | 항법·궤도·전리층·지자기 지수 등 외부자료 취득 | `cache/external/` |
| `W_FEAT` | 특징·ROTI·대역차분 추출 (가장 무거움) | `features/` |
| `W_BASE` | 정상 기준선 학습·동결 | `baselines/` |
| `W_DET` | 다중 검출기 이상탐지·StationEvent | `candidates/station_*` |
| `W_NET` | 망 동조성·공간통계·NetworkEvent | `candidates/network_*` |
| `W_FALS` | 반증 엔진·분류·증거등급 | `candidates/`, 반증 로그 |
| `W_VAL` | 공식 사건 정규화·replay (**유일한 unblinded 역할**) | `validation_unblinded/` |
| `W_FIG` | 그림 생성 | `figures/` |
| `W_REP` | 보고서·claim 확정 (**항상 1개**) | `reports/`, claim registry |

규칙: **동시에 도는 프로세스는 하나의 역할만 맡는다.** 한 사람/에이전트가 여러 역할을 순차로 하는 것은 허용된다.

### 3.3 왜 `W_VAL`만 따로 떼어 놓는가

"공식 사건이 언제 있었는지" 아는 상태로 임계값을 고르면, 그건 탐지가 아니라 사후 맞추기다. 그래서 공식 사건정보를 다루는 역할은 **별도 프로세스·별도 출력 경로**로 격리하고, 블라인드 산출물이 동결(freeze)된 뒤에만 작동시킨다(22.6절, 배리어 B3).

---

## 4. WHERE — 어디서, 어떤 자료로

### 4.1 경로

| 구분 | 경로 | 규칙 |
|---|---|---|
| 원시자료 | `E:\worldtechRnD\Pro_phd_data\rinex\Daily` | **읽기 전용.** 이름변경·이동·덮어쓰기·수정·삭제 금지 |
| 결과 | `E:\worldtechRnD\Pro_phd_data\rinex\analysis_30s_interference` | 모든 생성물은 여기에만 |
| 임시 압축해제 | 결과폴더의 `cache/` | 원본과 해시·크기·시각 연결관계 기록 |
| 워커 작업본 | `runs/<run_id>__<worker_id>/` | 검증 후 공식 경로로 승격 |
| 공식 사건 | `validation_unblinded/` | 블라인드 워커 접근 금지 |

보고서·표에는 절대경로가 아니라 **원시루트 기준 상대경로**만 적는다.

### 4.2 어떤 자료를 읽는가

- **관측파일(RINEX OBS)**: 2/3/4 버전, `.rnx`, `.obs`, RINEX 2 연도접미, Hatanaka(`.crx`/`.d`), `.gz`, `.Z`, `.zip` 등. **파일명으로 유형을 확정하지 말고 헤더로 판별**한다.
- **항법자료**: 로컬 NAV, BRDC, SP3(정밀궤도), CLK. 없으면 위성 고도각·잔차 계산이 제한된다.
- **외부 참조자료**(있으면): IGS GIM(IONEX) 전리층 지도, GFZ Kp 지수, Kyoto WDC Dst 지수, NOAA SWPC 경보, IGS MGEX의 시간유효 GLONASS 채널 metadata.
- **공식 사건자료**(트랙 B): 정부·항공교통·해양(NAVAREA XI)·ICAO APAC 1차 출처, NOTAM, AIS 위치이상 집계 등. 각각 `source_tier`와 advisory/confirmed를 구분한다.

외부에서 받은 것은 URL·취득시각·해시를 남기고 비공식 출처는 쓰지 않는다.

### 4.3 공간 범위 주의점

- 한국 관측소는 QZSS(J) 가시성이 높고 KASS 운용 후 SBAS(S) 관측이 있을 수 있다 → 존재를 인벤토리에서 확인하고 포함/제외 정책을 설정에 명시
- 서해·동해 도서 관측소는 공간통계에서 **이웃이 없어 고립**될 수 있다 → 먼 내륙 관측소와 강제로 연결하지 말고 `spatial_isolate=true`로 기록하고 제외 사실을 보고

---

## 5. WHEN — 언제의 자료를, 어떤 순서로

### 5.1 분석 대상 기간

- 사용자는 "2021~2026년"이라고 말했지만 **그대로 믿지 않는다.** 헤더의 `TIME OF FIRST/LAST OBS`와 실제 epoch로 확인한다.
- `analysis_cutoff_utc = min(configured_end_utc, latest_valid_observation_epoch)`로 고정한다.
- 2026년이 완전한 1년임이 증명되지 않으면 반드시 **`2026 YTD`**로 표기한다.
- 연도 간 비교는 동일 DOY 범위 또는 유효 station-day로 노출량을 표준화한다.
- 실행 시각 이후이거나 설정 종료를 넘는 epoch는 시계·파일 오류 후보로 격리한다.

### 5.2 시간 표기와 함정

- RINEX의 time system은 GPS time / UTC / GLONASS time / BDT / GST가 섞일 수 있다. 내부 기준시각을 하나로 통일하고 leap second 처리를 검증한 뒤 UTC와 KST 열을 만든다.
- **모든 원시시각에 그냥 9시간을 더하지 말라**고 명시되어 있다.
- 모든 사건표·그림은 UTC와 KST를 병기한다.
- 30초 표본이므로 시작·종료시각에는 `time_uncertainty_s`가 항상 붙는다. 관측소 간 1 epoch 차이는 "30초 해상도 범위의 불확실성"이지 전파 이동시간이 아니다.

### 5.3 실행 순서 — 세 가지 축이 동시에 작동한다

**(1) 분석 단계 0~11** — 무엇을 하는가의 순서
**(2) 게이트 P0~P12** — 통과하지 못하면 다음으로 못 감

| 게이트 | 필수 산출물 | 실패 시 |
|---|---|---|
| P0 | 환경·기존자산 감사 | 규칙·경로 해결 전 중단 |
| P1 | 전수 인벤토리 | 실패파일 분류 후 재감사 |
| P2 | 시간/관측소/regime | 망 동시성 분석 금지 |
| P3 | canonical parser | parser 수정 후 R1 반복 |
| P4 | 데이터 품질 | 후보생성 전 품질정책 수정 |
| P5 | 기하/궤도 | 독립 특징만 진행 |
| P6 | 특징 | 잘못된 family 비활성화 |
| P7 | 기준선 | 기준선 재학습 |
| P8 | StationEvent | 임계값·집계 감사 |
| P9 | NetworkEvent | clustering 수정 |
| P10 | 반증 | final candidate 금지 |
| P11 | official replay | 검증결과 분리/무효화 |
| P12 | 평가 | 성능주장 금지 |

**(3) 규모 확장 R1~R5** — 얼마나 크게 돌리는가

| 단계 | 범위 | 목적 |
|---|---|---|
| R1 | 파일 1~3개(손상 파일 포함) | 파서·단위·시간·원자적 쓰기 검증 |
| R2 | station-day 1~2개 end-to-end | 전 경로 + 강제중단 후 resume + golden 생성 |
| R3 | 3~10 관측소, 1개월~여러 주 | 사건률 폭증 여부, 기준선 coverage, **실측 처리량** |
| R4 | 대표 연도/지역 (전체의 5~20%) | 여기서 **schema·config·임계값 정책을 동결** |
| R5 | 확인된 전체기간·전체망 | 전량 실행, manifest reconciliation |

**R4에서 동결한 임계값을 R5 결과를 보고 다시 바꾸지 말라**는 조항이 핵심이다(사후 튜닝 금지).

**(4) 병렬 배리어 B1~B3** (V7) — 워커가 넘을 수 없는 벽

- **B1**: 인벤토리·품질이 끝나기 전에 특징추출을 파일럿 범위 밖으로 확대 금지
- **B2**: 기준선이 동결되기 전에 탐지 task 실행 금지 (워커마다 다른 기준선을 쓰면 후보가 워커 수에 의존하게 된다)
- **B3**: 블라인드 후보가 동결되기 전에 공식 사건자료 사용 금지

배리어 통과 선언은 orchestrator만 한다.

---

## 6. HOW — 어떻게 수행하는가

### 6.1 분석 파이프라인 11단계

#### 단계 0 — 환경·기존 자산 감사
기존 코드·문서·사건목록·관측소 메타데이터를 찾아 ① 그대로 재사용 ② 수정 후 사용 ③ 제외 로 분류한다. Python 패키지(`georinex`, `xarray`, `pandas`, `pyarrow`, `scipy`, `statsmodels`, `scikit-learn`, `ruptures`, `matplotlib`, `pyproj` 등)와 GFZRNX·Hatanaka 도구 유무를 기록한다.
→ `inventory/project_inventory.csv`, `reports/00_...`, `logs/environment.txt`

#### 단계 1 — 헤더 중심 전수 인벤토리
**본문(관측 데이터)을 다 읽지 않고** 모든 파일의 헤더만 훑는다. 파일별로 상대경로·크기·압축·RINEX 버전·관측소 ID·첫/마지막 epoch·수신기/안테나·관측코드·위성군(G/R/E/C/J/S/I)·예상 대비 실제 epoch 수·중복/손상 여부를 기록한다.
→ `inventory/rinex_file_inventory.parquet`, `station_year_coverage.csv`, `observation_code_matrix.csv`, `duplicate_and_corrupt_files.csv`

#### 단계 2 — 품질 게이트
관측소×일자 단위로 관측률, 최장 공백, 위성 수 분포, S 관측값 유무, LLI 유무, 이중주파수 가능 여부 등을 계산하고 **Q0~Q4 등급**을 매긴다. Q0~Q1은 삭제하거나 억지로 보정하지 말고 제외 사유를 남긴다. SNR이 없는 관측소는 별도 특징세트로 다루고 **SNR을 추정 생성하지 않는다.**

#### 단계 3 — 항법자료·시간·좌표 표준화
궤도자료가 없으면 고도각 보정 등은 `not_computed`로 남기고 가능한 분석만 진행한다. GLONASS FDMA 채널번호는 헤더 → 로컬 항법자료 → IGS MGEX **시간유효** metadata 순으로 해결하고, **현재 시점 PRN 정적 룩업은 금지**한다. 우주기상 참조자료(Kp·Dst·GIM)를 모으되 Kp는 3시간, Dst는 1시간 해상도라 30초 사건과 직접 비교할 수 없음을 기록한다. 관측소 좌표의 기준계(ITRF/국가기준계)를 확인한다.

#### 단계 4 — 특징 추출 (핵심)
- **4.1 관측가용성·tracking**: 위성 수, 결측률, 소실·재획득, gap, LLI bit 0/1 분리, 이중주파수 조합 기반 cycle slip 후보
- **4.2 신호강도**: `Sxx`가 dB-Hz로 확인될 때만 사용. `S1C`와 `S1W`는 같은 S family 안에서만 비교하고, `C1C`(의사거리)와 섞지 않는다. RINEX 2의 `S1`을 임의로 `S1C`로 매핑하지 말고 `legacy_ambiguous`로 격리한다.
- **4.3 코드·반송파·Doppler·위치**: code-minus-carrier, ionosphere-free/geometry-free 조합, 잔차, SPP 위치·clock bias
- **4.5 대역·위성군 차분**: 대역별 Tracking Ratio(L1만 죽고 L2/L5는 살아있는가 vs 전 대역 동시 저하), 대역 간 SNR 하락 격차, CDMA(GPS) vs FDMA(GLONASS) 차이, **ROTI**(전리층 변동 지표)

ROTI는 아무 값이나 쓰지 않는다. 연속 arc에서 유효 epoch ≥ 8, ROT 차분 ≥ 7, window coverage ≥ 0.80, LLI·cycle slip 없음을 모두 만족해야 유효값이며, 대표값은 단일 slip에 취약한 `max`가 아니라 `median`·`Q90`·유효비율을 쓴다.

#### 단계 5 — 정상 기준선
"전체기간 평균 하나"로 만들면 안 된다. **관측소 × metadata regime(수신기·안테나·펌웨어) × 위성군 × 정확 관측코드 × 실제 주파수 × 고도각 구간 × 시간대·계절**로 나눈다.

```
robust_z = (x - median) / max(1.4826 × MAD, empirical_scale_floor)
```

MAD가 0일 때 임의의 작은 값을 넣어 큰 z를 만들지 말고, 정해진 fallback 순서(인접 고도각 bin → 동일 band → 유사 장비 관측소 → 경험적 floor → baseline unavailable)를 따르고 fallback 사용률을 보고한다. **미래 데이터로 과거 기준선을 학습하는 누수를 금지**한다.

#### 단계 6 — 다중 검출기 이상탐지
독립 특징군 5개를 쓴다: ① signal-strength ② tracking ③ measurement-consistency ④ solution ⑤ availability.
**기본 후보 생성 규칙은 "같은 시간창에서 최소 두 개의 독립 특징군이 이상"**이다. 대역차분·CDMA/FDMA 지표는 기존 family 내부의 세부 피처로 쓰고 family 수를 부풀리지 않는다. ROTI는 검출기가 아니라 반증 단계의 대조 지표다. 다중검정 문제를 고려해 FDR 또는 경험적 오경보율을 보고한다.

#### 단계 7 — 다중 관측소 시공간 동조성
단순히 "동시 이상 관측소 수"를 세는 데서 멈추지 않는다.

- **공간 자기상관**: Moran's I 또는 Geary's C + 순열검정 p-value. 가중행렬은 k-NN+최대거리, 거리밴드, 1/d, 1/d², adaptive kernel, Delaunay 중 **최소 3개 대안을 비교**한다. 80 km는 표준이 아니라 50/80/120 km 민감도 후보일 뿐이다.
- **거리–동조성**: 관측소 쌍 상관과 거리, semivariogram을 **기술통계로만** 보고. 지형·차폐를 자유공간 감쇠로 바꾸지 않는다.
- 세 관점으로 분해: 단일 관측소×다수 위성(→수신기/현장), 다수 관측소×단일 위성(→위성/궤도제품), 인접 다수 관측소×다수 위성(→지역 RF 가능성 상승), 전국 동시 공백(→수집·배포 장애 우선)

**전파원 위치를 추정했다고 표현하지 않는다.** 지도에는 `이상 관측망 범위`만 표시한다.

#### 단계 8 — 블라인드 탐지와 외부검증 분리
- **트랙 A(블라인드)**: 공식 사건일을 보지 않고 기준선·후보를 확정하고 **동결(freeze)** — 생성시각·코드 버전·설정 해시 기록
- **트랙 B(공식 사건 replay)**: 동결 후에만 공식 사건표(`event_id, source_agency, source_url, start/end_utc, area, ...`)와 대조. 언론기사는 탐색 보조일 뿐 최종 근거는 1차 출처 원문.
- **트랙 C(matched control)**: 사건일과 비슷한 조건(요일·시간대·계절, **유사 지자기 활동 수준 포함**)의 비사건일과 비교

공식 사건과 시간이 겹친다는 이유만으로 같은 원인이라고 확정하지 않는다. 공식 사건이 관측망 밖이거나 시공간이 모호하면 "검출 실패"가 아니라 **평가불가**로 처리한다.

#### 단계 9 — 반증 엔진과 분류
상위 후보는 전부 다음 대안설명을 거친다.

1. 수신기·안테나·현장 (장비 변경, 리셋, 다중경로, 같은 sidereal time 반복, 저고도 편중)
2. 위성·항법제품 (단일 위성 광역 이상, ephemeris age, SP3/CLK 공백)
3. 전리층·우주기상 (ROTI, GIM, Kp/Dst, 광역성, 주파수 의존성)
4. 기상 (강수·적설·착빙)
5. 데이터 파이프라인 (전국 동시 gap, 파일 경계, 시간변환 오류가 만든 가짜 동시성)

반증 상태: `hard_refuted` / `softly_explained` / `not_refuted` / `untestable` / `conflicting_evidence`.
**`untestable`은 긍정 증거가 아니다.** 후보가 단계마다 몇 개씩 줄어드는지 funnel로 기록한다.

#### 단계 10~11 — 확대와 시험
파일럿 → 확대 → 전체로 가되 모든 표·그림에 `pilot / expanded / full` 범위를 표기한다. 시험에는 압축형식, 윤년·DOY·leap second, LLI bit, GLONASS FDMA, **BDS B1I(1561.098 MHz) ≠ B1C/L1(1575.42 MHz) 분리**, L2C와 L2W 분리, 합성 사건 탐지, 정상 자료 오경보, 결정적 재실행, 중단 후 resume, 실제 파일 수동 검산이 포함된다.

### 6.2 병렬 실행 방법 (V7의 39~41절)

#### 병렬화의 3가지 축
1. **데이터 병렬** — 같은 일을 다른 자료에 (station×day 파티션). 처리량의 대부분이 여기서 나온다.
2. **역할 병렬** — 다른 일을 동시에 (특징추출 중에 외부자료 다운로드·그림 생성)
3. **구현 병렬** — 코드 작성 분담 (모듈 경계로 나눔)

#### 단계별 작업 단위

| 단계 | shard key | 역할 | 병렬도 |
|---|---|---|---|
| 인벤토리 | `file_id` 묶음 | W_INV | 높음(디스크 IO가 병목) |
| 품질 | `station×day` | W_QC | 높음 |
| 외부자료 | 날짜/product | W_EXT | 낮음(2~4, single-flight) |
| 특징·ROTI | `station×day`(+halo) | W_FEAT | 최고(CPU 바운드) |
| 기준선 | baseline group_key | W_BASE | 중간(배리어 뒤) |
| 탐지 | `station×day` | W_DET | 최고 |
| 망 동조성 | 시간블록×전 관측소 | W_NET | 중간(경계 재병합 필요) |
| 반증·그림 | `candidate_id` | W_FALS/W_FIG | 높음 |
| 보고서 | — | W_REP | **항상 1** |

#### 반드시 단일 워커로 해야 하는 것
기준선·임계값 확정, blind freeze, NetworkEvent 병합·clustering, 공간 가중행렬 선택과 다중검정 보정 범위, claim registry·보고서 수치 확정.

#### 병렬화의 두 가지 함정 (초보자가 반드시 걸림)

**① 경계(halo) 문제** — 자료를 일자 단위로 나누면 자정을 걸친 현상이 잘린다.
- 창 특징: 앞뒤로 창 최대길이 이상 **읽기 패딩**을 두되 **쓰기는 자기 구간만**
- ROTI arc: 자정 경계 arc는 앞뒤 30분 포함해 연속성 판정
- 사건: 경계에 닿으면 `boundary_open=true`로 표시하고 이웃 파티션 완료 후 **단일 reduce에서 병합**

**② 분산 집계 문제** — 파티션별로 구한 값을 합치는 방식이 통계량마다 다르다.
- 합산 가능: count, sum, sum of squares, min/max, 고정 bin 히스토그램
- **불가능: median, MAD, 분위수** ← 기준선이 바로 이걸 쓴다. 파티션별 median을 평균내면 틀린다.
  → 해결: 2-pass(정확·느림) 또는 t-digest 같은 병합 가능한 스케치(빠름·근사, 오차 보고 필수)

#### 작업 큐와 워커
pull 모델. orchestrator가 task를 만들고 워커가 자기 역할의 task를 가져간다.
- `task_id = hash(stage, shard_key, config_hash, code_hash, schema_version)` — 재실행해도 같은 ID
- 상태: `pending → leasable → leased → running → done | failed | poison`
- 리스(임대)와 heartbeat로 단일 writer 보장, 워커가 죽으면 만료 후 재할당
- 실패는 재시도 후 `poison`으로 격리하고 **전체 실행을 멈추지 않되 격리 목록을 반드시 보고**

#### 실행 명령 예시 (40.1절)

```powershell
python -m rinex_interference.cli doctor  --config config/analysis.yaml
python -m rinex_interference.cli plan    --config config/analysis.yaml --scale r3 --shards 16

python -m rinex_interference.cli worker --role W_INV  --workers 6      # IO 바운드
python -m rinex_interference.cli worker --role W_QC   --workers 6
python -m rinex_interference.cli worker --role W_EXT  --workers 2      # 동시에 진행 가능
python -m rinex_interference.cli barrier declare --name b1_inventory_quality_complete

python -m rinex_interference.cli worker --role W_FEAT --workers 8      # CPU 바운드
python -m rinex_interference.cli worker --role W_BASE --workers 4
python -m rinex_interference.cli barrier declare --name b2_baseline_frozen --evidence <HASH>

python -m rinex_interference.cli worker --role W_DET  --workers 8
python -m rinex_interference.cli worker --role W_NET  --workers 2
python -m rinex_interference.cli reduce --stage network_events         # 경계 재병합

python -m rinex_interference.cli freeze-blind
python -m rinex_interference.cli barrier declare --name b3_blind_freeze_before_official
python -m rinex_interference.cli worker --role W_VAL --workers 1       # 별도 프로세스
```

#### 순서 규칙
R1·R2는 **워커 1개 직렬**로 정확성을 확보하고, R3에서 큐·배리어·샤딩을 도입해 **불변성 시험**(`--shards 1/4/16`, `--workers 1/N`의 결과 해시가 같은가)을 통과한 뒤에만 워커를 늘린다. **워커 수를 늘려 결과가 달라지면 성능 문제가 아니라 정확성 결함이다.**

#### 코드 작성을 여러 명이 나눌 때 (40.2절)
1. 인터페이스 먼저 동결(스키마·설정·큐 스키마·ID 규칙) — 이게 끝나기 전엔 병렬 구현 시작 금지
2. 골든 픽스처(작은 실제 파일 + 기대 출력) 먼저 만들기
3. 모듈 파일 단위로 소유권 분배 (같은 파일 동시 수정 금지)
4. 병합은 하위 의존(파서·시간·기하)부터 상위(평가·보고)로

### 6.3 품질보증 장치

| 장치 | 내용 |
|---|---|
| Claim Registry | 보고서의 모든 핵심 숫자(파일 수, 기간, 후보 수, 처리량 포함)를 claim ID로 등록하고 산출물·계산식으로 역추적. 재실행 결과가 다르면 **삭제하지 말고 supersede** |
| Threshold Traceability | 모든 임계값의 출처(이론/표준/문헌후보/수신기문서/데이터교정)와 민감도 범위, 최종평가 전 선택 여부 기록 |
| Source Register | 인용한 모든 문서의 버전·접근일·적용 한계 |
| placeholder 금지 | `TODO`, `NotImplementedError`, 빈 함수, mock 결과, 하드코딩된 그럴듯한 수치 스캔 |
| 결정성 | 같은 입력·설정·코드 → 같은 결과. worker 수·chunk 크기·파일 순서가 ID를 바꾸면 안 됨 |
| 원자적 쓰기·재개 | 부분 `.tmp`는 성공이 아님. 입력·설정·코드·스키마 해시가 모두 같을 때만 skip |
| 즉시 중단조건 | 원시자료 쓰기 시도, 디스크 안전마진 미달, 시간변환 미검증, parser 손실, 스키마 drift, **공식 사건 누출 발견** 등 |

### 6.4 보고와 마무리

최종 보고는 장황한 과정이 아니라 정해진 항목만 간결히: 실제 분석 기간·관측소·파일 수 / 성공·제외·실패 수 / 후보 수와 증거등급 분포 / 공식 사건 중첩 수 / 가장 강한 후보 5건 / **확정할 수 없는 것과 그 이유** / 산출물 경로 / 전체 실행 완료 여부와 남은 작업 / 병렬 실행 구성과 재개 명령.

**경로에 접근 못 했거나 실제 분석을 끝내지 못했으면 "분석 완료"라고 말하지 않는다.**

---

## 7. 자주 하는 오해 12가지

| # | 오해 | 실제 |
|---|---|---|
| 1 | SNR이 떨어졌으니 재밍이다 | 수신기 장애·안테나 변경·다중경로·기상·저장 장애를 먼저 배제해야 한다 |
| 2 | LLI 비트가 올랐으니 교란이다 | LLI bit 0은 loss of lock 가능성일 뿐. 단독으로 확정 근거가 못 된다 |
| 3 | `Sxx`와 SSI(1~9)는 같은 것 | 다르다. 헤더의 `SIGNAL STRENGTH UNIT`을 확인해야 하고, SSI를 dB-Hz 연속값처럼 쓰면 안 된다 |
| 4 | RINEX 2의 `S1`은 `S1C`다 | 유일하게 복원되지 않는다. 근거 없으면 `legacy_ambiguous`로 격리 |
| 5 | BDS B1I도 L1 대역 | B1I는 1561.098 MHz, L1/B1C는 1575.42 MHz. 별칭 금지 |
| 6 | L2가 죽었으니 L2 표적 간섭 | L2W(semi-codeless)는 원래 저고도·저SNR에서 취약하다. 추적방식 취약성을 먼저 검토 |
| 7 | 이상이 안 보였으니 간섭이 없었다 | 수신기 내부 완화기능이 약한 간섭을 가릴 수 있다. "관측되지 않음"일 뿐 |
| 8 | 여러 관측소 이상 강도로 송신원 위치를 추정할 수 있다 | 금지. footprint는 관측 범위이지 위치가 아니며 귀속은 더더욱 불가 |
| 9 | Moran's I가 유의하니 간섭원이 있다 | 공간군집의 증거일 뿐 송신원 존재·위치의 증거가 아니다 |
| 10 | NOTAM에 있으니 확정 사건이다 | NOTAM·항행경보는 예방적 advisory일 수 있다. 단독으로 E4 불가 |
| 11 | 지자기 폭풍 기간이니 자연현상으로 제외 | 자동 제외 금지. 반증을 강화하고 `conflicting_evidence`로 남긴다 |
| 12 | 이상탐지 모델 점수가 높으니 사건이다 | 모델 점수는 원인 규명이 아니다. 관측 근거·반증·대안설명이 있어야 한다 |

---

## 8. 용어 사전

| 용어 | 설명 |
|---|---|
| **CORS** | 상시관측소. 위치가 고정·기지인 GNSS 기준국 |
| **RINEX** | GNSS 관측자료 표준 텍스트 형식. 버전 2/3/4가 혼재하며 관측코드 표기가 다르다 |
| **epoch** | 한 시각의 관측 묶음. 여기서는 30초 간격 |
| **observation code** | 관측 종류 코드. RINEX 3/4는 3자리(예: `C1C`=의사거리, `S1C`=신호강도, `L1C`=반송파, `D1C`=Doppler) |
| **C/N0, SNR** | 신호 대 잡음비. 간섭 시 떨어지는 대표 지표 |
| **LLI** | Loss of Lock Indicator. bit 0 = 위상추적 끊김 가능성, bit 1 = half-cycle 모호성 |
| **cycle slip** | 반송파 위상 추적이 끊겨 정수 모호도가 튀는 현상 |
| **elevation angle** | 위성 고도각. 낮을수록 신호가 약하고 다중경로가 심해 반드시 보정해야 함 |
| **multipath** | 반사파 때문에 생기는 오차. 같은 방위·고도에서 반복되는 특징이 있다 |
| **geometry-free / ionosphere-free** | 두 주파수를 조합해 기하항 또는 전리층항을 제거한 관측량 |
| **ROTI** | Rate Of TEC Index. 전리층 총전자량 변화율의 5분 표준편차. 전리층 교란 지표이며 진폭 scintillation(S4)의 직접 측정은 아님 |
| **TEC / GIM / IONEX** | 총전자량 / 전지구 전리층 지도 / 그 파일 형식. 광역·저해상도 배경자료 |
| **Kp / Dst** | 지자기 활동 지수(3시간) / 폭풍 강도 지수(1시간) |
| **SP3 / CLK / BRDC** | 정밀궤도 / 정밀시계 / 방송궤도력 |
| **Hatanaka** | RINEX 관측파일 전용 압축(`.crx`, `.d`) |
| **CDMA / FDMA** | 위성 구분 방식. GPS 등은 CDMA(같은 주파수), GLONASS는 FDMA(위성마다 주파수 다름) → 채널번호 필요 |
| **MGEX** | IGS의 다중 GNSS 실험 프로젝트. 시간유효 메타데이터 제공 |
| **metadata regime** | 수신기·펌웨어·안테나·좌표·관측코드가 안정적인 기간. 기준선을 나누는 단위 |
| **robust z / MAD** | 중앙값·중앙절대편차 기반 강건 표준화. 이상치에 덜 흔들림 |
| **change-point detection** | 시계열에서 통계적 성질이 바뀌는 지점 탐지 |
| **Moran's I / Geary's C** | 공간 자기상관 지표. 이상값이 공간적으로 뭉쳐 있는지 |
| **semivariogram** | 거리에 따른 값 차이 구조를 보는 지리통계 도구 |
| **block bootstrap** | 시계열·공간 상관을 고려해 블록 단위로 재표본해 신뢰구간을 얻는 방법 |
| **FDR / Benjamini-Hochberg** | 다중검정에서 위발견율을 통제하는 보정 |
| **matched control** | 사건일과 조건이 유사한 비사건일. 비교 기준 |
| **leakage(누출)** | 평가에 쓸 정보가 학습·임계값 선택에 새어 들어가는 것. 여기서는 특히 공식 사건정보 |
| **blind freeze** | 공식 사건을 보기 전에 블라인드 결과를 동결·해시하는 절차 |
| **evidence grade** | 증거등급 E0~E5 |
| **falsification** | 반증. 대안설명을 적극적으로 검토해 후보를 떨어뜨리는 과정 |
| **provenance** | 산출물이 어떤 파일·설정·코드·워커에서 나왔는지 추적 정보 |
| **halo / padding** | 파티션 경계 계산을 위해 앞뒤로 더 읽는 여유 구간 |
| **t-digest** | 병합 가능한 분위수 근사 자료구조. 분산 환경에서 median 계산에 사용 |
| **barrier** | 앞 단계가 완전히 끝나기 전에는 다음 단계를 시작하지 못하게 하는 동기화 지점 |
| **lease / heartbeat** | 작업 점유권과 생존 신호. 워커가 죽으면 만료 후 회수 |
| **YTD** | Year To Date. 완전하지 않은 연도 표기 |

---

## 9. 어디를 보면 되는가 — 질문별 본문 색인

| 궁금한 것 | 원문 위치 |
|---|---|
| 이 자료로 뭘 주장하면 안 되는가 | "가장 중요한 과학적 제한", 31.4절 금지 표현 |
| 원시자료를 건드려도 되는가 | "작업 및 안전 원칙" 1~2항 |
| 폴더 구조 | "프로젝트 구조", 13절 |
| 모든 설정값 | 14절 (`analysis.yaml` 전체 예시) |
| 파일 인벤토리 스키마 | 16.1절 |
| 기준선을 어떻게 나누는가 | 단계 5, 19절 |
| 사건 생성·병합 규칙 | 20절 |
| 반증에서 무엇을 검토하는가 | 21절 |
| 블라인드 A/B/C 트랙 | 22절, 워커 격리는 22.6절 |
| 증거등급 부여 조건 | 9단계, 23절 |
| 통계·평가 규칙 | 24절 |
| R1~R5 확대 절차 | 25절 |
| 메모리·디스크·중단조건 | 26절 |
| 재개·결정성 | 27절 |
| 시험 목록 | 28절 (병렬 시험은 28.10) |
| CLI 명령 | 29절 |
| 후보 Evidence Bundle 형식 | 30절 |
| 그림 규칙·금지 표현 | 31절 |
| claim·임계값·출처 관리 | 32절 |
| 필수 연구문서 | 33절 |
| 게이트 승인표 | 34절 |
| 1초 RINEX·NMEA 후속검증 | 35절 |
| 최종 체크리스트 | 36절 |
| 최종 보고 형식 | 37절 |
| 논문·학위논문 지원 | 38절 |
| **병렬 실행 설계** | **39절** |
| **역할별 실행 런북** | **40절** |
| **병렬 검증·성능** | **41절** |

---

## 10. 처음 시작하는 사람을 위한 5단계

1. **원문의 "가장 중요한 과학적 제한"과 39.2절 표만 먼저 읽는다.** 이 둘이 문서의 뼈대다.
2. 원시자료 폴더에 읽기 전용으로 접근되는지, 결과 폴더를 만들 수 있는지, 디스크 여유가 있는지 확인한다.
3. 워커 1개로 R1(파일 1개)을 끝까지 돌려본다. 헤더·시간계·관측코드가 예상과 맞는지가 전부다.
4. R2(하루치 end-to-end) → R3(3~10 관측소)까지 간 다음, 여기서 처음으로 병렬(큐·배리어·샤딩)을 도입한다.
5. 후보가 나오기 시작하면 **탐지보다 반증에 시간을 더 쓴다.** 남는 후보가 적은 것이 정상이다.

> **문서 전체를 관통하는 원칙 한 줄**
> "30초 CORS RINEX는 강력한 관측망 증거를 줄 수 있지만, RF 원인을 단독으로 확정하는 센서는 아니다."
