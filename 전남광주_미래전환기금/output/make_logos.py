"""
전남광주 통합특별시 로고 2종 SVG 생성
Logo A: 원형 그라데이션 심벌 (통합·상생 콘셉트)
Logo B: 텍스트 기반 워드마크 (모던 행정 콘셉트)
"""

LOGO_A = '''<?xml version="1.0" encoding="UTF-8"?>
<svg width="400" height="400" viewBox="0 0 400 400"
     xmlns="http://www.w3.org/2000/svg"
     xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <!-- 광주(파랑)→전남(초록) 그라데이션 -->
    <linearGradient id="grdAB" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%"   stop-color="#1565C0"/>
      <stop offset="100%" stop-color="#1B5E20"/>
    </linearGradient>
    <linearGradient id="grdText" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%"   stop-color="#1565C0"/>
      <stop offset="100%" stop-color="#1B5E20"/>
    </linearGradient>
    <!-- 원형 클리핑 -->
    <clipPath id="circClip">
      <circle cx="200" cy="170" r="120"/>
    </clipPath>
  </defs>

  <!-- 배경 원 (연한 회색) -->
  <circle cx="200" cy="170" r="135" fill="#F5F7FA"/>

  <!-- 외곽 링 -->
  <circle cx="200" cy="170" r="135" fill="none" stroke="url(#grdAB)" stroke-width="5"/>

  <!-- 광주(파랑) 반원 -->
  <path d="M200 50 A120 120 0 0 0 200 290 Z"
        fill="#1565C0" opacity="0.90"/>

  <!-- 전남(초록) 반원 -->
  <path d="M200 50 A120 120 0 0 1 200 290 Z"
        fill="#1B5E20" opacity="0.90"/>

  <!-- 중앙 흰 원 (상생 여백) -->
  <circle cx="200" cy="170" r="48" fill="white"/>

  <!-- 가운데 전 字 이니셜 + 광 字 -->
  <text x="200" y="163" text-anchor="middle"
        font-family="'Apple SD Gothic Neo','Noto Sans KR',sans-serif"
        font-size="22" font-weight="700" fill="#1565C0">광</text>
  <text x="200" y="187" text-anchor="middle"
        font-family="'Apple SD Gothic Neo','Noto Sans KR',sans-serif"
        font-size="22" font-weight="700" fill="#1B5E20">전남</text>

  <!-- 작은 별 4개 (사방 균형) -->
  <polygon points="200,55 203,63 212,63 205,69 208,77 200,72 192,77 195,69 188,63 197,63"
           fill="white" opacity="0.85"/>

  <!-- 아래 텍스트 -->
  <text x="200" y="340"
        text-anchor="middle"
        font-family="'Apple SD Gothic Neo','Noto Sans KR',sans-serif"
        font-size="26" font-weight="800" fill="#1A237E">전남광주특별시</text>
  <text x="200" y="368"
        text-anchor="middle"
        font-family="'Apple SD Gothic Neo','Noto Sans KR',sans-serif"
        font-size="13" font-weight="400" fill="#555" letter-spacing="3">Jeonnam-Gwangju Special City</text>
</svg>'''

LOGO_B = '''<?xml version="1.0" encoding="UTF-8"?>
<svg width="560" height="200" viewBox="0 0 560 200"
     xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="barGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%"   stop-color="#1565C0"/>
      <stop offset="50%"  stop-color="#0D9488"/>
      <stop offset="100%" stop-color="#1B5E20"/>
    </linearGradient>
  </defs>

  <!-- 심볼: 남도 해안·산 모티프 (추상 웨이브) -->
  <!-- 산 실루엣 (전남 무등산) -->
  <path d="M20 130 Q40 60 70 80 Q90 50 110 90 Q130 40 155 85 L155 130 Z"
        fill="#1B5E20" opacity="0.80"/>
  <!-- 물결 (광주천·남해) -->
  <path d="M20 130 Q50 140 80 128 Q110 116 140 130 Q155 136 155 136 L155 155 L20 155 Z"
        fill="#1565C0" opacity="0.70"/>

  <!-- 수직 구분선 -->
  <rect x="170" y="40" width="4" height="120" rx="2"
        fill="url(#barGrad)"/>

  <!-- 한글 로고타입 -->
  <text x="190" y="100"
        font-family="'Apple SD Gothic Neo','Noto Sans KR',sans-serif"
        font-size="52" font-weight="900" fill="#1A237E">전남광주</text>
  <text x="192" y="130"
        font-family="'Apple SD Gothic Neo','Noto Sans KR',sans-serif"
        font-size="22" font-weight="400" fill="#37474F"
        letter-spacing="6">특별시</text>

  <!-- 영문 서브텍스트 -->
  <text x="192" y="155"
        font-family="'Helvetica Neue','Arial',sans-serif"
        font-size="12" fill="#78909C" letter-spacing="2">
    JEONNAM-GWANGJU SPECIAL CITY
  </text>

  <!-- 그라데이션 하단 바 -->
  <rect x="192" y="162" width="360" height="3" rx="1.5"
        fill="url(#barGrad)"/>

  <!-- 슬로건 태그라인 -->
  <text x="192" y="185"
        font-family="'Apple SD Gothic Neo','Noto Sans KR',sans-serif"
        font-size="11" fill="#90A4AE" letter-spacing="1">
    100년 성장자본 · 미래전환기금 · 상생발전
  </text>
</svg>'''

with open("/home/user/michaechang_study/전남광주_미래전환기금/output/logo_A_circle.svg", "w", encoding="utf-8") as f:
    f.write(LOGO_A)

with open("/home/user/michaechang_study/전남광주_미래전환기금/output/logo_B_wordmark.svg", "w", encoding="utf-8") as f:
    f.write(LOGO_B)

print("로고 SVG 생성 완료")
