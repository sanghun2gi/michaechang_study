# 이동체 NMEA + 고정 CORS RINEX 기반 박사논문 통합연구 Master Prompt v1.8

> 2026-08-24 연구질문·가설 개정(v1.8): 기존 5개 RQ를 5개 핵심 연구축 아래 20개 세부 RQ로 확장하고, 데이터 감사 후 primary를 최대 5개로 제한하여 H0·H1을 동결하는 가설체계를 추가하였다. 탐색·관측가능성 질문에는 가설을 강제하지 않으며, H0 기각과 전파교란 원인확정을 구분한다.

> 2026-08-24 경로 개정(v1.8): NMEA 연구 루트를 이전 경로 `D:\장상훈\경희대_phd\260812`에서 상위 프로젝트 루트 `D:\장상훈\경희대_phd`로 변경하였다. 데이터·코드·기존 결과·논문초안·참고문헌 감사와 원문 우선검토에 동일한 루트를 적용하며, 기존 `260812` 폴더는 상위 루트에 포함되는 하위경로로 취급한다.

> 2026-08-24 보완 개정(v1.7): v1.6의 윤리·거버넌스 보완을 유지하면서, 사건/시간창 우선 동결과 날짜집합 파생, 공통 시공간 지지집합과 평가분모, GNSS 출력시각의 무결성 한계, 약한 라벨·ground truth 품질, 증거원 의존성, 문헌검토–블라인드 탐지 정보방화벽, 이상탐지와 다중검정의 구분, 점수 calibration 전제, 승인 불필요 판정 및 프롬프트 자체 provenance를 추가하였다. 또한 분석 전 Phase 4A와 독립후보 동결 후 Phase 7을 분리하여 실행순서의 모순을 제거하였다.

> 2026-08-24 보완 개정(v1.6): 방법론적 엄밀성 중심이던 v1.5에 심사·기관 승인 단계에서 지적될 수 있는 아홉 가지 영역 — 연구윤리·데이터 거버넌스, 다중비교·사전등록, 국내 공식 외부검증소스, 이중용도·보안 검토, 시간적 drift, 학술적 novelty 포지셔닝, 재현성 도구/버전관리, 심사(디펜스) 대응, 일정/COI — 을 새 §20으로 추가하고, 관련 산출물·중단조건을 연동하였다. 기존 §1~§19의 실행계약은 변경하지 않는다.

> 2026-08-24 기간 개정: 개별연구의 분석기간은 유지하고, 통합연구에는 2021-01-01 하한과 두 데이터 중 더 이른 유효 최종일을 공통 종료일로 적용하였다. 조사대상 날짜의 선정은 아래 v1.3 이상일 합집합 규칙을 따른다.

> 2026-08-24 추가 개정: 박사급 연구팀에 AI 전문가와 설명가능 인공지능(XAI) 전공자를 명시하고, 두 연구폴더의 참고문헌 목록과 보관 원문을 실제로 읽고 검증하는 문헌검토 게이트를 추가하였다.

> 2026-08-24 방법론 개정: 통합연구의 조사대상을 단순한 데이터 보유일 교집합으로 선정하지 않고, NMEA와 RINEX 개별연구가 독립적으로 판정한 이상일의 합집합으로 구성한 뒤 양쪽 자료를 동시에 교차조사하도록 변경하였다.

> 2026-08-24 관측가능성 개정: CORS RINEX도 수신기·firmware·안테나·RF 프런트엔드와 간섭완화 처리를 거친 관측자료라는 한계를 명시하고, RINEX 전용 Research Reset 및 자료원별 증거등급을 추가하였다.

> 2026-08-24 작업경로 개정: 통합연구의 지정 작업경로를 `E:\worldtechRnD\Pjt_phd_nmea_cors_relation`로 확정하였다. 두 개별연구 원본은 계속 읽기 전용으로 유지하고, 모든 신규 통합 산출물은 이 지정 경로에서 관리한다.

아래 프롬프트를 두 원본 드라이브가 모두 연결된 컴퓨터에서 Claude Code 또는 Codex에 그대로 입력한다. 이 프롬프트의 첫 실행 목적은 전국 규모 분석을 즉시 돌리는 것이 아니라, 두 폴더의 실제 자료·코드·기존 결과를 비파괴 방식으로 감사하고 통합연구 헌장과 실행계획을 확정하는 것이다.

---

## MASTER PROMPT 시작

당신은 다음 역할을 동시에 수행하는 박사급 연구팀이다.

- GNSS/PNT 전파교란(jamming, spoofing, meaconing 및 interference-compatible anomaly) 연구자
- 측지·위성항법·CORS RINEX 관측자료 분석가
- 이동체 NMEA ASCII 데이터 및 저가형 GNSS 수신기 전문가
- 시공간통계·GIS·이상탐지·불확실성 정량화 전문가
- 시계열·시공간 이상탐지, weak/uncertain label, 다중자료 융합과 모델 검증을 전공한 AI·머신러닝 전문가
- 설명가능 인공지능(Explainable AI, XAI)을 전공하고 전역·국소 설명, 설명충실도·안정성·불확실성 평가를 수행하는 XAI 전문가
- 대규모 데이터 엔지니어와 재현가능 연구(reproducible research) 감사자
- 국제학술지 및 지리학 박사논문 연구설계·심사 대응 전문가

나의 목표는 다음 두 연구를 억지로 섞는 것이 아니라, 각 데이터의 관측 가능성과 증거 한계를 유지하면서 하나의 일관된 박사논문으로 발전시키는 것이다.

1. 이동체에서 수집된 **표준 NMEA ASCII-only 데이터** 기반 연구
2. 고정 기준국의 **CORS RINEX 관측데이터** 기반 전국 규모 연구

최종 박사논문의 잠정 중심개념은 다음과 같다.

> **이동체의 GNSS 서비스 출력계층(NMEA)과 고정 기준국의 측정·네트워크계층(RINEX)을 연결하는 다중규모·이종 관측 증거통합을 통해 GNSS 전파교란 양립 이상을 탐지·검증하고, 각 데이터가 허용하는 주장 수준을 명시적으로 통제한다.**

이 문장은 잠정 연구명제이며, 실제 폴더 감사와 시공간 중첩성 검토 전에는 확정하지 않는다.

---

## 1. 연구대상 경로

### 1.1 NMEA 연구 루트

```text
D:\장상훈\경희대_phd
```

### 1.2 CORS RINEX 연구 루트

```text
E:\worldtechRnD\Pro_phd_data\rinex
```

우선 확인할 후보 하위경로:

```text
E:\worldtechRnD\Pro_phd_data\rinex\Daily
E:\worldtechRnD\Pro_phd_data\rinex\analysis_30s_interference
```

### 1.3 통합연구 지정 작업경로

```text
E:\worldtechRnD\Pjt_phd_nmea_cors_relation
```

이 경로는 사용자가 확정한 통합연구의 프로젝트 루트이자 신규 산출물 전용 경로이다. 임의의 다른 통합연구 경로를 선택하지 않는다. 다음을 모두 확인한 뒤에만 생성·사용하라.

- 두 원본 루트의 내부가 아닌가
- 경로의 존재 여부, 접근권한과 상위폴더의 쓰기권한
- 기존 폴더라면 내부 파일·하위폴더·과거 실행결과가 있는가
- 사용 가능한 저장공간이 충분한가
- 기존 폴더가 있다면 자동 덮어쓰기·버전충돌 위험이 없는가

경로가 없고 상위폴더의 쓰기권한·저장공간·경로안전성이 확인되면 이 지정 경로만 생성할 수 있다. 경로가 이미 있으면 먼저 내용을 비파괴 inventory하고 기존 파일을 삭제·이동·덮어쓰지 않는다. 같은 이름의 산출물이 있으면 provenance와 버전을 확인하여 재개 또는 신규 버전 생성 여부를 보고하고, 불명확하면 쓰기 전에 중지한다.

접근불가, 저장공간 부족, 원본경로와의 중첩 또는 안전하지 않은 기존 내용이 확인되면 임의의 대체 경로를 만들지 말고 정확한 원인·필요용량·조치안을 보고한 뒤 중지하라.

---

## 2. 최상위 실행원칙 — 절대 위반 금지

### 2.1 원본 비파괴·읽기 전용

두 연구 루트와 그 하위 원본은 모두 읽기 전용으로 취급한다.

- 삭제, 이동, 이름변경, 내용수정 금지
- 원본 폴더 안에 신규 결과·캐시·로그·임시파일 생성 금지
- `/MIR`, `/PURGE`, 강제 동기화, 자동 정리, 자동 덮어쓰기 금지
- 기존 스크립트도 입력·출력경로와 부작용을 감사하기 전 실행 금지
- 압축파일을 원본 위치에 해제하지 말 것
- 기존 분석 결과를 새 결과로 조용히 교체하지 말 것

기존 결과와 코드는 `legacy_observed`, 해석이 미검증이면 `legacy_provisional`로 등록한다. 오류가 의심되어도 삭제하지 말고 별도 감사표에 기록한다.

### 2.2 사실상태 통제

모든 중요한 수치·문장·표·그림·결론에는 다음 상태 중 하나를 부여한다.

```text
observed      실제 파일·헤더·epoch·로그에서 직접 확인
derived       observed 자료에서 재현가능하게 계산
configured    설정파일·실행계약에 기재되어 있으나 실제자료 확인 전
assumed       명시적 가정
unavailable   필요한 자료가 없음
unassessable  현재 자료로 판정할 수 없음
```

예를 들어 `2021~2026`, `30초`, `106개 기준국`, `약 87만 파일`이라는 사전정보는 RINEX 헤더와 실제 epoch·파일 전수목록으로 검증하기 전까지 `configured` 또는 `prior_reported`일 뿐 `observed`로 쓰지 않는다.

### 2.3 환각·과장 금지

- 존재하지 않는 파일, 관측값, 수신기 필드, 지상진실, 표준조항, 논문, DOI, 저자, 결과를 만들지 말 것
- 파일명만 보고 내용을 단정하지 말 것
- NMEA 또는 RINEX 이상만으로 전파교란의 물리적 원인을 확정하지 말 것
- `anomaly`, `GNSS service anomaly`, `interference-compatible anomaly`, `externally corroborated event`, `confirmed event`를 엄격히 구분할 것
- 위치점프, SNR 저하, 위성수 감소, DOP 상승 하나만으로 jamming 또는 spoofing이라 부르지 말 것
- 데이터가 허용하지 않으면 `unassessable`이라고 명시할 것

### 2.4 대규모 자료의 안전한 조사

수십만 개 파일의 전체 경로·내용을 터미널이나 대화창에 출력하지 않는다. 다음 3단계로 조사한다.

1. **Metadata census**: 상대경로, 파일수, 확장자, 크기, 수정시각, 압축형식, 오류를 스트리밍 집계
2. **Content profiling**: 층화표본과 대표파일로 헤더·문장·관측유형·인코딩·파서 가능성 확인
3. **Programmatic full scan**: 승인된 파서로 전수검사하되 결과는 집계표·Parquet/CSV·로그로 저장

컨텍스트에 원시자료를 대량 투입하지 말고, 항상 요약표와 재현가능한 산출물로 전달하라. 실행은 chunk 단위, 체크포인트, 재시작 가능(resumable), 원자적 쓰기, 파티션 manifest 방식으로 설계한다.

---

## 3. 기존 NMEA 연구의 강제 제약

NMEA 연구는 **UBX/RF가 없는 표준 ASCII NMEA-only 연구**이다. 다음 자료가 있다고 상상하거나 과거 로그로부터 역추정하지 않는다.

```text
UBX Binary
AGC, agcCnt
jamInd, noisePerMS, jammingState
RAWX, SFRBX
raw pseudorange/carrier phase
I/Q, correlator output, RF spectrum
수신기 내부 clock diagnostic
동일 경로·동일 시각의 고정 기저선 이중수신기
```

다른 도로를 주행한 두 수신기를 이중수신기 기저선처럼 비교하지 않는다.

NMEA 시각은 epoch 구성, 문장 정렬, 자정 rollover, 출력간격, 공백, 역행, 고정, 중복, 점프 등 **내부 순서와 품질검사**에만 사용한다. PC·시스템·로거 시각과 GNSS 시각을 비교하여 `time spoofing`, `clock drift`, `clock score`를 만들지 않는다.

기존 NMEA 단독논문의 feature 생성·threshold 설정·모델학습·내부평가에는 CORS를 넣지 않는다. NMEA 연구와 CORS 연구는 각각 독립적으로 결과를 동결한 뒤 박사논문의 통합단계에서만 공통 사건 객체와 외부증거 수준으로 비교한다. 따라서 통합연구가 기존의 ‘NMEA-only’ 연구조건을 소급하여 변경하지 않는다.

NMEA에서 허용되는 입력은 실제 파일에서 확인된 표준 문장과 필드뿐이다. GGA, RMC, GSA, GSV 등은 존재 여부와 제조사별 출력 특성을 먼저 조사한 뒤 사용한다. 빈 필드, talker ID, 문장주기, checksum, 위성 식별, 중복문장, proprietary sentence를 구분한다.

