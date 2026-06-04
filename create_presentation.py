"""
함평군 통합 축산 프로젝트 발표자료 PPTX 생성
함평군 CI: 녹색(#2E7D32 / #43A047), 황토(#8D6E63), 흰색/회색 계열
나비 축제 심볼 → 자연·생태·그린 이미지
"""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Cm
import copy

# ── 함평군 CI 색상 팔레트 ──────────────────────────────────────
COL_GREEN_DARK   = RGBColor(0x1B, 0x5E, 0x20)   # #1B5E20  진녹색(메인)
COL_GREEN_MID    = RGBColor(0x2E, 0x7D, 0x32)   # #2E7D32  녹색
COL_GREEN_LIGHT  = RGBColor(0xA5, 0xD6, 0xA7)   # #A5D6A7  연녹색
COL_AMBER        = RGBColor(0xF9, 0xA8, 0x25)   # #F9A825  황금/나비
COL_BROWN        = RGBColor(0x6D, 0x4C, 0x41)   # #6D4C41  황토
COL_WHITE        = RGBColor(0xFF, 0xFF, 0xFF)
COL_LIGHT_GRAY   = RGBColor(0xF5, 0xF5, 0xF5)
COL_DARK_GRAY    = RGBColor(0x21, 0x21, 0x21)
COL_MID_GRAY     = RGBColor(0x75, 0x75, 0x75)
COL_ACCENT_BLUE  = RGBColor(0x01, 0x57, 0x9B)   # 강조(물/수계)

SLIDE_W = Inches(13.33)
SLIDE_H = Inches(7.5)

prs = Presentation()
prs.slide_width  = SLIDE_W
prs.slide_height = SLIDE_H

BLANK = prs.slide_layouts[6]   # 완전 빈 레이아웃

# ── 헬퍼 함수 ────────────────────────────────────────────────────

def add_rect(slide, l, t, w, h, fill_rgb=None, line_rgb=None, line_pt=0):
    from pptx.util import Pt
    shape = slide.shapes.add_shape(1, l, t, w, h)   # MSO_SHAPE_TYPE.RECTANGLE=1
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

def add_label_value(slide, label, value, lx, ty, w=Inches(3.8), label_size=11, val_size=13):
    add_text(slide, label, lx, ty, w, Inches(0.3),
             font_size=label_size, color=COL_MID_GRAY)
    add_text(slide, value, lx, ty + Inches(0.3), w, Inches(0.4),
             font_size=val_size, bold=True, color=COL_DARK_GRAY)

def header_bar(slide, title_text, subtitle_text=""):
    """상단 헤더 바 (진녹색 배경 + 황금 액센트 선)"""
    add_rect(slide, 0, 0, SLIDE_W, Inches(1.25), fill_rgb=COL_GREEN_DARK)
    add_rect(slide, 0, Inches(1.25), SLIDE_W, Inches(0.06), fill_rgb=COL_AMBER)
    # 왼쪽 로고 대체 텍스트
    add_text(slide, "함평군", Inches(0.3), Inches(0.1), Inches(1.5), Inches(0.6),
             font_size=20, bold=True, color=COL_AMBER, font_name="맑은 고딕")
    add_text(slide, "Hampyeong-gun", Inches(0.3), Inches(0.65), Inches(2), Inches(0.4),
             font_size=9, color=COL_GREEN_LIGHT, font_name="맑은 고딕")
    # 제목
    add_text(slide, title_text, Inches(2.0), Inches(0.1), Inches(9.5), Inches(0.7),
             font_size=24, bold=True, color=COL_WHITE, align=PP_ALIGN.CENTER)
    if subtitle_text:
        add_text(slide, subtitle_text, Inches(2.0), Inches(0.78), Inches(9.5), Inches(0.38),
                 font_size=13, color=COL_GREEN_LIGHT, align=PP_ALIGN.CENTER)
    # 우측 슬로건
    add_text(slide, "나비의 고장 함평", Inches(11.2), Inches(0.45), Inches(2), Inches(0.45),
             font_size=10, color=COL_AMBER, align=PP_ALIGN.RIGHT)

def footer_bar(slide, page_num, total=20):
    """하단 푸터"""
    add_rect(slide, 0, Inches(7.15), SLIDE_W, Inches(0.35), fill_rgb=COL_GREEN_DARK)
    add_text(slide, "함평 산지방목 그린축산·에너지공유 특구 조성사업",
             Inches(0.3), Inches(7.18), Inches(9), Inches(0.28),
             font_size=9, color=COL_GREEN_LIGHT)
    add_text(slide, f"{page_num} / {total}", Inches(12.5), Inches(7.18),
             Inches(0.7), Inches(0.28),
             font_size=9, color=COL_GREEN_LIGHT, align=PP_ALIGN.RIGHT)

def section_chip(slide, text, lx, ty, w=Inches(2.2), h=Inches(0.38)):
    """섹션 레이블 칩"""
    add_rect(slide, lx, ty, w, h, fill_rgb=COL_GREEN_MID)
    add_text(slide, text, lx, ty, w, h,
             font_size=12, bold=True, color=COL_WHITE, align=PP_ALIGN.CENTER)

def bullet_list(slide, items, lx, ty, w, line_h=Inches(0.42), font_size=13):
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
             font_size=26, bold=True, color=val_color, align=PP_ALIGN.CENTER)
    add_text(slide, unit, lx, ty + Inches(0.92), w, Inches(0.3),
             font_size=10, color=COL_MID_GRAY, align=PP_ALIGN.CENTER)


# ════════════════════════════════════════════════════════════════
#  SLIDE 1 — 표지
# ════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
add_rect(s, 0, 0, SLIDE_W, SLIDE_H, fill_rgb=COL_GREEN_DARK)
# 배경 패턴(연녹 사각형들)
for i, (lf, tp, wd, ht, op) in enumerate([
    (Inches(10), Inches(0), Inches(4), Inches(4), COL_GREEN_MID),
    (Inches(11.5), Inches(3), Inches(3), Inches(5), RGBColor(0x1B,0x69,0x1B)),
    (Inches(0), Inches(5.5), Inches(5), Inches(2.5), RGBColor(0x16,0x50,0x16)),
]):
    add_rect(s, lf, tp, wd, ht, fill_rgb=op)

