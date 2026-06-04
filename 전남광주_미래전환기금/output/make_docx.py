"""
전남광주 미래전환기금 — 민형배 시장 보고용 DOCX 보고서
디자인: 전남(#1B5E20)·광주(#1565C0)·네이비(#1A237E) 컬러
폰트:  맑은 고딕 (정부 문서 표준 폴백)
"""

from docx import Document
from docx.shared import Pt, RGBColor, Inches, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

# ── 색상 ──
C_GWANGJU = RGBColor(0x15, 0x65, 0xC0)
C_JEONNAM = RGBColor(0x1B, 0x5E, 0x20)
C_NAVY    = RGBColor(0x1A, 0x23, 0x7E)
C_GOLD    = RGBColor(0xC8, 0x8A, 0x00)
C_DARK    = RGBColor(0x21, 0x21, 0x21)
C_GRAY    = RGBColor(0x60, 0x60, 0x60)
C_RED     = RGBColor(0xC6, 0x28, 0x28)
C_WHITE   = RGBColor(0xFF, 0xFF, 0xFF)

FONT = "맑은 고딕"

doc = Document()

# 기본 스타일 폰트 지정
style = doc.styles["Normal"]
style.font.name = FONT
style.font.size = Pt(10.5)
style._element.rPr.rFonts.set(qn("w:eastAsia"), FONT)

# 여백
for section in doc.sections:
    section.top_margin = Cm(2.0)
    section.bottom_margin = Cm(2.0)
    section.left_margin = Cm(2.2)
    section.right_margin = Cm(2.2)


def set_kfont(run, name=FONT):
    run.font.name = name
    rPr = run._element.get_or_add_rPr()
    rFonts = rPr.find(qn("w:rFonts"))
    if rFonts is None:
        rFonts = OxmlElement("w:rFonts")
        rPr.append(rFonts)
    rFonts.set(qn("w:eastAsia"), name)


def shade_cell(cell, hex_color):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hex_color)
    tcPr.append(shd)


def para(text="", size=10.5, bold=False, color=C_DARK,
         align=None, space_after=6, space_before=0, italic=False):
    p = doc.add_paragraph()
    if align:
        p.alignment = align
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.space_before = Pt(space_before)
    if text:
        run = p.add_run(text)
        run.font.size = Pt(size)
        run.font.bold = bold
        run.font.italic = italic
        run.font.color.rgb = color
        set_kfont(run)
    return p


def heading(text, level=1):
    """컬러 헤딩"""
    if level == 1:
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(16)
        p.paragraph_format.space_after = Pt(8)
        # 좌측 바 효과(■)
        run = p.add_run("■ " + text)
        run.font.size = Pt(15)
        run.font.bold = True
        run.font.color.rgb = C_NAVY
        set_kfont(run)
        # 하단 테두리
        pPr = p._element.get_or_add_pPr()
        pBdr = OxmlElement("w:pBdr")
        bottom = OxmlElement("w:bottom")
        bottom.set(qn("w:val"), "single")
        bottom.set(qn("w:sz"), "12")
        bottom.set(qn("w:space"), "4")
        bottom.set(qn("w:color"), "1565C0")
        pBdr.append(bottom)
        pPr.append(pBdr)
    else:
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(4)
        run = p.add_run("▶ " + text)
        run.font.size = Pt(12)
        run.font.bold = True
        run.font.color.rgb = C_JEONNAM
        set_kfont(run)
    return p


def bullet(text, color=C_DARK, size=10.5):
    p = doc.add_paragraph(style="List Bullet")
    p.paragraph_format.space_after = Pt(3)
    run = p.add_run(text)
    run.font.size = Pt(size)
    run.font.color.rgb = color
    set_kfont(run)
    return p