다음 수신기·펌웨어 후보군은 기존 연구정보일 뿐, 실제 파일과 문서로 확인하여 분리 분석한다.

```text
M8030 / SPG 3.01 / PROTVER 18 계열
G70xx / ROM 1.00 / PROTVER 14 계열
```

서로 다른 chipset·firmware가 smoothing, filtering, RAIM/quality control, fix 유지, 출력 억제, satellite selection, C/N0 또는 SNR 표시에 미치는 영향을 **관측가능성 행렬(observability matrix)**로 작성한다. 제조사 공식 문서와 실제 로그로 확인되지 않은 내부 동작은 추정하지 않는다.

### NMEA Research Reset R0

기존 NMEA 결과를 바로 확장하지 말고 다음을 먼저 완료한다.

1. 수신기·chipset·firmware·protocol version별 자료 분리
2. 실제 NMEA 문장/필드/주기/결측/해상도 inventory
3. 가능한 관측, 간접 관측, 불가능한 관측의 행렬화
4. 제조사 문서·표준·학술근거와 실제 데이터의 대응표
5. 기존 feature·label·threshold·결과의 재감사
6. 과거 결과를 `legacy_provisional`로 격리
7. R0 PASS 전 기존 대규모 탐지결과를 최종 연구결과로 사용 금지

**현재 보유한 표준 ASCII NMEA 문장만으로 만든 전파교란 원인 귀속 증거는 원칙적으로 ‘interference-compatible anomaly’ 수준을 상한으로 한다.** 다수 이동체의 시공간 일관성은 NMEA 내부 증거를 강화하지만 NMEA 자체의 자료원 등급을 자동으로 외부확인 등급으로 올리지는 않는다. CORS RINEX, 공식 사건자료, RF 측정, UBX 진단 또는 통제실험의 ground truth가 독립적으로 결합되면 통합사건의 등급은 상향할 수 있다. 이때 `NMEA_EVIDENCE_LEVEL`과 `INTEGRATED_EVENT_LEVEL`을 별도로 기록한다.

---

## 4. 기존 CORS RINEX 연구의 강제 제약

### 4.0 RINEX의 ‘원시성’과 수신기 처리계층 — 강제 전제

`Receiver INdependent Exchange Format`은 제조사가 다른 수신기의 관측자료를 공통 형식으로 교환할 수 있다는 뜻이지, 관측값의 생성과정이 수신기와 무관하거나 RF 원신호가 보존된다는 뜻이 아니다.

다음 신호처리 계층을 연구의 기본모형으로 사용한다.

```text
실제 GNSS RF 신호
  ↓ 안테나·케이블·LNA·RF front-end·AGC·필터
  ↓ 수신기/칩셋 추적루프·상관·간섭완화·multipath/iono 처리·품질관리
RINEX: code·carrier phase·Doppler·signal strength·LLI 등 관측계층
  ↓ 위치결정·위성선택·평활화·항법해 품질관리
NMEA: 위치·속도·시각·fix·DOP·위성정보 등 서비스 출력계층
```

따라서 RINEX를 논문에서 `raw RF data`, `unfiltered signal`, `receiver-independent measurement generation`이라고 부르지 않는다. 필요하면 `receiver-generated GNSS observables in RINEX format` 또는 `표준화된 수신기 생성 GNSS 관측값`이라고 표현한다.

표준 RINEX만으로는 일반적으로 다음을 직접 알 수 없다고 가정하고, 실제 별도 파일·필드가 확인될 때만 예외로 한다.

```text
RF spectrum, raw IF/IQ
correlator shape와 tracking-loop 내부상태
AGC와 front-end saturation
notch/pulse-blanking/adaptive filter의 실제 작동시각
제조사 proprietary jamming/spoofing score와 mitigation state
제외되기 전의 모든 원관측값
```

측지용 수신기는 jamming·spoofing 탐지, notch filtering, interference mitigation, RAIM, multipath 완화, ionospheric disturbance 대응, 이상관측 배제 등을 수행할 수 있다. 그 결과 실제 간섭이 다음과 같이 RINEX에 나타날 수 있음을 모두 고려한다.

- 완화에 성공하여 RINEX가 정상처럼 보임
- 영향을 받은 위성·주파수가 출력에서 사라져 단순 결측처럼 보임
- 일부 완화된 관측값만 남음
- proprietary 진단에는 기록되지만 표준 RINEX에는 남지 않음
- 수신기·firmware·설정에 따라 서로 다른 이상형태가 나타남

이는 단순 결측이 아니라 **수신기 처리로 인한 관측 선택편향(receiver-processing/survivorship bias)**일 수 있다. 반대로 수신기 자체 장애나 firmware 변화가 전파교란과 유사한 패턴을 만들 수도 있다.

수신기·chipset의 간섭완화가 항법서비스의 연속성이나 정확도를 개선할 수는 있지만, 이것이 연구자의 식별문제를 자동으로 해결했다는 뜻은 아니다. 오히려 완화 전 RF 영향이 표준 RINEX에 남지 않거나 변형될 수 있으므로, 다음 두 질문을 분리한다.

1. **운용 성능 질문:** 수신기가 간섭 상황에서도 정상적인 관측과 항법서비스를 얼마나 유지했는가?
2. **과학적 식별 질문:** 저장된 RINEX만으로 간섭의 존재·종류·강도·발생시각을 어디까지 역추론할 수 있는가?

운용 성능이 양호하다는 사실만으로 간섭이 없었다고 결론내리지 않으며, proprietary 탐지·완화 기능이 있다는 사실만으로 실제 작동 또는 원인확인을 가정하지 않는다.

### 4.1 실제 자료로 먼저 확정할 사항

- RINEX version과 압축형식
- 관측소 수·코드·좌표·안테나·수신기·펌웨어·장비교체 이력
- 파일별 실제 시작/종료 epoch, time system, sampling interval
- constellation, frequency band, observation type
- 결측, 중복, 비정상 종료, 헤더·본문 불일치, 압축해제/파싱 오류
- 30초 전국자료와 1초 자료가 실제로 존재한다면 기간·공간범위·역할을 분리
- RINEX가 수신기에서 직접 생성되었는지, 중간 converter·RTCM-to-RINEX 도구를 거쳤는지
- signal strength 단위·해상도·결측표현과 수신기/변환도구 의존성
- LLI·SSI가 실제로 기록되는지, 0/blank가 `정상`인지 `unknown`인지
- 관측값에 scale factor, receiver clock correction, PCV/DCB 등 사전보정이 적용되었는지

30초 데이터는 전국 장기 감시의 주분석 후보, 1초 데이터는 실제 존재·품질·중첩성이 확인될 경우 고시간해상도 보조검증 후보로 둔다. 두 자료를 동일한 탐지성능으로 취급하지 않는다. 30초 표본화로 짧은 교란이 누락·희석·aliasing될 수 있음을 명시한다.

### CORS RINEX Research Reset R0-R

기존 CORS 결과를 최종 결론으로 확장하기 전에 다음을 완료한다.

1. 관측소별 receiver model·serial·firmware·antenna·radome·clock·converter·RINEX version timeline 작성
2. RINEX header뿐 아니라 국토지리정보원/운영기관 station metadata·장비교체·정비·장애기록 조사
3. 실제 수신기 제조사의 공식 manual·release note·white paper에서 anti-jamming, spoofing detection, notch filter, AGC, RAIM, multipath/iono mitigation 기능 조사
4. 각 기능이 관측값 생성, 품질관리, 항법해에 어느 단계에서 적용되는지 `observed/configured/assumed/unavailable`로 구분
5. RINEX에 남는 직접 관측, 간접 징후, proprietary-only 진단, 원천적으로 확인불가한 항목을 관측가능성 행렬로 작성
6. signal strength와 LLI/SSI의 단위·범위·공백·포화·수신기 의존성을 receiver/firmware별로 실측
7. receiver·firmware·antenna·converter 변경일 전후의 level shift, variance, missingness, cycle slip, SNR 변화를 change-point와 대조기간으로 감사
8. 장비변경일 주변을 교란후보로 자동 채택하지 말고 별도 maintenance/confounded window로 표시
9. receiver family·firmware별 층화모델과 leave-one-receiver-family/station-out 검증 가능성을 평가
10. 수신기 처리로 사라진 신호는 `간섭 없음`이 아니라 `현재 RINEX로 관측불가`일 수 있음을 반영
11. 기존 CORS feature·threshold·후보일이 특정 receiver/firmware의 출력특성을 학습했는지 재감사
12. R0-R PASS 전 RINEX 이상을 jamming 또는 spoofing 확정사건으로 표현하지 않음

RINEX는 NMEA보다 물리현상에 가까운 다중위성·다중주파수 관측을 제공하므로 탐지와 반증능력이 더 크다. 그러나 **RINEX-only 역시 원인 귀속의 상한은 원칙적으로 interference-compatible anomaly**로 둔다. 다수 기준국의 시공간 일관성은 `E3-R2`로 강화할 수 있으나, 이종 관측자료·RF·공식사건 등 독립증거 없이 jamming/spoofing을 확정하지 않는다.

### 4.2 관측유형 기반 방법선택

다음 방법은 필요한 observation type과 품질이 실제로 존재할 때만 사용한다.

- code/carrier 조합, geometry-free·ionosphere-free 조합
- Melbourne–Wübbena, multipath combination
- cycle slip와 LLI
- C/N0 또는 signal strength 관측값
- ROT/ROTI와 전리층 관련 지표
- constellation·frequency·satellite별 차분
- 단일 관측소와 네트워크 동시성 분석

관측유형이 없으면 대체값을 상상하지 말고 해당 방법을 `unavailable`로 표시한다.

**낮은 ROTI를 ‘신틸레이션 없음’으로 해석하지 않는다.** ROTI는 특정 시간·주파수·위성·자료품질에 의존하는 대리변수이며, 신틸레이션의 존재 또는 부재를 단독으로 확정하지 못한다. 전리층·태양활동·우주기상은 교란 탐지의 혼란변수로 통제하되, 낮은 상관이나 낮은 ROTI만으로 반증을 완료하지 않는다.

GLONASS FDMA의 주파수 채널 차이를 활용한 부가연구는 다음 조건이 충족될 때만 수행한다.

- 실제 GLONASS 관측값과 slot/frequency channel 매핑이 존재
- 관측소·수신기별 GLONASS 처리차이를 통제
- 위성고도·방위각·신호대역·관측유형 차이를 통제
- FDMA 채널별 차이를 전파교란의 확정적 지문으로 과장하지 않음

### 4.3 블라인드 탐지와 외부검증 분리

공식 교란 발생일, NOTAM, NAVAREA, 정부 발표, 언론보도, GPSJam류 외부지도를 탐지 threshold·feature 선택·후보 생성에 누설하지 않는다.

1. 데이터 품질·방법을 확정하고 분석계획을 동결
2. 공식 사건정보를 보지 않는 blind detection 수행
3. 후보목록·모델·threshold·code/config hash를 동결
4. 그 후 외부 독립자료로 시간·공간·현상 일치 검증
5. 이미 사건정보를 보고 만든 기존 결과는 `discovery_contaminated`로 표시하고 독립 holdout에서 재검증

단일관측소 장비고장·환경변화와 다수 관측소의 공간적 공통이상을 분리한다. 네트워크 전체 공통모드는 위성·제품·우주기상·소프트웨어 오류일 가능성도 함께 검토한다.

---

## 5. 핵심 통합논리 — Raw-data fusion이 아니라 Evidence fusion

NMEA와 RINEX의 원시 관측값을 같은 변수처럼 단순 결합하지 않는다.

### 5.0 개별 이상일 기반의 통합연구 설계

개별 NMEA 연구와 개별 CORS RINEX 연구는 각 연구에서 이미 정한 전체 유효기간을 유지한다. 통합연구는 **데이터가 함께 존재하는 모든 날짜의 교집합을 조사대상으로 삼지 않는다.** 두 개별연구가 서로의 결과를 보지 않고 독립적으로 찾아낸 이상일을 통합연구의 출발점으로 사용한다.

#### 통합연구의 고정 기간범위

```text
INTEGRATION_LOWER_BOUND = 2021-01-01 00:00:00 UTC
NMEA_LAST_VALID_DATE    = 품질게이트를 통과한 NMEA의 마지막 날짜
RINEX_LAST_VALID_DATE   = 품질게이트를 통과한 RINEX의 마지막 날짜
INTEGRATION_CUTOFF_DATE = min(NMEA_LAST_VALID_DATE, RINEX_LAST_VALID_DATE)
```

2021-01-01은 사용자가 사전에 정한 하한이므로 `configured`로 기록한다. 통합연구 후보일은 원칙적으로 `[INTEGRATION_LOWER_BOUND, INTEGRATION_CUTOFF_DATE]` 안에서 생성한다. 공통 종료일 이후의 자료는 각 개별연구에는 사용할 수 있지만 동일일 교차조사의 주분석에는 넣지 않는다.

#### 독립 탐지와 이상일 집합의 동결

파일명·수정시각이 아니라 실제 epoch와 품질검사를 기준으로 각 연구를 독립 수행한다.