add_rect(s, 0, Inches(5.2), SLIDE_W, Inches(0.06), fill_rgb=COL_AMBER)

# 군명 + 슬로건
add_text(s, "함평군", Inches(0.7), Inches(0.5), Inches(3), Inches(0.8),
         font_size=28, bold=True, color=COL_AMBER)
add_text(s, "Hampyeong-gun, Jeollanam-do", Inches(0.7), Inches(1.25), Inches(5), Inches(0.4),
         font_size=12, color=COL_GREEN_LIGHT)

# 메인 타이틀
add_text(s, "함평 산지방목\n그린축산·에너지공유 특구\n조성사업",
         Inches(0.7), Inches(2.0), Inches(8.5), Inches(2.5),
         font_size=36, bold=True, color=COL_WHITE, align=PP_ALIGN.LEFT)
add_rect(s, Inches(0.7), Inches(4.6), Inches(1.2), Inches(0.06), fill_rgb=COL_AMBER)

add_text(s, "10년 국가급 농축산 전환 프로젝트",
         Inches(0.7), Inches(4.8), Inches(8), Inches(0.5),
         font_size=16, color=COL_GREEN_LIGHT)

# 날짜·기관
add_text(s, "2026. 06.", Inches(0.7), Inches(5.5), Inches(3), Inches(0.4),
         font_size=13, color=COL_AMBER)
add_text(s, "함평군청  ·  산지방목특구추진단",
         Inches(0.7), Inches(5.9), Inches(5), Inches(0.4),
         font_size=13, color=COL_WHITE)

footer_bar(s, 1)


# ════════════════════════════════════════════════════════════════
#  SLIDE 2 — 목차
# ════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
add_rect(s, 0, 0, SLIDE_W, SLIDE_H, fill_rgb=COL_LIGHT_GRAY)
header_bar(s, "목  차", "Contents")

toc_items = [
    ("01", "프로젝트 개요 및 배경"),
    ("02", "함평군 현황 — 인구·축산 통계"),
    ("03", "핵심 문제 진단 — 규제·현안"),
    ("04", "10대 사업축 종합"),
    ("05", "산지·초지 순환방목"),
    ("06", "기존 축사 지붕형 태양광"),
    ("07", "주민조합·군민펀드 배당"),
    ("08", "AI Agent 통합관리"),
    ("09", "GIS 후보지 분석 결과"),
    ("10", "특별법·법률 패키지 필요성"),
    ("11", "손불면 평지축산 시나리오"),
    ("12", "국립축산과학원 연계 R&D"),
    ("13", "예산 확보 전략"),
    ("14", "단계별 추진 일정"),
    ("15", "기대효과 종합"),
    ("16", "리스크 및 대응방안"),
    ("17", "주민·농가 협의 계획"),
    ("18", "전라남도 연계 전략"),
    ("19", "다음 행동계획"),
    ("20", "참고자료 및 출처"),
]

col_w = Inches(5.8)
for i, (num, title) in enumerate(toc_items):
    col = i // 10
    row = i % 10
    lx = Inches(0.5) + col * (col_w + Inches(0.8))
    ty = Inches(1.55) + row * Inches(0.52)
    add_rect(s, lx, ty + Inches(0.07), Inches(0.55), Inches(0.38), fill_rgb=COL_GREEN_MID)
    add_text(s, num, lx, ty + Inches(0.05), Inches(0.55), Inches(0.4),
             font_size=12, bold=True, color=COL_WHITE, align=PP_ALIGN.CENTER)
    add_text(s, title, lx + Inches(0.65), ty, col_w - Inches(0.7), Inches(0.5),
             font_size=13, color=COL_DARK_GRAY)

footer_bar(s, 2)


# ════════════════════════════════════════════════════════════════
#  SLIDE 3 — 프로젝트 개요 및 배경
# ════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
add_rect(s, 0, 0, SLIDE_W, SLIDE_H, fill_rgb=COL_LIGHT_GRAY)
header_bar(s, "01  프로젝트 개요 및 배경")

section_chip(s, "한 문장 정의", Inches(0.4), Inches(1.45))
add_rect(s, Inches(0.4), Inches(1.9), Inches(12.5), Inches(0.85), fill_rgb=COL_WHITE)
add_rect(s, Inches(0.4), Inches(1.9), Inches(0.1), Inches(0.85), fill_rgb=COL_AMBER)
add_text(s, "함평군의 기존 축산업을 산지방목, 축사태양광, 주민배당, AI축산, 고부가가치 축산물,\n산불예방, 농촌공간 재구조화와 결합한 10년 국가급 농축산 전환 프로젝트로 설계한다.",
         Inches(0.65), Inches(1.95), Inches(12.1), Inches(0.75),
         font_size=13, color=COL_DARK_GRAY)

section_chip(s, "추진 배경", Inches(0.4), Inches(2.95))
bg_items = [
    "축산업 고령화·규모화 정체 → 수익성 한계 심화",
    "탄소중립·그린뉴딜 정책 전환 → 친환경 전환 의무화",
    "산지·초지 미활용 증가 → 산불·생태 위험 상승",
    "농촌 인구 감소 → 지역소멸 위기 가속",
    "RE100·ESG 수요 확대 → 축사태양광 신시장 개방",
]
bullet_list(s, bg_items, Inches(0.5), Inches(3.45), Inches(12))

section_chip(s, "목표", Inches(0.4), Inches(5.7))
add_text(s, "2027년 300억 선도사업 착수  →  2036년 1조 8,000억 통합특구 완성",
         Inches(0.5), Inches(6.15), Inches(12), Inches(0.5),
         font_size=14, bold=True, color=COL_GREEN_DARK)
footer_bar(s, 3)


# ════════════════════════════════════════════════════════════════
#  SLIDE 4 — 함평군 현황 통계
# ════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
add_rect(s, 0, 0, SLIDE_W, SLIDE_H, fill_rgb=COL_LIGHT_GRAY)
header_bar(s, "02  함평군 현황 — 인구·축산 통계")

