"""
전남광주 미래전환기금 — 민형배 시장 보고용 20페이지 PPTX
디자인: 전남(#1B5E20) ↔ 광주(#1565C0) 투톤 그라데이션 + 네이비 강조
폰트:  나눔고딕(폴백: 맑은고딕) / Calibri
"""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.util import Inches, Pt
from pptx.enum.dml import MSO_THEME_COLOR
import pptx.oxml.ns as nsmap
from lxml import etree
import copy

# ── 색상 팔레트 ─────────────────────────────────────────────
C_GWANGJU   = RGBColor(0x15, 0x65, 0xC0)   # 광주 블루
C_JEONNAM   = RGBColor(0x1B, 0x5E, 0x20)   # 전남 그린
C_TEAL      = RGBColor(0x00, 0x89, 0x7B)   # 중간 틸
C_NAVY      = RGBColor(0x1A, 0x23, 0x7E)   # 네이비 (타이틀)
C_GOLD      = RGBColor(0xFF, 0xB3, 0x00)   # 강조 골드
C_LIGHT     = RGBColor(0xE8, 0xF5, 0xE9)   # 연그린 배경
C_LIGHTBLUE = RGBColor(0xE3, 0xF2, 0xFD)   # 연블루 배경
C_WHITE     = RGBColor(0xFF, 0xFF, 0xFF)
C_DARK      = RGBColor(0x21, 0x21, 0x21)
C_GRAY      = RGBColor(0x75, 0x75, 0x75)
C_LGRAY     = RGBColor(0xF5, 0xF5, 0xF5)
C_RED       = RGBColor(0xD3, 0x2F, 0x2F)

# ── 유틸 ────────────────────────────────────────────────────
prs = Presentation()
prs.slide_width  = Inches(13.33)
prs.slide_height = Inches(7.5)
W = prs.slide_width
H = prs.slide_height
BLANK = prs.slide_layouts[6]  # 완전 빈 레이아웃

def add_rect(slide, x, y, w, h, fill=None, line_color=None, line_width=None):
    shape = slide.shapes.add_shape(1, Inches(x), Inches(y), Inches(w), Inches(h))
    shape.line.fill.background()
    if fill:
        shape.fill.solid()
        shape.fill.fore_color.rgb = fill
    else:
        shape.fill.background()
    if line_color:
        shape.line.color.rgb = line_color
        shape.line.width = Pt(line_width or 1)
    else:
        shape.line.fill.background()
    return shape

def add_text(slide, text, x, y, w, h,
             size=20, bold=False, color=C_DARK,
             align=PP_ALIGN.LEFT, wrap=True, italic=False):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = wrap
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = color
    run.font.name = "맑은 고딕"
    return tb

def add_header_bar(slide, title, sub="", bg=C_NAVY, left_accent=C_GOLD):
    """상단 헤더 바"""
    add_rect(slide, 0, 0, 13.33, 1.1, fill=bg)
    add_rect(slide, 0, 0, 0.08, 1.1, fill=left_accent)
    add_text(slide, title, 0.22, 0.1, 10, 0.6,
             size=28, bold=True, color=C_WHITE)
    if sub:
        add_text(slide, sub, 0.22, 0.68, 10, 0.35,
                 size=13, color=RGBColor(0xBB, 0xDE, 0xFB))

def slide_footer(slide, page_num, total=20):
    add_rect(slide, 0, 7.15, 13.33, 0.35, fill=C_NAVY)
    add_text(slide, "전남광주 미래전환기금 | 민형배 시장 보고자료 | 2026.06",
             0.3, 7.17, 9, 0.28, size=9, color=RGBColor(0xBB, 0xDE, 0xFB))
    add_text(slide, f"{page_num} / {total}",
             12.5, 7.17, 0.8, 0.28, size=9,
             color=C_WHITE, align=PP_ALIGN.RIGHT)

def accent_box(slide, x, y, w, h, color, title, value, unit=""):
    add_rect(slide, x, y, w, h, fill=color)
    add_text(slide, title, x+0.1, y+0.05, w-0.2, 0.3,
             size=11, color=C_WHITE, align=PP_ALIGN.CENTER)
    add_text(slide, value, x+0.1, y+0.32, w-0.2, 0.55,
             size=26, bold=True, color=C_WHITE, align=PP_ALIGN.CENTER)
    if unit:
        add_text(slide, unit, x+0.1, y+0.82, w-0.2, 0.25,
                 size=10, color=RGBColor(0xBB, 0xDE, 0xFB), align=PP_ALIGN.CENTER)

def two_col_bullet(slide, items_left, items_right,
                   y_start=1.3, row_h=0.38):
    for i, item in enumerate(items_left):
        y = y_start + i * row_h
        add_text(slide, "▶ " + item, 0.4, y, 5.9, row_h-0.02,
                 size=14, color=C_DARK)
    for i, item in enumerate(items_right):
        y = y_start + i * row_h
        add_text(slide, "▶ " + item, 6.8, y, 5.9, row_h-0.02,
                 size=14, color=C_DARK)

# ════════════════════════════════════════════════════════════
# SLIDE 01 — 표지
# ════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
# 좌측 그라데이션 사이드바 (그린)
add_rect(s, 0, 0, 3.2, 7.5, fill=C_JEONNAM)
add_rect(s, 3.1, 0, 0.15, 7.5, fill=C_TEAL)
# 배경
add_rect(s, 3.2, 0, 10.13, 7.5, fill=C_WHITE)
# 우상단 광주 블루 강조
add_rect(s, 3.2, 0, 10.13, 0.15, fill=C_GWANGJU)

# 사이드바 텍스트
add_text(s, "전남광주\n미래전환기금", 0.2, 0.7, 2.8, 2.0,
         size=24, bold=True, color=C_WHITE, align=PP_ALIGN.CENTER)
add_text(s, "Future\nTransformation\nFund", 0.2, 2.9, 2.8, 1.5,
         size=14, italic=True, color=RGBColor(0xA5, 0xD6, 0xA7),
         align=PP_ALIGN.CENTER)
add_text(s, "보고일: 2026. 06", 0.2, 6.8, 2.8, 0.5,
         size=10, color=RGBColor(0xA5, 0xD6, 0xA7), align=PP_ALIGN.CENTER)

# 로고 영역 (원 심볼 대체)
add_rect(s, 4.0, 0.5, 1.8, 1.8, fill=C_GWANGJU)
add_rect(s, 5.8, 0.5, 1.8, 1.8, fill=C_JEONNAM)
add_text(s, "광", 4.0, 0.8, 1.8, 1.2, size=40, bold=True,
         color=C_WHITE, align=PP_ALIGN.CENTER)
add_text(s, "전남", 5.8, 0.8, 1.8, 1.2, size=40, bold=True,
         color=C_WHITE, align=PP_ALIGN.CENTER)
add_text(s, "전남광주특별시", 3.8, 2.3, 4.0, 0.6,
         size=16, bold=True, color=C_NAVY, align=PP_ALIGN.CENTER)

# 제목
add_text(s, "20조 원을 100년 성장자본으로", 4.0, 3.2, 9.0, 0.9,
         size=34, bold=True, color=C_NAVY)
add_text(s, "전남광주 미래전환기금 조성 및 국민연금식 장기자산배분 운용방안",
         4.0, 4.1, 9.0, 0.6, size=16, color=C_GRAY)
add_rect(s, 4.0, 4.75, 9.0, 0.05, fill=C_GWANGJU)
add_text(s, "민형배 시장 보고자료 | 전남광주통합특별시 출범 대비 재정전략",
         4.0, 4.85, 9.0, 0.4, size=13, color=C_GRAY)
add_text(s, "핵심 슬로건: 쓰고 끝나는 20조가 아니라, 매년 돌아오는 20조",
         4.0, 5.5, 9.0, 0.5, size=15, bold=True, color=C_GWANGJU)