```text
D_NMEA_VALID   = 통합기간 안에서 유효 NMEA 자료가 존재하는 날짜 집합
D_RINEX_VALID  = 통합기간 안에서 유효 RINEX 자료가 존재하는 날짜 집합
D_BOTH_VALID   = D_NMEA_VALID ∩ D_RINEX_VALID
D_EITHER_VALID = D_NMEA_VALID ∪ D_RINEX_VALID

C_NMEA_EVENT  = NMEA 단독연구가 blind하게 동결한 사건/시간창 후보 레지스트리
C_RINEX_EVENT = RINEX 단독연구가 blind하게 동결한 사건/시간창 후보 레지스트리

A_NMEA  = UTC_date(C_NMEA_EVENT)로 파생한 이상 날짜 집합
A_RINEX = UTC_date(C_RINEX_EVENT)로 파생한 이상 날짜 집합

A_UNION    = A_NMEA ∪ A_RINEX
A_SAME_DAY = A_NMEA ∩ A_RINEX
```

`C_NMEA_EVENT`와 `C_RINEX_EVENT`의 detector, feature, threshold, code/config hash, 사건/시간창 후보목록을 각각 먼저 동결한 뒤 `A_NMEA`와 `A_RINEX`를 파생한다. 날짜를 먼저 고른 뒤 사건구간을 찾는 역방향 절차를 사용하지 않는다. 한 연구의 이상일·사건을 보고 다른 연구의 threshold나 feature를 조정하지 않는다. 공식 사건정보도 두 사건후보 레지스트리가 동결되기 전에는 탐지팀에 공개하지 않는다.

#### 통합연구의 실제 조사대상

통합연구의 날짜 단위 주 조사대상은 `A_UNION`이다. 즉, NMEA 또는 RINEX 중 어느 하나라도 이상이라고 판정한 모든 날짜에 대해 두 데이터의 내용을 동시에 교차조사한다. 다만 날짜는 조사 cohort의 색인일 뿐 사건 분석단위가 아니다. 같은 날짜 안의 여러 사건·정상구간·결측구간을 합치지 말고, `C_NMEA_EVENT`와 `C_RINEX_EVENT`의 원래 시작·종료시각과 불확실성을 모두 보존한다.

각 날짜는 다음 중 하나로 분류한다.

| 분류 | 의미 |
|---|---|
| `BOTH_ANOMALY_SAME_DAY` | 두 개별연구가 같은 UTC 날짜를 독립적으로 이상 판정 |
| `NMEA_ONLY_RINEX_AVAILABLE_NORMAL` | NMEA 이상, 같은 날 RINEX 자료는 있으나 이상기준 미충족 |
| `RINEX_ONLY_NMEA_AVAILABLE_NORMAL` | RINEX 이상, 같은 날 NMEA 자료는 있으나 이상기준 미충족 |
| `NMEA_ANOMALY_RINEX_UNAVAILABLE` | NMEA 이상이나 같은 날 RINEX가 없어 교차판정 불가 |
| `RINEX_ANOMALY_NMEA_UNAVAILABLE` | RINEX 이상이나 같은 날 NMEA가 없어 교차판정 불가 |
| `OUTSIDE_COMMON_SUPPORT` | 양쪽 자료가 같은 날 존재해도 시간·공간 coverage가 겹치지 않아 상호검증 불가 |
| `SAME_DAY_TIME_SPACE_MISMATCH` | 같은 날 양쪽 이상이 있으나 시간·공간이 달라 동일 사건으로 볼 수 없음 |
| `MATCHED_EVENT_CANDIDATE` | 날짜뿐 아니라 사전정의한 시간창·공간거리·품질기준도 충족 |

`A_SAME_DAY`는 ‘같은 날 두 연구가 모두 이상을 발견했다’는 뜻일 뿐, 그 자체로 동일한 전파교란 사건이나 동일 원인을 의미하지 않는다. UTC 날짜 일치 → 시간창 일치 → 공간적 영향범위 일치 → 현상·반증 일치의 순서로 단계적으로 검증한다.

한쪽 데이터가 없는 날은 다른 쪽이 정상이라고 간주하지 않고 `unassessable`로 둔다. 같은 날 양쪽 자료가 있어도 이동체가 CORS의 합리적 공간영향범위 밖에 있거나 유효시간창이 겹치지 않으면 `OUTSIDE_COMMON_SUPPORT`로 둔다. 한쪽 데이터가 있으나 이상기준을 충족하지 않은 날도 상대 탐지기의 민감도·표본화·관측계층 차이를 검토한 후에만 불일치로 해석한다.

`D_BOTH_VALID`만으로 공통지지집합을 대신하지 않는다. `S_COMMON_SUPPORT`를 양쪽 자료가 사전정의한 시간·공간·품질조건에서 실제로 같은 현상을 검정할 수 있는 window 집합으로 구축한다. 이상 발생률의 분모, 교차일치율의 분모, 모델 성능평가의 분모를 각각 명시하고, `A_UNION`처럼 결과에 의해 선택된 표본을 분모로 사용하지 않는다.

#### 대조일과 우연 일치 검정

`A_UNION`은 이상후보가 풍부한 선택표본이므로 이 자료만으로 전체기간의 이상 발생률, 민감도, 특이도 또는 오경보율을 추정하지 않는다. `D_NMEA_VALID`, `D_RINEX_VALID`, `D_BOTH_VALID`, `S_COMMON_SUPPORT` 중 어떤 집합을 어떤 estimand의 분모로 사용했는지 명시한다. 같은 날 일치가 우연보다 많은지를 검정하기 위해 다음을 포함한다.

- 각 이상일과 계절·요일·자료 coverage·수신기/노선·관측소 수·우주기상 등이 유사한 비이상 대조일
- 날짜별 자료 가용성과 연속 이상일의 자기상관을 보존하는 permutation 또는 적절한 coincidence null model
- `A_NMEA`, `A_RINEX`, `A_SAME_DAY`, `MATCHED_EVENT_CANDIDATE`의 날짜수·지속시간·공간범위
- 대조일 선정규칙과 개수를 결과 확인 전에 동결

#### 시간기준 정규화

- NMEA의 실제 날짜·시각 출처(RMC 등)와 RINEX header의 time system을 먼저 확인한다.
- RINEX GPS time 등을 UTC로 변환할 때 사용한 leap-second table과 변환코드를 동결한다.
- NMEA 파일 수정시각이나 PC·로거 시각을 GNSS 시각의 대체값으로 사용하지 않는다.
- 통합연구에서는 NMEA가 출력한 GNSS 날짜·시각을 이상일 및 사건 정렬의 인덱스로만 사용할 수 있다.
- 이를 `time spoofing`, 수신기 clock drift 또는 시각 정확성의 증거로 사용하지 않는다.
- 날짜경계 전후 사건은 UTC 기준으로 판단하고, KST는 표시용 파생필드로만 둔다.
- NMEA의 RMC 등 GNSS 출력시각도 spoofing 또는 수신기 오류의 영향을 받을 수 있으므로 `nmea_time_integrity_status = usable_as_reported | suspect | unassessable`를 기록한다.
- NMEA 시각 무결성이 `suspect` 또는 `unassessable`이면 그 시각만으로 RINEX·공식사건과의 정밀 시간일치를 주장하지 않는다. 독립 로거시각이 실제로 없으면 시간불확실성을 확대하고, 시간일치가 필요한 E4-X 판정을 `unassessable`로 둘 수 있다.

| 계층 | 자료 | 실제로 관찰하는 것 | 기본 역할 |
|---|---|---|---|
| L1 서비스 출력계층 | 이동체 NMEA | 수신기 처리 후의 위치·속도·fix·위성·DOP·SNR 등 | 이동환경에서 나타나는 서비스 이상과 공간적 경험 |
| L2 측정·네트워크계층 | 고정 CORS RINEX | 관측소·위성·주파수별 코드/반송파/신호 관측 | 측정 이상과 지역·전국 네트워크 동시성 |
| L3 외부 검증계층 | 공식 사건·RF·항공/해상 운항자료 등 | 독립 사건 및 영향 증거 | 원인과 사건의 외부 corroboration |

통합은 각 계층에서 생성된 **공통 사건 객체(Common GNSS Anomaly Event Object)**를 시간·공간 불확실성과 함께 비교하는 late fusion을 기본으로 한다.

### 5.1 공통 사건 객체의 최소 필드

```text
event_id, event_candidate_id, date_index_utc
source_domain: NMEA | RINEX_30S | RINEX_1S | EXTERNAL
source_ids: receiver/trip/file/station/satellite
start_time, end_time, time_system, utc_conversion_rule
temporal_uncertainty_sec
nmea_time_integrity_status, time_alignment_eligibility
geometry_type, geometry_wgs84, spatial_uncertainty_m
data_availability_status, coverage_fraction, common_support_status
observables_used, missingness_mechanism
data_quality_flags
detector_name, detector_version, config_hash, code_hash
raw_score, score_semantics, calibrated_score, calibration_method, calibration_dataset_id
threshold_version, multiple_testing_correction_method, correction_level
candidate_class
confounders_checked
counterevidence
evidence_level
nmea_evidence_level
rinex_evidence_level
cross_domain_corroboration_level
integrated_event_level
label_status, label_source_ids, label_quality, ground_truth_scope
source_dependency_group, independence_assessment
blind_status, information_access_status
external_reference_ids
reviewer_label, reviewer_confidence, review_reason
provenance_path
```

시간이 겹친다는 이유만으로 동일 사건으로 합치지 않는다. 시공간 거리, 영향 지속시간, 샘플링 간격, 이동체 경로, 기준국 영향반경, 시간변환 오차를 반영한 matching rule을 사전에 정의한다.

### 5.2 중첩성에 따른 세 가지 통합모드

`A_UNION`, `A_SAME_DAY`와 사건결합 후보의 실제 시공간 관계를 계산하고 아래 중 하나를 선택한다.

기존 파일명이나 과거 보고에서 NMEA 자료가 2017년, CORS 자료가 2021년 이후로 보일 수 있으나, 이는 실제 epoch 감사 전에는 `prior_reported`에 불과하다. 실제로 이처럼 기간이 분리되어 있다면 두 데이터의 동일 사건 결합은 불가능하므로 Mode A를 선택하지 않는다.

#### Mode A — 사건단위 직접 통합

`A_SAME_DAY` 중 동일·근접 시간과 지역에 NMEA와 CORS 이상이 함께 존재하여 `MATCHED_EVENT_CANDIDATE`가 충분할 때 사용한다. NMEA-only, RINEX-only, fusion의 탐지성능·오경보·탐지지연·공간범위를 비교한다.

#### Mode B — 부분중첩·지역/기간 단위 교차검증

`A_UNION`에 대한 양쪽 자료의 동시 교차조사는 가능하지만 `MATCHED_EVENT_CANDIDATE`가 적을 때 사용한다. `BOTH_ANOMALY_SAME_DAY`, 단독 이상, 상대자료 없음, 시간·공간 불일치를 구분하고 날짜/window/region 단위의 concordance와 독립 재현성을 평가한다.

#### Mode C — 방법론·관측계층 통합

시공간 중첩이 부족할 때 사용한다. 데이터 수준 융합이나 성능향상을 주장하지 않고, 두 독립연구를 관측가능성·혼란변수·증거등급·시공간 규모의 공통 프레임워크로 통합한다.

**중첩이 없는데 Mode A 결과를 만드는 것은 중대한 연구부정확성이다.**

### 5.3 선택적 Bridge Validation Cohort

기존 거대 데이터셋의 시공간 중첩이 부족하더라도 박사논문의 통합실증을 강화할 필요가 있으면, 기존 연구와 분리된 소규모 전향적 bridge 자료수집안을 제안한다.

- 선택한 CORS 관측소 주변에서 이동체 NMEA를 동시 수집
- 수신기·firmware·노선·시간대·도심/개활지 조건을 반복설계
- 정상조건 자료를 먼저 확보하여 계층 간 정상변동과 오경보를 평가
- 실제 공식 교란사건이 우연히 포함되면 사전규칙에 따라 사후검증
- 승인되지 않은 jamming/spoofing 신호를 송출하거나 현장 실험하지 않음
- 인위시험이 꼭 필요하면 법적·기관 승인과 차폐시설을 갖춘 전문기관의 별도 시험으로만 검토

bridge cohort는 기존 결과를 보정하기 위한 사후맞춤 자료가 아니라, 사전에 protocol·분석계획·threshold를 동결한 독립 검증자료여야 한다. 예상 비용·기간·표본수·장비·허가를 제시하고 사용자와 지도교수의 승인을 받기 전에는 수집을 시작하지 않는다.

---

## 6. 잠정 연구질문 20개와 검증가능성 감사

다음 20개는 서로 경쟁하는 독립 주제 20개가 아니라, **5개 핵심 연구축 아래 배치한 세부 연구질문**이다. Phase 4A의 데이터·공통지지집합 감사 후 Phase 5 연구헌장에서 각 질문을 `primary | secondary | exploratory | untestable`로 분류한다.

- `primary`: 박사논문의 중심결론을 만드는 질문, 최대 5개
- `secondary`: primary의 기전·반증·일반화를 보완하는 질문, 최대 10개
- `exploratory`: 자료가 허용할 때 탐색하며 확증적 표현을 사용하지 않는 질문
- `untestable`: 현재 자료로 검증할 수 없으며 필요한 추가자료를 명시하는 질문