# 통계 박스 행 1
stats1 = [
    ("총 인구", "37,012", "명"),
    ("총 세대", "21,089", "세대"),
    ("행정구역", "1읍 8면", ""),
    ("면적", "391.4", "km²"),
    ("축사 수", "1,437", "개소"),
]
for i, (lb, val, unit) in enumerate(stats1):
    stat_box(s, lb, val, unit, Inches(0.3 + i * 2.6), Inches(1.45), Inches(2.5), Inches(1.35))

# 통계 박스 행 2
stats2 = [
    ("축사 면적", "1,246천㎡", "합계"),
    ("영업중 사업장", "834", "개소"),
    ("한우 사업장", "381", "개소"),
    ("돼지 사업장", "87", "개소"),
    ("태양광 잠재량", "125MW", "1차 시나리오"),
]
for i, (lb, val, unit) in enumerate(stats2):
    stat_box(s, lb, val, unit, Inches(0.3 + i * 2.6), Inches(3.0), Inches(2.5), Inches(1.35),
             bg=RGBColor(0xE8, 0xF5, 0xE9), val_color=COL_GREEN_MID)

section_chip(s, "읍면별 축사 분포 주요 현황", Inches(0.4), Inches(4.55))
eup_data = "손불면 218개(최다) · 신광면 196개 · 대동면 177개 · 함평읍 158개 · 엄다면 153개 · 학교면 138개"
add_text(s, eup_data, Inches(0.5), Inches(5.05), Inches(12.3), Inches(0.5),
         font_size=12, color=COL_DARK_GRAY)
add_text(s, "※ 공식자료: 함평군 가축사육업 현황, 함평군 축사현황, 통계청 2023",
         Inches(0.5), Inches(5.6), Inches(12), Inches(0.35),
         font_size=10, color=COL_MID_GRAY, italic=True)
footer_bar(s, 4)


# ════════════════════════════════════════════════════════════════
#  SLIDE 5 — 핵심 문제 진단
# ════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
add_rect(s, 0, 0, SLIDE_W, SLIDE_H, fill_rgb=COL_LIGHT_GRAY)
header_bar(s, "03  핵심 문제 진단 — 규제·현안")

section_chip(s, "규제 중첩 정량 분석 결과", Inches(0.4), Inches(1.45))
reg_items = [
    "가축사육제한구역 해당 사업장 93% — 사실상 신규 축사 불가",
    "등록농림지 내 축사 100% → 농지전용·산지전용 이중 규제",
    "수계·도로 이격 규정으로 잠재 부지의 70%↑ 탈락",
    "현행 법령 내 신규 방목단지 조성 경로 사실상 부재",
]
bullet_list(s, reg_items, Inches(0.5), Inches(1.95), Inches(12), font_size=13)

section_chip(s, "문제 구조 요약", Inches(0.4), Inches(3.6))
# 3박스 구조
boxes = [
    ("현행 규제\n한계", "가축사육제한\n농지·산지법\n수계이격"),
    ("결과", "신규 부지\n확보 불가\n기존 농가 고착"),
    ("필요 조치", "특별법 제정\n조례 패키지\n특구 지정"),
]
for i, (title, body) in enumerate(boxes):
    lx = Inches(0.5 + i * 4.2)
    add_rect(s, lx, Inches(4.1), Inches(3.8), Inches(2.0),
             fill_rgb=COL_GREEN_MID if i != 1 else COL_AMBER)
    add_text(s, title, lx, Inches(4.15), Inches(3.8), Inches(0.55),
             font_size=14, bold=True, color=COL_WHITE, align=PP_ALIGN.CENTER)
    add_text(s, body, lx, Inches(4.75), Inches(3.8), Inches(1.3),
             font_size=13, color=COL_WHITE if i != 1 else COL_DARK_GRAY,
             align=PP_ALIGN.CENTER)

add_text(s, "→", Inches(4.35), Inches(4.85), Inches(0.4), Inches(0.5),
         font_size=22, bold=True, color=COL_GREEN_DARK, align=PP_ALIGN.CENTER)
add_text(s, "→", Inches(8.55), Inches(4.85), Inches(0.4), Inches(0.5),
         font_size=22, bold=True, color=COL_GREEN_DARK, align=PP_ALIGN.CENTER)
footer_bar(s, 5)


# ════════════════════════════════════════════════════════════════
#  SLIDE 6 — 10대 사업축
# ════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
add_rect(s, 0, 0, SLIDE_W, SLIDE_H, fill_rgb=COL_LIGHT_GRAY)
header_bar(s, "04  10대 사업축 종합")

axes = [
    ("①", "산지·초지\n순환방목"),
    ("②", "기존 축사\n지붕형 태양광"),
    ("③", "축산농가\n보상·지분참여"),
    ("④", "주민조합\n군민펀드 배당"),
    ("⑤", "AI Agent\n통합관리"),
    ("⑥", "법률·인허가\n조례 패키지"),
    ("⑦", "국립축산과학원\n연계 R&D"),
    ("⑧", "시범단지\n100~300ha"),
    ("⑨", "통합특구\n1조 8,000억"),
    ("⑩", "2027년\n300억 선도"),
]
cols = 5
for i, (num, label) in enumerate(axes):
    col = i % cols
    row = i // cols
    lx = Inches(0.4 + col * 2.5)
    ty = Inches(1.5 + row * 2.55)
    bg = COL_GREEN_MID if row == 0 else COL_BROWN
    add_rect(s, lx, ty, Inches(2.3), Inches(2.2), fill_rgb=bg)
    add_text(s, num, lx, ty + Inches(0.1), Inches(2.3), Inches(0.5),
             font_size=20, bold=True, color=COL_AMBER, align=PP_ALIGN.CENTER)
    add_text(s, label, lx, ty + Inches(0.6), Inches(2.3), Inches(1.4),
             font_size=13, bold=True, color=COL_WHITE, align=PP_ALIGN.CENTER)
footer_bar(s, 6)


# ════════════════════════════════════════════════════════════════
#  SLIDE 7 — 산지·초지 순환방목
# ════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
add_rect(s, 0, 0, SLIDE_W, SLIDE_H, fill_rgb=COL_LIGHT_GRAY)
header_bar(s, "05  산지·초지 순환방목")