slide_footer(s, 1)

# ════════════════════════════════════════════════════════════
# SLIDE 02 — 목차
# ════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
add_rect(s, 0, 0, 13.33, 7.5, fill=C_LGRAY)
add_header_bar(s, "목  차", "Table of Contents")

contents = [
    ("01", "현황과 문제 인식 — 20조의 기회와 위기",      "3"),
    ("02", "두 가지 선택: 예산 vs 자본",                   "4"),
    ("03", "제안 핵심: 전남광주 미래전환기금",              "5"),
    ("04", "기금 규모 시나리오 (8·12·15조)",               "6"),
    ("05", "운용 구조: 국민연금식 자산배분 벤치마크",       "7"),
    ("06", "참조 포트폴리오 설계",                          "8"),
    ("07", "OCIO 위탁운용 구조",                            "9"),
    ("08", "지역전략투자 분야 (AI·에너지·농수축산 등)",     "10"),
    ("09", "법률·제도 선결 과제",                           "11"),
    ("10", "기금 거버넌스 — 정치 개입 차단 장치",           "12"),
    ("11", "해외 성공사례 비교",                            "13"),
    ("12", "이해당사자별 설득 논리",                        "14"),
    ("13", "예상 반론 Q&A",                                 "15"),
    ("14", "수익 시뮬레이션",                               "16"),
    ("15", "추진 로드맵 (6개월)",                           "17"),
    ("16", "성과지표 체계",                                 "18"),
    ("17", "핵심 슬로건과 메시지",                          "19"),
    ("18", "결론 및 지금 필요한 결정",                      "20"),
]

col1 = contents[:9]
col2 = contents[9:]
for i, (num, title, page) in enumerate(col1):
    y = 1.3 + i * 0.6
    add_rect(s, 0.4, y, 0.5, 0.42, fill=C_GWANGJU)
    add_text(s, num, 0.4, y+0.04, 0.5, 0.38, size=13, bold=True,
             color=C_WHITE, align=PP_ALIGN.CENTER)
    add_text(s, title, 1.0, y+0.04, 5.2, 0.38, size=12, color=C_DARK)
    add_text(s, f"p.{page}", 6.1, y+0.04, 0.5, 0.38, size=10,
             color=C_GRAY, align=PP_ALIGN.RIGHT)

for i, (num, title, page) in enumerate(col2):
    y = 1.3 + i * 0.6
    add_rect(s, 6.8, y, 0.5, 0.42, fill=C_JEONNAM)
    add_text(s, num, 6.8, y+0.04, 0.5, 0.38, size=13, bold=True,
             color=C_WHITE, align=PP_ALIGN.CENTER)
    add_text(s, title, 7.4, y+0.04, 5.0, 0.38, size=12, color=C_DARK)
    add_text(s, f"p.{page}", 12.3, y+0.04, 0.6, 0.38, size=10,
             color=C_GRAY, align=PP_ALIGN.RIGHT)
slide_footer(s, 2)

# ════════════════════════════════════════════════════════════
# SLIDE 03 — 현황과 문제 인식
# ════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
add_header_bar(s, "현황과 문제 인식", "01 | 전남광주특별시 출범과 20조 원의 기회")
# 큰 숫자 강조
accent_box(s, 0.4, 1.3, 2.8, 1.2, C_GWANGJU, "중앙정부 지원 규모", "20조", "원 (4년)")
accent_box(s, 3.4, 1.3, 2.8, 1.2, C_JEONNAM, "통합 인구", "320만", "명")
accent_box(s, 6.4, 1.3, 2.8, 1.2, C_TEAL,    "출범 목표", "2026.07", "전남광주특별시")
accent_box(s, 9.4, 1.3, 3.1, 1.2, C_NAVY,    "4년 후 재원(기존 방식)", "0원", "소멸 확정")

add_text(s, "■ 기존 방식대로 집행하면 어떻게 되는가?",
         0.4, 2.75, 12.5, 0.4, size=15, bold=True, color=C_NAVY)
rows = [
    ("SOC·도로·청사",  "가시 성과 빠름",  "유지관리비 영구 부담, 정치 배분"),
    ("산업단지 조성",   "기업유치 명분",   "미분양·중복투자 위험"),
    ("보조금 살포",     "단기 체감",       "의존성 심화, 4년 후 소멸"),
    ("숙원사업 분산",   "반발 완화",       "전략성 소멸, 100년 계획 불가"),
]
headers = ["지출 방식", "단기 장점", "구조적 한계"]
col_x = [0.4, 3.2, 6.0]
col_w = [2.6, 2.6, 6.8]
for ci, h in enumerate(headers):
    add_rect(s, col_x[ci], 3.25, col_w[ci], 0.36, fill=C_NAVY)
    add_text(s, h, col_x[ci]+0.05, 3.28, col_w[ci]-0.1, 0.3,
             size=12, bold=True, color=C_WHITE, align=PP_ALIGN.CENTER)
for ri, row in enumerate(rows):
    bg = C_LGRAY if ri % 2 == 0 else C_WHITE
    for ci, cell in enumerate(row):
        add_rect(s, col_x[ci], 3.65+ri*0.42, col_w[ci], 0.4, fill=bg,
                 line_color=RGBColor(0xCC,0xCC,0xCC), line_width=0.5)
        clr = C_RED if ci == 2 else C_DARK
        add_text(s, cell, col_x[ci]+0.08, 3.67+ri*0.42, col_w[ci]-0.16, 0.38,
                 size=12, color=clr)
add_text(s, "⚠  4년 집행 후 재원 소멸 → 유지관리비와 정치갈등만 잔존",
         0.4, 5.45, 12.5, 0.4, size=13, bold=True, color=C_RED)
add_rect(s, 0.4, 5.45, 12.5, 0.38, fill=RGBColor(0xFF,0xEB,0xEE))
add_text(s, "⚠  4년 집행 후 재원 소멸 → 유지관리비와 정치갈등만 잔존",
         0.5, 5.5, 12.3, 0.38, size=13, bold=True, color=C_RED)
add_text(s, "→ 전남광주특별시는 20조 원을 '소비'하는 도시가 아니라 '자본화'하는 도시가 되어야 한다",
         0.4, 6.0, 12.5, 0.4, size=13, bold=True, color=C_NAVY)
slide_footer(s, 3)

# ════════════════════════════════════════════════════════════
# SLIDE 04 — 두 가지 선택
# ════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
add_header_bar(s, "두 가지 선택: 예산 vs 자본",
               "02 | 전통적 예산 방식과 미래전환기금 방식의 비교")

add_rect(s, 0.3, 1.2, 5.9, 5.5, fill=RGBColor(0xFF,0xEB,0xEE))
add_rect(s, 6.5, 1.2, 6.5, 5.5, fill=RGBColor(0xE8,0xF5,0xE9))

add_rect(s, 0.3, 1.2, 5.9, 0.55, fill=C_RED)
add_text(s, "❌  전통적 예산 방식", 0.5, 1.25, 5.7, 0.45,
         size=16, bold=True, color=C_WHITE)
add_rect(s, 6.5, 1.2, 6.5, 0.55, fill=C_JEONNAM)
add_text(s, "✅  미래전환기금 방식 (권장)", 6.7, 1.25, 6.3, 0.45,
         size=16, bold=True, color=C_WHITE)