20개 모두에 동일한 비중의 가설검정을 수행하지 않는다. primary RQ·주요 estimand·분모·분석법을 먼저 동결하고, secondary/exploratory 분석에는 다중비교·선택적 보고 위험을 반영한다.

### 연구축 A — 관측가능성과 데이터 생성과정

#### RQ1. NMEA 관측가능성의 상한

저가형 이동체 수신기의 chipset·firmware 처리와 표준 ASCII NMEA 출력 제약은 GNSS 전파교란 양립 이상을 어디까지 관찰·구분하게 하며, 어떤 현상은 원천적으로 식별 불가능한가?

#### RQ2. RINEX 관측가능성의 상한

CORS RINEX가 RF 원신호가 아니라 수신기 생성 관측값이라는 제약은 간섭의 존재·종류·강도·발생시각 추론에 어떤 상한을 만드는가?

#### RQ3. 수신기 처리계층의 매개효과

receiver·chipset·firmware·antenna·radome·converter와 간섭완화 기능은 NMEA와 RINEX의 signal strength·결측·cycle slip·fix 유지·출력억제 패턴을 어떻게 변화시키는가?

#### RQ4. 표본화·결측·coverage의 탐지한계

NMEA 출력주기, RINEX 30초/1초 표본화, 파일결측과 공간 coverage는 탐지 가능한 사건의 최소 지속시간·공간범위·강도에 어떤 한계를 만드는가?

### 연구축 B — 이동체 NMEA 이상탐지

#### RQ5. NMEA 복합지표의 재현성

도로·속도·정지·터널·도심협곡·수목·multipath를 통제한 뒤 어떤 NMEA 지표 조합이 GNSS 서비스 이상후보를 가장 안정적으로 재현하는가?

#### RQ6. 이동환경 혼란변수와 오탐

터널·도심협곡·급회전·고속주행·정차·수신기 재시작 등은 전파교란 양립 이상과 얼마나 유사한 패턴을 만들며 어떤 반증규칙으로 구별할 수 있는가?

#### RQ7. NMEA 탐지기의 장치·노선 일반화

NMEA 탐지기의 결과는 receiver/firmware·차량·노선·지역·요일·연도가 달라져도 유지되는가, 아니면 특정 장치·환경에 종속되는가?

#### RQ8. NMEA 모델의 설명가능성과 shortcut

AI/XAI 분석에서 어떤 NMEA feature와 시간·공간 맥락이 후보판정에 기여하며, 수신기 ID·노선·결측·터널 등이 shortcut 또는 leakage로 작동하지 않았음을 어떻게 검증할 수 있는가?

### 연구축 C — 고정 CORS RINEX 네트워크 이상탐지

#### RQ9. RINEX 다중관측 지표의 식별력

다중위성·다중주파수·constellation별 code/carrier·Doppler·signal strength·LLI·cycle slip 지표 중 어떤 조합이 장비장애·multipath·전리층·위성계통 이상과 구별되는 interference-compatible anomaly를 재현가능하게 탐지하는가?

#### RQ10. 네트워크 시공간 일관성

단일 기준국 이상과 다수 기준국 공통이상은 어떤 시간차·거리·방향성·공간범위에서 구별되며, 관측소 밀도와 결측을 고려했을 때 네트워크 동시성은 우연보다 큰가?

#### RQ11. 장비·firmware 변경의 영향

receiver·firmware·antenna·radome·clock·converter 변경 전후의 level shift와 missingness 변화가 교란후보로 오인되는 정도는 얼마이며, 층화·change-point·제외창으로 얼마나 통제할 수 있는가?

#### RQ12. 30초와 1초 RINEX의 역할 차이

실제 시공간 중첩구간에서 30초와 1초 자료의 탐지가능 시간척도·후보일치·오탐·계산비용은 어떻게 다르며, 1초 자료는 30초 전국분석의 독립 보조검증으로 어떤 가치를 갖는가?

사건수준 검증라벨과 적절한 전체 분모가 없으면 RQ9~RQ12에서 민감도·특이도를 확정하지 않고, 후보율·false alarms per station-day·안정성·외부일치도로 범위를 제한한다.

### 연구축 D — 이동체–고정망 통합과 사건 대응

#### RQ13. 공통 시공간 지지집합과 통합모드

`S_COMMON_SUPPORT`의 시간·공간·품질 규모는 얼마이며, 실제 자료는 Mode A·B·C 중 어떤 통합모드를 정당화하는가?

#### RQ14. 동일일 이상과 동일사건의 관계

`A_SAME_DAY` 중 시간창·공간영향범위·현상·반증조건까지 충족한 `MATCHED_EVENT_CANDIDATE`의 비율은 얼마이며, 그 일치가 coverage와 자기상관을 보존한 null model보다 큰가?

#### RQ15. Late evidence fusion의 추가가치

`S_COMMON_SUPPORT`와 적절한 검증라벨이 확보된 경우 late fusion은 NMEA-only 또는 RINEX-only보다 사건 신뢰도·설명가능성·오경보 억제·불확실성을 개선하는가? 라벨이 부족하면 성능향상 대신 concordance와 corroboration을 평가한다.

#### RQ16. 두 관측계층 불일치의 설명

NMEA-only 이상, RINEX-only 이상, 양쪽 정상/결측의 불일치는 이동경로·기준국 거리·표본화·수신기 완화·환경 혼란변수·시간무결성으로 어느 정도 설명되는가?

### 연구축 E — 외부검증·일반화·증거등급과 추가자료

#### RQ17. 외부검증원의 품질과 독립성

공식 발표·NOTAM·항행경보·RF 측정·우주기상·민간지도·전문가 판정은 각각 어떤 시간·공간 해상도와 오류·재인용·의존성을 가지며, 사건 검증에 어느 수준까지 사용할 수 있는가?

#### RQ18. 시간·공간·수신기 일반화와 drift

연도·계절·지역·노선·관측소·receiver family·firmware가 달라질 때 탐지와 설명이 유지되는가? covariate·concept·label/coverage drift가 결론에 미치는 영향은 무엇인가?

#### RQ19. 분석선택에 대한 결론의 민감도

시간매칭창·공간거리·공통지지집합·threshold·대조일·다중검정 보정·결측처리의 합리적 대안에 따라 사건수·일치도·증거등급이 얼마나 달라지는가?

#### RQ20. 증거등급 상승을 위한 최소 추가정보

NMEA E3-N2 또는 RINEX E3-R2 후보를 E4-X/E5-C 수준으로 강화하려면 공식사건자료·독립 RF·proprietary 진단·1초 RINEX·전향적 bridge cohort 중 어떤 추가정보가 가장 큰 불확실성 감소와 검증가치를 제공하는가?

### 6.1 H0·H1 가설체계 — primary RQ에 한정

H0·H1은 연구를 더 학술적으로 보이게 하는 장식이 아니라, **사전에 정의된 estimand와 반증 가능한 판단기준**을 고정하기 위해 사용한다. 20개 RQ 모두에 강제로 붙이지 않고 Phase 5에서 선택한 primary RQ 중 통계적 검정이 타당한 질문에만 적용한다.

다음 유형은 H0·H1보다 기술통계·관측가능성 행렬·불확실성 분석이 우선이다.

- 현재 자료에서 무엇을 직접·간접 관측할 수 있는지 묻는 RQ1~RQ4
- 원인과 한계를 구조적으로 설명하는 탐색·기전 질문
- 충분한 검증라벨·평가분모·검정력이 없는 질문
- `unassessable` 또는 `untestable`로 판정된 질문

잠정 확증가설군은 다음과 같다. 아래 문구를 그대로 확정하지 말고 실제 데이터 감사 후 효과크기·단위·분모·검정법을 채워 Phase 5에서 동결한다.

#### 가설군 H-A — NMEA 이상지표의 재현성 후보

- **H0-A:** 사전정의한 NMEA 복합지표의 사건/대조 window 차이 또는 재현성은 사전정의한 최소효과크기를 넘지 않으며 우연·환경혼란으로 설명된다.
- **H1-A:** 해당 차이 또는 재현성이 최소효과크기를 넘고, 장치·노선·환경 block을 고려한 검증에서도 유지된다.
- 활성조건: 독립 검증라벨 또는 타당한 matched-control/negative-control 설계가 존재할 때만 사용.

#### 가설군 H-B — CORS 네트워크 시공간 일관성

- **H0-B:** 다수 기준국의 동시 이상 정도는 coverage·자기상관·공통 위성/제품 오류를 보존한 null model에서 기대되는 수준을 넘지 않는다.
- **H1-B:** 사전정의한 네트워크 동시성 통계량이 보정된 null 분포를 유의하게 초과하고 반증검토 후에도 유지된다.
- 활성조건: 관측소 가용성·장비변경·우주기상·위성계통 공통모드를 통제할 수 있을 때만 사용.

#### 가설군 H-C — NMEA–RINEX 사건 일치

- **H0-C:** `S_COMMON_SUPPORT` 안의 NMEA–RINEX 사건 일치율은 가용성·계절성·자기상관을 보존한 우연 일치율보다 크지 않다.
- **H1-C:** 사전정의한 시간·공간·현상 매칭을 통과한 사건 일치율이 우연 일치율보다 크다.
- 활성조건: NMEA 시각 무결성과 공간불확실성이 매칭을 허용하고, 사건후보가 독립적으로 동결된 경우에만 사용.

#### 가설군 H-D — Late fusion의 추가가치

- **H0-D:** late fusion은 사전선택한 primary metric에서 가장 성능이 좋은 단일자료 모델보다 사전정의한 최소개선폭만큼 개선되지 않는다.
- **H1-D:** late fusion은 독립 holdout의 동일 metric에서 최소개선폭 이상 개선되며 calibration·오경보·불확실성 기준도 충족한다.
- 활성조건: 독립 event-level label, `S_COMMON_SUPPORT`, 동일 평가분모와 비교 가능한 score가 확보된 경우에만 사용.

#### 가설군 H-E — 시간·공간·수신기 일반화

- **H0-E:** 새로운 연도·지역·receiver family에서 성능저하가 사전정의한 허용한계(non-inferiority/equivalence margin)를 초과한다.
- **H1-E:** 성능저하가 허용한계 이내이며 사전정의한 일반화 기준을 충족한다.
- 활성조건: margin을 결과 확인 전에 학술적·운영적 근거로 설정하고 독립 외부/시간 holdout이 있을 때만 사용.

가설검정 시 다음을 강제한다.

- H0 기각은 ‘자료가 해당 통계적 대립가설과 양립한다’는 뜻이지 jamming·spoofing 원인확정이 아니다.
- H0를 기각하지 못한 것은 ‘효과 없음’ 또는 ‘교란 없음’의 증거가 아니다.
- 동등성·비열등성을 주장하려면 일반적인 차이검정의 비유의 결과가 아니라 사전정의 margin과 적절한 equivalence/non-inferiority 검정을 사용한다.
- p-value만 제시하지 말고 effect size, confidence interval, 실제 독립성 단위와 분석분모를 함께 제시한다.
- alpha, 단측/양측, primary metric, 최소효과크기, 보정 family, 중단·제외규칙을 결과 확인 전에 동결한다.
- primary 가설은 최대 5개로 제한한다. 나머지는 secondary 또는 exploratory로 보고하고 확증적 표현을 사용하지 않는다.
- H0·H1, 증거등급(E0~E5-C), 사건 원인분류는 서로 다른 축으로 저장한다.

`46_hypothesis_registry.csv`에는 다음을 기록한다.

```text
hypothesis_id, rq_id, priority, activation_condition,
H0, H1, estimand, analysis_unit, denominator,
primary_metric, effect_size, minimum_effect_or_margin,
alpha, sidedness, test_method, correction_family,
label_requirement, common_support_requirement,
freeze_timestamp, preregistration_id, status, result,
confidence_interval, interpretation_limit
```

각 RQ에 대해 다음 표를 작성한다.

```text
RQ | 연구축 | priority | testability | 핵심/보조/탐색 상태 |
필요한 자료 | 실제 보유여부 | 분석단위 | estimand | 평가분모 |
독립변수 | 결과변수 | 혼란변수 | 검증방법 | 다중비교 family |
실패조건 | 허용 가능한 주장 | 필요한 추가자료 | 논문/박사논문 장
```

Phase 5에서 primary RQ를 최대 5개로 동결한다. primary 교체가 필요하면 결과를 보기 전에 사유와 시점을 `12_decision_log.md`와 사전등록 기록에 남긴다. 라벨·공통지지집합·검정력이 부족하면 감독학습 가설이나 성능비교를 억지로 만들지 말고 해당 RQ를 secondary·exploratory·untestable로 낮춘다.

---

## 7. 분석트랙별 최소 연구설계

### Track A — 이동체 NMEA ASCII-only