section_chip(s, "개념", Inches(0.4), Inches(1.45))
add_text(s, "산지·초지·농지가 인접한 권역에 순환방목 구획을 설정하고,\n"
            "한우·면양 등 초식축을 계절별·구획별로 로테이션 방목하는 방식",
         Inches(0.5), Inches(1.9), Inches(12), Inches(0.75),
         font_size=13, color=COL_DARK_GRAY)

section_chip(s, "기대 효과", Inches(0.4), Inches(2.85))
effects = [
    "조사료 자급률 향상 → 사료비 30~40% 절감",
    "산불 예방 연료 제거 → 낙엽·잡관목 지속 관리",
    "고품질 방목육 생산 → 프리미엄 축산물 브랜드화",
    "탄소흡수원 유지·복원 → 탄소크레딧 수익",
    "가축 복지 개선 → 동물복지 인증 취득",
]
bullet_list(s, effects, Inches(0.5), Inches(3.35), Inches(6.0), font_size=13)

section_chip(s, "우선 대상 읍면", Inches(7.0), Inches(2.85))
priority = [
    "손불면 — 평지·조사료 최적 (1순위)",
    "신광면 — 산지 접합 우수",
    "대동면 — 축사 밀집·수계 관리",
    "엄다면 — 초지화 가능지 다수",
    "학교면 — 산지 비율 높음",
]
bullet_list(s, priority, Inches(7.1), Inches(3.35), Inches(5.8), font_size=13)

section_chip(s, "입지 선정 기준", Inches(0.4), Inches(5.65))
add_text(s, "충분한 산지 + 초지 또는 초지화 가능지 + 조사료 농지 인접 + 방역·마을이격·도로접근 가능",
         Inches(0.5), Inches(6.1), Inches(12.3), Inches(0.45),
         font_size=13, bold=True, color=COL_GREEN_DARK)
footer_bar(s, 7)


# ════════════════════════════════════════════════════════════════
#  SLIDE 8 — 기존 축사 지붕형 태양광
# ════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
add_rect(s, 0, 0, SLIDE_W, SLIDE_H, fill_rgb=COL_LIGHT_GRAY)
header_bar(s, "06  기존 축사 지붕형 태양광")

section_chip(s, "잠재량 산출 (1차 시나리오)", Inches(0.4), Inches(1.45))

solar_stats = [
    ("전체 축사 면적", "1,246천㎡", ""),
    ("지붕 활용 가능", "~780천㎡", "62% 적용"),
    ("설치 용량", "~125MW", "160W/㎡"),
    ("연간 발전량", "~156GWh", "1,250시간"),
    ("연간 수익", "~86억원", "55원/kWh"),
]
for i, (lb, val, note) in enumerate(solar_stats):
    lx = Inches(0.4 + i * 2.55)
    stat_box(s, lb, val, note, lx, Inches(1.95), Inches(2.4), Inches(1.4))

section_chip(s, "사업 구조", Inches(0.4), Inches(3.55))
structure = [
    "축산농가 지붕 임대 → 농가 임대료 수입(연 500~800만원/농가)",
    "발전사업자·지역조합 공동 투자 → 수익 배분",
    "군민펀드 연계 → 지역주민 배당 수익",
    "RE100 기업 PPA 연계 → 프리미엄 단가 확보",
]
bullet_list(s, structure, Inches(0.5), Inches(4.05), Inches(12), font_size=13)

section_chip(s, "주의사항", Inches(0.4), Inches(5.6))
add_text(s, "가축사육제한구역 93% 해당 → 현행법상 별도 허가 절차 필요 / 특별법 적용 시 일괄 허용 가능",
         Inches(0.5), Inches(6.05), Inches(12.3), Inches(0.45),
         font_size=12, color=COL_BROWN, bold=True)
footer_bar(s, 8)


# ════════════════════════════════════════════════════════════════
#  SLIDE 9 — 주민조합·군민펀드 배당
# ════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
add_rect(s, 0, 0, SLIDE_W, SLIDE_H, fill_rgb=COL_LIGHT_GRAY)
header_bar(s, "07  주민조합·군민펀드 배당")

section_chip(s, "배당 구조", Inches(0.4), Inches(1.45))
# 플로우 박스
flow = ["태양광\n발전 수익", "지역에너지\n협동조합", "군민펀드\n운용", "주민 1인당\n배당"]
for i, t in enumerate(flow):
    lx = Inches(0.5 + i * 3.1)
    add_rect(s, lx, Inches(2.0), Inches(2.7), Inches(1.3), fill_rgb=COL_GREEN_MID)
    add_text(s, t, lx, Inches(2.1), Inches(2.7), Inches(1.1),
             font_size=13, bold=True, color=COL_WHITE, align=PP_ALIGN.CENTER)
    if i < 3:
        add_text(s, "→", lx + Inches(2.75), Inches(2.45), Inches(0.35), Inches(0.45),
                 font_size=20, bold=True, color=COL_GREEN_DARK, align=PP_ALIGN.CENTER)

section_chip(s, "배당 시나리오 (연간)", Inches(0.4), Inches(3.55))
scenarios = [
    ("보수적 (50MW)", "연간 43억원 발전수익", "가구당 약 20만원"),
    ("기본 (125MW)", "연간 86억원 발전수익", "가구당 약 41만원"),
    ("적극 (200MW)", "연간 110억원 발전수익", "가구당 약 52만원"),
]
for i, (case, rev, div) in enumerate(scenarios):
    lx = Inches(0.5 + i * 4.1)
    bg = COL_GREEN_LIGHT if i == 1 else RGBColor(0xF5,0xF5,0xF5)
    add_rect(s, lx, Inches(4.1), Inches(3.9), Inches(2.0), fill_rgb=bg)
    if i == 1:
        add_rect(s, lx, Inches(4.1), Inches(3.9), Inches(0.06), fill_rgb=COL_AMBER)
    add_text(s, case, lx, Inches(4.15), Inches(3.9), Inches(0.45),
             font_size=13, bold=True, color=COL_GREEN_DARK, align=PP_ALIGN.CENTER)
    add_text(s, rev, lx, Inches(4.65), Inches(3.9), Inches(0.45),
             font_size=12, color=COL_DARK_GRAY, align=PP_ALIGN.CENTER)
    add_text(s, div, lx, Inches(5.2), Inches(3.9), Inches(0.6),
             font_size=16, bold=True, color=COL_GREEN_DARK if i == 1 else COL_MID_GRAY,
             align=PP_ALIGN.CENTER)