left_items = [
    "20조 원 → SOC·보조금·숙원사업 분산 집행",
    "4년 집행 → 재원 0원 소멸 (확정)",
    "완공 후 유지관리비 영구 증가",
    "선거 주기 중심, 단기성과 편향",
    "중앙 지원 종료 후 독자 재원 없음",
    "정치적 배분 → 전략성 소멸",
    "미래세대에게 빚과 유지비만 남김",
]
right_items = [
    "12조 기금 + 8조 직접전략투자 병행",
    "연 4% 기준 → 매년 4,800억 원 수익 지속",
    "원금 보전 → 100년 후에도 작동",
    "국민연금식 장기분산·위험관리 벤치마크",
    "중앙 지원 종료 후에도 독자 전략재원 확보",
    "공개경쟁 OCIO → 정치 개입 차단",
    "미래세대에게 지속 가능한 성장자본 승계",
]
for i, item in enumerate(left_items):
    y = 1.9 + i * 0.6
    add_text(s, item, 0.5, y, 5.5, 0.55, size=13, color=C_DARK)
for i, item in enumerate(right_items):
    y = 1.9 + i * 0.6
    add_rect(s, 6.55, y+0.05, 0.25, 0.3, fill=C_JEONNAM)
    add_text(s, item, 6.9, y, 5.9, 0.55, size=13, color=C_DARK)

add_text(s, "20년 누적 수익(12조·4%): 약 9.6조 원",
         6.7, 6.15, 5.9, 0.4, size=14, bold=True, color=C_JEONNAM)
slide_footer(s, 4)

# ════════════════════════════════════════════════════════════
# SLIDE 05 — 제안 핵심
# ════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
add_header_bar(s, "제안 핵심: 전남광주 미래전환기금",
               "03 | 5대 설계 원칙")

# 중앙 큰 메시지
add_rect(s, 0.4, 1.2, 12.5, 0.8, fill=C_NAVY)
add_text(s, '"20조 원을 100년 성장자본으로"',
         0.6, 1.28, 12.1, 0.65, size=26, bold=True,
         color=C_GOLD, align=PP_ALIGN.CENTER)

principles = [
    (C_GWANGJU, "①  원금보전", "원금은 미래세대 자산\n임의 사용 금지 (재난·위기 시 의회 2/3 동의)"),
    (C_JEONNAM, "②  장기분산", "국내외 주식·채권·대체투자 분산\n국민연금식 원칙 벤치마크 (복제 아님)"),
    (C_TEAL,    "③  수익지출", "운용수익 범위 내 지출\n연간 지출률 상한 설정 (3~4.5%)"),
    (C_NAVY,    "④  공공성",   "재무수익률 + 지역 파급효과\nDouble Bottom Line"),
    (C_GOLD,    "⑤  투명성",   "운용성과·지출 전면 공개\n외부감사·의회보고 의무화"),
]
box_w = 2.35
for i, (color, title, desc) in enumerate(principles):
    x = 0.3 + i * (box_w + 0.15)
    add_rect(s, x, 2.2, box_w, 4.4, fill=color)
    add_text(s, title, x+0.1, 2.3, box_w-0.2, 0.6,
             size=16, bold=True, color=C_WHITE, align=PP_ALIGN.CENTER)
    add_rect(s, x+0.1, 2.92, box_w-0.2, 0.04, fill=C_WHITE)
    add_text(s, desc, x+0.1, 3.0, box_w-0.2, 2.8,
             size=12, color=C_WHITE, align=PP_ALIGN.CENTER)

add_text(s, "★ 핵심 선결 과제: 특별법·교부조건에 '기금 출연 가능성' 명시 — 교부조건 확정 전이 골든타임",
         0.4, 6.7, 12.5, 0.4, size=12, bold=True, color=C_RED)
slide_footer(s, 5)

# ════════════════════════════════════════════════════════════
# SLIDE 06 — 기금 규모 시나리오
# ════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
add_header_bar(s, "기금 규모 시나리오",
               "04 | 8조 / 12조 / 15조 비교 및 권장안")

scenarios = [
    ("8조 원\n기금화",  "12조 원\n기금화 ★",  "15조 원\n기금화"),
    (C_GWANGJU,        C_JEONNAM,             C_TEAL),
    ("직접투자: 12조\n정치 수용성: 높음\n시군 갈등: 낮음",
     "직접투자: 8조\n정치 수용성: 중간\n시군 갈등: 중간",
     "직접투자: 5조\n정치 수용성: 낮음\n시군 갈등: 높음"),
]
cols = [
    ("연 3%", "2,400억", "3,600억", "4,500억"),
    ("연 4%", "3,200억", "4,800억", "6,000억"),
    ("연 5%", "4,000억", "6,000억", "7,500억"),
]
bx = [0.4, 4.6, 8.8]
bw = 4.0
for i in range(3):
    clr = [C_GWANGJU, C_JEONNAM, C_TEAL][i]
    add_rect(s, bx[i], 1.2, bw, 0.7, fill=clr)
    add_text(s, scenarios[0][i], bx[i]+0.1, 1.24, bw-0.2, 0.62,
             size=17, bold=True, color=C_WHITE, align=PP_ALIGN.CENTER)
    add_text(s, scenarios[2][i], bx[i]+0.1, 1.98, bw-0.2, 0.9,
             size=12, color=C_DARK, align=PP_ALIGN.CENTER)

# 수익표
row_labels = ["연 3% 수익", "연 4% 수익 ★", "연 5% 수익"]
for ri, row in enumerate(cols):
    y = 3.05 + ri * 0.65
    bg = RGBColor(0xFF,0xF9,0xC4) if ri == 1 else (C_LGRAY if ri%2==0 else C_WHITE)
    for ci in range(4):
        xx = 0.4 if ci == 0 else bx[ci-1]
        ww = 1.8 if ci == 0 else bw
        add_rect(s, xx, y, ww, 0.6, fill=bg,
                 line_color=RGBColor(0xDD,0xDD,0xDD), line_width=0.5)
        add_text(s, row[ci], xx+0.08, y+0.05, ww-0.16, 0.5,
                 size=14, bold=(ri==1), color=C_DARK, align=PP_ALIGN.CENTER)

add_text(s, "★ 권장: 12조 기금화 — 장기성과·현실성·정치 수용성의 최적 균형점",
         0.4, 5.1, 12.5, 0.45, size=14, bold=True, color=C_JEONNAM)
add_rect(s, 0.4, 5.1, 12.5, 0.42, fill=RGBColor(0xE8,0xF5,0xE9))
add_text(s, "★ 권장: 12조 기금화 — 장기성과·현실성·정치 수용성의 최적 균형점",
         0.6, 5.15, 12.1, 0.42, size=14, bold=True, color=C_JEONNAM)

add_text(s, "복리 재투자 30% 시: 30년 후 기금 원금 약 20.2조로 성장, 연 지출 가용액 5,656억",
         0.4, 5.7, 12.5, 0.35, size=12, color=C_GRAY)
add_text(s, "※ 수익률은 역사적 참조값. 수수료·세금 미반영. 미래 수익 보장 아님.",
         0.4, 6.1, 12.5, 0.3, size=10, italic=True, color=C_GRAY)
slide_footer(s, 6)

# ════════════════════════════════════════════════════════════
# SLIDE 07 — 국민연금식 자산배분 벤치마크
# ════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
add_header_bar(s, "운용 구조: 국민연금식 자산배분 벤치마크",
               "05 | 원칙 참조 모델 (복제·추종 아님)")

add_rect(s, 0.3, 1.2, 12.7, 0.5, fill=RGBColor(0xFF,0xF3,0xE0))
add_text(s,
    "⚠  '국민연금 포트폴리오를 복제한다'가 아니라 장기·분산·위험관리 원칙을 전남광주형으로 벤치마크한다",
    0.5, 1.25, 12.3, 0.42, size=13, bold=True, color=RGBColor(0xE6,0x5C,0x00))