def make_table(headers, rows, header_color="1A237E",
               col_widths=None, zebra=True):
    table = doc.add_table(rows=1, cols=len(headers))
    table.style = "Table Grid"
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    # 헤더
    hdr = table.rows[0].cells
    for i, h in enumerate(headers):
        shade_cell(hdr[i], header_color)
        p = hdr[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(h)
        run.font.bold = True
        run.font.size = Pt(10)
        run.font.color.rgb = C_WHITE
        set_kfont(run)
    # 데이터
    for ri, row in enumerate(rows):
        cells = table.add_row().cells
        for ci, val in enumerate(row):
            if zebra and ri % 2 == 0:
                shade_cell(cells[ci], "EEF3FB")
            p = cells[ci].paragraphs[0]
            run = p.add_run(str(val))
            run.font.size = Pt(9.5)
            run.font.color.rgb = C_DARK
            set_kfont(run)
    if col_widths:
        for ci, w in enumerate(col_widths):
            for row in table.rows:
                row.cells[ci].width = Cm(w)
    return table


def hr():
    p = doc.add_paragraph()
    pPr = p._element.get_or_add_pPr()
    pBdr = OxmlElement("w:pBdr")
    bottom = OxmlElement("w:bottom")
    bottom.set(qn("w:val"), "single")
    bottom.set(qn("w:sz"), "6")
    bottom.set(qn("w:space"), "1")
    bottom.set(qn("w:color"), "CCCCCC")
    pBdr.append(bottom)
    pPr.append(pBdr)


def callout(text, fill="FFF3E0", text_color=C_RED):
    """강조 박스 (1셀 테이블)"""
    t = doc.add_table(rows=1, cols=1)
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = t.rows[0].cells[0]
    shade_cell(cell, fill)
    p = cell.paragraphs[0]
    run = p.add_run(text)
    run.font.bold = True
    run.font.size = Pt(11)
    run.font.color.rgb = text_color
    set_kfont(run)
    doc.add_paragraph().paragraph_format.space_after = Pt(2)


# ════════════════════════════════════════════
# 표지
# ════════════════════════════════════════════
for _ in range(3):
    doc.add_paragraph()

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p.add_run("전남광주특별시")
run.font.size = Pt(18)
run.font.bold = True
run.font.color.rgb = C_JEONNAM
set_kfont(run)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p.add_run("미 래 전 환 기 금")
run.font.size = Pt(36)
run.font.bold = True
run.font.color.rgb = C_NAVY
set_kfont(run)

doc.add_paragraph()
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p.add_run("20조 원을 100년 성장자본으로")
run.font.size = Pt(20)
run.font.bold = True
run.font.color.rgb = C_GWANGJU
set_kfont(run)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p.add_run("국민연금식 장기자산배분 벤치마크 운용방안")
run.font.size = Pt(14)
run.font.color.rgb = C_GRAY
set_kfont(run)

for _ in range(6):
    doc.add_paragraph()

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p.add_run("쓰고 끝나는 20조가 아니라, 매년 돌아오는 20조")
run.font.size = Pt(13)
run.font.italic = True
run.font.color.rgb = C_JEONNAM
set_kfont(run)

for _ in range(4):
    doc.add_paragraph()

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p.add_run("민형배 시장 보고자료  |  2026. 06\n전남광주 미래전환기금 준비위원회")
run.font.size = Pt(11)
run.font.color.rgb = C_GRAY
set_kfont(run)

doc.add_page_break()

# ════════════════════════════════════════════
# 0. 핵심 요약
# ════════════════════════════════════════════
heading("핵심 요약 (Executive Summary)")
para("전남광주특별시가 수령할 중앙정부 지원 재원 20조 원은 단기 지출예산이 아니라 통합특별시의 초기 자본금이다. "
     "이 중 12조 원을 전남광주 미래전환기금으로 제도화하여, 국민연금식 장기·분산·위험관리형 자산배분 원칙을 "
     "벤치마크하고, 공적기금 OCIO 경험이 있는 전문기관을 대상으로 공개경쟁 위탁운용 구조를 설계해야 한다.",
     size=10.5)

make_table(
    ["구분", "핵심 내용"],
    [
        ["무엇을", "중앙정부 지원 재원 20조 중 12조를 미래전환기금으로 제도화"],
        ["어떻게", "국민연금식 자산배분 원칙 벤치마크, OCIO 전문기관 공개경쟁 위탁"],
        ["왜", "4년 소멸성 예산 → 100년 지속 성장자본으로 전환"],
        ["효과", "연 4% 기준 매년 약 4,800억 원 독자 전략재원 (지원 종료 후에도 지속)"],
        ["선결 조건", "특별법·교부조건에 '기금 출연 가능성' 명시 (이것이 없으면 전부 불가)"],
    ],
    header_color="1A237E", col_widths=[3.0, 13.0]
)
doc.add_paragraph()
callout("★ 핵심 슬로건: 쓰고 끝나는 20조가 아니라, 매년 돌아오는 20조", "E3F2FD", C_GWANGJU)

# ════════════════════════════════════════════
# 1. 현황과 문제 인식
# ════════════════════════════════════════════
heading("1. 현황과 문제 인식")
para("전남광주특별시는 광주광역시와 전라남도의 행정통합으로 출범하는 대한민국 최초 초광역 통합특별시이다. "
     "2026년 7월 출범, 인구 약 320만 명의 메가시티를 목표로 하며, 중앙정부는 4년간 최대 20조 원 규모 지원을 검토·발표하였다.")

heading("기존 방식대로 집행하면 어떻게 되는가?", 2)
make_table(
    ["지출 방식", "단기 장점", "구조적 한계"],
    [
        ["SOC·도로·청사", "가시 성과 빠름", "유지관리비 영구 부담, 정치 배분"],
        ["산업단지 조성", "기업유치 명분", "미분양·중복투자 위험"],
        ["보조금 살포", "단기 체감", "의존성 심화, 4년 후 소멸"],
        ["숙원사업 분산", "반발 완화", "전략성 소멸, 100년 계획 불가"],
    ],
    col_widths=[4.0, 4.0, 8.0]
)
doc.add_paragraph()
callout("⚠ 4년 집행 후 재원 소멸 → 유지관리비와 정치갈등만 잔존", "FFEBEE", C_RED)

# ════════════════════════════════════════════
# 2. 두 가지 선택
# ════════════════════════════════════════════
heading("2. 두 가지 선택: 예산 vs 자본")
make_table(
    ["구분", "❌ 전통적 예산 방식", "✅ 미래전환기금 방식 (권장)"],
    [
        ["집행 형태", "SOC·보조금·숙원사업 분산", "직접투자(8조) + 기금(12조) 병행"],
        ["4년 후 재원", "0원 (소멸)", "매년 수익 지속 발생"],
        ["연 4% 수익", "해당 없음", "3,200~4,800억 원"],
        ["20년 후", "유지관리비·정치갈등 잔존", "누적 6.4~9.6조 원 수익"],
        ["통제 가능성", "사후 통제 어려움", "원금보전·지출상한·외부감사·공시"],
    ],
    col_widths=[2.8, 6.4, 6.8]
)

# ════════════════════════════════════════════
# 3. 제안 핵심 - 5대 원칙
# ════════════════════════════════════════════
heading("3. 제안 핵심: 전남광주 미래전환기금 (5대 운용 원칙)")
make_table(
    ["원칙", "내용"],
    [
        ["① 원금보전", "원금은 미래세대 자산 — 임의 사용 금지(재난·위기 시 의회 2/3 동의 예외)"],
        ["② 장기분산", "국내외 주식·채권·대체투자 분산 (국민연금식 벤치마크, 복제 아님)"],
        ["③ 수익지출", "운용수익 범위 내 지출, 연간 지출률 상한 설정(3~4.5%)"],
        ["④ 공공성", "재무수익률 + 지역경제 파급효과 이중목표(Double Bottom Line)"],
        ["⑤ 투명성", "운용성과·지출내역 전면 공개, 외부감사 의무화"],
    ],
    col_widths=[3.0, 13.0]
)

# ════════════════════════════════════════════
# 4. 기금 규모 시나리오
# ════════════════════════════════════════════
heading("4. 기금 규모 시나리오")
make_table(
    ["구분", "8조 기금화", "12조 기금화 (권장)", "15조 기금화"],
    [
        ["직접투자 가용", "12조", "8조", "5조"],
        ["연 4% 수익", "3,200억", "4,800억", "6,000억"],
        ["정치 수용성", "높음", "중간", "낮음"],
        ["장기 재원", "보통", "충분", "풍부"],
        ["시군 갈등 위험", "낮음", "중간", "높음"],
    ],
    col_widths=[3.4, 4.2, 4.6, 3.8]
)
doc.add_paragraph()
callout("★ 권장: 12조 기금화 — 장기성과·현실성·정치 수용성의 최적 균형점", "E8F5E9", C_JEONNAM)

para("권장 재원 배분안", size=11, bold=True, color=C_NAVY, space_before=8)
make_table(
    ["구분", "금액", "용도"],
    [
        ["미래전환기금", "12조 원", "원금보전형 장기 분산운용"],
        ["미래산업 직접투자", "4조 원", "AI·에너지·반도체·바이오"],
        ["농수축산·지역산업", "2조 원", "스마트농업·스마트축산·수산가공"],
        ["생활·교통·교육·의료", "1조 원", "지역균형 생활기반"],
        ["행정통합·디지털전환", "1조 원", "통합행정·데이터플랫폼"],
    ],
    col_widths=[4.5, 3.0, 8.5]
)

# ════════════════════════════════════════════
# 5. 국민연금식 벤치마크
# ════════════════════════════════════════════
heading("5. 운용 구조: 국민연금식 자산배분 벤치마크")
callout("⚠ '국민연금 포트폴리오를 복제'하는 것이 아니라, 장기·분산·위험관리 원칙을 전남광주형으로 벤치마크한다.",
        "FFF3E0", C_GOLD)
make_table(
    ["벤치마크 원칙", "국민연금 현황", "전남광주 적용 방향"],
    [
        ["장기 투자 시계", "10년+ 기준", "영구기금 구조(원금보전)"],
        ["글로벌 분산", "해외 50%+", "해외주식 35%+해외채권 10%"],
        ["중기자산배분", "5년 목표비중", "투자정책서 5년 주기"],
        ["위험관리", "VaR·손실한도", "위원회 한도 설정"],
        ["성과공시", "연간 기금보고서", "분기 공시 의무화"],
        ["직접+위탁 병행", "직접+외부위탁", "OCIO 위탁 중심"],
    ],
    col_widths=[4.0, 5.0, 7.0]
)

# ════════════════════════════════════════════
# 6. 참조 포트폴리오
# ════════════════════════════════════════════
heading("6. 참조 포트폴리오 설계 (초기 5년 권장)")
make_table(
    ["자산군", "기준비중", "허용범위", "목적"],
    [
        ["해외주식", "35%", "±5%", "장기 성장수익"],
        ["국내주식", "10%", "±3%", "국내 산업 연계"],
        ["국내채권", "20%", "±5%", "안정성·유동성"],
        ["해외채권", "10%", "±3%", "분산효과"],
        ["대체투자", "15%", "±5%", "인프라·에너지·부동산·사모"],
        ["유동성", "5%", "±2%", "집행 안정성"],
        ["지역전략투자", "5%", "±2%", "전남광주 미래산업 연계"],
    ],
    col_widths=[3.5, 3.0, 3.0, 6.5]
)
para("환헤지: 해외주식 부분헤지(0~50%) | 해외채권 완전헤지 원칙", size=9.5, color=C_GRAY, space_before=4)

# ════════════════════════════════════════════
# 7. OCIO 구조
# ════════════════════════════════════════════
heading("7. OCIO 위탁운용 구조")
para("OCIO(Outsourced Chief Investment Officer): 자산배분·위험관리·성과평가·운용사 선정을 외부 전문기관에 위탁하는 구조")
para("선정 절차", size=11, bold=True, color=C_NAVY, space_before=6)
para("RFI(시장검증) → RFP(제안요청) → 외부전문가 평가위원회 → 위원회 의결 → 복수기관 분산위탁",
     size=10.5, color=C_GWANGJU, bold=True)
para("RFI 대상 후보군 (모두 동등한 공개경쟁 — 사전 내정 없음)", size=11, bold=True, color=C_NAVY, space_before=6)
para("미래에셋자산운용 · 삼성자산운용 · KB자산운용 · 한국투자신탁운용 · NH투자증권 · 한화자산운용", size=10.5)

# ════════════════════════════════════════════
# 8. 지역전략투자
# ════════════════════════════════════════════
heading("8. 지역전략투자 분야 (기금 5% 내)")
make_table(
    ["분야", "핵심 투자"],
    [
        ["AI", "집적단지 고도화·공공 AI 실증·AI반도체·인재양성"],
        ["에너지", "해상풍력·그린수소·RE100·ESS·스마트그리드"],
        ["반도체", "전력반도체·패키징·소부장·테스트베드"],
        ["농수축산", "스마트팜·스마트축산·유통플랫폼·수산 고부가"],
        ["바이오·헬스", "고령친화·식품바이오·헬스케어데이터·바이오소재"],
        ["모빌리티", "자율주행·정밀지도·드론물류·공간정보"],
        ["청년·대학", "연구펀드·인재정착·창업펀드·산학연"],
    ],
    col_widths=[3.5, 12.5]
)
para("투자 방식 우선순위: 펀드출자(LP) > 공동투자 > 직접투자(원칙 제한)", size=9.5, color=C_GRAY, space_before=4)

# ════════════════════════════════════════════
# 9. 법률 선결 과제
# ════════════════════════════════════════════
heading("9. 법률·제도 선결 과제")
callout("⚠ 최대 리스크: 교부조건 확정 후에는 기금화가 보조금법상 '용도 외 사용'으로 불가능해질 수 있다.",
        "FFEBEE", C_RED)
make_table(
    ["단계", "필수 조치", "핵심 쟁점"],
    [
        ["특별법", "기금 설치 + 지원금 출연 근거", "일반법 특례 부여"],
        ["시행령", "운용·위탁·지출·감독 기준", "위임 범위"],
        ["조례", "목적·재원·위원회·공시·감사", "재정민주주의"],
        ["교부조건", "기금 출연 가능성 명시", "용도 외 사용 회피의 핵심"],
        ["투자정책서", "자산배분·위험한도·지출률", "위원회 의결"],
    ],
    col_widths=[3.0, 7.0, 6.0]
)

# ════════════════════════════════════════════
# 10. 거버넌스
# ════════════════════════════════════════════
heading("10. 기금 거버넌스 (정치 개입 차단)")
make_table(
    ["위원회", "역할"],
    [
        ["미래전환기금운용위원회", "최고 의결 (공무원 의결권 배제)"],
        ["투자정책위원회", "자산배분·목표수익률"],
        ["위험관리위원회", "VaR·손실한도·유동성·환위험"],
        ["지역전략사업위원회", "수익금 사용 심사"],
        ["시민감시위원회", "투명성·이해충돌·정치개입 감시"],
        ["외부감사인", "회계·운용 적정성"],
    ],
    col_widths=[5.0, 11.0]
)
para("10대 차단장치: 투자정책서 사전공시 · 자산군 허용범위 · 특정기업 직접투자 제한 · 지역투자 별도심사 · "
     "위원·회의록 공개 · 외부감사 의무 · 의회보고 의무 · 이해충돌 신고 · 운용기관 공개경쟁 · 성과 공개",
     size=9.5, color=C_GRAY, space_before=4)

# ════════════════════════════════════════════
# 11. 해외사례
# ════════════════════════════════════════════
heading("11. 해외 성공사례 비교")
make_table(
    ["사례", "규모(2025 추정)", "원금보호", "지출준칙", "핵심 시사점"],
    [
        ["노르웨이 GPFG", "약 1.9조 달러", "법적 보호", "실질 3% 룰", "지출준칙·글로벌분산·공시"],
        ["알래스카 영구기금", "약 760억 달러", "헌법 명시", "수익 한도", "원금 헌법보호·주민배당"],
        ["아일랜드 ISIF", "약 130억 유로", "부분", "재무+경제", "Double Bottom Line"],
        ["싱가포르 테마섹", "약 3,820억 SGD", "이사회 자율", "수익중심", "전략산업+독립 거버넌스"],
    ],
    col_widths=[3.5, 3.2, 2.5, 2.5, 4.3]
)

# ════════════════════════════════════════════
# 12. 수익 시뮬레이션
# ════════════════════════════════════════════
heading("12. 수익 시뮬레이션 (12조·연4%·재투자 30%)")
make_table(
    ["시점", "기금규모", "연간수익(4%)", "지출가용(60%)", "재투자(30%)"],
    [
        ["1년", "12.0조", "4,800억", "3,360억", "1,440억"],
        ["5년", "12.9조", "5,160억", "3,612억", "1,548억"],
        ["10년", "14.1조", "5,640억", "3,948억", "1,692억"],
        ["20년", "16.9조", "6,760억", "4,732억", "2,028억"],
        ["30년", "20.2조", "8,080억", "5,656억", "2,424억"],
    ],
    col_widths=[2.5, 3.0, 3.5, 3.5, 3.5]
)
para("⚠ 단순 산술 참조값. 수수료·세금·환율·시장변동 미반영. 미래 수익 보장 아님.",
     size=9, italic=True, color=C_GRAY, space_before=4)

# ════════════════════════════════════════════
# 13. 이해당사자별 설득 논리
# ════════════════════════════════════════════
heading("13. 이해당사자별 설득 논리")
make_table(
    ["대상", "한 줄 메시지"],
    [
        ["민형배 시장", "임기 성과(8조) + 임기 후 지속재원(12조)의 균형 = 100년 레거시"],
        ["중앙정부", "예산낭비 방지·지방재정 책임성·균형발전 표준모델"],
        ["국회", "원금보전·지출상한·외부감사·공시 = 가장 통제하기 쉬운 구조"],
        ["지역주민", "한 번 쓰는 20조 vs 매년 돌아오는 20조"],
        ["금융기관", "국내 최초급 지방정부형 대규모 장기 OCIO"],
    ],
    col_widths=[3.0, 13.0]
)

# ════════════════════════════════════════════
# 14. 예상 반론 Q&A
# ════════════════════════════════════════════
heading("14. 예상 반론 Q&A")
qas = [
    ("당장 쓸 곳 많은데 왜 묶나?", "전액 아닌 12조만. 8조는 즉시 직접투자"),
    ("손실 나면?", "위탁·분산·한도·감사·지출상한 제도화. 전액 소비는 소멸 확정"),
    ("국민연금 못 맡기면 불가능?", "원칙 벤치마크 + OCIO 공개경쟁으로 가능"),
    ("미래에셋 특혜?", "후보군 중 하나, 복수기관 공개경쟁"),
    ("국고지원금 투자 불법?", "교부조건·특별법·조례에 근거 사전 명시"),
    ("직접 쓰는 게 낫지 않나?", "8조 직접투자 병행. 기금은 지속성 확보"),
    ("시장 나빠지면?", "10년 장기평균·3~5년 평균 평가액 기준"),
]
make_table(
    ["반론", "핵심 답변"],
    qas,
    col_widths=[5.5, 10.5]
)

# ════════════════════════════════════════════
# 15. 로드맵
# ════════════════════════════════════════════
heading("15. 추진 로드맵 (6개월)")
make_table(
    ["단계", "기간", "핵심 작업"],
    [
        ["① 개념 정립", "~1개월", "기본구상·시나리오·당선자 보고자료"],
        ["② 법률·제도", "1~2개월", "특별법 검토·조례안·교부조건·외부법률자문"],
        ["③ RFI", "2~3개월", "OCIO 후보군 시장검증"],
        ["④ 보고서 확정", "3~4개월", "본보고서·법률안·투자정책서 초안"],
        ["⑤ 정치·입법", "4~6개월", "캠프·중앙정부·국회·시민공론화"],
    ],
    col_widths=[3.2, 2.5, 10.3]
)
doc.add_paragraph()
callout("★ 골든타임: 특별법·교부조건 협상 단계가 기금화 성패를 가른다 — 출범(2026.07) 전후가 최적 시점",
        "FFEBEE", C_RED)

# ════════════════════════════════════════════
# 16. 결론
# ════════════════════════════════════════════
heading("16. 결론 및 8대 정책 제언")
para("전남광주는 20조 원을 소비하는 도시가 아니라, 자본화하여 대한민국 균형발전의 새 표준을 만드는 도시가 되어야 한다.",
     size=11, bold=True, color=C_NAVY)
recs = [
    "① 원금은 원칙적으로 보전한다",
    "② 운용수익 중심으로 지출한다",
    "③ 국민연금식 자산배분 원칙을 벤치마크한다 (복제 아님)",
    "④ 전문기관은 RFI·공개경쟁으로 검토한다 (특혜 차단)",
    "⑤ 특별법·시행령·조례·교부조건에 법적 근거를 명시한다 (최우선)",
    "⑥ 지역전략투자는 전체의 일부로 제한한다",
    "⑦ AI·에너지·농수축산·바이오·모빌리티·청년·대학에 집중한다",
    "⑧ 모든 성과·지출을 공개한다",
]
for r in recs:
    bullet(r, color=C_DARK)

doc.add_paragraph()
para("지금 당장 필요한 결정", size=12, bold=True, color=C_GWANGJU, space_before=8)
nows = [
    "1. 특별법·교부조건 협상 시 '기금 출연 가능성' 명시",
    "2. 법률자문 즉시 의뢰 (보조금법·지방기금법 검토)",
    "3. 기금 규모 정치적 결정 (권장: 12조 기금 + 8조 직접투자)",
    "4. OCIO 후보군 RFI 준비 (공개경쟁 원칙 천명)",
    "5. 기금운용위원회 구성 착수 (공무원 의결권 배제 설계)",
]
for n in nows:
    bullet(n, color=C_DARK)

doc.add_paragraph()
hr()
para("※ 본 문서는 정책 검토 단계 초안이며, 법적 실행 전 전문 법률자문과 관계기관 협의가 반드시 필요합니다. "
     "수익률 수치는 역사적 참조값으로 미래 수익을 보장하지 않습니다.",
     size=9, italic=True, color=C_GRAY)

# ── 저장 ──
out = "/home/user/michaechang_study/전남광주_미래전환기금/output/전남광주_미래전환기금_보고서_민형배시장.docx"
doc.save(out)
print(f"✅ DOCX 저장 완료: {out}")