footer_bar(s, 9)


# ════════════════════════════════════════════════════════════════
#  SLIDE 10 — AI Agent 통합관리
# ════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
add_rect(s, 0, 0, SLIDE_W, SLIDE_H, fill_rgb=COL_LIGHT_GRAY)
header_bar(s, "08  AI Agent 통합관리")

section_chip(s, "시스템 개요", Inches(0.4), Inches(1.45))
add_text(s, "AI 기반 통합 플랫폼으로 방목·태양광·방역·배당을 실시간 연동 관리",
         Inches(0.5), Inches(1.9), Inches(12), Inches(0.45),
         font_size=13, color=COL_DARK_GRAY)

modules = [
    ("방목 모니터링", "GPS 위치추적\n채식량 자동 측정\n구획 로테이션 알림"),
    ("태양광 관리", "발전량 실시간 모니터\n이상 탐지 AI 경보\n수익 자동 정산"),
    ("방역 관리", "질병 조기경보\n차단방역 동선 최적화\n입출입 기록 자동화"),
    ("배당 관리", "조합원 수익 자동 계산\n배당 명세 자동 발송\n군민펀드 실시간 현황"),
]
for i, (title, body) in enumerate(modules):
    lx = Inches(0.4 + i * 3.2)
    add_rect(s, lx, Inches(2.55), Inches(3.0), Inches(3.5),
             fill_rgb=COL_WHITE)
    add_rect(s, lx, Inches(2.55), Inches(3.0), Inches(0.5),
             fill_rgb=COL_ACCENT_BLUE)
    add_text(s, title, lx, Inches(2.6), Inches(3.0), Inches(0.42),
             font_size=13, bold=True, color=COL_WHITE, align=PP_ALIGN.CENTER)
    add_text(s, body, lx + Inches(0.15), Inches(3.15), Inches(2.7), Inches(2.7),
             font_size=12, color=COL_DARK_GRAY)

add_text(s, "※ 국립축산과학원 R&D + 민간 AI 기업 협력 개발",
         Inches(0.5), Inches(6.35), Inches(12), Inches(0.35),
         font_size=10, color=COL_MID_GRAY, italic=True)
footer_bar(s, 10)


# ════════════════════════════════════════════════════════════════
#  SLIDE 11 — GIS 후보지 분석 결과
# ════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
add_rect(s, 0, 0, SLIDE_W, SLIDE_H, fill_rgb=COL_LIGHT_GRAY)
header_bar(s, "09  GIS 후보지 분석 결과 (v2.1)")

section_chip(s, "분석 데이터셋", Inches(0.4), Inches(1.45))
data_items = [
    "DEM·행정경계·수계·도로·토지피복 (OSM·Copernicus 오픈소스)",
    "연속지적도·용도지역·가축사육제한구역 (VWorld API)",
    "축사 주소 지오코딩 1,429/1,437개소(99.4%) 완료",
    "지목 기반 방목적합지 추출 — 연속지적도 24만 필지 분석",
]
bullet_list(s, data_items, Inches(0.5), Inches(1.95), Inches(12), font_size=12)

section_chip(s, "점수화 체계 (v2.1)", Inches(0.4), Inches(3.2))
criteria = [
    ("산지·초지 면적", "30점"),
    ("조사료 농지 인접", "20점"),
    ("수계·도로 이격", "15점"),
    ("규제 중첩도", "15점"),
    ("기존 축사 밀도", "10점"),
    ("마을 이격 거리", "10점"),
]
for i, (item, pt) in enumerate(criteria):
    col = i % 3
    row = i // 3
    lx = Inches(0.4 + col * 4.2)
    ty = Inches(3.7 + row * 0.75)
    add_rect(s, lx, ty, Inches(4.0), Inches(0.65),
             fill_rgb=COL_WHITE)
    add_rect(s, lx, ty, Inches(0.08), Inches(0.65), fill_rgb=COL_GREEN_MID)
    add_text(s, item, lx + Inches(0.15), ty + Inches(0.08), Inches(3.0), Inches(0.45),
             font_size=12, color=COL_DARK_GRAY)
    add_text(s, pt, lx + Inches(3.1), ty + Inches(0.08), Inches(0.8), Inches(0.45),
             font_size=13, bold=True, color=COL_GREEN_DARK, align=PP_ALIGN.RIGHT)

add_text(s, "※ 후보지 10곳 → 3곳 압축 → 최종 1곳 현장조사 계획 수립 진행 중",
         Inches(0.5), Inches(5.65), Inches(12), Inches(0.4),
         font_size=11, color=COL_BROWN, italic=True)
add_text(s, "※ 보전산지·초지 파일 확보 후 필지 단위 최종 선정 예정",
         Inches(0.5), Inches(6.05), Inches(12), Inches(0.4),
         font_size=11, color=COL_BROWN, italic=True)
footer_bar(s, 11)


# ════════════════════════════════════════════════════════════════
#  SLIDE 12 — 특별법 필요성
# ════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
add_rect(s, 0, 0, SLIDE_W, SLIDE_H, fill_rgb=COL_LIGHT_GRAY)
header_bar(s, "10  특별법·법률 패키지 필요성")

section_chip(s, "현행 규제 한계", Inches(0.4), Inches(1.45))
limits = [
    "가축분뇨법 · 가축사육제한조례 → 신규 축사 및 방목단지 허가 실질 차단",
    "농지법 · 산지관리법 중복 규제 → 농림지 전용 이중 절차 필요",
    "소규모 농가 REC·PPA 참여 법적 근거 미비",
]
bullet_list(s, limits, Inches(0.5), Inches(1.95), Inches(12), font_size=13)