headers2 = ["벤치마크 원칙", "국민연금 현황", "전남광주 적용 방향"]
cx2 = [0.3, 3.8, 7.3]
cw2 = [3.4, 3.4, 5.7]
for ci, h in enumerate(headers2):
    add_rect(s, cx2[ci], 1.85, cw2[ci], 0.38, fill=C_NAVY)
    add_text(s, h, cx2[ci]+0.05, 1.88, cw2[ci]-0.1, 0.32,
             size=13, bold=True, color=C_WHITE, align=PP_ALIGN.CENTER)
rows2 = [
    ("장기 투자 시계",   "10년+ 기준",       "영구기금 구조 (원금보전)"),
    ("글로벌 분산",      "해외 50%+",        "해외주식 35%+해외채권 10%"),
    ("자산 다각화",      "주식·채권·대체",   "동일 구조 적용"),
    ("중기자산배분",     "5년 목표비중",      "투자정책서 5년 주기"),
    ("위험관리",         "VaR·손실한도",      "위원회 한도 설정"),
    ("성과공시",         "연간 기금보고서",   "분기 공시 의무화"),
    ("직접+위탁 병행",   "직접 40%+위탁",    "OCIO 위탁 중심"),
]
for ri, row in enumerate(rows2):
    bg = C_LGRAY if ri % 2 == 0 else C_WHITE
    y = 2.28 + ri * 0.52
    for ci, cell in enumerate(row):
        add_rect(s, cx2[ci], y, cw2[ci], 0.5, fill=bg,
                 line_color=RGBColor(0xDD,0xDD,0xDD), line_width=0.5)
        clr = C_GWANGJU if ci==2 else C_DARK
        add_text(s, cell, cx2[ci]+0.08, y+0.05, cw2[ci]-0.16, 0.42,
                 size=12, color=clr)

add_text(s, "▶ 직접위탁 불가 이유: 법적목적 제한·자금혼합 부적절·책임구조 불명확 → OCIO 공개경쟁으로 대체",
         0.3, 6.75, 12.7, 0.38, size=12, bold=True, color=C_GWANGJU)
slide_footer(s, 7)

# ════════════════════════════════════════════════════════════
# SLIDE 08 — 참조 포트폴리오
# ════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
add_header_bar(s, "참조 포트폴리오 설계",
               "06 | 기본안 및 단계별 전환 (보수→중립→성장)")

# 기본 포트폴리오 표
allocs = [
    ("해외주식", "35%", "±5%", "글로벌 성장수익"),
    ("국내주식", "10%", "±3%", "국내 산업 연계"),
    ("국내채권", "20%", "±5%", "안정성·유동성"),
    ("해외채권", "10%", "±3%", "분산효과"),
    ("대체투자", "15%", "±5%", "인프라·에너지·부동산·사모"),
    ("유동성",   "5%",  "±2%", "집행 안정성"),
    ("지역전략", "5%",  "±2%", "전남광주 미래산업"),
]
ht = ["자산군", "기준비중", "허용범위", "목적"]
hx = [0.3, 2.3, 3.8, 5.1]
hw = [1.9, 1.4, 1.2, 4.5]
for ci, h in enumerate(ht):
    add_rect(s, hx[ci], 1.2, hw[ci], 0.38, fill=C_NAVY)
    add_text(s, h, hx[ci]+0.05, 1.23, hw[ci]-0.1, 0.32,
             size=12, bold=True, color=C_WHITE, align=PP_ALIGN.CENTER)
colors8 = [C_GWANGJU, RGBColor(0x42,0xA5,0xF5), C_JEONNAM,
           RGBColor(0x66,0xBB,0x6A), C_TEAL, C_GOLD, C_NAVY]
for ri, row in enumerate(allocs):
    y = 1.62 + ri * 0.5
    for ci, cell in enumerate(row):
        bg = RGBColor(0xF0,0xF4,0xFF) if ri%2==0 else C_WHITE
        add_rect(s, hx[ci], y, hw[ci], 0.48, fill=bg,
                 line_color=RGBColor(0xDD,0xDD,0xDD), line_width=0.5)
    add_rect(s, hx[0], y, 0.06, 0.48, fill=colors8[ri])
    for ci, cell in enumerate(row):
        clr = C_DARK if ci != 1 else colors8[ri]
        bld = ci == 1
        add_text(s, cell, hx[ci]+0.1, y+0.07, hw[ci]-0.2, 0.38,
                 size=12, bold=bld, color=clr)

# 단계 표
stages = [
    ("1단계\n1~3년", "보수형", "25%", "45%", "10%", "10%", "5%", "3~4%"),
    ("2단계\n3~7년", "중립형", "40%", "32%", "15%", "5%",  "5%", "4~5%"),
    ("3단계\n7년+",  "성장형", "52%", "23%", "17%", "3%",  "5%", "5~6%"),
]
sht = ["단계", "유형", "주식", "채권", "대체", "유동", "지역", "기대수익"]
shx = [9.8+ci*0.44 for ci in range(8)]
sht_colors = [C_NAVY]*8
shw = [0.82]*8
for ci, h in enumerate(sht):
    add_rect(s, 9.8+ci*0.46, 1.2, 0.44, 0.38, fill=C_NAVY)
    add_text(s, h, 9.82+ci*0.46, 1.23, 0.42, 0.32,
             size=8, bold=True, color=C_WHITE, align=PP_ALIGN.CENTER)
stage_colors = [C_GWANGJU, C_JEONNAM, C_TEAL]
for ri, row in enumerate(stages):
    for ci, cell in enumerate(row):
        y2 = 1.62 + ri * 0.5
        bg2 = RGBColor(0xF0,0xF4,0xFF) if ri%2==0 else C_WHITE
        add_rect(s, 9.8+ci*0.46, y2, 0.44, 0.48, fill=bg2,
                 line_color=RGBColor(0xDD,0xDD,0xDD), line_width=0.5)
        clr2 = stage_colors[ri] if ci==1 else C_DARK
        add_text(s, cell, 9.82+ci*0.46, y2+0.06, 0.42, 0.38,
                 size=8, color=clr2, align=PP_ALIGN.CENTER)

add_text(s, "성장형 전환은 성과 검증 + 의회 동의 후 단계적으로만",
         9.8, 4.18, 3.5, 0.3, size=9, italic=True, color=C_GRAY)
add_text(s, "환헤지: 해외주식 부분헤지(0~50%) | 해외채권 완전헤지 원칙",
         0.3, 6.75, 9.5, 0.35, size=11, color=C_GRAY)
slide_footer(s, 8)

# ════════════════════════════════════════════════════════════
# SLIDE 09 — OCIO 위탁운용
# ════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
add_header_bar(s, "OCIO 위탁운용 구조",
               "07 | 외부 전문기관 공개경쟁 선정")

add_text(s, "OCIO (Outsourced Chief Investment Officer)",
         0.4, 1.2, 8, 0.45, size=17, bold=True, color=C_NAVY)
add_text(s, "자산배분·위험관리·성과평가·운용사 선정을 외부 전문기관에 위탁하는 구조",
         0.4, 1.65, 10, 0.38, size=13, color=C_DARK)

reasons = [
    ("전문성", "지방정부 직접 운용\n인력 확보 불가"),
    ("이해충돌 방지", "외부 운용 →\n정치 개입 차단"),
    ("글로벌 네트워크", "해외자산 운용\n파트너십 필요"),
    ("성과 책임", "계약 기반\n명확한 책임"),
]
for i, (title, desc) in enumerate(reasons):
    x = 0.4 + i * 3.1
    add_rect(s, x, 2.15, 2.8, 1.4, fill=C_LIGHTBLUE)
    add_text(s, title, x+0.1, 2.2, 2.6, 0.4,
             size=13, bold=True, color=C_GWANGJU, align=PP_ALIGN.CENTER)
    add_text(s, desc, x+0.1, 2.65, 2.6, 0.8,
             size=11, color=C_DARK, align=PP_ALIGN.CENTER)