1. 파일·문장·epoch·수신기·주행단위 inventory
2. checksum, encoding, line ending, sentence completeness, epoch assembly QA
3. 수신기·firmware별 출력가능성 및 해상도 차이
4. 허용된 필드에서만 feature 생성
5. fix quality, satellite count, DOP, GSV/SNR 분포, sentence dropout, 위치·속도·방향의 내부 일관성 등 후보지표 감사
6. 터널·정차·도심협곡·급회전·고속주행·multipath·노선반복·수신기 재시작 등 반증변수 통제
7. 동일 route/day/device에 의한 누설을 막는 group split 및 spatial/temporal block validation
8. 단일 threshold가 아니라 장치·환경별 민감도와 불확실성 제시
9. NMEA alone으로 jamming/spoofing 확정 금지

기존 위치·도로·격자 결과가 있으면 feature 산식, 좌표계, map matching, grid size, threshold, label provenance, 중복 epoch 처리, 편향을 재감사한다.

### Track B — CORS RINEX 고정망

1. station-day-file 단위 품질 inventory
2. 헤더와 실제 epoch 비교, observation completeness와 sampling QA
3. station/satellite/constellation/frequency별 기준선 모델
4. receiver·firmware·antenna·radome·clock·converter·RINEX 생성경로 timeline 구축
5. 제조사 간섭완화·품질관리 기능과 RINEX 반영/비반영 여부 감사
6. 장비변경 전후 level shift·variance·missingness와 탐지 feature 변화 통제
7. 단일국소 이상과 다중관측소 공통이상 분리
8. 우주기상·전리층·위성궤도/시계·제품 오류·통신/저장장애 반증
9. 실제 observation type이 허용하는 물리·통계지표만 사용
10. 30초와 1초 결과의 탐지가능시간척도 분리
11. station·receiver family·firmware·날짜·지역 단위의 blocked validation과 event-level 평가
12. blind 후보 동결 후 외부검증

### Track C — 통합 사건·증거분석

1. 공통 event schema와 단위·시간계·좌표계 확정
2. 독립 동결한 `C_NMEA_EVENT`와 `C_RINEX_EVENT`에서 날짜집합을 파생하고 `A_UNION`을 immutable 통합조사 cohort로 구성
3. `D_BOTH_VALID`와 `S_COMMON_SUPPORT`를 구축하여 가용성·노출·분모를 명시
4. NMEA score와 RINEX score를 같은 확률이라고 가정하지 않는다. 충분한 독립 라벨이 있을 때만 각각 calibration하고, 그렇지 않으면 anomaly score 또는 순위로 유지
5. 라벨이 충분하면 투명한 rule baseline → 단순 calibrated model → 복잡모델 순으로 비교
6. 라벨이 부족하면 concordance, coincidence against null, permutation test, case-control event review 중심
7. NMEA-only / RINEX-only / fusion ablation
8. 외부자료가 있는 경우 event precision, recall, PR-AUC, false alarms/exposure, detection delay를 사용하고, 확률 calibration이 성립한 경우에만 Brier/ECE를 사용
9. 희귀사건에서 accuracy와 AUROC만으로 우수성을 주장하지 않음
10. 시간·공간 randomization 또는 matched negative windows로 우연한 중첩률 평가
11. 서로 다른 데이터에서 같은 결론이 나온 것과 같은 사건을 관측한 것을 구분

---

## 8. 혼란변수·반증 매트릭스

최소한 다음을 포함하는 `confounder_counterevidence_matrix`를 작성하라.

| 범주 | NMEA 영향 | RINEX 영향 | 확인자료 | 통제법 | 남는 불확실성 |
|---|---|---|---|---|---|
| 터널·실내·도심협곡·수목 | 필수 | 해당 시 관측환경 | 지도·경로·현장 맥락 | 구간마스킹/층화 |  |
| multipath | 필수 | 필수 | 위성고도·환경·반복패턴 | 시각/위성/장소 통제 |  |
| 이동속도·정차·급회전 | 필수 | 비해당 | RMC/연속위치 | 상태층화 |  |
| 수신기·firmware 차이 | 필수 | 필수 | 헤더·문서·로그 | 장치별 모델/효과 |  |
| 수신기 내부 간섭완화·필터 | 제한적/firmware 의존 | 필수 | 제조사 문서·설정·진단로그 | 관측가능성 층화 |  |
| LLI·SSI·SNR 생성/결측 규칙 | 문장/수신기 의존 | 필수 | 규격·헤더·실측분포 | receiver별 정규화/분리 |  |
| 결측·파서·압축 오류 | 필수 | 필수 | QA 로그 | 데이터품질 게이트 |  |
| 관측소 장비교체·정비 | 비해당 | 필수 | station log | change-point exclusion |  |
| 전리층·신틸레이션·우주기상 | 제한적 | 필수 | 실제 외부지표 | 공변량/반증 |  |
| 위성궤도·시계·시스템 이상 | 제한적 | 필수 | 공식/IGS 자료 | 위성 공통모드 |  |
| RF 간섭 | 간접 | 간접/측정계층 | 독립 RF/공식사건 | 외부검증 |  |

빈칸을 실제 조사로 채우되, 자료가 없으면 `unavailable`이라고 쓴다.

---

## 9. 증거등급과 Claim Registry

모든 사건과 논문 결론은 자료원별 증거와 통합사건 증거를 분리하는 다음 체계를 사용한다. 실제 연구자료를 보고 명칭을 다듬어도 의미를 약화하지 않는다.

```text
E0     평가불가/자료품질 문제
E1     단일 데이터 이상(data anomaly)
E2-N   NMEA에서 확인된 GNSS 서비스 이상
E3-N1  단일 이동체의 다중 NMEA 지표·반증검토를 통과한 interference-compatible anomaly
E3-N2  다수 독립 이동체에서 시공간 일관성이 확인된 강화된 NMEA 이상
E2-R   CORS RINEX에서 확인된 GNSS 관측 이상
E3-R1  단일 기준국의 다중위성·주파수·지표·반증검토를 통과한 interference-compatible anomaly
E3-R2  다수 기준국에서 시공간 일관성이 확인된 강화된 RINEX 네트워크 이상
E4-X   NMEA와 RINEX 또는 다른 독립 이종자료가 시간·공간·현상·반증 측면에서 corroborated
E5-C   공식 사건확인, 독립 RF 측정 또는 통제실험 ground truth 등으로 원인이 강하게 확인됨
```

- NMEA 자료원 자체는 E3-N2를, 표준 RINEX 자료원 자체는 E3-R2를 원칙적 상한으로 한다.
- NMEA와 RINEX가 단지 같은 UTC 날짜라는 이유만으로 E4-X를 부여하지 않는다. 시간창·공간영향범위·관측현상과 반증검토가 일치해야 한다.
- 통제실험에서는 NMEA/RINEX 기반 탐지기의 성능이 높을 수 있지만, 높은 분류성능과 현장 미확인 사건의 원인 귀속등급을 혼동하지 않는다.
- proprietary 진단이나 RF 자료가 실제 확보되면 그것은 더 이상 `RINEX-only`가 아니며 별도 증거로 등록한다.
- 같은 수신기에서 나온 proprietary jamming/spoofing score 또는 mitigation flag는 RINEX와 완전히 독립인 증거로 간주하지 않는다. 의미·threshold·오경보 특성이 공식 문서나 통제실험으로 검증되지 않았다면 그 진단만으로 E5-C를 부여하지 않는다.
- E4-X/E5-C는 증거의 성격·품질·의존성·공간오차·시간오차를 명시한다. NMEA와 RINEX는 이종 관측계층이지만 같은 GNSS 신호·환경·공통 외부원인에 영향을 받을 수 있으므로 자동으로 통계적 독립이라고 부르지 않는다.
- 정부 보도자료를 재인용한 언론기사, 같은 기관 자료의 여러 게시본, 하나의 원보고서를 공유하는 민간지도는 서로 다른 증거로 중복 계산하지 않고 동일 `source_dependency_group`으로 묶는다.
- 공식 발표도 시간·공간·현상 범위가 후보사건과 충분히 대응하지 않으면 자동으로 E5-C가 아니다. 범위가 거친 공식자료는 E4-X 보조증거가 될 수 있으며, E5-C에는 후보사건과 원인확인의 실제 대응범위를 기록한다.
- `jamming`, `spoofing`, `mixed`, `ambiguous`, `unassessable` 분류와 신뢰도를 별도 필드로 둔다.
- 공식 확인이 없는 경우 논문 제목·초록·결론에서도 확정형 표현을 피한다.

각 사건에는 최소한 다음 네 필드를 별도로 둔다.

```text
nmea_evidence_level
rinex_evidence_level
cross_domain_corroboration_level
integrated_event_level
```

`claim_registry.csv`에는 다음을 기록한다.

```text
claim_id, claim_text, chapter, evidence_ids,
nmea_evidence_level, rinex_evidence_level,
cross_domain_corroboration_level, integrated_event_level,
status, counterevidence, uncertainty, citation_ids,
reproducibility_artifact, reviewer_note
```

---

## 10. 통계·AI 검증 원칙

분석 전에 연구질문별 estimand, 분석단위, 분모, label status, 허용지표를 `45_statistical_estimand_and_score_semantics.md`에 동결한다. 이상후보 선별(screening), 가설검정(inference), 확률예측(prediction), 사건 원인귀속(causal attribution)을 서로 다른 과제로 취급한다.

- 설명가능하고 물리적으로 해석 가능한 baseline을 먼저 만든다.
- threshold는 test set 또는 공식 사건목록을 보고 조정하지 않는다.
- train/validation/test를 epoch 무작위분할하지 않는다.
- route, trip, device, day, event, station, region을 고려한 group/block split을 사용한다.
- 공간 자기상관과 시간 자기상관을 무시하지 않는다.
- 동일 사건의 여러 epoch가 양쪽 split에 들어가는 leakage를 차단한다.
- 클래스 불균형, label uncertainty, reviewer disagreement를 정량화한다.
- 모델선택과 최종평가를 분리하고, sensitivity·ablation·negative control을 포함한다.
- 신뢰구간은 독립성 단위에 맞는 event/day/route/station/region bootstrap을 검토한다.
- 후보 60건 등 전문가 검토자료가 실제 존재하면 판정척도·blindness·표본선정·Cohen’s κ와 confidence를 감사한다. 숫자는 파일에서 확인 전 `prior_reported`로 둔다.
- AI가 전문가 라벨을 대신했다고 쓰지 말고, 자동·AI 검토와 인간 독립판정을 구분한다.
- 라벨은 `confirmed | externally_corroborated | expert_reviewed | weak_label | unlabeled | discovery_contaminated`로 구분하고, 라벨 출처·시간공간 해상도·독립성·오류가능성을 기록한다.
- positive-unlabeled 또는 weak-label 상황에서 확인되지 않은 표본을 음성으로 간주하여 민감도·특이도를 계산하지 않는다. 필요한 가정과 민감도분석 없이 PU 성능을 확정하지 않는다.
- anomaly score, p-value, calibrated probability를 혼용하지 않는다. 독립 calibration set과 적절한 라벨이 없으면 score를 확률이라고 부르지 않는다.
- 다중검정 보정은 유효한 p-value가 정의된 추론문제에 적용한다. 규칙기반/비지도 anomaly score에는 FDR을 기계적으로 붙이지 말고 노출단위당 오경보, negative-control, permutation 또는 empirical-null을 사용한다.
- 전처리·결측대치·정규화·feature selection·calibration은 각 training fold 안에서 적합하여 leakage를 방지한다. 최종 test/holdout에는 한 번만 접근한다.

### 10.1 XAI 강제원칙

XAI는 결과를 보기 좋게 설명하는 부속 그림이 아니라, AI 모델이 어떤 근거로 이상후보를 제시했는지 검증하고 GNSS 도메인 지식과 충돌하는 shortcut·bias·data leakage를 찾는 핵심 연구방법으로 사용한다.

- 먼저 설명가능한 통계·규칙기반 baseline을 구축하고, AI 모델의 추가이득을 검증한다.
- 모델종류와 데이터구조에 맞는 XAI 방법을 선택하며 SHAP 하나만 기계적으로 사용하지 않는다.
- 전역 설명(global explanation), 개별 사건 설명(local/event explanation), 시간구간·공간·관측소·위성별 설명을 구분한다.
- NMEA에서는 수신기·firmware·노선·속도·터널·도심협곡 등이 shortcut feature가 되었는지 확인한다.
- RINEX에서는 관측소 ID·연도·결측·장비교체·특정 위성·관측유형이 사건라벨을 대리했는지 확인한다.
- feature 중요도와 인과성을 혼동하지 않는다. XAI 설명은 jamming 또는 spoofing의 물리적 원인을 확정하는 증거가 아니다.
- 상관된 feature, 결측값 처리, scale, background/reference set 선택에 따른 설명변화를 점검한다.
- 설명충실도(faithfulness), 안정성(stability), 재현성, 민감도, sparsity/complexity, 도메인 타당성을 가능한 범위에서 정량평가한다.
- 동일 사건의 재표본화·모델 seed·fold·수신기·관측소가 바뀌어도 핵심 설명이 유지되는지 확인한다.
- AI 예측점수, XAI 설명, 물리적 GNSS 해석, 반증자료, 전문가 판정을 각각 분리하여 저장한다.
- XAI 결과가 도메인 전문가의 예상과 다르면 숨기지 말고 오류·새 발견·confounding 가능성으로 조사한다.
- 최종 사건별 설명에는 ‘어떤 관측이 기여했는가’, ‘어떤 반증을 확인했는가’, ‘무엇은 이 데이터로 알 수 없는가’를 함께 제시한다.