section_chip(s, "특별법 핵심 조항 (안)", Inches(0.4), Inches(3.3))
provisions = [
    "산지방목 특구 지정 → 가축사육제한구역 적용 특례",
    "친환경축산 용도구역 설정 → 농지·산지 전용 간소화",
    "축사태양광 공동개발 허용 → 소규모 농가 참여 법적 근거",
    "주민배당형 에너지협동조합 법인격 신설",
    "지방자치단체 주도 축산구조전환 사업 근거",
]
bullet_list(s, provisions, Inches(0.5), Inches(3.8), Inches(12), font_size=13)

add_rect(s, Inches(0.4), Inches(5.95), Inches(12.5), Inches(0.8),
         fill_rgb=COL_GREEN_DARK)
add_text(s, "결론: 현행 규제 체계 내에서는 사업 진행 불가 → 특별법 제정이 선결 조건",
         Inches(0.5), Inches(6.0), Inches(12.3), Inches(0.7),
         font_size=14, bold=True, color=COL_AMBER, align=PP_ALIGN.CENTER)
footer_bar(s, 12)


# ════════════════════════════════════════════════════════════════
#  SLIDE 13 — 손불면 평지축산 시나리오
# ════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
add_rect(s, 0, 0, SLIDE_W, SLIDE_H, fill_rgb=COL_LIGHT_GRAY)
header_bar(s, "11  손불면 평지축산 시나리오")

section_chip(s, "손불면 선정 이유", Inches(0.4), Inches(1.45))
reasons = [
    "함평군 축사 수 최다 (218개소, 15.2%) — 집약적 관리 유리",
    "평지·조사료 농지 비율 높음 → 사육두수 확대 여지",
    "기존 축사 밀집 → 태양광 설치 잠재 최대",
]
bullet_list(s, reasons, Inches(0.5), Inches(1.95), Inches(12), font_size=13)

section_chip(s, "시나리오 내용", Inches(0.4), Inches(3.0))
scenario_boxes = [
    ("조사료 자급", "조사료 농지 확대\n호당 30% 자급\n→ 사료비 절감"),
    ("사육두수 확대", "초지화 가능지 활용\n현 대비 20% 증두\n→ 소득 증대"),
    ("태양광 발전", "218개소 전면 설치\n추정 21.8MW\n→ 연간 14억원"),
    ("통합 브랜드", "손불 그린한우\n프리미엄 출하\n→ kg당 15% 프리미엄"),
]
for i, (title, body) in enumerate(scenario_boxes):
    lx = Inches(0.4 + i * 3.2)
    add_rect(s, lx, Inches(3.5), Inches(3.0), Inches(2.5),
             fill_rgb=COL_WHITE)
    add_rect(s, lx, Inches(3.5), Inches(3.0), Inches(0.45),
             fill_rgb=COL_BROWN)
    add_text(s, title, lx, Inches(3.53), Inches(3.0), Inches(0.4),
             font_size=13, bold=True, color=COL_WHITE, align=PP_ALIGN.CENTER)
    add_text(s, body, lx + Inches(0.15), Inches(4.05), Inches(2.7), Inches(1.8),
             font_size=12, color=COL_DARK_GRAY)

add_text(s, "※ 기준값은 공식자료 재집계 후 재설정 가능",
         Inches(0.5), Inches(6.2), Inches(12), Inches(0.35),
         font_size=10, color=COL_MID_GRAY, italic=True)
footer_bar(s, 13)


# ════════════════════════════════════════════════════════════════
#  SLIDE 14 — 국립축산과학원 연계 R&D
# ════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
add_rect(s, 0, 0, SLIDE_W, SLIDE_H, fill_rgb=COL_LIGHT_GRAY)
header_bar(s, "12  국립축산과학원 연계 R&D")

section_chip(s, "연계 필요성", Inches(0.4), Inches(1.45))
add_text(s, "산지방목 기술기준 부재 → 과학적 실증 데이터 필수 / 정부 R&D 예산 확보 통로",
         Inches(0.5), Inches(1.9), Inches(12), Inches(0.45),
         font_size=13, color=COL_DARK_GRAY)

section_chip(s, "주요 연구 과제", Inches(0.4), Inches(2.55))
rd_items = [
    "한국형 산지방목 기술기준 수립 (구획면적·두수밀도·로테이션 주기)",
    "방목 한우·면양 성장·품질 실증 데이터 구축",
    "조사료 자급 모델 최적화 (사료작물 선발·수확 체계)",
    "축사태양광 설치 기준 및 발전·축산 복합 효율 실증",
    "AI 기반 방역·건강관리 시스템 현장 적용 연구",
    "탄소흡수량 측정 방법론 개발 → 탄소크레딧 인증 체계",
]
bullet_list(s, rd_items, Inches(0.5), Inches(3.05), Inches(12), font_size=13)

section_chip(s, "협력 모델", Inches(0.4), Inches(5.6))
add_text(s, "국립축산과학원 현장 시험지 지정 → 함평군 시범단지 → 전국 확산 모델 개발",
         Inches(0.5), Inches(6.05), Inches(12), Inches(0.45),
         font_size=13, bold=True, color=COL_GREEN_DARK)
footer_bar(s, 14)


# ════════════════════════════════════════════════════════════════
#  SLIDE 15 — 예산 확보 전략
# ════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
add_rect(s, 0, 0, SLIDE_W, SLIDE_H, fill_rgb=COL_LIGHT_GRAY)
header_bar(s, "13  예산 확보 전략")

section_chip(s, "단계별 예산 목표", Inches(0.4), Inches(1.45))
budget_rows = [
    ("2027년", "선도사업", "300억원", "군비+도비+국비 매칭"),
    ("2028~2030년", "1단계 확장", "2,500억원", "국가균형발전특별회계"),
    ("2031~2036년", "통합특구 완성", "1조 5,200억원", "통합특구법 특별예산"),
    ("합계", "10년 총계", "1조 8,000억원", "국가급 농축산 전환"),
]
cols_w = [Inches(2.2), Inches(2.5), Inches(2.5), Inches(5.0)]
col_labels = ["기간", "단계", "예산", "재원"]
lx_start = Inches(0.4)
# 헤더
lx = lx_start
for j, (lb, cw) in enumerate(zip(col_labels, cols_w)):
    add_rect(s, lx, Inches(2.0), cw - Inches(0.05), Inches(0.45), fill_rgb=COL_GREEN_DARK)
    add_text(s, lb, lx, Inches(2.0), cw, Inches(0.45),
             font_size=12, bold=True, color=COL_WHITE, align=PP_ALIGN.CENTER)
    lx += cw