# 선정 절차 흐름
add_text(s, "■ 선정 절차 (공개경쟁 원칙)", 0.4, 3.7, 8, 0.38,
         size=14, bold=True, color=C_NAVY)
steps = ["RFI 발송\n(시장검증)", "RFP 발송\n(제안요청)", "외부전문가\n평가위원회", "위원회\n최종의결", "복수기관\n분산위탁"]
for i, step in enumerate(steps):
    x = 0.5 + i * 2.45
    add_rect(s, x, 4.15, 2.1, 0.9, fill=C_JEONNAM)
    add_text(s, step, x+0.05, 4.2, 2.0, 0.8,
             size=12, bold=True, color=C_WHITE, align=PP_ALIGN.CENTER)
    if i < 4:
        add_text(s, "→", x+2.1, 4.45, 0.35, 0.4,
                 size=18, bold=True, color=C_NAVY, align=PP_ALIGN.CENTER)

# 후보군
add_text(s, "■ RFI 대상 후보군 (모두 동등한 공개경쟁 — 사전 내정 없음)",
         0.4, 5.2, 12.5, 0.38, size=14, bold=True, color=C_NAVY)
candidates = ["미래에셋자산운용", "삼성자산운용", "KB자산운용",
              "한국투자신탁운용", "NH투자증권", "한화자산운용"]
