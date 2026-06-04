"""
함평군수 당선자 전용 보고자료 PPTX 생성
- 정치적 리더십 프레이밍 강화
- 당선 축하 + 비전 제시 구조
- 10년 레거시 프로젝트로 포지셔닝
"""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

COL_GREEN_DARK   = RGBColor(0x1B, 0x5E, 0x20)
COL_GREEN_MID    = RGBColor(0x2E, 0x7D, 0x32)
COL_GREEN_LIGHT  = RGBColor(0xA5, 0xD6, 0xA7)
COL_AMBER        = RGBColor(0xF9, 0xA8, 0x25)
COL_BROWN        = RGBColor(0x6D, 0x4C, 0x41)
COL_WHITE        = RGBColor(0xFF, 0xFF, 0xFF)
COL_LIGHT_GRAY   = RGBColor(0xF5, 0xF5, 0xF5)
COL_DARK_GRAY    = RGBColor(0x21, 0x21, 0x21)
COL_MID_GRAY     = RGBColor(0x75, 0x75, 0x75)
COL_ACCENT_BLUE  = RGBColor(0x01, 0x57, 0x9B)
COL_GOLD         = RGBColor(0xFF, 0xD7, 0x00)

SLIDE_W = Inches(13.33)
SLIDE_H = Inches(7.5)

prs = Presentation()
prs.slide_width  = SLIDE_W
prs.slide_height = SLIDE_H
BLANK = prs.slide_layouts[6]


def add_rect(slide, l, t, w, h, fill_rgb=None, line_rgb=None, line_pt=0):
    shape = slide.shapes.add_shape(1, l, t, w, h)
    if fill_rgb:
        shape.fill.solid()
        shape.fill.fore_color.rgb = fill_rgb
    else:
        shape.fill.background()
    if line_rgb:
        shape.line.color.rgb = line_rgb
        shape.line.width = Pt(line_pt) if line_pt else Pt(0.5)
    else:
        shape.line.fill.background()
    return shape