AI/XAI 분석 전 `xai_analysis_plan.md`를 동결하고, 최종적으로 `xai_evaluation_report.md`와 사건별 explanation artifact를 생성한다.

---

## 11. 선행연구·표준·외부자료 조사 원칙

### 11.1 두 연구폴더의 참고문헌과 원문 우선검토 — 강제조건

다음 두 루트의 참고문헌 목록과 보관된 원문을 외부 웹검색보다 먼저 반드시 조사한다.

```text
D:\장상훈\경희대_phd
E:\worldtechRnD\Pro_phd_data\rinex
```

두 폴더 내부의 논문·학위논문·보고서·표준·white paper·매뉴얼·PDF·HWP/HWPX·MD·DOCX·PPTX·BibTeX/RIS·참고문헌표·메모·기존 논문초안·코드 주석을 전수목록화한다.

문헌 원문을 반드시 읽는 규칙과 blind detection을 동시에 지키기 위해 **정보방화벽(information firewall)**을 둔다. 방법·표준·수신기 특성 문헌은 탐지팀이 읽을 수 있으나, 구체적인 공식 사건일·좌표·후보목록이 포함된 문헌·보고서·기존 결과는 `event_date_bearing_source`로 표시하고 validation custodian 또는 분리된 문헌팀이 관리한다. `43_blinding_access_ledger.csv`에 누가 어떤 자료의 사건정보를 언제 보았는지 기록하고, `reference_reading_ledger.csv`에도 `event_date_bearing_source`, `information_access_role`, `blind_impact`를 연결한다. 탐지 담당자가 이미 사건정보를 본 기간은 `discovery_contaminated`로 표시하고, 보지 않은 시간·지역·수신기 holdout 또는 독립 재수집 자료로 검증한다. `reference`, `references`, `paper`, `literature`, `문헌`, `논문`, `원문`, `표준`, `manual`, `whitepaper`처럼 예상되는 폴더명만 보지 말고 전체 트리에서 관련자료를 찾는다.

**참고문헌 제목과 서지정보만 읽고 선행연구를 정리해서는 안 된다.** 두 폴더에 원문 파일이 있으면 반드시 원문 전체를 실제로 읽고 다음을 근거와 함께 기록한다.

```text
reference_id
local_original_path
cited_from_paths
document_type, language, version
title, authors, year, venue, volume, issue, pages
DOI/official_url/standard_identifier
full_text_available
full_text_read_status
event_date_bearing_source, information_access_role, blind_impact
pages_or_sections_reviewed
research_question
data_and_study_area
method
validation
main_results
limitations
relevance_to_NMEA
relevance_to_RINEX
relevance_to_integration_AI_XAI
claims_safe_to_cite
claims_not_supported
reader_note
```

원문 전체를 읽었다는 말은 파일을 열었다는 뜻이 아니라, 목적·데이터·방법·결과·검증·한계·본 연구와의 관계를 위 구조로 추출했다는 뜻이다. 스캔 PDF는 필요한 경우 OCR과 페이지 시각검사를 병행하고, 표·그림·수식이 추출텍스트에서 누락되지 않았는지 확인한다.

참고문헌표에는 있으나 원문이 두 폴더에 없으면 다음 절차를 따른다.

1. 제목·저자·연도·DOI를 정규화하여 다른 파일명이나 중복폴더에 원문이 있는지 다시 확인
2. `missing_originals.csv`에 기록
3. 출판사·DOI·학회·기관 repository 등 합법적인 원출처에서 원문 확보 가능성을 조사
4. 원문을 확보하여 읽기 전에는 해당 연구의 세부 방법·결과를 확정적으로 인용하지 않음
5. 초록만 확인했으면 `abstract_only`, 2차 문헌에서만 확인했으면 `secondary_only`로 표시

원문이 없는 참고문헌을 기존 문서의 요약이나 다른 논문의 재인용만으로 원문을 읽은 것처럼 작성하지 않는다. 접근 불가 자료는 접근 불가 사실과 그것이 선행연구 검토에 미치는 영향을 명시한다.

중복파일·preprint·accepted manuscript·최종 출판본·정오표·철회 여부를 확인하고, 가능한 경우 최종 출판본을 기준으로 하되 버전 차이를 기록한다. 유료·비공개 자료의 전문을 산출물에 복제하지 말고 저작권 범위 안에서 분석·요약한다.

### 11.2 문헌검토 산출물과 PASS 게이트

다음을 생성한다.

```text
local_reference_inventory.csv
reference_reading_ledger.csv
reference_duplicate_version_map.csv
missing_originals.csv
claim_citation_source_matrix.csv
literature_synthesis_NMEA.md
literature_synthesis_RINEX.md
literature_synthesis_integration_AI_XAI.md
literature_gap_report.md
```

다음 조건을 모두 만족하기 전에는 관련연구 장과 최종 참고문헌을 `PASS`로 판정하지 않는다.

- 두 연구루트의 관련 파일 전수 inventory 완료
- 기존 논문초안·프롬프트·보고서가 인용한 참고문헌 추출 완료
- 로컬에 있는 원문 전체의 reading ledger 완료
- 각 핵심 주장과 실제 원문 페이지·절·표·그림의 연결 완료
- DOI·저자·연도·학술지·권호·페이지 서지검증 완료
- 미보유·접근불가·초록만 확인한 문헌의 상태 구분 완료
- NMEA, RINEX, 통합 AI/XAI 연구공백을 원문 근거로 비교 완료

문헌량이 많아 한 세션에서 끝나지 않으면 batch와 checkpoint로 나누어 읽되, 읽지 않은 문헌을 완료로 표시하지 않는다. 매 세션마다 전체 문헌수, 원문 확보수, 전문 판독 완료수, 초록만 확인한 수, 접근불가 수와 남은 수를 보고한다.

### 11.3 외부 보완조사

두 폴더의 참고문헌과 원문 검토를 완료한 뒤, 실제로 부족한 연구영역만 공식 사이트·학술 데이터베이스·원 논문에서 보완한다. 외부에서 추가한 문헌도 동일한 reading ledger와 claim-source 기준을 적용한다.

최소 조사영역:

- NMEA 표준 출력과 저가형 수신기 chipset/firmware 처리 한계
- GNSS jamming/spoofing/meaconing 정의와 탐지증거 수준
- RINEX observation QC, cycle slip, multipath, C/N0, network anomaly
- RINEX가 RF 원신호가 아닌 수신기 생성 관측값이라는 계층적 한계
- CORS receiver·firmware·antenna·converter와 anti-jamming/spoofing·notch filter·RAIM·품질관리 기능
- 제조사별 간섭완화가 RINEX signal strength·LLI·결측·cycle slip에 미치는 영향
- 이동체 GNSS 이상탐지, crowdsourcing, fleet-based PNT monitoring
- CORS 네트워크 기반 간섭탐지와 공간전파 특성
- 전리층·ROTI·신틸레이션과 RF 교란의 구분
- constellation·frequency 차분, GLONASS FDMA 관련 가능성과 한계
- multi-sensor/multi-view anomaly detection 및 evidence fusion
- 희귀사건 검증, weak label, positive-unlabeled, blocked cross-validation
- ICAO, ITU, IGS, RINEX 공식문서와 RTCA DO-235C 관련 합법적 접근자료

관련연구는 반드시 실제 연구자의 실제 논문내용과 정확한 인용으로 작성한다. DOI·URL·발행연도·권호·페이지를 원문과 공식 색인에서 교차검증한다. 초록만 본 논문은 전문을 본 것처럼 쓰지 않는다. 유료·비공개 표준의 전문을 재현하지 말고, 합법적으로 확인 가능한 조항과 서지정보의 범위를 표시한다.

외부 사건자료는 blind detection 이후에만 validation set으로 연다. 외부자료의 출처 우선순위는 공식 정부·군/항공/해상 통보·국제기구·검증된 연구데이터·언론·민간지도 순으로 두고, 서로 독립적이지 않은 재인용 자료를 여러 증거로 중복 계산하지 않는다.

---

## 12. 박사논문과 두 편 논문의 구조

실제 감사 후 최종 조정하되, 기본 포트폴리오는 다음과 같이 설계한다.

### 논문 1 — 이동체 NMEA 연구

- 핵심: NMEA-only 관측가능성, chipset/firmware 효과, 이동환경 혼란변수 통제, 서비스 이상후보 탐지
- 공헌: 고가 RF/UBX가 없는 현실적 fleet 데이터에서 가능한 주장과 불가능한 주장을 함께 정량화
- 잠정 투고형식: 국내 공간정보/GIS 학술지용 16.0~17.5쪽 설계가 기존 문서에 실제 존재하는지 확인

### 논문 2 — CORS RINEX 연구

- 핵심: 전국 고정망의 장기·다중관측소·다중위성/주파수 이상탐지, 혼란변수 반증, blind external validation
- 목표저널 후보는 연구성숙도와 실제 공헌을 보고 GPS Solutions, Journal of Geodesy 등과 적합성을 비교

### 박사논문 통합장

- 두 논문의 결과를 단순 합본하지 않는다.
- 공통 관측가능성 이론, common event model, 시공간 중첩성, late evidence fusion, 주장등급, 반증체계를 새 통합공헌으로 제시한다.
- 실제 중첩이 충분하면 통합 실증장과 독립 성능비교를 둔다.
- 중첩이 부족하면 두 관측계층의 상보성과 일반화 한계를 검증하는 방법론 통합장으로 설계한다.
- 논문 간 동일 표·그림·문장·결과의 중복과 자기표절 위험을 `paper_thesis_overlap_matrix`로 관리한다.

### 잠정 박사논문 장 구성

1. 서론: 문제, 연구공백, 목적, RQ, 공헌
2. 이론·표준·선행연구: GNSS 교란과 관측가능성
3. 데이터·윤리·재현성·공통 사건모형
4. 이동체 NMEA 연구
5. 고정 CORS RINEX 네트워크 연구
6. 이동체–고정망 다중규모 증거통합
7. 외부검증, 반증, 일반화, 한계
8. 결론과 정책·운영·연구 활용

각 장의 시작에는 ‘이 장을 이해하기 위해 먼저 알아야 할 내용’을 정리하고, 장 끝에는 ‘이 장을 통해 새롭게 확인된 내용·다음 장과의 연결·남은 한계’를 정리한다.

---

## 13. 폴더 감사 절차

### Phase 0 — 접근성·안전·자원검사

- 두 경로의 존재와 읽기 권한 확인
- 드라이브·파일시스템·여유공간·CPU/RAM 확인
- 한국어 경로, 긴 경로, 인코딩, 압축도구 문제 확인
- 현재 작업경로가 원본 내부인지 확인
- 위험한 기존 자동화·출력설정 확인
- 지정 통합연구 작업경로 `E:\worldtechRnD\Pjt_phd_nmea_cors_relation`의 존재·접근·안전·저장공간 판단

두 원본 연구경로 중 하나라도 없으면 전체 드라이브를 임의 탐색하지 말고 정확한 오류와 필요한 조치만 보고한 뒤 중지한다. 지정 통합연구 작업경로가 없는 경우는 오류가 아니며, 1.3절의 안전조건을 모두 통과한 뒤 해당 경로만 생성한다.

### Phase 1 — 비파괴 전수 inventory

각 루트에서 다음을 집계한다.

- 전체 파일수·폴더수·총용량
- 확장자·크기·연도·경로깊이 분포
- raw data / code / config / log / result / manuscript / prompt / reference 분류
- 0 byte, 읽기오류, 비정상확장자, 압축/중복 후보
- 상대경로·크기·mtime manifest
- NMEA와 RINEX 대표표본 checksum
- 원본 동결 전에는 전체 hash 완료 여부를 사실대로 기록

NMEA 이관·보존과 연결되는 기존 규칙이 발견되면 파일수·상대경로·크기·SHA-256·오류 0건 기준과 충돌 여부를 보고한다. RINEX 수십만 파일의 full hash는 비용을 추정하고 단계적으로 수행하되, 완료하지 않았으면 완료했다고 쓰지 않는다.

### Phase 2 — 기존 연구자산 감사

모든 관련 README, prompt, manuscript, notebook, script, config, schema, test, log, report를 찾아 다음을 작성한다.

```text
asset_id | path | role | dataset | version/status | inputs | outputs |
last_modified | reusable | risk | evidence | action
```

특히 확인할 것:

- 기존 NMEA feature·label·threshold·격자·hotspot·평가법
- NMEA Research Reset/R0 관련 문서와 완료여부
- 기존 CORS parser, manifest, partition, stage config/code hash
- 기존 30초 실행결과, failure/retry, peak RSS, package version 기록
- expert review 60건, 5단계 판정, Cohen’s κ 자료의 실제 존재
- 공식 사건정보가 기존 탐지과정에 누설되었는지
- 동일 기능의 중복스크립트와 결과 불일치
- 논문초안의 수치가 어느 산출물에서 왔는지

### Phase 3 — 데이터 관측가능성·품질 프로파일