for i, row in enumerate(budget_rows):
    lx = lx_start
    bg = COL_WHITE if i % 2 == 0 else COL_LIGHT_GRAY
    if i == 3:
        bg = RGBColor(0xE8, 0xF5, 0xE9)
    for j, (cell, cw) in enumerate(zip(row, cols_w)):
        add_rect(s, lx, Inches(2.5 + i * 0.7), cw - Inches(0.05), Inches(0.65), fill_rgb=bg)
        fc = COL_GREEN_DARK if (i == 3 and j == 2) else COL_DARK_GRAY
        add_text(s, cell, lx + Inches(0.05), Inches(2.55 + i * 0.7),
                 cw - Inches(0.1), Inches(0.55),
                 font_size=12 if j != 2 else 14,
                 bold=(j == 2), color=fc, align=PP_ALIGN.CENTER)
        lx += cw

section_chip(s, "재원 조달 채널", Inches(0.4), Inches(5.5))
channels = [
    "농식품부 스마트팜·축산환경 개선 국고보조",
    "전라남도 그린에너지·농촌공간재구조화 도비",
    "RPS 신재생에너지 공급인증서(REC) 수익",
    "민간 RE100 기업 PPA 투자 유치",
]
bullet_list(s, channels, Inches(0.5), Inches(6.0), Inches(12), font_size=12, line_h=Inches(0.35))
footer_bar(s, 15)


# ════════════════════════════════════════════════════════════════
#  SLIDE 16 — 단계별 추진 일정
# ════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
add_rect(s, 0, 0, SLIDE_W, SLIDE_H, fill_rgb=COL_LIGHT_GRAY)
header_bar(s, "14  단계별 추진 일정")

phases = [
    ("1단계\n2026~2027", ["특별법 입법 추진", "GIS 후보지 1곳 확정", "시범단지 기본계획 수립", "300억 선도사업 예산 확보"]),
    ("2단계\n2028~2030", ["시범단지 조성 착수", "방목 실증 R&D 시작", "축사태양광 1차 설치", "주민조합 설립·운영"]),
    ("3단계\n2031~2033", ["방목단지 100ha 완성", "태양광 50MW 달성", "군민펀드 배당 개시", "AI플랫폼 전면 가동"]),
    ("4단계\n2034~2036", ["통합특구 300ha 완성", "125MW 발전 목표", "전국 확산 모델 수출", "1조 8,000억 완성"]),
]
for i, (phase, tasks) in enumerate(phases):
    lx = Inches(0.35 + i * 3.25)
    add_rect(s, lx, Inches(1.5), Inches(3.1), Inches(5.3), fill_rgb=COL_WHITE)
    add_rect(s, lx, Inches(1.5), Inches(3.1), Inches(0.75),
             fill_rgb=COL_GREEN_DARK if i == 0 else COL_GREEN_MID)
    add_text(s, phase, lx, Inches(1.55), Inches(3.1), Inches(0.65),
             font_size=13, bold=True, color=COL_WHITE, align=PP_ALIGN.CENTER)
    for j, task in enumerate(tasks):
        add_text(s, f"✓  {task}", lx + Inches(0.15), Inches(2.4 + j * 0.95),
                 Inches(2.85), Inches(0.85),
                 font_size=12, color=COL_DARK_GRAY)
footer_bar(s, 16)


# ════════════════════════════════════════════════════════════════
#  SLIDE 17 — 기대효과 종합
# ════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
add_rect(s, 0, 0, SLIDE_W, SLIDE_H, fill_rgb=COL_LIGHT_GRAY)
header_bar(s, "15  기대효과 종합")

effect_cats = [
    ("경제적 효과", COL_GREEN_MID, [
        "10년 누적 생산유발 2조 2천억원",
        "지역 고용 창출 2,200명",
        "농가 소득 30~50% 향상",
        "군민 1인당 연 배당 41만원(기본)",
    ]),
    ("환경·생태", COL_ACCENT_BLUE, [
        "탄소 감축 연 12만톤 CO₂",
        "산불 예방 연료 제거 연 1,500ha",
        "생물다양성 회복",
        "축산 악취·오염수 저감",
    ]),
    ("사회·지역", COL_BROWN, [
        "농촌공간 재구조화 모델 구축",
        "청년 귀농 유입 → 인구 감소 완화",
        "함평군 전국 그린축산 선도지위",
        "전국 확산 모델 수출 가능",
    ]),
]
for i, (cat, color, items) in enumerate(effect_cats):
    lx = Inches(0.4 + i * 4.3)
    add_rect(s, lx, Inches(1.5), Inches(4.1), Inches(5.2), fill_rgb=COL_WHITE)
    add_rect(s, lx, Inches(1.5), Inches(4.1), Inches(0.5), fill_rgb=color)
    add_text(s, cat, lx, Inches(1.53), Inches(4.1), Inches(0.45),
             font_size=14, bold=True, color=COL_WHITE, align=PP_ALIGN.CENTER)
    for j, item in enumerate(items):
        add_text(s, f"▸  {item}", lx + Inches(0.15), Inches(2.15 + j * 1.05),
                 Inches(3.85), Inches(0.9),
                 font_size=12, color=COL_DARK_GRAY)
footer_bar(s, 17)


# ════════════════════════════════════════════════════════════════
#  SLIDE 18 — 리스크 및 대응방안
# ════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
add_rect(s, 0, 0, SLIDE_W, SLIDE_H, fill_rgb=COL_LIGHT_GRAY)
header_bar(s, "16  리스크 및 대응방안")