for i, c in enumerate(candidates):
    x = 0.4 + (i % 3) * 4.2
    y = 5.7 + (i // 3) * 0.5
    add_rect(s, x, y, 3.9, 0.42, fill=C_LGRAY,
             line_color=C_GWANGJU, line_width=1)
    add_text(s, c, x+0.1, y+0.05, 3.7, 0.35, size=12, color=C_DARK)
slide_footer(s, 9)

# ════════════════════════════════════════════════════════════
# SLIDE 10 — 지역전략투자
# ════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
add_header_bar(s, "지역전략투자 분야",
               "08 | 기금 5% 내, Double Bottom Line")

add_text(s, "기금 전체의 5%(권장) 내에서 재무수익 + 지역경제 파급효과를 동시 추구",
         0.4, 1.2, 12.5, 0.38, size=13, color=C_DARK)

fields = [
    (C_GWANGJU, "🤖  AI",             "집적단지 고도화\n공공 AI 실증·AI반도체\n인재양성"),
    (C_JEONNAM, "⚡  에너지",          "해상풍력·그린수소\nRE100·ESS\n스마트그리드"),
    (C_TEAL,    "🌱  농수축산",        "스마트팜·축산\n유통플랫폼\n수산 고부가"),
    (C_NAVY,    "🧬  바이오·헬스",    "고령친화산업\n식품바이오\n헬스케어데이터"),
    (C_GOLD,    "🚗  모빌리티",        "자율주행·드론물류\n정밀지도\n공간정보"),
    (C_RED,     "🎓  청년·대학",       "연구펀드\n인재정착지원\n청년창업"),
]
bw2 = 2.05
for i, (clr, title, desc) in enumerate(fields):
    x = 0.3 + i * (bw2 + 0.07)
    add_rect(s, x, 1.72, bw2, 4.5, fill=clr)
    add_text(s, title, x+0.05, 1.77, bw2-0.1, 0.5,
             size=13, bold=True, color=C_WHITE, align=PP_ALIGN.CENTER)
    add_rect(s, x+0.1, 2.3, bw2-0.2, 0.04, fill=C_WHITE)
    add_text(s, desc, x+0.08, 2.4, bw2-0.16, 3.4,
             size=12, color=C_WHITE, align=PP_ALIGN.CENTER)

add_text(s, "투자 방식 우선순위: 펀드출자(LP) > 공동투자 > 직접투자(원칙 제한)  |  이해충돌 방지 심사 필수",
         0.3, 6.35, 12.7, 0.38, size=12, color=C_GRAY)
add_text(s, "성과지표: IRR·고용창출·청년유입·민간투자 매칭률·특허·탄소감축",
         0.3, 6.72, 12.7, 0.35, size=11, color=C_GRAY)
slide_footer(s, 10)

# ════════════════════════════════════════════════════════════
# SLIDE 11 — 법률·제도 선결 과제
# ════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
add_header_bar(s, "법률·제도 선결 과제",
               "09 | 교부조건 명시가 가장 중요한 선결 과제")

add_rect(s, 0.3, 1.2, 12.7, 0.65, fill=RGBColor(0xFF,0xEB,0xEE))
add_text(s, "⚠  최대 리스크: 교부조건 확정 후에는 기금화가 보조금법상 '용도 외 사용'으로 불가능해질 수 있다",
         0.5, 1.28, 12.3, 0.55, size=13, bold=True, color=C_RED)

legal_items = [
    ("특별법", C_NAVY, "기금 설치 + 중앙정부 지원금 출연 근거 명시\n일반법 특례 부여"),
    ("시행령", C_GWANGJU, "운용 원칙·위탁 기준·지출한도·선정 절차\n성과평가·보고 기준"),
    ("조례",   C_JEONNAM, "목적·재원·용도·원금보전·위원회\n정보공개·외부감사"),
    ("교부조건", C_RED,   "기금 출연 가능성 사전 명시 ← 최우선\n용도 외 사용 리스크 차단"),
    ("투자정책서", C_TEAL, "자산배분·위험한도·지출률·벤치마크\n위원회 의결 후 즉시 공개"),
]
for i, (title, clr, desc) in enumerate(legal_items):
    y = 2.05 + i * 0.9
    add_rect(s, 0.3, y, 2.2, 0.82, fill=clr)
    add_text(s, title, 0.35, y+0.15, 2.1, 0.55,
             size=16, bold=True, color=C_WHITE, align=PP_ALIGN.CENTER)
    add_rect(s, 2.5, y, 10.5, 0.82, fill=C_LGRAY,
             line_color=clr, line_width=1.5)
    add_text(s, desc, 2.65, y+0.08, 10.1, 0.68, size=12, color=C_DARK)

add_text(s, "법령 검토 우선순위: 보조금법 → 지방기금법 → 지방재정법 → 특별법 → 자본시장법·외국환거래법",
         0.3, 6.6, 12.7, 0.35, size=11, color=C_GRAY)
add_text(s, "전문 법률자문 의뢰 필수 — 모든 조문은 '가능하도록 법적 근거를 마련해야 한다'는 전제",
         0.3, 6.95, 12.7, 0.3, size=10, italic=True, color=C_GRAY)
slide_footer(s, 11)

# ════════════════════════════════════════════════════════════
# SLIDE 12 — 거버넌스
# ════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
add_header_bar(s, "기금 거버넌스",
               "10 | 정치적 개입 차단 10가지 장치")

# 조직도 박스
org = [
    (5.4, 1.25, 2.5, 0.6, C_NAVY,    "전남광주특별시장"),
    (4.8, 2.15, 3.7, 0.6, C_GWANGJU, "미래전환기금운용위원회\n(공무원 의결권 배제)"),
    (0.4, 3.3,  2.9, 0.6, C_JEONNAM, "투자정책위원회"),
    (3.5, 3.3,  2.9, 0.6, C_TEAL,    "위험관리위원회"),
    (6.6, 3.3,  2.9, 0.6, C_NAVY,    "지역전략사업위원회"),
    (9.7, 3.3,  2.9, 0.6, C_GOLD,    "시민감시위원회"),
    (3.8, 4.4,  5.5, 0.6, C_GWANGJU, "OCIO 전문운용기관 (공개경쟁 선정)"),
    (0.4, 5.5,  3.5, 0.5, C_JEONNAM, "특별시의회 보고"),
    (4.1, 5.5,  3.5, 0.5, C_TEAL,    "외부감사인"),
    (7.8, 5.5,  4.5, 0.5, C_NAVY,    "중앙정부·국회 보고"),
]
for (x, y, w, h, clr, txt) in org:
    add_rect(s, x, y, w, h, fill=clr)
    add_text(s, txt, x+0.05, y+0.05, w-0.1, h-0.1,
             size=11, bold=True, color=C_WHITE, align=PP_ALIGN.CENTER)

# 10대 차단장치
devices = [
    "① 투자정책서 사전공시",    "② 자산군 허용범위 고정",
    "③ 특정기업 직접투자 금지", "④ 지역투자 별도 심사",
    "⑤ 위원·회의록 공개",       "⑥ 외부감사 의무",
    "⑦ 의회보고 의무",          "⑧ 이해충돌 신고 의무",
    "⑨ 운용기관 공개경쟁",      "⑩ 성과 전면 공개",
]
add_text(s, "■ 10대 정치개입 차단장치", 0.3, 6.2, 6, 0.35,
         size=12, bold=True, color=C_NAVY)
for i, d in enumerate(devices):
    x = 0.3 + (i % 5) * 2.6
    y = 6.58 + (i // 5) * 0.0
    add_rect(s, x, 6.55, 2.4, 0.32, fill=C_NAVY if i<5 else C_JEONNAM)
    add_text(s, d, x+0.05, 6.57, 2.3, 0.28,
             size=9, color=C_WHITE, align=PP_ALIGN.CENTER)
slide_footer(s, 12)

# ════════════════════════════════════════════════════════════
# SLIDE 13 — 해외 성공사례
# ════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
add_header_bar(s, "해외 성공사례 비교",
               "11 | 노르웨이·알래스카·아일랜드·싱가포르")

cases = [
    (C_GWANGJU, "🇳🇴 노르웨이 GPFG",
     "규모: 약 1.9조 달러\n재원: 석유세입\n지출준칙: 실질 3% 룰\n특징: 글로벌 분산·완전 공시",
     "→ 3% 지출률·\n   글로벌분산 직접 참조"),
    (C_JEONNAM, "🇺🇸 알래스카 영구기금",
     "규모: 약 760억 달러\n재원: 석유 로열티\n원금보호: 헌법 명시\n특징: 주민배당",
     "→ 원금보호 강제력\n   특별법·조례 적용"),
    (C_TEAL,    "🇮🇪 아일랜드 ISIF",
     "규모: 약 130억 유로\n목적: 성장+고용\nDouble Bottom Line\n직접·공동·펀드투자",
     "→ 이중목표 운용\n   지역전략투자 모델"),
    (C_NAVY,    "🇸🇬 싱가포르 테마섹",
     "규모: 약 3,820억 SGD\n성격: 국가전략투자\n독립이사회 거버넌스\n장기수익+공공목적",
     "→ 독립 거버넌스\n   전략산업 투자"),
]
bw3 = 3.0
for i, (clr, title, body, lesson) in enumerate(cases):
    x = 0.3 + i * (bw3 + 0.15)
    add_rect(s, x, 1.2, bw3, 0.5, fill=clr)
    add_text(s, title, x+0.05, 1.24, bw3-0.1, 0.42,
             size=13, bold=True, color=C_WHITE, align=PP_ALIGN.CENTER)
    add_rect(s, x, 1.73, bw3, 3.0, fill=C_LGRAY,
             line_color=clr, line_width=1)
    add_text(s, body, x+0.12, 1.8, bw3-0.24, 2.8, size=11, color=C_DARK)
    add_rect(s, x, 4.78, bw3, 0.8, fill=clr)
    add_text(s, lesson, x+0.1, 4.83, bw3-0.2, 0.7,
             size=11, bold=True, color=C_WHITE, align=PP_ALIGN.CENTER)

add_text(s, "공통점: 일시적 재원 → 영구 성장자본 전환 | 원금보전 | 글로벌 분산 | 투명 공시 | 독립 거버넌스",
         0.3, 5.72, 12.7, 0.38, size=12, bold=True, color=C_NAVY)
add_text(s, "전남광주도 이 경로를 따를 수 있다 — 대한민국 균형발전의 새 표준",
         0.3, 6.15, 12.7, 0.38, size=13, bold=True, color=C_JEONNAM)
slide_footer(s, 13)

# ════════════════════════════════════════════════════════════
# SLIDE 14 — 이해당사자별 설득 논리
# ════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
add_header_bar(s, "이해당사자별 설득 논리",
               "12 | 각 주체별 맞춤 메시지")

stakeholders = [
    (C_GWANGJU, "민형배 시장",
     ["임기 성과(8조) + 임기 후 지속재원(12조)", "20조 기획을 제도화하는 구체적 수단",
      "정치적 나눠먹기 방지 → 리더십 강화", "100년 레거시 — 노르웨이식 첫 지방정부"]),
    (C_JEONNAM, "중앙정부",
     ["예산낭비 방지 → 책임재정 혁신", "지방재정 자립 → 의존도 영구 감소",
      "초광역통합 표준모델", "교부조건·공시·감사로 관리 용이"]),
    (C_TEAL,    "국 회",
     ["원금보전·지출상한 → 과다 지출 차단", "외부감사·분기공시 → 국회 감시 용이",
      "특혜방지 공개경쟁 구조", "보조금 용도외 사용 원천 차단"]),
    (C_NAVY,    "지역주민",
     ["한 번 쓰는 20조 vs 매년 돌아오는 20조", "청년정착·농업·의료·교육 지속 투자",
      "광주·전남 균형 배분 구조", "우리 아이들도 쓰는 기금"]),
]
bw4 = 3.0
for i, (clr, who, points) in enumerate(stakeholders):
    x = 0.3 + i * (bw4 + 0.15)
    add_rect(s, x, 1.2, bw4, 0.5, fill=clr)
    add_text(s, who, x+0.05, 1.24, bw4-0.1, 0.42,
             size=15, bold=True, color=C_WHITE, align=PP_ALIGN.CENTER)
    for j, pt in enumerate(points):
        y = 1.8 + j * 0.62
        add_rect(s, x+0.1, y, 0.25, 0.4, fill=clr)
        add_text(s, pt, x+0.42, y+0.03, bw4-0.56, 0.38,
                 size=11, color=C_DARK)
slide_footer(s, 14)

# ════════════════════════════════════════════════════════════
# SLIDE 15 — 예상 반론 Q&A
# ════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
add_header_bar(s, "예상 반론 Q&A",
               "13 | 7대 반론과 핵심 답변")

qas = [
    ("당장 쓸 곳 많은데 왜 묶나?",
     "전액 아님. 12조만. 8조는 즉시 AI·에너지·농수축산 직접투자"),
    ("손실 나면 누가 책임?",
     "전문위탁·분산·손실한도·외부감사 제도화. 전액 소비는 소멸 확정"),
    ("국민연금 못 맡기면 불가능?",
     "원칙 벤치마크 + 복수 OCIO 공개경쟁으로 완전 대체 가능"),
    ("미래에셋 특혜 아닌가?",
     "후보군 중 하나. 삼성·KB·NH·한국투자·한화 복수 공개경쟁"),
    ("국고지원금 투자 불법?",
     "교부조건·특별법·조례에 근거 사전 명시 시 해소 가능"),
    ("직접 쓰는 게 낫지 않나?",
     "8조 직접투자 병행. 기금은 지속성 확보 장치"),
    ("시장 나쁘면 수익 없을 수도",
     "10년 장기평균 기준. 3~5년 평균 평가액으로 지출률 결정"),
]
for i, (q, a) in enumerate(qas):
    y = 1.2 + i * 0.76
    add_rect(s, 0.3, y, 0.5, 0.55, fill=C_GWANGJU)
    add_text(s, f"Q{i+1}", 0.3, y+0.1, 0.5, 0.38,
             size=12, bold=True, color=C_WHITE, align=PP_ALIGN.CENTER)
    add_rect(s, 0.85, y, 5.1, 0.55, fill=RGBColor(0xE3,0xF2,0xFD))
    add_text(s, q, 0.95, y+0.08, 4.9, 0.45, size=12, bold=True, color=C_GWANGJU)
    add_rect(s, 0.85, y, 0.04, 0.55, fill=C_GWANGJU)
    add_rect(s, 6.0, y, 7.0, 0.55, fill=C_LGRAY)
    add_text(s, "▷ " + a, 6.1, y+0.08, 6.8, 0.45, size=12, color=C_DARK)
slide_footer(s, 15)

# ════════════════════════════════════════════════════════════
# SLIDE 16 — 수익 시뮬레이션
# ════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
add_header_bar(s, "수익 시뮬레이션",
               "14 | 12조 기준, 복리 재투자 30% 시나리오")

accent_box(s, 0.3,  1.2, 2.9, 1.1, C_GWANGJU, "연 4% 기준 연간 수익", "4,800억", "원")
accent_box(s, 3.4,  1.2, 2.9, 1.1, C_JEONNAM, "10년 누적 수익",        "4.8조",   "원")
accent_box(s, 6.5,  1.2, 2.9, 1.1, C_TEAL,    "20년 누적 수익",        "9.6조",   "원")
accent_box(s, 9.6,  1.2, 3.3, 1.1, C_NAVY,    "30년 후 기금(재투자)", "20.2조",  "원(추산)")

# 연도별 표
sim = [
    ("1년",  "12.0조", "4,800억", "3,360억", "1,440억", "480억"),
    ("5년",  "12.9조", "5,160억", "3,612억", "1,548억", "516억"),
    ("10년", "14.1조", "5,640억", "3,948억", "1,692억", "564억"),
    ("20년", "16.9조", "6,760억", "4,732억", "2,028억", "676억"),
    ("30년", "20.2조", "8,080억", "5,656억", "2,424억", "808억"),
]
heads = ["시점", "기금규모", "연간수익(4%)", "지출가용(60%)", "재투자(30%)", "준비금(10%)"]
hx2 = [0.3, 1.8, 3.7, 5.8, 8.1, 10.4]
hw2 = [1.4, 1.8, 2.0, 2.2, 2.2, 2.5]
for ci, h in enumerate(heads):
    add_rect(s, hx2[ci], 2.45, hw2[ci], 0.38, fill=C_NAVY)
    add_text(s, h, hx2[ci]+0.05, 2.48, hw2[ci]-0.1, 0.32,
             size=11, bold=True, color=C_WHITE, align=PP_ALIGN.CENTER)
for ri, row in enumerate(sim):
    bg = RGBColor(0xFF,0xF9,0xC4) if ri == 2 else (C_LGRAY if ri%2==0 else C_WHITE)
    for ci, cell in enumerate(row):
        add_rect(s, hx2[ci], 2.88+ri*0.5, hw2[ci], 0.48, fill=bg,
                 line_color=RGBColor(0xDD,0xDD,0xDD), line_width=0.5)
        clr = C_JEONNAM if ci in [1,2] and ri==2 else C_DARK
        add_text(s, cell, hx2[ci]+0.08, 2.93+ri*0.5, hw2[ci]-0.16, 0.38,
                 size=12, color=clr, align=PP_ALIGN.CENTER)

add_text(s, "수익 배분: 지출 60% / 재투자 30% / 위험준비금 10%  |  복리 효과로 기금 원금 자체도 성장",
         0.3, 5.48, 12.7, 0.38, size=12, color=C_GRAY)
add_text(s, "⚠ 단순 산술 참조값. 수수료·세금·환율·시장변동 미반영. 미래 수익 보장 아님.",
         0.3, 5.88, 12.7, 0.35, size=10, italic=True, color=C_GRAY)
slide_footer(s, 16)

# ════════════════════════════════════════════════════════════
# SLIDE 17 — 추진 로드맵
# ════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
add_header_bar(s, "추진 로드맵 (6개월)",
               "15 | 5단계 추진 일정")

stages2 = [
    (C_GWANGJU, "① 개념 정립\n즉시~1개월",
     ["기본구상 작성", "8·12·15조 시나리오", "당선자 보고자료", "슬로건·메시지 확정"]),
    (C_JEONNAM, "② 법률·제도\n1~2개월",
     ["특별법 검토", "조례안 초안", "교부조건 문구 협의", "외부 법률자문"]),
    (C_TEAL,    "③ RFI 실시\n2~3개월",
     ["후보군 RFI 발송", "응답 분석", "OCIO 구조 설계", "수수료·리스크 검토"]),
    (C_NAVY,    "④ 보고서 확정\n3~4개월",
     ["본보고서 확정", "법률 조문안", "투자정책서 초안", "RFI 결과분석"]),
    (C_GOLD,    "⑤ 정치·입법\n4~6개월",
     ["캠프·인수팀 보고", "중앙정부 TF 협의", "국회 설득", "시민공론화·조례 제정"]),
]
bw5 = 2.4
for i, (clr, title, items) in enumerate(stages2):
    x = 0.3 + i * (bw5 + 0.12)
    add_rect(s, x, 1.2, bw5, 0.75, fill=clr)
    add_text(s, title, x+0.05, 1.25, bw5-0.1, 0.65,
             size=13, bold=True, color=C_WHITE, align=PP_ALIGN.CENTER)
    for j, item in enumerate(items):
        y = 2.05 + j * 0.62
        add_rect(s, x+0.1, y, 0.25, 0.4, fill=clr)
        add_text(s, item, x+0.4, y+0.04, bw5-0.5, 0.38, size=12, color=C_DARK)
    if i < 4:
        add_text(s, "→", x+bw5+0.02, 1.45, 0.1, 0.38,
                 size=20, bold=True, color=C_NAVY, align=PP_ALIGN.CENTER)

add_text(s, "★ 골든타임: 특별법·교부조건 협상 단계가 기금화 성패를 가른다 — 출범(2026.07) 전후가 최적 시점",
         0.3, 4.6, 12.7, 0.45, size=13, bold=True, color=C_RED)
add_rect(s, 0.3, 4.6, 12.7, 0.42, fill=RGBColor(0xFF,0xEB,0xEE))
add_text(s, "★ 골든타임: 특별법·교부조건 협상 단계가 기금화 성패를 가른다 — 출범(2026.07) 전후가 최적 시점",
         0.5, 4.65, 12.3, 0.42, size=13, bold=True, color=C_RED)
slide_footer(s, 17)

# ════════════════════════════════════════════════════════════
# SLIDE 18 — 성과지표
# ════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
add_header_bar(s, "성과지표 체계",
               "16 | 금융·지역·재정 3축 KPI")

kpi_cols = [
    (C_GWANGJU, "금융성과 지표",
     [("연평균 수익률", "3·5·10년 누적"),
      ("최대손실률(MDD)", "사전 한도 이내"),
      ("샤프비율", "0.5 이상 목표"),
      ("VaR(95%)", "허용한도 준수"),
      ("벤치마크 대비", "초과수익"),
      ("유동성 비율", "최소기준 유지")]),
    (C_JEONNAM, "지역성과 지표",
     [("청년 순유입", "20~39세 이동"),
      ("GRDP 증가", "산업별 부가가치"),
      ("창업기업 수", "기술·농식품"),
      ("고용창출", "직접·간접"),
      ("재생에너지 자립도", "RE% 비율"),
      ("민간 매칭 배율", "기금 대비 민간")]),
    (C_TEAL, "재정성과 지표",
     [("자체재원 증가율", "지방세·세외수입"),
      ("중앙 의존도", "국고보조 비중 변화"),
      ("재정승수", "지출 대비 경제효과"),
      ("수익재투자율", "운용수익 재투자 비중"),
      ("원금 보전율", "100% 유지"),
      ("지출률 준수", "투자정책서 기준")]),
]
bw6 = 4.1
for i, (clr, title, items) in enumerate(kpi_cols):
    x = 0.3 + i * (bw6 + 0.15)
    add_rect(s, x, 1.2, bw6, 0.45, fill=clr)
    add_text(s, title, x+0.05, 1.24, bw6-0.1, 0.37,
             size=14, bold=True, color=C_WHITE, align=PP_ALIGN.CENTER)
    for j, (kpi, desc) in enumerate(items):
        y = 1.72 + j * 0.72
        bg = C_LGRAY if j%2==0 else C_WHITE
        add_rect(s, x, y, bw6, 0.68, fill=bg,
                 line_color=RGBColor(0xDD,0xDD,0xDD), line_width=0.5)
        add_rect(s, x, y, 0.06, 0.68, fill=clr)
        add_text(s, kpi, x+0.14, y+0.04, bw6-0.24, 0.32,
                 size=12, bold=True, color=C_DARK)
        add_text(s, desc, x+0.14, y+0.35, bw6-0.24, 0.28,
                 size=10, color=C_GRAY)

add_text(s, "평가 주기: 월(평가액·위험) / 분기(수익률·보고서) / 연(종합·의회) / 3~5년(장기·정책재검토)",
         0.3, 6.7, 12.7, 0.38, size=11, color=C_GRAY)
slide_footer(s, 18)

# ════════════════════════════════════════════════════════════
# SLIDE 19 — 핵심 슬로건
# ════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
add_rect(s, 0, 0, 13.33, 7.5, fill=C_NAVY)
add_rect(s, 0, 0, 0.15, 7.5, fill=C_GWANGJU)
add_rect(s, 13.18, 0, 0.15, 7.5, fill=C_JEONNAM)
add_rect(s, 0, 0, 13.33, 0.15, fill=C_GOLD)

add_text(s, "핵심 슬로건", 0.5, 0.4, 12.3, 0.5,
         size=18, color=RGBColor(0x90,0xA4,0xAE))

add_rect(s, 1.0, 1.1, 11.33, 1.0, fill=C_GWANGJU)
add_text(s, '"쓰고 끝나는 20조가 아니라, 매년 돌아오는 20조"',
         1.1, 1.18, 11.1, 0.85, size=28, bold=True,
         color=C_WHITE, align=PP_ALIGN.CENTER)

add_rect(s, 1.0, 2.3, 11.33, 0.75, fill=C_JEONNAM)
add_text(s, '"20조 원을 100년 성장자본으로"',
         1.1, 2.38, 11.1, 0.6, size=24, bold=True,
         color=C_WHITE, align=PP_ALIGN.CENTER)

sub_slogans = [
    "우리 아이들도 쓰는 기금",
    "전남광주 주도성장의 재정 엔진",
    "토목예산을 넘어 미래자본으로",
    "청년이 돌아오는 미래전환기금",
    "중앙정부 지원금을 지역의 독립재정으로",
]
add_text(s, "보조 슬로건 후보",
         1.0, 3.25, 11, 0.38, size=14, color=RGBColor(0x90,0xA4,0xAE))
for i, sl in enumerate(sub_slogans):
    y = 3.7 + i * 0.5
    add_rect(s, 1.0, y, 11.33, 0.45, fill=RGBColor(0x1A,0x23,0x7E))
    add_text(s, f"• {sl}", 1.2, y+0.06, 11.0, 0.36,
             size=15, color=RGBColor(0xBB, 0xDE, 0xFB))

add_text(s, "2026. 06  |  전남광주 미래전환기금 준비위원회",
         1.0, 6.9, 11.33, 0.38, size=11,
         color=RGBColor(0x78,0x90,0x9C), align=PP_ALIGN.CENTER)
slide_footer(s, 19)

# ════════════════════════════════════════════════════════════
# SLIDE 20 — 결론 및 지금 필요한 결정
# ════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
add_rect(s, 0, 0, 13.33, 7.5, fill=RGBColor(0xF8,0xFB,0xFF))
add_rect(s, 0, 0, 13.33, 0.12, fill=C_GWANGJU)
add_rect(s, 0, 7.38, 13.33, 0.12, fill=C_JEONNAM)

add_text(s, "결론 및 지금 필요한 결정",
         0.5, 0.2, 12.3, 0.6, size=24, bold=True, color=C_NAVY)

add_rect(s, 0.4, 0.95, 12.5, 0.65, fill=C_NAVY)
add_text(s,
    "전남광주는 20조 원을 소비하는 도시가 아니라, 자본화하여 대한민국 균형발전의 새 표준을 만드는 도시",
    0.6, 1.02, 12.1, 0.55, size=15, bold=True,
    color=C_GOLD, align=PP_ALIGN.CENTER)

add_text(s, "■ 8대 핵심 제언", 0.4, 1.78, 6, 0.38,
         size=14, bold=True, color=C_NAVY)
recs = [
    "① 원금은 원칙적으로 보전한다",
    "② 운용수익 중심으로 지출한다",
    "③ 국민연금식 자산배분 원칙을 벤치마크한다 (복제 아님)",
    "④ 전문기관은 RFI·공개경쟁으로 검토한다 (특혜 차단)",
    "⑤ 특별법·조례·교부조건에 법적 근거를 명시한다",
    "⑥ 지역전략투자는 기금의 일부로 제한한다",
    "⑦ AI·에너지·농수축산·바이오·청년·대학에 집중한다",
    "⑧ 모든 성과·지출내역을 공개한다",
]
for i, rec in enumerate(recs):
    y = 2.22 + i * 0.48
    clr = C_GWANGJU if i < 4 else C_JEONNAM
    add_rect(s, 0.4, y, 0.35, 0.38, fill=clr)
    add_text(s, rec, 0.82, y+0.03, 5.4, 0.38, size=12, color=C_DARK)

# 오른쪽 NOW BOX
add_rect(s, 6.8, 1.78, 6.1, 4.95, fill=C_GWANGJU)
add_text(s, "⚡ 지금 당장 필요한 결정",
         6.9, 1.85, 5.9, 0.48, size=16, bold=True,
         color=C_WHITE, align=PP_ALIGN.CENTER)
nows = [
    "1. 특별법·교부조건 협상 시\n   '기금 출연 가능성' 명시",
    "2. 법률자문 즉시 의뢰\n   (보조금법·지방기금법 검토)",
    "3. 기금 규모 정치적 결정\n   (권장: 12조 기금 + 8조 직접)",
    "4. OCIO 후보군 RFI 준비\n   (공개경쟁 원칙 천명)",
    "5. 기금운용위원회 구성 착수\n   (공무원 의결권 배제 설계)",
]
for i, n in enumerate(nows):
    y = 2.45 + i * 0.82
    add_rect(s, 6.9, y, 5.8, 0.72, fill=RGBColor(0x1A,0x23,0x7E))
    add_text(s, n, 7.0, y+0.07, 5.6, 0.6, size=12, color=C_WHITE)

add_text(s, '"골든타임은 지금입니다"',
         6.9, 6.5, 5.8, 0.45, size=18, bold=True,
         color=C_GOLD, align=PP_ALIGN.CENTER)
slide_footer(s, 20)

# ── 저장 ─────────────────────────────────────────────────
out_path = "/home/user/michaechang_study/전남광주_미래전환기금/output/전남광주_미래전환기금_보고서_민형배시장.pptx"
prs.save(out_path)
print(f"✅ PPTX 저장 완료: {out_path}")