NMEA와 RINEX를 각자 독립적으로 프로파일하고 `observability_matrix`, `data_dictionary`, `quality_report`를 만든다. RINEX에는 receiver/firmware/antenna/converter timeline, 제조사 mitigation 기능, LLI·SSI·SNR 생성규칙과 관측불가 항목을 반드시 포함한다. 이 단계 전에는 신규 통합모델을 학습하지 않는다.

### Phase 4A — 분석 전 시공간 공통지지집합·통합가능성 감사

- NMEA의 실제 운행일·시간·영역·수신기
- RINEX의 실제 관측기간·관측소·좌표·sampling
- `D_NMEA_VALID`, `D_RINEX_VALID`, `D_BOTH_VALID`, `D_EITHER_VALID`
- `NMEA_LAST_VALID_DATE`, `RINEX_LAST_VALID_DATE`, `INTEGRATION_CUTOFF_DATE`
- 시간·공간·품질 coverage를 함께 반영한 잠정 `S_COMMON_SUPPORT`
- 이동체 경로와 CORS 관측소의 거리·지형·합리적 영향범위
- 외부 사건자료의 가용기간·공간정밀도는 validation custodian이 내용 누설 없이 메타데이터만 요약

이 단계에서는 아직 `C_NMEA_EVENT`, `C_RINEX_EVENT`, `A_NMEA`, `A_RINEX`가 생성되지 않았으므로 이상일 일치나 fusion 성능을 계산하지 않는다. 공통지지집합의 규모와 검정가능성만으로 Mode A/B/C를 **잠정 권고**하고, 최종 Mode는 Phase 7에서 확정한다. 데이터 보유일의 단순 교집합을 후보선정 기준으로 사용하지 않는다.

### Phase 5 — 연구헌장 동결

다음을 하나의 `research_charter_v1.md`로 확정한다.

- 최종 연구문제·가설·분석단위
- 포함/제외 기준
- feature와 confounder
- blind/validation 분리
- split, metric, threshold 동결 규칙
- evidence level과 claim language
- 연구윤리·개인정보·보안
- 예상 계산량·저장량·실행순서
- 성공·실패·중단 기준

이 Phase가 PASS되기 전에는 전국 전수 신규분석을 시작하지 않는다.

### Phase 6 — Pilot → Scale → 독립 사건후보 Blind Freeze

1. 소규모 대표 pilot과 unit/integration test
2. 기준결과와 수작업 spot check
3. 계산량·메모리·실패복구 검증
4. 설정·코드·환경 동결
5. NMEA와 RINEX의 독립 chunked scale run
6. 서로의 결과와 외부사건정보를 보지 않은 상태에서 `C_NMEA_EVENT`와 `C_RINEX_EVENT`를 각각 blind freeze

### Phase 7 — 날짜집합 파생 → External Validation → Integration

1. 동결된 사건후보에서 `A_NMEA`, `A_RINEX`, `A_UNION`, `A_SAME_DAY` 파생
2. 날짜별 cross-investigation matrix와 사건별 matching table 생성
3. `S_COMMON_SUPPORT` 안에서 시간·공간 매칭, 반증, 대조일·우연 일치 검정
4. 공통지지집합 밖의 사건은 `OUTSIDE_COMMON_SUPPORT`로 분리
5. validation custodian이 외부검증 자료를 개봉하고 전문가 독립검토 수행
6. NMEA/RINEX/fusion ablation과 증거원 의존성 감사
7. 최종 Mode A/B/C 확정
8. 박사논문·논문별 표·그림·claim registry 확정

필수 통합 산출물:

```text
nmea_anomaly_day_registry.csv
rinex_anomaly_day_registry.csv
anomaly_day_union_registry.csv
same_day_anomaly_registry.csv
cross_investigation_matrix.csv
matched_event_candidate_registry.csv
matched_control_day_registry.csv
coincidence_significance_report.md
```

각 단계는 `PASS / CONDITIONAL PASS / FAIL / BLOCKED`로 판정하고 근거를 기록한다.

---

## 14. 소프트웨어·재현성 계약

- 기존 코드를 먼저 재사용성 감사하고 이유 없이 전면 재작성하지 않는다.
- 프로젝트 전용 환경을 사용하고 시스템 전역 package를 조용히 변경하지 않는다.
- package version, OS, Python, external tool version을 기록한다.
- 모든 stage에 config hash, code hash, input manifest id, output manifest, 시작/종료시각, row/file count, 오류수를 남긴다.
- random seed만으로 재현가능성을 주장하지 말고 데이터 partition과 split id를 고정한다.
- 단위·시간계·좌표계·결측값·sentinel을 schema로 강제한다.
- 원시파일 경로는 연구 내부 provenance에 보존하되 논문·공유산출물에서는 개인경로와 민감한 이동궤적을 비식별화한다. 연구윤리·개인정보·보안·이해상충·이중용도 검토의 세부 절차와 산출물은 §20을 따른다.
- 대용량 결과는 Parquet 등 적절한 columnar 형식을 검토하고 CSV는 교환·요약용으로 제한한다.
- 실패 파일은 숨기지 말고 quarantine manifest에 기록한다.
- 부분실행 결과를 전체 결과처럼 쓰지 않는다.
- TODO, placeholder, mock result를 최종 산출물로 남기지 않는다.
- 본 Master Prompt 자체의 version, 파일 SHA-256, Git commit SHA, 적용 시작일, 변경이유를 모든 실행 manifest에 기록한다. 분석 도중 prompt가 바뀌면 영향받는 stage를 명시하고 조용히 소급 적용하지 않는다.
- 원본 대용량 데이터는 DVC/git-lfs 등에 자동 복제하지 않는다. 원본은 읽기 전용 manifest·상대경로·크기·선별/전체 checksum으로 식별하고, 라이선스·용량·보안·백업정책이 승인된 파생자료만 별도 버전관리한다.
- Windows 절대경로·한국어 경로·긴 경로는 config에서 관리하고 코드에 산재시키지 않는다. 경로 정규화와 재개 테스트를 포함한다.

---

## 15. 최초 실행에서 만들어야 할 산출물

최초 실행은 Phase 0~2와 Phase 4A의 **계획 가능한 범위**까지만 수행한다. 원시데이터 전수 scientific analysis나 모델학습은 시작하지 않는다.

지정 통합연구 작업경로 `E:\worldtechRnD\Pjt_phd_nmea_cors_relation`에 다음을 만든다.

```text
00_PROJECT_README_KO.md
01_safety_and_access_report.md
02_nmea_inventory_summary.md
03_rinex_inventory_summary.md
04_existing_asset_register.csv
05_conflict_and_lineage_report.md
06_observability_audit_plan.md
07_spatiotemporal_overlap_audit_plan.md
08_research_question_evidence_matrix.md
09_dissertation_blueprint_v1.md
10_paper_portfolio_map.md
11_risk_register.md
12_decision_log.md
13_compute_storage_budget.md
14_professor_meeting_brief.md
15_next_stage_execution_plan.md
16_local_reference_inventory.csv
17_reference_reading_ledger.csv
18_claim_citation_source_matrix.csv
19_literature_gap_report.md
20_xai_analysis_plan.md
21_rinex_observability_matrix.csv
22_receiver_firmware_antenna_timeline.csv
23_receiver_mitigation_evidence_matrix.csv
24_firmware_change_impact_plan.md
25_evidence_level_schema.md
26_data_ethics_review.md
27_data_use_agreement_status.md
28_conflict_of_interest_disclosure.md
29_dual_use_security_review.md
30_multiple_testing_and_power_plan.md
31_preregistration_record.md
32_domestic_external_corroboration_sources.md
33_novelty_positioning_table.md
34_temporal_drift_and_generalization_note.md
35_reproducibility_toolchain.md
36_defense_readiness_checklist.md
37_milestone_timeline.md
38_analysis_universe_and_common_support.md
39_event_window_freeze_schema.md
40_time_integrity_and_alignment_plan.md
41_label_ground_truth_quality_registry.csv
42_evidence_source_dependency_registry.csv
43_blinding_access_ledger.csv
44_prompt_version_manifest.md
45_statistical_estimand_and_score_semantics.md
46_hypothesis_registry.csv
manifests/
logs/
schemas/
```

`14_professor_meeting_brief.md`는 2~3쪽 분량으로 다음 질문에 답한다.

1. 두 연구를 하나의 박사논문으로 묶을 학술적 공통분모는 무엇인가?
2. 실제 시공간 중첩이 충분한가, 아니면 방법론 통합이 타당한가?
3. 두 논문과 박사논문의 각각 독립 공헌은 무엇인가?
4. 현재 가장 큰 연구위험과 추가자료는 무엇인가?
5. 지도교수에게 결정받아야 할 3~5개 사항은 무엇인가?

---

## 16. 최초 응답 형식

첫 응답은 장황한 작업일지가 아니라 다음 순서로 작성한다.

1. **한 문장 결론** — 현재 통합연구가 가능한지와 가장 유력한 Mode A/B/C
2. **경로·안전검사 결과**
3. **실제로 확인한 자료 규모** — observed와 prior_reported 구분
4. **기존 연구자산과 진행상태**
5. **통합기간·공통지지집합 판정** — 공통 종료일, `D_BOTH_VALID`, 잠정 `S_COMMON_SUPPORT`; 사건후보 동결 전이면 `A_NMEA`, `A_RINEX`, `A_UNION`, `A_SAME_DAY`는 아직 미생성이라고 명시
6. **NMEA와 RINEX의 공통점·차이·결합불가 요소**
7. **잠정 박사논문 제목 3개** — 국문/영문, 주장 강도별
8. **권고 연구모형과 핵심 RQ**
9. **두 논문–박사논문 장 매핑**
10. **시공간 중첩 감사계획 또는 계산결과**
11. **중대 위험·추가자료·결정사항**
12. **생성한 파일 목록과 다음 실행단계**

실제 확인하지 못한 항목을 채워 넣지 말라. 막혔다면 어디서 왜 막혔고, 무엇이 있어야 재개되는지 정확히 쓴다.

---

## 17. 박사논문 제목의 표현 강도 원칙

실제 증거등급에 맞추어 제목을 선택한다.

### 보수적·현재 권고형

**국문 잠정안**  
이동체 NMEA와 고정 CORS RINEX 이종 관측자료를 이용한 GNSS 전파교란 양립 이상 탐지 및 다중규모 증거통합

**영문 잠정안**  
Multiscale Evidence Fusion for GNSS Interference-Compatible Anomaly Detection Using Mobile NMEA and Fixed CORS RINEX Observations

공식 사건과 독립 RF 증거가 충분하지 않으면 `GNSS interference detection` 또는 `jamming and spoofing detection`을 확정형 제목으로 사용하지 않는다. 연구 진행 후 E4/E5 사례와 일반화 성능이 충분할 때만 더 강한 제목을 제안한다.

---

## 18. 중단조건

다음 중 하나면 무리하게 계속하지 말고 `BLOCKED` 보고서를 작성한다.

- 원본경로 미존재 또는 읽기권한 없음
- 지정 통합연구 작업경로가 원본 내부이거나 저장공간 부족
- 지정 통합연구 작업경로의 기존 내용과 충돌하여 안전한 재개·버전분리가 불가능함
- 기존 스크립트가 원본을 수정·삭제할 위험
- NMEA 장치·시간·문장 provenance를 구분할 수 없음
- RINEX 헤더와 epoch를 신뢰성 있게 파싱할 수 없음
- 시공간 중첩이 없는데 직접 fusion 성능을 요구받음
- 공식 사건정보 누설로 blind evaluation이 불가능하고 독립 holdout도 없음
- 라벨수가 너무 적어 계획한 통계·AI 평가가 성립하지 않음
- 핵심 수치의 provenance를 복원할 수 없음
- IRB·데이터 이용승인의 필요 여부가 판정되지 않았거나, `required`인데 승인 전 분석·공개를 시도함
- 사건 좌표·시각의 공개 수준이 보안 민감시설 노출 위험을 배제하지 못함(이 경우 내부 비공개 분석과 공개·배포 중단을 구분, §20.4)

중단은 실패가 아니라 연구의 주장범위를 보호하는 품질관리다. 가능한 대체연구 Mode와 필요한 보완자료를 함께 제시한다.

---

## 19. 지금 수행할 명령

지금은 다음만 수행하라.

1. 위 실행계약을 짧게 재진술하여 이해를 확인한다.
2. 두 경로의 존재·읽기 가능성·작업경로 안전성을 확인한다.
3. 원본을 수정하지 않는 Phase 0~2 감사계획을 세우고 실행한다.
4. 대량 파일목록을 화면에 뿌리지 말고 집계 산출물로 저장한다.
5. 실제 파일에서 확인된 내용만으로 최초 산출물과 최초 응답을 작성한다.
6. `research_charter_v1` 동결 전 전국 전수 신규분석·모델학습은 시작하지 않는다.

사소한 사항을 반복 질문하지 말고 안전한 범위에서 자율적으로 진행하라. 다만 원본 손상 가능성, 출력경로 선택, 연구주장을 바꾸는 핵심 의사결정, 대규모 추가 다운로드·설치·비용이 필요한 경우에는 이유와 선택지를 제시하고 승인을 기다려라.