def add_text(slide, text, l, t, w, h,
             font_size=18, bold=False, color=None, align=PP_ALIGN.LEFT,
             font_name="맑은 고딕", wrap=True, italic=False):
    txBox = slide.shapes.add_textbox(l, t, w, h)
    tf = txBox.text_frame
    tf.word_wrap = wrap
    para = tf.paragraphs[0]
    para.alignment = align
    run = para.add_run()
    run.text = text
    run.font.size = Pt(font_size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.name = font_name
    if color:
        run.font.color.rgb = color
    return txBox


def header_bar(slide, title_text, subtitle_text="", badge=""):
    add_rect(slide, 0, 0, SLIDE_W, Inches(1.25), fill_rgb=COL_GREEN_DARK)
    add_rect(slide, 0, Inches(1.25), SLIDE_W, Inches(0.06), fill_rgb=COL_AMBER)
    add_text(slide, "함평군", Inches(0.3), Inches(0.1), Inches(1.5), Inches(0.6),
             font_size=20, bold=True, color=COL_AMBER)
    add_text(slide, "Hampyeong-gun", Inches(0.3), Inches(0.65), Inches(2), Inches(0.4),
             font_size=9, color=COL_GREEN_LIGHT)
    add_text(slide, title_text, Inches(2.0), Inches(0.1), Inches(9.0), Inches(0.7),
             font_size=22, bold=True, color=COL_WHITE, align=PP_ALIGN.CENTER)
    if subtitle_text:
        add_text(slide, subtitle_text, Inches(2.0), Inches(0.78), Inches(9.0), Inches(0.38),
                 font_size=12, color=COL_GREEN_LIGHT, align=PP_ALIGN.CENTER)
    if badge:
        add_rect(slide, Inches(11.0), Inches(0.2), Inches(2.1), Inches(0.8),
                 fill_rgb=COL_AMBER)
        add_text(slide, badge, Inches(11.0), Inches(0.25), Inches(2.1), Inches(0.7),
                 font_size=11, bold=True, color=COL_DARK_GRAY, align=PP_ALIGN.CENTER)


def footer_bar(slide, page_num, total=20):
    add_rect(slide, 0, Inches(7.15), SLIDE_W, Inches(0.35), fill_rgb=COL_GREEN_DARK)
    add_text(slide, "함평군수 당선자 보고자료  |  함평 산지방목 그린축산·에너지공유 특구 조성사업",
             Inches(0.3), Inches(7.18), Inches(10), Inches(0.28),
             font_size=9, color=COL_GREEN_LIGHT)
    add_text(slide, f"{page_num} / {total}", Inches(12.5), Inches(7.18),
             Inches(0.7), Inches(0.28),
             font_size=9, color=COL_GREEN_LIGHT, align=PP_ALIGN.RIGHT)


def section_chip(slide, text, lx, ty, w=Inches(2.5), h=Inches(0.38)):
    add_rect(slide, lx, ty, w, h, fill_rgb=COL_GREEN_MID)
    add_text(slide, text, lx, ty, w, h,
             font_size=12, bold=True, color=COL_WHITE, align=PP_ALIGN.CENTER)


def bullet_list(slide, items, lx, ty, w, line_h=Inches(0.45), font_size=13):
    for i, item in enumerate(items):
        add_text(slide, f"▪  {item}", lx, ty + i * line_h, w, line_h,
                 font_size=font_size, color=COL_DARK_GRAY)


def stat_box(slide, label, value, unit, lx, ty, w=Inches(2.5), h=Inches(1.3),
             bg=COL_GREEN_LIGHT, val_color=COL_GREEN_DARK):
    add_rect(slide, lx, ty, w, h, fill_rgb=bg)
    add_rect(slide, lx, ty, w, Inches(0.04), fill_rgb=COL_GREEN_MID)
    add_text(slide, label, lx, ty + Inches(0.08), w, Inches(0.35),
             font_size=11, color=COL_MID_GRAY, align=PP_ALIGN.CENTER)
    add_text(slide, value, lx, ty + Inches(0.4), w, Inches(0.55),
             font_size=24, bold=True, color=val_color, align=PP_ALIGN.CENTER)
    add_text(slide, unit, lx, ty + Inches(0.92), w, Inches(0.3),
             font_size=10, color=COL_MID_GRAY, align=PP_ALIGN.CENTER)


# ════════════════════════════════════════════════════════════════
#  SLIDE 1 — 표지 (군수 당선자 전용)
# ════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
add_rect(s, 0, 0, SLIDE_W, SLIDE_H, fill_rgb=COL_GREEN_DARK)
add_rect(s, Inches(9.5), 0, Inches(4), Inches(4.5), fill_rgb=COL_GREEN_MID)
add_rect(s, Inches(11), Inches(3.8), Inches(3), Inches(4), fill_rgb=RGBColor(0x16,0x50,0x16))
add_rect(s, 0, Inches(5.0), SLIDE_W, Inches(0.07), fill_rgb=COL_AMBER)

# 당선자 전용 배지
add_rect(s, Inches(0.6), Inches(0.4), Inches(3.8), Inches(0.6), fill_rgb=COL_AMBER)
add_text(s, "군수 당선자 보고자료  (비공개)", Inches(0.6), Inches(0.42), Inches(3.8), Inches(0.55),
         font_size=13, bold=True, color=COL_DARK_GRAY, align=PP_ALIGN.CENTER)

add_text(s, "함평군", Inches(0.7), Inches(1.2), Inches(3), Inches(0.7),
         font_size=26, bold=True, color=COL_AMBER)
add_text(s, "Hampyeong-gun, Jeollanam-do", Inches(0.7), Inches(1.85), Inches(5), Inches(0.4),
         font_size=11, color=COL_GREEN_LIGHT)

add_text(s, "함평 산지방목\n그린축산·에너지공유\n특구 조성사업",
         Inches(0.7), Inches(2.35), Inches(8.5), Inches(2.3),
         font_size=34, bold=True, color=COL_WHITE, align=PP_ALIGN.LEFT)

add_rect(s, Inches(0.7), Inches(4.7), Inches(1.5), Inches(0.06), fill_rgb=COL_AMBER)
add_text(s, "10년 국가급 농축산 전환 프로젝트  |  총예산 1조 8,000억원",
         Inches(0.7), Inches(4.9), Inches(9), Inches(0.45),
         font_size=14, color=COL_GREEN_LIGHT)
add_text(s, "2027년 300억 선도사업 → 2036년 통합특구 완성",
         Inches(0.7), Inches(5.35), Inches(9), Inches(0.45),
         font_size=13, color=COL_AMBER, bold=True)

add_text(s, "2026. 06.  |  산지방목특구추진단",
         Inches(0.7), Inches(6.1), Inches(5), Inches(0.4),
         font_size=12, color=COL_WHITE)


# ════════════════════════════════════════════════════════════════
#  SLIDE 2 — 왜 지금인가 (군수 임기 4년 골든타임)
# ════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
add_rect(s, 0, 0, SLIDE_W, SLIDE_H, fill_rgb=COL_LIGHT_GRAY)
header_bar(s, "왜 지금인가 — 군수 임기 4년이 골든타임", badge="긴급성")

section_chip(s, "지금 시작해야 하는 이유", Inches(0.4), Inches(1.45), w=Inches(3.0))
reasons = [
    "탄소중립 2030 목표 → 2027년 이전 착수 없으면 국비 배분 대열 탈락",
    "RE100·ESG 기업 PPA 시장은 2025~2028년이 선점 윈도우 → 이후 경쟁 포화",
    "농촌공간재구조화 사업 (농식품부) 1차 공모 2027년 마감 예정",
    "전국 지자체 그린축산 선점 경쟁 시작 — 함평이 먼저 깃발 꽂지 않으면 타 군이 선점",
    "특별법 입법 최소 2년 소요 → 군수 임기 1년차에 입법 로드맵 수립 필수",
]
bullet_list(s, reasons, Inches(0.5), Inches(1.95), Inches(12.3), font_size=13)

# 임기 타임라인
add_rect(s, Inches(0.4), Inches(4.6), Inches(12.5), Inches(0.06), fill_rgb=COL_GREEN_MID)
milestones = [
    (Inches(0.5), "2026\n취임"),
    (Inches(3.5), "2027\n선도사업\n착공"),
    (Inches(6.5), "2028\n특별법\n시행"),
    (Inches(9.5), "2030\n임기 완료\n시범단지 완성"),
    (Inches(12.0), "2036\n통합특구\n완성"),
]
for lx, label in milestones:
    add_rect(s, lx, Inches(4.45), Inches(0.22), Inches(0.3), fill_rgb=COL_AMBER)
    add_text(s, label, lx - Inches(0.5), Inches(4.8), Inches(1.2), Inches(0.9),
             font_size=10, bold=True, color=COL_GREEN_DARK, align=PP_ALIGN.CENTER)

add_text(s, "군수 임기 4년 (2026~2030) 내에 선도사업 착공 + 특별법 시행 + 시범단지 1단계 완성",
         Inches(0.5), Inches(5.95), Inches(12.3), Inches(0.45),
         font_size=13, bold=True, color=COL_GREEN_DARK, align=PP_ALIGN.CENTER)
footer_bar(s, 2)


# ════════════════════════════════════════════════════════════════
#  SLIDE 3 — 함평군 현황 진단
# ════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
add_rect(s, 0, 0, SLIDE_W, SLIDE_H, fill_rgb=COL_LIGHT_GRAY)
header_bar(s, "함평군 현황 진단 — 위기와 기회", badge="현황")

section_chip(s, "위기 지표", Inches(0.4), Inches(1.45), w=Inches(1.8))
crisis = [
    ("인구", "37,012명", "전남 최저 수준 / 고령화율 35%↑"),
    ("축산", "1,437개 축사", "93% 가축사육제한구역 해당"),
    ("소득", "농업소득 정체", "비축산 대안 부재"),
    ("인프라", "도로·수계 취약", "접근성 한계"),
]
for i, (cat, val, note) in enumerate(crisis):
    lx = Inches(0.4 + i * 3.2)
    add_rect(s, lx, Inches(1.95), Inches(3.0), Inches(1.3),
             fill_rgb=RGBColor(0xFF,0xEB,0xEE))
    add_rect(s, lx, Inches(1.95), Inches(3.0), Inches(0.05),
             fill_rgb=RGBColor(0xC6,0x28,0x28))
    add_text(s, cat, lx, Inches(2.0), Inches(3.0), Inches(0.35),
             font_size=11, color=COL_MID_GRAY, align=PP_ALIGN.CENTER)
    add_text(s, val, lx, Inches(2.35), Inches(3.0), Inches(0.45),
             font_size=15, bold=True, color=RGBColor(0xC6,0x28,0x28), align=PP_ALIGN.CENTER)
    add_text(s, note, lx, Inches(2.8), Inches(3.0), Inches(0.4),
             font_size=10, color=COL_MID_GRAY, align=PP_ALIGN.CENTER)

section_chip(s, "기회 자원", Inches(0.4), Inches(3.45), w=Inches(1.8))
opps = [
    ("산지·초지", "광활한 미활용\n산지·초지 보유"),
    ("태양광", "1,246천㎡ 축사\n지붕 잠재 125MW"),
    ("조사료", "평지 조사료 농지\n자급 잠재 높음"),
    ("브랜드", "나비축제 인지도\n친환경 이미지"),
]
for i, (cat, body) in enumerate(opps):
    lx = Inches(0.4 + i * 3.2)
    add_rect(s, lx, Inches(3.95), Inches(3.0), Inches(1.5), fill_rgb=RGBColor(0xE8,0xF5,0xE9))
    add_rect(s, lx, Inches(3.95), Inches(3.0), Inches(0.05), fill_rgb=COL_GREEN_MID)
    add_text(s, cat, lx, Inches(4.0), Inches(3.0), Inches(0.35),
             font_size=11, color=COL_MID_GRAY, align=PP_ALIGN.CENTER)
    add_text(s, body, lx, Inches(4.4), Inches(3.0), Inches(0.9),
             font_size=13, bold=True, color=COL_GREEN_DARK, align=PP_ALIGN.CENTER)

add_rect(s, Inches(0.4), Inches(5.65), Inches(12.5), Inches(0.8), fill_rgb=COL_GREEN_DARK)
add_text(s, "결론: 위기를 기회로 전환할 전략이 '산지방목 그린축산·에너지공유 특구'",
         Inches(0.5), Inches(5.7), Inches(12.3), Inches(0.7),
         font_size=15, bold=True, color=COL_AMBER, align=PP_ALIGN.CENTER)
footer_bar(s, 3)


# ════════════════════════════════════════════════════════════════
#  SLIDE 4 — 프로젝트 전체 구조 (One-page)
# ════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
add_rect(s, 0, 0, SLIDE_W, SLIDE_H, fill_rgb=COL_LIGHT_GRAY)
header_bar(s, "프로젝트 전체 구조 한눈에 보기", badge="핵심")

# 중앙 허브
add_rect(s, Inches(5.3), Inches(2.8), Inches(2.8), Inches(1.6), fill_rgb=COL_GREEN_DARK)
add_text(s, "함평\n특구", Inches(5.3), Inches(2.9), Inches(2.8), Inches(1.4),
         font_size=22, bold=True, color=COL_AMBER, align=PP_ALIGN.CENTER)

# 주변 사업축 (6개)
axes6 = [
    (Inches(0.3), Inches(1.5), "산지·초지\n순환방목"),
    (Inches(0.3), Inches(3.5), "축사\n태양광"),
    (Inches(0.3), Inches(5.5), "주민배당\n군민펀드"),
    (Inches(10.5), Inches(1.5), "AI Agent\n통합관리"),
    (Inches(10.5), Inches(3.5), "국립축산\nR&D 연계"),
    (Inches(10.5), Inches(5.5), "특별법\n제정"),
]
for lx, ty, label in axes6:
    add_rect(s, lx, ty, Inches(2.2), Inches(1.3), fill_rgb=COL_GREEN_MID)
    add_text(s, label, lx, ty + Inches(0.15), Inches(2.2), Inches(1.0),
             font_size=13, bold=True, color=COL_WHITE, align=PP_ALIGN.CENTER)

# 화살표 텍스트 중앙 연결
add_text(s, "← 연동 →", Inches(2.55), Inches(3.2), Inches(2.8), Inches(0.5),
         font_size=12, color=COL_MID_GRAY, align=PP_ALIGN.CENTER)
add_text(s, "← 연동 →", Inches(8.15), Inches(3.2), Inches(2.3), Inches(0.5),
         font_size=12, color=COL_MID_GRAY, align=PP_ALIGN.CENTER)

# 하단 성과 지표
perf = [("1조 8,000억", "총 투자"), ("125MW", "태양광"), ("연 12만톤", "탄소감축"), ("군민 41만원", "연 배당")]
for i, (val, lb) in enumerate(perf):
    lx = Inches(0.5 + i * 3.2)
    add_rect(s, lx, Inches(6.35), Inches(3.0), Inches(0.7), fill_rgb=COL_AMBER)
    add_text(s, val, lx, Inches(6.37), Inches(3.0), Inches(0.4),
             font_size=15, bold=True, color=COL_DARK_GRAY, align=PP_ALIGN.CENTER)
    add_text(s, lb, lx, Inches(6.78), Inches(3.0), Inches(0.25),
             font_size=10, color=COL_DARK_GRAY, align=PP_ALIGN.CENTER)
footer_bar(s, 4)


# ════════════════════════════════════════════════════════════════
#  SLIDE 5 — 규제 장벽과 특별법 전략
# ════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
add_rect(s, 0, 0, SLIDE_W, SLIDE_H, fill_rgb=COL_LIGHT_GRAY)
header_bar(s, "규제 장벽과 특별법 전략", badge="선결과제")

section_chip(s, "핵심 규제 장벽", Inches(0.4), Inches(1.45), w=Inches(2.2))
add_text(s, "현행법 내에서는 산지방목 특구 조성이 실질적으로 불가능합니다.",
         Inches(0.5), Inches(1.9), Inches(12.3), Inches(0.4),
         font_size=13, bold=True, color=RGBColor(0xC6,0x28,0x28))

walls = [
    ("가축사육제한구역", "사업장 93% 해당 → 신규 축사·방목단지 사실상 불허"),
    ("농지법·산지관리법", "농림지 전용 이중 규제 → 방목구획 설정 법적 근거 없음"),
    ("소규모 농가 RE법", "REC·PPA 참여 법적 근거 미비 → 태양광 수익 배분 불가"),
]
for i, (law, issue) in enumerate(walls):
    lx = Inches(0.4)
    ty = Inches(2.4 + i * 0.85)
    add_rect(s, lx, ty, Inches(2.8), Inches(0.72), fill_rgb=RGBColor(0xC6,0x28,0x28))
    add_text(s, law, lx, ty + Inches(0.12), Inches(2.8), Inches(0.5),
             font_size=12, bold=True, color=COL_WHITE, align=PP_ALIGN.CENTER)
    add_rect(s, Inches(3.3), ty, Inches(9.7), Inches(0.72), fill_rgb=COL_WHITE)
    add_text(s, issue, Inches(3.4), ty + Inches(0.1), Inches(9.5), Inches(0.55),
             font_size=12, color=COL_DARK_GRAY)

section_chip(s, "특별법 추진 전략", Inches(0.4), Inches(5.05), w=Inches(2.2))
strategy = [
    "2026년 하반기: 입법 로드맵 수립 + 국회의원 협력 채널 구축",
    "2027년 상반기: 특별법 발의 → 국회 농림위 통과 목표",
    "2027년 하반기: 시행령·조례 패키지 완비 → 선도사업 허가 착수",
]
bullet_list(s, strategy, Inches(0.5), Inches(5.55), Inches(12.3), font_size=13)
footer_bar(s, 5)


# ════════════════════════════════════════════════════════════════
#  SLIDE 6 — GIS 후보지 현황
# ════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
add_rect(s, 0, 0, SLIDE_W, SLIDE_H, fill_rgb=COL_LIGHT_GRAY)
header_bar(s, "GIS 후보지 분석 현황", badge="진행중")

section_chip(s, "분석 완료 현황", Inches(0.4), Inches(1.45), w=Inches(2.0))
done_items = [
    "축사 주소 지오코딩 완료 (1,429/1,437개소, 99.4%)",
    "행정경계·수계·도로·DEM 분석 완료 (OSM·Copernicus)",
    "연속지적도 24만 필지 지목 분석 완료",
    "가축사육제한구역·용도지역 중첩 분석 완료 (VWorld)",
    "9개 읍면 예비 후보권역 생성 + 1차 점수화 완료",
]
for i, item in enumerate(done_items):
    add_rect(s, Inches(0.4), Inches(1.95 + i * 0.55), Inches(0.45), Inches(0.45),
             fill_rgb=COL_GREEN_MID)
    add_text(s, "✓", Inches(0.4), Inches(1.98 + i * 0.55), Inches(0.45), Inches(0.4),
             font_size=13, bold=True, color=COL_WHITE, align=PP_ALIGN.CENTER)
    add_text(s, item, Inches(0.95), Inches(1.95 + i * 0.55), Inches(12.0), Inches(0.5),
             font_size=13, color=COL_DARK_GRAY)

section_chip(s, "다음 단계 (보전산지·초지 파일 확보 후)", Inches(0.4), Inches(4.75), w=Inches(3.8))
next_items = [
    "후보지 10곳 도출 → 3곳 압축 → 최종 1곳 현장조사",
    "보전산지·초지 GIS 파일: 산림청·농식품부 요청 진행 중",
]
bullet_list(s, next_items, Inches(0.5), Inches(5.25), Inches(12.3), font_size=13)

# 읍면별 현황 요약
add_rect(s, Inches(0.4), Inches(5.95), Inches(12.5), Inches(0.08), fill_rgb=COL_AMBER)
add_text(s, "최우선 검토: 손불면(218개, 조사료 최적) · 신광면(196개, 산지 우수) · 대동면(177개)",
         Inches(0.5), Inches(6.1), Inches(12.3), Inches(0.45),
         font_size=13, bold=True, color=COL_GREEN_DARK)
footer_bar(s, 6)


# ════════════════════════════════════════════════════════════════
#  SLIDE 7 — 손불면 선도 시나리오
# ════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
add_rect(s, 0, 0, SLIDE_W, SLIDE_H, fill_rgb=COL_LIGHT_GRAY)
header_bar(s, "손불면 선도 시나리오 — 1순위 후보", badge="1순위")

section_chip(s, "손불면 선택 근거", Inches(0.4), Inches(1.45), w=Inches(2.2))
rationale = [
    "함평군 축사 수 최다 — 218개소 (전체 15.2%) → 집약적 첫 성과 창출 가능",
    "평지·조사료 농지 비율 높음 → 방목 + 조사료 자급 동시 실증 최적",
    "기존 축사 밀집 → 태양광 설치 잠재 21.8MW (연간 수익 약 14억원)",
    "도로 접근성 양호 → 방역·관리 차량 동선 확보 용이",
]
bullet_list(s, rationale, Inches(0.5), Inches(1.95), Inches(12.3), font_size=13)

section_chip(s, "손불면 선도사업 성과 목표 (2027~2030)", Inches(0.4), Inches(3.65), w=Inches(4.0))
targets = [
    ("조사료 자급", "호당 30% 달성\n→ 사료비 절감"),
    ("태양광 설치", "218개소 순차 설치\n→ 연 14억원 수익"),
    ("방목 브랜드", "손불 그린한우\n→ kg당 15% 프리미엄"),
    ("주민배당", "손불면 가구\n연 50만원↑ 배당"),
]
for i, (title, body) in enumerate(targets):
    lx = Inches(0.4 + i * 3.2)
    add_rect(s, lx, Inches(4.15), Inches(3.0), Inches(2.5), fill_rgb=COL_WHITE)
    add_rect(s, lx, Inches(4.15), Inches(3.0), Inches(0.45), fill_rgb=COL_BROWN)
    add_text(s, title, lx, Inches(4.17), Inches(3.0), Inches(0.42),
             font_size=13, bold=True, color=COL_WHITE, align=PP_ALIGN.CENTER)
    add_text(s, body, lx + Inches(0.15), Inches(4.7), Inches(2.7), Inches(1.8),
             font_size=13, color=COL_DARK_GRAY, align=PP_ALIGN.CENTER)
footer_bar(s, 7)


# ════════════════════════════════════════════════════════════════
#  SLIDE 8 — 주민 동의 전략
# ════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
add_rect(s, 0, 0, SLIDE_W, SLIDE_H, fill_rgb=COL_LIGHT_GRAY)
header_bar(s, "주민·농가 동의 확보 전략", badge="협의")

section_chip(s, "이해관계자 지도", Inches(0.4), Inches(1.45), w=Inches(2.2))
stakeholders = [
    ("축산 농가", "직접 이해당사자", "지분참여·임대수익 제시"),
    ("인근 주민", "악취·소음 민원", "배당 수익 공유 → 찬성 전환"),
    ("군의회", "예산 의결권", "고용·세수 효과 자료 제시"),
    ("전남도청", "도비 매칭", "광역 그린축산 모델 포지셔닝"),
]
cols_w = [Inches(2.5), Inches(3.0), Inches(3.0), Inches(4.2)]
col_lbs = ["이해관계자", "핵심 관심사", "설득 핵심 메시지"]
lx = Inches(0.3)
for j, (lb, cw) in enumerate(zip(col_lbs, cols_w[:3])):
    add_rect(s, lx + Inches(j * 3.15), Inches(1.95), cw - Inches(0.05), Inches(0.45),
             fill_rgb=COL_GREEN_DARK)
    add_text(s, lb, lx + Inches(j * 3.15), Inches(1.95), cw, Inches(0.45),
             font_size=11, bold=True, color=COL_WHITE, align=PP_ALIGN.CENTER)
add_rect(s, Inches(9.45), Inches(1.95), Inches(3.8), Inches(0.45), fill_rgb=COL_GREEN_DARK)
add_text(s, "대응 전략", Inches(9.45), Inches(1.95), Inches(3.8), Inches(0.45),
         font_size=11, bold=True, color=COL_WHITE, align=PP_ALIGN.CENTER)

for i, (who, concern, msg, action) in enumerate([
    ("축산 농가", "수익·땅·권리 유지", "지분참여 = 소유권 유지", "선도 농가 인센티브 우선"),
    ("인근 주민", "악취·경관·안전", "배당 + 악취 저감 동시", "주민설명회 배당 모델 공개"),
    ("군의회", "표심·예산 효율", "고용 2,200명·세수 확대", "의회 브리핑 데이터 패키지"),
    ("전남도청", "도 정책 부합성", "RE100·그린뉴딜 선도", "도지사 공동 발표 제안"),
]):
    bg = COL_WHITE if i % 2 == 0 else COL_LIGHT_GRAY
    row_data = [who, concern, msg, action]
    cols_x = [Inches(0.3), Inches(2.85), Inches(6.0), Inches(9.45)]
    cols_ww = [Inches(2.5), Inches(3.1), Inches(3.4), Inches(3.8)]
    for j, (cell, lx2, cw) in enumerate(zip(row_data, cols_x, cols_ww)):
        add_rect(s, lx2, Inches(2.45 + i * 0.82), cw - Inches(0.05), Inches(0.78), fill_rgb=bg)
        add_text(s, cell, lx2 + Inches(0.05), Inches(2.5 + i * 0.82),
                 cw - Inches(0.1), Inches(0.68),
                 font_size=11, color=COL_DARK_GRAY, align=PP_ALIGN.CENTER if j < 3 else PP_ALIGN.LEFT)

section_chip(s, "추진 순서", Inches(0.4), Inches(5.9), w=Inches(1.8))
add_text(s, "비공개 간담회(농가) → 주민설명회 → 군의회 보고 → 전남도 협의 → 입법 추진",
         Inches(0.5), Inches(6.35), Inches(12.3), Inches(0.45),
         font_size=13, bold=True, color=COL_GREEN_DARK)
footer_bar(s, 8)


# ════════════════════════════════════════════════════════════════
#  SLIDE 9 — 예산 확보 로드맵
# ════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
add_rect(s, 0, 0, SLIDE_W, SLIDE_H, fill_rgb=COL_LIGHT_GRAY)
header_bar(s, "예산 확보 로드맵", badge="예산")

section_chip(s, "2027년 300억 선도사업 구성안", Inches(0.4), Inches(1.45), w=Inches(3.5))
budget_2027 = [
    ("국비", "150억원", "농식품부 축산환경개선+신재생에너지"),
    ("도비", "75억원", "전남도 그린에너지·농촌재구조화"),
    ("군비", "45억원", "함평군 일반회계+특별회계"),
    ("민간", "30억원", "RE100 기업·농협 공동투자"),
]
for i, (src, amt, detail) in enumerate(budget_2027):
    lx = Inches(0.4 + i * 3.2)
    add_rect(s, lx, Inches(1.95), Inches(3.0), Inches(1.5),
             fill_rgb=COL_GREEN_LIGHT if i < 3 else RGBColor(0xFF, 0xF8, 0xE1))
    add_text(s, src, lx, Inches(2.0), Inches(3.0), Inches(0.38),
             font_size=12, color=COL_MID_GRAY, align=PP_ALIGN.CENTER)
    add_text(s, amt, lx, Inches(2.38), Inches(3.0), Inches(0.48),
             font_size=20, bold=True, color=COL_GREEN_DARK, align=PP_ALIGN.CENTER)
    add_text(s, detail, lx, Inches(2.9), Inches(3.0), Inches(0.5),
             font_size=9, color=COL_MID_GRAY, align=PP_ALIGN.CENTER)

section_chip(s, "10년 총예산 1조 8,000억원 분해", Inches(0.4), Inches(3.65), w=Inches(3.5))
yr_budgets = [
    ("2027", "300억", COL_GREEN_MID),
    ("2028~30", "2,500억", COL_GREEN_MID),
    ("2031~33", "6,200억", COL_AMBER),
    ("2034~36", "9,000억", COL_AMBER),
]
for i, (yr, amt, color) in enumerate(yr_budgets):
    lx = Inches(0.4 + i * 3.2)
    bar_h = Inches(0.4 + i * 0.35)
    add_rect(s, lx, Inches(6.85) - bar_h, Inches(3.0), bar_h, fill_rgb=color)
    add_text(s, yr, lx, Inches(4.2), Inches(3.0), Inches(0.4),
             font_size=11, color=COL_MID_GRAY, align=PP_ALIGN.CENTER)
    add_text(s, amt, lx, Inches(4.6), Inches(3.0), Inches(0.4),
             font_size=13, bold=True, color=COL_GREEN_DARK, align=PP_ALIGN.CENTER)
footer_bar(s, 9)


# ════════════════════════════════════════════════════════════════
#  SLIDE 10 — 군수 임기 내 핵심 성과 목표
# ════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
add_rect(s, 0, 0, SLIDE_W, SLIDE_H, fill_rgb=COL_LIGHT_GRAY)
header_bar(s, "군수 임기 내 핵심 성과 목표 (2026~2030)", badge="성과목표")

add_text(s, "임기 4년 안에 이것만 이루면 됩니다",
         Inches(0.4), Inches(1.45), Inches(12.5), Inches(0.55),
         font_size=16, bold=True, color=COL_GREEN_DARK, align=PP_ALIGN.CENTER)

kpis = [
    ("①", "특별법 제정", "2028년까지 국회 통과", COL_GREEN_MID),
    ("②", "선도사업 착공", "2027년 3월 300억 착공", COL_GREEN_MID),
    ("③", "시범단지 1단계", "손불면 100ha 조성 착수", COL_BROWN),
    ("④", "태양광 1차", "30MW 설치 완료", COL_BROWN),
    ("⑤", "주민배당 개시", "2029년 배당 첫 지급", COL_ACCENT_BLUE),
    ("⑥", "전국 모델 수출", "타 지자체 벤치마킹 1건↑", COL_ACCENT_BLUE),
]
for i, (num, title, target, color) in enumerate(kpis):
    col = i % 3
    row = i // 3
    lx = Inches(0.4 + col * 4.3)
    ty = Inches(2.2 + row * 2.15)
    add_rect(s, lx, ty, Inches(4.1), Inches(1.9), fill_rgb=COL_WHITE)
    add_rect(s, lx, ty, Inches(4.1), Inches(0.55), fill_rgb=color)
    add_text(s, f"{num}  {title}", lx + Inches(0.1), ty + Inches(0.05),
             Inches(3.9), Inches(0.48),
             font_size=14, bold=True, color=COL_WHITE)
    add_text(s, target, lx + Inches(0.1), ty + Inches(0.7), Inches(3.9), Inches(0.9),
             font_size=14, color=COL_DARK_GRAY)

footer_bar(s, 10)


# ════════════════════════════════════════════════════════════════
#  SLIDE 11 — 기대효과 (군수 리더십 프레임)
# ════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
add_rect(s, 0, 0, SLIDE_W, SLIDE_H, fill_rgb=COL_LIGHT_GRAY)
header_bar(s, "군수 임기 레거시 — 함평을 전국 모델로", badge="레거시")

add_text(s, "이 프로젝트가 성공하면 함평군수는 대한민국 그린축산 전환의 선구자가 됩니다.",
         Inches(0.4), Inches(1.45), Inches(12.5), Inches(0.5),
         font_size=14, italic=True, color=COL_GREEN_DARK, align=PP_ALIGN.CENTER)

legacy_items = [
    ("경제 레거시", COL_GREEN_MID,
     "• 10년 누적 생산유발 2조 2천억원\n• 지역 고용 2,200명 창출\n• 군민 1인 연 배당 41만원"),
    ("환경 레거시", COL_ACCENT_BLUE,
     "• 탄소 연 12만톤 감축\n• 산지 생태 복원 1,500ha\n• 악취 민원 80% 저감"),
    ("정책 레거시", COL_BROWN,
     "• 특별법 제정 선도\n• 전국 확산 모델 개발\n• 농림부 우수사례 선정"),
]
for i, (title, color, body) in enumerate(legacy_items):
    lx = Inches(0.4 + i * 4.3)
    add_rect(s, lx, Inches(2.2), Inches(4.1), Inches(4.0), fill_rgb=COL_WHITE)
    add_rect(s, lx, Inches(2.2), Inches(4.1), Inches(0.6), fill_rgb=color)
    add_text(s, title, lx + Inches(0.1), Inches(2.22), Inches(3.9), Inches(0.56),
             font_size=16, bold=True, color=COL_WHITE)
    add_text(s, body, lx + Inches(0.15), Inches(2.9), Inches(3.8), Inches(3.2),
             font_size=14, color=COL_DARK_GRAY)

add_rect(s, Inches(0.4), Inches(6.35), Inches(12.5), Inches(0.7), fill_rgb=COL_GREEN_DARK)
add_text(s, "\"함평이 먼저, 전국이 따른다\" — 군수님의 10년 비전을 지금 시작합니다",
         Inches(0.5), Inches(6.4), Inches(12.3), Inches(0.6),
         font_size=14, bold=True, color=COL_AMBER, align=PP_ALIGN.CENTER)
footer_bar(s, 11)


# ════════════════════════════════════════════════════════════════
#  SLIDE 12 — 축산농가 보상·지분 참여
# ════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
add_rect(s, 0, 0, SLIDE_W, SLIDE_H, fill_rgb=COL_LIGHT_GRAY)
header_bar(s, "축산농가 보상·지분 참여 구조", badge="농가설득")

section_chip(s, "농가 참여 유인 설계", Inches(0.4), Inches(1.45), w=Inches(2.5))
incentives = [
    ("지붕 임대수익", "연 500~800만원/농가 (태양광 임대료)"),
    ("지분 참여", "발전사업 10~20% 지분 → 수익 지속 배당"),
    ("방목지 전환 보상", "유휴 농지 방목지 임대 → 토지 수익화"),
    ("브랜드 프리미엄", "그린축산 인증 → 출하가 15% 프리미엄"),
    ("사료비 절감", "조사료 자급 30% → 연 300~500만원 절감"),
    ("AI 관리 지원", "방역·성장 AI 모니터링 무상 제공"),
]
for i, (title, detail) in enumerate(incentives):
    col = i % 2
    row = i // 2
    lx = Inches(0.4 + col * 6.4)
    ty = Inches(1.95 + row * 1.25)
    add_rect(s, lx, ty, Inches(6.1), Inches(1.1), fill_rgb=COL_WHITE)
    add_rect(s, lx, ty, Inches(0.1), Inches(1.1), fill_rgb=COL_AMBER)
    add_text(s, title, lx + Inches(0.2), ty + Inches(0.08), Inches(5.8), Inches(0.42),
             font_size=13, bold=True, color=COL_GREEN_DARK)
    add_text(s, detail, lx + Inches(0.2), ty + Inches(0.52), Inches(5.8), Inches(0.5),
             font_size=12, color=COL_DARK_GRAY)

add_rect(s, Inches(0.4), Inches(5.85), Inches(12.5), Inches(0.7), fill_rgb=COL_GREEN_DARK)
add_text(s, "핵심 원칙: 농가는 소유권을 유지하면서 수익만 추가로 얻는 구조",
         Inches(0.5), Inches(5.9), Inches(12.3), Inches(0.6),
         font_size=14, bold=True, color=COL_AMBER, align=PP_ALIGN.CENTER)
footer_bar(s, 12)


# ════════════════════════════════════════════════════════════════
#  SLIDE 13 — 전라남도 연계 전략
# ════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
add_rect(s, 0, 0, SLIDE_W, SLIDE_H, fill_rgb=COL_LIGHT_GRAY)
header_bar(s, "전라남도 연계 전략", badge="도비확보")

section_chip(s, "전남도 정책 연계 포인트", Inches(0.4), Inches(1.45), w=Inches(3.0))
jn_links = [
    "전남 그린에너지 2030 → 함평 축사태양광 125MW = 도 목표 기여",
    "전남 농촌공간재구조화 사업 → 함평 산지방목 선도 모델 = 도 대표 사례",
    "전남 RE100 산단 유치 → 함평 PPA 공급원 = 상호 보완",
    "전남 청년 귀농·귀촌 사업 → 함평 특구 청년 유입 = 인구 목표 기여",
]
bullet_list(s, jn_links, Inches(0.5), Inches(1.95), Inches(12.3), font_size=13)

section_chip(s, "도비 확보 전략", Inches(0.4), Inches(3.85), w=Inches(2.2))
strategy_items = [
    "도지사 면담 → 함평 특구 도 대표 사업 지정 요청",
    "전남도 축산환경개선 지원사업 공모 최우선 신청",
    "전남도 신재생에너지 특화단지 공동 지정 제안",
    "전남 농업기술원·국립축산과학원 공동 R&D 협약",
]
bullet_list(s, strategy_items, Inches(0.5), Inches(4.35), Inches(12.3), font_size=13)

add_rect(s, Inches(0.4), Inches(6.05), Inches(12.5), Inches(0.7), fill_rgb=RGBColor(0xE8,0xF5,0xE9))
add_rect(s, Inches(0.4), Inches(6.05), Inches(0.08), Inches(0.7), fill_rgb=COL_GREEN_MID)
add_text(s, "목표: 2026년 하반기 도지사 보고 → 전남도 대표 농축산 전환 사업으로 격상",
         Inches(0.55), Inches(6.1), Inches(12.1), Inches(0.6),
         font_size=13, bold=True, color=COL_GREEN_DARK)
footer_bar(s, 13)


# ════════════════════════════════════════════════════════════════
#  SLIDE 14 — 단계별 추진 일정 (군수 임기 중심)
# ════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
add_rect(s, 0, 0, SLIDE_W, SLIDE_H, fill_rgb=COL_LIGHT_GRAY)
header_bar(s, "단계별 추진 일정", badge="로드맵")

phases = [
    ("준비기\n2026.06~12", [
        "GIS 후보지 확정",
        "특별법 로드맵 수립",
        "농가 간담회 개최",
        "전남도 협의 착수",
    ], COL_GREEN_DARK),
    ("선도기\n2027.01~12", [
        "특별법 발의",
        "300억 착공",
        "시범단지 설계",
        "태양광 1차 허가",
    ], COL_GREEN_MID),
    ("확장기\n2028~2030", [
        "특별법 시행",
        "방목단지 100ha",
        "30MW 발전 개시",
        "주민배당 첫 지급",
    ], COL_BROWN),
    ("완성기\n2031~2036", [
        "통합특구 300ha",
        "125MW 달성",
        "전국 모델 수출",
        "1조 8천억 완성",
    ], COL_AMBER),
]
for i, (phase, tasks, color) in enumerate(phases):
    lx = Inches(0.35 + i * 3.25)
    add_rect(s, lx, Inches(1.5), Inches(3.1), Inches(5.2), fill_rgb=COL_WHITE)
    add_rect(s, lx, Inches(1.5), Inches(3.1), Inches(0.8), fill_rgb=color)
    add_text(s, phase, lx, Inches(1.55), Inches(3.1), Inches(0.7),
             font_size=13, bold=True, color=COL_WHITE if color != COL_AMBER else COL_DARK_GRAY,
             align=PP_ALIGN.CENTER)
    for j, task in enumerate(tasks):
        add_text(s, f"✓  {task}", lx + Inches(0.15), Inches(2.45 + j * 1.0),
                 Inches(2.85), Inches(0.85),
                 font_size=12, color=COL_DARK_GRAY)

# 군수 임기 강조 박스
add_rect(s, Inches(0.35), Inches(6.8), Inches(6.55), Inches(0.25), fill_rgb=COL_GREEN_MID)
add_text(s, "← 군수 임기 (2026~2030)", Inches(0.35), Inches(6.82), Inches(6.55), Inches(0.22),
         font_size=10, bold=True, color=COL_WHITE, align=PP_ALIGN.CENTER)
footer_bar(s, 14)


# ════════════════════════════════════════════════════════════════
#  SLIDE 15 — AI 통합관리 플랫폼
# ════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
add_rect(s, 0, 0, SLIDE_W, SLIDE_H, fill_rgb=COL_LIGHT_GRAY)
header_bar(s, "AI Agent 통합관리 플랫폼", badge="스마트")

section_chip(s, "플랫폼 개요", Inches(0.4), Inches(1.45), w=Inches(2.0))
add_text(s, "방목·태양광·방역·배당을 하나의 AI 대시보드로 실시간 통합 관리",
         Inches(0.5), Inches(1.9), Inches(12.3), Inches(0.4),
         font_size=13, color=COL_DARK_GRAY)

modules = [
    ("방목\n모니터링", "GPS 위치\n채식량 측정\n로테이션 알림", COL_GREEN_MID),
    ("태양광\n관리", "발전량 실시간\n이상탐지 경보\n수익 자동정산", COL_ACCENT_BLUE),
    ("방역\n관리", "질병 조기경보\n차단방역 최적화\n입출입 자동화", RGBColor(0xC6,0x28,0x28)),
    ("배당\n관리", "수익 자동계산\n배당명세 발송\n군민펀드 현황", COL_BROWN),
]
for i, (title, body, color) in enumerate(modules):
    lx = Inches(0.4 + i * 3.2)
    add_rect(s, lx, Inches(2.5), Inches(3.0), Inches(3.3), fill_rgb=COL_WHITE)
    add_rect(s, lx, Inches(2.5), Inches(3.0), Inches(0.55), fill_rgb=color)
    add_text(s, title, lx, Inches(2.53), Inches(3.0), Inches(0.5),
             font_size=14, bold=True, color=COL_WHITE, align=PP_ALIGN.CENTER)
    add_text(s, body, lx + Inches(0.2), Inches(3.15), Inches(2.65), Inches(2.5),
             font_size=13, color=COL_DARK_GRAY, align=PP_ALIGN.CENTER)

add_text(s, "※ 국립축산과학원 + 민간 AI 기업 협력 / 군청 통합관제센터 설치",
         Inches(0.5), Inches(6.1), Inches(12.3), Inches(0.35),
         font_size=10, color=COL_MID_GRAY, italic=True)
footer_bar(s, 15)


# ════════════════════════════════════════════════════════════════
#  SLIDE 16 — 리스크 및 대응
# ════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
add_rect(s, 0, 0, SLIDE_W, SLIDE_H, fill_rgb=COL_LIGHT_GRAY)
header_bar(s, "리스크 및 대응방안", badge="리스크")

risks = [
    ("특별법 지연", "높음", "규제샌드박스 선적용 + 조례 우선"),
    ("주민 반대", "중간", "배당 조기 가시화 → 찬성 전환"),
    ("농가 저조", "중간", "선도 농가 인센티브 패키지"),
    ("부지 미확보", "낮음", "9읍면 동시 평가 대안 확보"),
    ("예산 미확보", "중간", "도비 + 민간투자 의존도 분산"),
    ("질병 발생", "중간", "AI 조기경보 + 분산방목 구조"),
]
level_col = {"높음": RGBColor(0xC6,0x28,0x28), "중간": COL_AMBER, "낮음": COL_GREEN_MID}
for i, (risk, level, response) in enumerate(risks):
    col = i % 2
    row = i // 2
    lx = Inches(0.4 + col * 6.4)
    ty = Inches(1.55 + row * 1.65)
    add_rect(s, lx, ty, Inches(6.1), Inches(1.5), fill_rgb=COL_WHITE)
    add_rect(s, lx, ty, Inches(6.1), Inches(0.07), fill_rgb=level_col[level])
    add_text(s, risk, lx + Inches(0.15), ty + Inches(0.15), Inches(4.0), Inches(0.45),
             font_size=14, bold=True, color=COL_DARK_GRAY)
    add_rect(s, lx + Inches(4.3), ty + Inches(0.1), Inches(1.6), Inches(0.42),
             fill_rgb=level_col[level])
    add_text(s, level, lx + Inches(4.3), ty + Inches(0.1), Inches(1.6), Inches(0.42),
             font_size=12, bold=True, color=COL_WHITE, align=PP_ALIGN.CENTER)
    add_text(s, f"대응: {response}", lx + Inches(0.15), ty + Inches(0.65), Inches(5.8), Inches(0.75),
             font_size=12, color=COL_MID_GRAY)
footer_bar(s, 16)


# ════════════════════════════════════════════════════════════════
#  SLIDE 17 — 국립축산과학원 R&D 연계
# ════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
add_rect(s, 0, 0, SLIDE_W, SLIDE_H, fill_rgb=COL_LIGHT_GRAY)
header_bar(s, "국립축산과학원 연계 R&D", badge="R&D")

section_chip(s, "연계 전략", Inches(0.4), Inches(1.45), w=Inches(1.8))
add_text(s, "함평 시범단지를 국립축산과학원 현장 시험지로 지정 → 정부 R&D 예산 자동 유입",
         Inches(0.5), Inches(1.9), Inches(12.3), Inches(0.45),
         font_size=13, bold=True, color=COL_GREEN_DARK)

rd_topics = [
    "한국형 산지방목 기술기준 수립",
    "방목 한우·면양 성장·품질 실증",
    "조사료 자급 모델 최적화",
    "축사태양광 복합 효율 실증",
    "AI 방역·건강관리 현장 적용",
    "탄소흡수량 측정·크레딧 인증",
]
for i, topic in enumerate(rd_topics):
    col = i % 2
    row = i // 2
    lx = Inches(0.4 + col * 6.4)
    ty = Inches(2.6 + row * 1.1)
    add_rect(s, lx, ty, Inches(6.1), Inches(1.0), fill_rgb=COL_WHITE)
    add_rect(s, lx, ty, Inches(0.08), Inches(1.0), fill_rgb=COL_GREEN_MID)
    add_text(s, topic, lx + Inches(0.2), ty + Inches(0.22), Inches(5.8), Inches(0.55),
             font_size=13, color=COL_DARK_GRAY)

add_rect(s, Inches(0.4), Inches(5.95), Inches(12.5), Inches(0.7), fill_rgb=COL_GREEN_DARK)
add_text(s, "성과: 전국 확산 기술 표준 개발 → 함평군이 대한민국 그린축산 기술 메카",
         Inches(0.5), Inches(6.0), Inches(12.3), Inches(0.6),
         font_size=14, bold=True, color=COL_AMBER, align=PP_ALIGN.CENTER)
footer_bar(s, 17)


# ════════════════════════════════════════════════════════════════
#  SLIDE 18 — 즉시 필요한 군수 결정 사항
# ════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
add_rect(s, 0, 0, SLIDE_W, SLIDE_H, fill_rgb=COL_LIGHT_GRAY)
header_bar(s, "즉시 필요한 군수 결정 사항", badge="의사결정")

section_chip(s, "취임 100일 내 결정·지시 사항", Inches(0.4), Inches(1.45), w=Inches(3.2))

decisions = [
    ("①", "특구추진 전담팀 구성",
     "산지방목특구추진단 TF 구성 지시\n(기획실 + 산업과 + 환경과 합동)"),
    ("②", "전남도 협력 채널 구축",
     "도지사 면담 일정 수립\n함평 특구 도 대표사업 지정 요청"),
    ("③", "GIS 자료 행정 요청",
     "보전산지·초지 파일 산림청 공문 발송\n악취민원·방역권역 농식품부 요청"),
    ("④", "농가 비공개 간담회",
     "선도 농가 20~30인 비공개 간담회\n지분참여·임대수익 모델 설명"),
    ("⑤", "법무 자문단 구성",
     "특별법 입법 자문 법무법인 선정\n조례 개정안 초안 작업 착수"),
    ("⑥", "2027년 예산 편성 지시",
     "선도사업 300억 군비 45억 편성\n농식품부 국비 신청 준비"),
]
for i, (num, title, detail) in enumerate(decisions):
    col = i % 2
    row = i // 2
    lx = Inches(0.4 + col * 6.4)
    ty = Inches(1.95 + row * 1.55)
    add_rect(s, lx, ty, Inches(6.1), Inches(1.42), fill_rgb=COL_WHITE)
    add_rect(s, lx, ty, Inches(0.55), Inches(1.42), fill_rgb=COL_AMBER)
    add_text(s, num, lx, ty + Inches(0.42), Inches(0.55), Inches(0.55),
             font_size=18, bold=True, color=COL_DARK_GRAY, align=PP_ALIGN.CENTER)
    add_text(s, title, lx + Inches(0.65), ty + Inches(0.08), Inches(5.35), Inches(0.45),
             font_size=13, bold=True, color=COL_GREEN_DARK)
    add_text(s, detail, lx + Inches(0.65), ty + Inches(0.55), Inches(5.35), Inches(0.8),
             font_size=11, color=COL_MID_GRAY)
footer_bar(s, 18)


# ════════════════════════════════════════════════════════════════
#  SLIDE 19 — 즉시 착수 일정표
# ════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
add_rect(s, 0, 0, SLIDE_W, SLIDE_H, fill_rgb=COL_LIGHT_GRAY)
header_bar(s, "즉시 착수 — 2026년 하반기 액션플랜", badge="액션")

action_months = [
    ("6월", ["특구추진 TF 구성", "GIS 자료 행정요청", "법무 자문단 선정"]),
    ("7월", ["농가 비공개 간담회", "전남도 면담 추진", "후보지 3곳 선정"]),
    ("8월", ["주민설명회 준비", "특별법 초안 작성", "예산 신청서 작성"]),
    ("9월", ["주민설명회 개최", "군의회 보고", "전남도 도비 신청"]),
    ("10~11월", ["국비 신청 제출", "국립축산원 협약", "시범단지 기본계획 확정"]),
    ("12월", ["2027년 예산 의결", "착공 준비 완료", "선도사업 허가 착수"]),
]
for i, (month, tasks) in enumerate(action_months):
    col = i % 3
    row = i // 3
    lx = Inches(0.35 + col * 4.3)
    ty = Inches(1.5 + row * 2.55)
    add_rect(s, lx, ty, Inches(4.1), Inches(2.35), fill_rgb=COL_WHITE)
    add_rect(s, lx, ty, Inches(4.1), Inches(0.5), fill_rgb=COL_GREEN_MID if row == 0 else COL_BROWN)
    add_text(s, f"2026년  {month}", lx + Inches(0.1), ty + Inches(0.06),
             Inches(3.9), Inches(0.42),
             font_size=13, bold=True, color=COL_WHITE)
    for j, task in enumerate(tasks):
        add_text(s, f"▸ {task}", lx + Inches(0.15), ty + Inches(0.6 + j * 0.55),
                 Inches(3.8), Inches(0.5),
                 font_size=12, color=COL_DARK_GRAY)
footer_bar(s, 19)


# ════════════════════════════════════════════════════════════════
#  SLIDE 20 — 마무리·협조 요청
# ════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
add_rect(s, 0, 0, SLIDE_W, SLIDE_H, fill_rgb=COL_GREEN_DARK)
add_rect(s, Inches(9.0), 0, Inches(4.5), SLIDE_H, fill_rgb=RGBColor(0x16,0x50,0x16))
add_rect(s, 0, Inches(4.8), SLIDE_W, Inches(0.08), fill_rgb=COL_AMBER)

# 배지
add_rect(s, Inches(0.6), Inches(0.4), Inches(3.5), Inches(0.55), fill_rgb=COL_AMBER)
add_text(s, "군수 당선자 보고자료  (비공개)", Inches(0.6), Inches(0.42), Inches(3.5), Inches(0.5),
         font_size=12, bold=True, color=COL_DARK_GRAY, align=PP_ALIGN.CENTER)

add_text(s, "함평이 먼저,\n전국이 따릅니다",
         Inches(0.7), Inches(1.2), Inches(8.0), Inches(1.8),
         font_size=38, bold=True, color=COL_WHITE, align=PP_ALIGN.LEFT)
add_rect(s, Inches(0.7), Inches(3.1), Inches(2.0), Inches(0.07), fill_rgb=COL_AMBER)

add_text(s, "군수님의 결단이 함평 10년을 바꿉니다.",
         Inches(0.7), Inches(3.35), Inches(8.0), Inches(0.55),
         font_size=16, color=COL_GREEN_LIGHT)

# 요청사항 박스
add_rect(s, Inches(0.7), Inches(4.15), Inches(7.8), Inches(2.3),
         fill_rgb=RGBColor(0x16,0x50,0x16))
add_text(s, "협조 요청 사항",
         Inches(0.85), Inches(4.2), Inches(7.5), Inches(0.45),
         font_size=14, bold=True, color=COL_AMBER)
requests_txt = [
    "① 특구추진 전담 TF 구성 지시",
    "② 전남도지사 면담 및 도 대표사업 지정 요청",
    "③ GIS 원자료 확보 공문 발송 (산림청·농식품부)",
    "④ 2027년 선도사업 예산 300억 편성 지시",
]
for j, req in enumerate(requests_txt):
    add_text(s, req, Inches(0.85), Inches(4.72 + j * 0.42), Inches(7.5), Inches(0.4),
             font_size=12, color=COL_WHITE)

add_text(s, "산지방목특구추진단  드림\n2026. 06.",
         Inches(0.7), Inches(6.55), Inches(5), Inches(0.55),
         font_size=12, color=COL_GREEN_LIGHT)

# 마지막 슬라이드 - 별도 푸터
add_rect(s, 0, Inches(7.15), SLIDE_W, Inches(0.35), fill_rgb=COL_GREEN_DARK)
add_text(s, "함평 산지방목 그린축산·에너지공유 특구 조성사업  |  군수 당선자 보고자료",
         Inches(0.3), Inches(7.18), Inches(12.5), Inches(0.28),
         font_size=9, color=COL_GREEN_LIGHT, align=PP_ALIGN.CENTER)


# ── 저장 ─────────────────────────────────────────────────────────
output_path = "/home/user/michaechang_study/함평_산지방목_군수당선자_보고자료.pptx"
prs.save(output_path)
print(f"✅ 군수 당선자 보고자료 PPTX 저장 완료: {output_path}")
print(f"   슬라이드 수: {len(prs.slides)}")