risks = [
    ("특별법 입법 지연", "높음", "지방자치단체 규제샌드박스 선적용 + 조례 우선 제정"),
    ("지역주민 반대", "중간", "비공개 간담회 → 배당 모델 조기 가시화 → 찬성 여론 형성"),
    ("축산농가 참여 저조", "중간", "선도 농가 인센티브 + 지분참여 구조로 이해관계 일치"),
    ("GIS 부지 확보 실패", "낮음", "9개 읍면 동시 평가 → 대안 부지 3~5개 확보"),
    ("예산 미확보", "중간", "전라남도 도비 선확보 + 민간투자 병행으로 의존도 분산"),
    ("기상·질병 리스크", "중간", "AI 방역 조기경보 + 분산방목 구조로 피해 최소화"),
]
cols_lbl = ["리스크", "가능성", "대응방안"]
cols_w2 = [Inches(3.0), Inches(1.2), Inches(8.8)]
lx = Inches(0.3)
for j, (lb, cw) in enumerate(zip(cols_lbl, cols_w2)):
    add_rect(s, lx, Inches(1.55), cw - Inches(0.05), Inches(0.45), fill_rgb=COL_GREEN_DARK)
    add_text(s, lb, lx, Inches(1.55), cw, Inches(0.45),
             font_size=12, bold=True, color=COL_WHITE, align=PP_ALIGN.CENTER)
    lx += cw
for i, (risk, level, response) in enumerate(risks):
    lx = Inches(0.3)
    bg = COL_WHITE if i % 2 == 0 else COL_LIGHT_GRAY
    row_data = [risk, level, response]
    level_colors = {"높음": RGBColor(0xC6,0x28,0x28), "중간": COL_AMBER, "낮음": COL_GREEN_MID}
    for j, (cell, cw) in enumerate(zip(row_data, cols_w2)):
        add_rect(s, lx, Inches(2.05 + i * 0.72), cw - Inches(0.05), Inches(0.68), fill_rgb=bg)
        fc = level_colors.get(cell, COL_DARK_GRAY) if j == 1 else COL_DARK_GRAY
        add_text(s, cell, lx + Inches(0.05), Inches(2.1 + i * 0.72),
                 cw - Inches(0.1), Inches(0.58),
                 font_size=11 if j == 2 else 12,
                 bold=(j == 1), color=fc, align=PP_ALIGN.CENTER if j != 2 else PP_ALIGN.LEFT)
        lx += cw
footer_bar(s, 18)


# ════════════════════════════════════════════════════════════════
#  SLIDE 19 — 다음 행동계획 (Next Steps)
# ════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
add_rect(s, 0, 0, SLIDE_W, SLIDE_H, fill_rgb=COL_LIGHT_GRAY)
header_bar(s, "19  다음 행동계획 (Next Steps)")

section_chip(s, "즉시 착수 (2026. 6~8)", Inches(0.4), Inches(1.45))
immediate = [
    "보전산지·초지·악취민원·방역권역 GIS 자료 확보 (산림청/농식품부)",
    "후보지 10곳 도출 → 3곳 압축 → 최종 1곳 현장조사",
    "축산농가 비공개 간담회 자료 준비 및 개최",
    "특별법 입법 로드맵 수립 (법무사·행정사 협의)",
]
bullet_list(s, immediate, Inches(0.5), Inches(1.95), Inches(12), font_size=13)

section_chip(s, "하반기 목표 (2026. 9~12)", Inches(0.4), Inches(3.65))
h2 = [
    "주민설명회 자료 작성 및 설명회 개최",
    "군수·군의회 보고자료 최종 확정",
    "전라남도·통합예산 제안 패키지 제출",
    "국립축산과학원 연계 협의 착수",
    "2027년 선도사업 예산 확보 신청",
]
bullet_list(s, h2, Inches(0.5), Inches(4.15), Inches(12), font_size=13)

add_rect(s, Inches(0.4), Inches(6.2), Inches(12.5), Inches(0.65), fill_rgb=COL_GREEN_DARK)
add_text(s, "🎯  목표: 2027년 3월 300억 선도사업 착공",
         Inches(0.5), Inches(6.25), Inches(12), Inches(0.55),
         font_size=15, bold=True, color=COL_AMBER, align=PP_ALIGN.CENTER)
footer_bar(s, 19)


# ════════════════════════════════════════════════════════════════
#  SLIDE 20 — 맺음말·Q&A
# ════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
add_rect(s, 0, 0, SLIDE_W, SLIDE_H, fill_rgb=COL_GREEN_DARK)
add_rect(s, 0, Inches(3.5), SLIDE_W, Inches(0.08), fill_rgb=COL_AMBER)

add_text(s, "함평이 먼저, 전국이 따른다",
         Inches(1.5), Inches(1.2), Inches(10.5), Inches(1.1),
         font_size=38, bold=True, color=COL_WHITE, align=PP_ALIGN.CENTER)
add_text(s, "산지방목 × 그린에너지 × 주민배당 × AI축산",
         Inches(1.5), Inches(2.35), Inches(10.5), Inches(0.65),
         font_size=18, color=COL_GREEN_LIGHT, align=PP_ALIGN.CENTER)

add_rect(s, Inches(1.5), Inches(3.8), Inches(10.5), Inches(2.2), fill_rgb=RGBColor(0x16,0x50,0x16))
add_text(s, "함평 산지방목 그린축산·에너지공유 특구 조성사업\n"
            "10년 총 1조 8,000억원 투자 · 탄소감축 연 12만톤\n"
            "군민 1인 연 배당 41만원 · 고용 2,200명",
         Inches(1.7), Inches(3.95), Inches(10.1), Inches(2.0),
         font_size=15, color=COL_WHITE, align=PP_ALIGN.CENTER)

add_text(s, "Q & A", Inches(5.5), Inches(6.1), Inches(2.5), Inches(0.7),
         font_size=28, bold=True, color=COL_AMBER, align=PP_ALIGN.CENTER)

add_text(s, "함평군청  |  산지방목특구추진단  |  2026. 06.",
         Inches(3.0), Inches(6.8), Inches(7.5), Inches(0.35),
         font_size=10, color=COL_GREEN_LIGHT, align=PP_ALIGN.CENTER)
# 마지막엔 별도 푸터 없음 (표지 스타일 유지)


# ── 저장 ─────────────────────────────────────────────────────────
output_path = "/home/user/michaechang_study/함평_산지방목_그린축산_특구_발표자료.pptx"
prs.save(output_path)
print(f"✅ PPTX 저장 완료: {output_path}")
print(f"   슬라이드 수: {len(prs.slides)}")