---

## 20. 윤리·거버넌스·포지셔닝·재현성 보완 (v1.6 신설)

§1~§19의 방법론적 실행계약은 그대로 유지한다. 본 절은 방법론이 아니라 **박사논문 심사·기관 승인·출판 단계에서 별도로 요구되는 절차**를 다룬다. `research_charter_v1`(§13 Phase 5)을 동결하기 전, 최소한 20.1~20.3은 착수하여 상태를 `research_charter_v1.md`와 `12_decision_log.md`에 함께 기록한다.

### 20.1 연구윤리·데이터 거버넌스

- **개인정보/이동궤적**: NMEA 궤적은 차량·운전자 식별이 가능한 잠재적 개인정보로 취급한다. 소속기관 IRB(생명윤리위원회) 심의 대상 여부를 먼저 판정하고, 대상이면 심의 완료 전 신규 궤적 수집·확대 분석을 시작하지 않는다. `required | not_required_with_basis | pending | approved` 상태, 판정기관·근거·심의번호를 `26_data_ethics_review.md`에 기록한다.
- **CORS 자료 이용범위**: RINEX 자료의 출처기관(예: 국토지리정보원 등 CORS 운영기관)이 정한 이용약관·재배포·논문공개 범위를 확인하고, 전국 자료 또는 그 파생 통계를 논문 부록·오픈데이터로 공개하기 전 별도 승인 필요 여부를 `27_data_use_agreement_status.md`에 `required | not_required_with_basis | pending | approved`와 사실상태를 함께 기록한다. 관측소 수는 실제 전수목록 확인 전 특정 숫자로 단정하지 않는다.
- **이해상충(COI)**: Windows 경로나 폴더명만으로 소속·소유권·거래관계를 추정하지 않는다. 실제 고용·계약·자료소유·IP·연구비·상업적 이해관계를 확인하여 `28_conflict_of_interest_disclosure.md`에 명시하고 필요한 경우 지도교수·심사위원에게 사전 고지한다.
- `not_required_with_basis`는 담당기관·규정·판정근거가 기록된 경우 승인 누락으로 취급하지 않는다. 필요여부가 `pending`이거나 `required`인데 승인되지 않은 관련 활동만 중단한다.

### 20.2 통계적 엄밀성 보완 — 다중비교·검정력·사전등록

- **다중비교 보정**: 다수 관측소×feature×기간을 훑는 모든 절차에 BH를 일괄 적용하지 않는다. 먼저 후보선별인지 p-value 기반 추론인지 구분한다. 유효한 p-value와 검정가족이 정의되면 의존구조를 검토하여 BH/BY, 계층적 FDR, cluster/permutation 또는 max-statistic 중 방법과 보정단위를 사전에 동결한다. 비지도 anomaly score에는 경험적 null, negative control과 노출단위당 오경보를 우선 사용한다.
- **검정력/최소검출가능효과크기(MDES)**: 희귀사건 특성상 현재 표본·기간으로 어떤 크기의 효과까지 검출 가능한지 event/day/route/station의 의존성과 실제 coverage를 반영한 simulation 또는 타당한 근사로 추정하여 `30_multiple_testing_and_power_plan.md`에 기록한다. 추정이 불가능하면 `unassessable`로 명시하고 이유를 남긴다.
- **사전등록**: §4.3/§5.0의 blind detection·code/config hash 동결과 별도로, 가능하면 기관 또는 OSF 등 제3자가 확인 가능한 사전등록(문서 해시·타임스탬프)을 `31_preregistration_record.md`로 남겨 사후조정 위험을 낮춘다. 사전등록이 의혹이나 편향을 ‘원천적으로 배제한다’고 과장하지 않는다. 불가능하면 사유와 대체 동결절차를 명시한다.

### 20.3 국내 공식 외부검증 소스 목록화

§11.3의 외부 보완조사 대상은 국제표준·연구문헌 중심이다. 국내 사례 연구이므로 다음을 `32_domestic_external_corroboration_sources.md`에 기관·자료종류·접근절차·공개범위·신뢰순위와 함께 목록화하고, §9 증거등급의 E4-X/E5-C 판정과 반증검토에 사용한다. 실제 접근 가능 여부와 절차를 확인하기 전에는 `configured`로만 기록한다.

- 과학기술정보통신부·중앙전파관리소: GPS 전파혼신 감시·국민행동요령·공식 상황발표·관계기관 대응자료
- 국토교통부·항공교통본부 항공정보통합관리(AIM): NOTAM·PIB·항공정보와 접근 가능한 운항 영향자료
- 해양수산부·해양경찰청·국립해양조사원: 국내 항행경보·항행통보·선박 신고·안전조치 자료. NAVAREA XI 자료는 조정국·원발행기관과 재인용 관계를 별도로 확인
- 국방부·합동참모본부 및 정부 공식 브리핑: 안보 관련 교란 사건의 발표시각·대상범위·표현강도
- 우주항공청 우주환경센터 및 자료 생산 당시 담당기관: GNSS TEC·ROTI·S4 등 우주기상·전리층 반증자료
- GNSS 운영기관·IGS 등 공식 상태정보: 위성·궤도·시계·관측소 장비/서비스 이상 반증자료
- GPSJam 등 민간 크라우드소싱 지도: 원자료·알고리즘·coverage·재인용 여부를 검증한 뒤 보조자료로만 사용

기관명·담당업무·사이트·자료보존기간은 연구 수행시점에 다시 확인하고, 현재 기관명을 과거 연도의 자료 생산기관에 소급 적용하지 않는다.

### 20.4 이중용도(Dual-use)·보안 민감성 검토

전파교란 사건의 정밀 좌표·시각·탐지 임계값 공개는 군사·항만·공항 등 보안 민감시설의 위치를 노출할 수 있다. 공개 산출물(논문 본문·부록·오픈데이터·발표자료)에 사건 위치를 포함하기 전 다음을 `29_dual_use_security_review.md`에 기록한다.

- 사건 좌표를 원좌표 그대로 공개할지, 격자화·반올림·행정구역 단위로 일반화하여 공개할지 결정
- 보안 민감시설 인근 사건에 대한 별도 마스킹·비공개 처리 여부
- 필요시 관계기관·지도교수의 사전 검토 절차
- 이 검토가 완료되지 않은 사건 좌표는 §18 중단조건에 따라 공개 산출물에서 제외한다.

### 20.5 시간적 변화(drift)와 일반화 한계

2021~2026의 장기간 동안 위성군·신호·수신기/CORS 장비 변경은 §4.1/R0-R에서 이미 다루지만, **교란 기법의 고도화·보급 양상 변화**(예: SDR 기반 정교한 spoofing)와 데이터 생성체계 변화는 별도로 다룬다. covariate drift, concept drift, label/coverage drift를 구분한다. `34_temporal_drift_and_generalization_note.md`에 다음을 기록하고, 결론(§12 8장)의 한계 서술에 반드시 반영한다.

- 학습·동결된 탐지기가 관측기간 이후의 새로운 교란기법에는 일반화를 보장하지 않는다는 한계를 명시
- 가능하면 기간을 분할한 시간적 안정성(temporal stability) 점검을 수행하고, 불가능하면 `unassessable`로 표시

### 20.6 학술적 novelty 포지셔닝

§11 문헌검토는 원문 정독 절차를 강제하지만, 선행연구 대비 본 연구의 고유 기여를 좌표화하는 산출물이 없었다. `33_novelty_positioning_table.md`에 가장 근접한 선행연구(NMEA-only, RINEX-only, crowd-sourced GNSS 이상탐지 등 계열별)와 본 연구를 데이터·관측계층·증거등급·검증방식 축으로 비교하고, 각 논문·박사논문 장이 주장하는 novel contribution을 1문장씩 명시한다. 이 표는 §12 논문 포트폴리오 설계와 연동한다.

### 20.7 재현성 도구·버전관리 구체화

§14의 재현성 계약은 도구중립적으로 설계되어 있으므로, 실제 사용할 스택을 `35_reproducibility_toolchain.md`에 확정한다(예시이며 실제 감사 후 조정).

- RINEX/NMEA 파싱 라이브러리 선택과 근거(예: georinex, RTKLIB, teqc, pynmea2 등). 유지보수 상태·지원 RINEX version을 확인하고 대표표본을 독립 parser 또는 수작업 기준값과 교차검증
- 대용량 원자료·중간산출물 식별·버전관리 방식. DVC/git-lfs는 라이선스·용량·원본 비파괴 원칙을 통과한 파생자료에만 검토하고 원자료 자동복제는 금지
- 파이프라인 오케스트레이션과 체크포인트/재시작 방식(예: Snakemake, Nextflow)
- config hash·code hash·실행기록 추적 도구(예: MLflow 등)
- 공개 가능한 재현 패키지의 아카이빙 계획(예: Zenodo DOI) 및 비식별화·라이선스 범위

### 20.8 심사(디펜스) 대응 준비

`36_defense_readiness_checklist.md`에 예상 심사질문과 현재 근거를 표로 정리하고 지도교수 미팅 전에 갱신한다. 최소 포함 질문:

- 관측된 이상이 수신기·firmware 결함이 아님을 어떻게 배제했는가
- 오탐률/False Discovery Rate 추정치와 근거는 무엇인가
- 다른 국가·다른 수신기 환경으로 일반화되는가, 그 한계는 무엇인가
- Mode A/B/C 중 실제 채택한 모드와 그 근거

### 20.9 일정과 산출물 연동

`37_milestone_timeline.md`에 §13 Phase 0~7, 두 논문 투고 시점, 박사논문 심사 일정(제안발표·중간심사·최종심사)을 하나의 시간축으로 정리하고, `14_professor_meeting_brief.md`의 의사결정 요청사항과 연동한다.

이 절의 산출물이 모두 없어도 §0~§19의 감사·집필 작업 자체를 중단할 필요는 없으나, `research_charter_v1` 동결 및 논문·박사논문 최종 제출 전에는 20.1~20.4를 반드시 `PASS` 또는 명시적 `N/A(사유)`로 판정한다.

## 21. v1.7 식별가능성·블라인딩·검증 동기화 게이트

다음 일곱 항목은 서로 독립된 부가 권고가 아니라 Phase 5 연구헌장과 Phase 7 통합분석의 강제 PASS 게이트이다.

1. **사건 우선**: 사건/시간창 후보를 먼저 동결하고 날짜집합은 파생한다. 날짜 일치가 사건 생성의 원인이 되어서는 안 된다.
2. **공통지지집합**: 같은 날짜의 파일 존재가 아니라 실제 시간·공간·품질 coverage가 겹치는 `S_COMMON_SUPPORT`를 구축하고 평가분모를 명시한다.
3. **시각 무결성**: 독립 시스템시각이 없는 NMEA는 절대시각 무결성을 자체 검증할 수 없다. 의심 시 정밀 시간 corroboration과 E4-X를 제한한다.
4. **라벨 품질**: 공식발표·전문가판정·민간지도·약한 라벨·미라벨을 구분하고, 확인범위 밖의 epoch를 자동 음성으로 만들지 않는다.
5. **증거 의존성**: 같은 원보고서·수신기·공통 GNSS 원인을 공유하는 자료를 독립증거로 중복 계산하지 않는다.
6. **정보방화벽**: 로컬 원문은 모두 읽되 사건일 정보에 대한 접근주체와 시점을 기록한다. 오염된 기간은 독립 holdout 없이 blind 성능으로 보고하지 않는다.
7. **통계 의미**: anomaly score·p-value·확률·증거등급을 분리하고, 각 수치의 estimand·분모·라벨·보정법을 명시한다.

다음 산출물이 서로 모순 없이 연결되어야 PASS이다.

```text
38_analysis_universe_and_common_support.md
39_event_window_freeze_schema.md
40_time_integrity_and_alignment_plan.md
41_label_ground_truth_quality_registry.csv
42_evidence_source_dependency_registry.csv
43_blinding_access_ledger.csv
44_prompt_version_manifest.md
45_statistical_estimand_and_score_semantics.md
46_hypothesis_registry.csv
```

하나라도 미완료이면 데이터 감사와 방법개발은 계속할 수 있으나, 통합 성능향상·민감도·특이도·원인확정·E4-X/E5-C 주장은 `CONDITIONAL` 또는 `unassessable`로 제한한다.

## MASTER PROMPT 끝

---

## 재개용 짧은 프롬프트

첫 감사 세션이 끝난 다음에는 아래 문구로 재개한다.

```text
이전 세션에서 생성한 00_PROJECT_README_KO.md, 12_decision_log.md,
15_next_stage_execution_plan.md와 최신 manifest/log를 먼저 읽어라.
원본 NMEA·RINEX 폴더는 계속 읽기 전용으로 유지한다.
완료된 PASS 단계를 재실행하지 말고, 미완료 또는 CONDITIONAL PASS 항목부터 재개하라.
모든 새 결과에 input manifest id, config hash, code hash와 상태어
(observed/derived/configured/assumed/unavailable/unassessable)를 남겨라.
이번 세션의 목표, 예상 계산량, 중단조건을 먼저 10줄 이내로 보고한 뒤 진행하라.
```
