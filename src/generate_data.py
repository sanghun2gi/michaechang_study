#!/usr/bin/env python3
"""
Korean Road GPS NMEA Sample Data Generator
한국 도로조사 NMEA 샘플 데이터 생성기
Usage: python generate_data.py [3|30|300]
"""

import os, math, random
from datetime import datetime, timedelta

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'gps_log')

# ─── Korean Road Routes ───────────────────────────────────────────────────────
ROUTES = [
    {'id': 'gyeongbu',   'base_speed': 100, 'pts': [
        (37.5665,126.9780),(37.2636,127.0286),(36.8151,127.1139),
        (36.3504,127.3845),(36.1192,128.3444),(35.8714,128.6014),(35.1796,129.0756)]},
    {'id': 'honam',      'base_speed': 100, 'pts': [
        (36.3504,127.3845),(35.8242,127.1489),(35.1595,126.8526),(34.8118,126.3922)]},
    {'id': 'seohaean',   'base_speed': 100, 'pts': [
        (37.4563,126.7052),(36.7800,126.4500),(36.3200,126.5800),
        (35.8242,127.1489),(35.1595,126.8526),(34.8118,126.3922)]},
    {'id': 'namhae',     'base_speed': 90, 'pts': [
        (35.1796,129.0756),(35.2285,128.6811),(35.1600,128.0200),
        (34.9400,127.7300),(34.7604,127.6622)]},
    {'id': 'donghaean',  'base_speed': 70, 'pts': [
        (38.2070,128.5912),(37.7519,128.8761),(37.4346,129.1651),
        (36.0194,129.3432),(35.5384,129.3114),(35.1796,129.0756)]},
    {'id': 'jungang',    'base_speed': 95, 'pts': [
        (37.5665,126.9780),(37.3422,127.9201),(36.5684,128.7294),(35.8714,128.6014)]},
    {'id': 'seoulring',  'base_speed': 80, 'pts': [
        (37.6900,126.7600),(37.7100,127.0560),(37.6500,127.2500),
        (37.4000,127.2500),(37.3200,127.1000),(37.4500,126.7600),(37.6900,126.7600)]},
    {'id': 'seoulurban', 'base_speed': 28, 'pts': [
        (37.5665,126.9780),(37.5172,127.0473),(37.4979,127.0276),
        (37.5326,126.8900),(37.5900,126.9700),(37.5665,126.9780)]},
]

SURVEY_HOURS = [6, 8, 10, 13, 16, 19, 21, 23]


# ─── NMEA Helpers ─────────────────────────────────────────────────────────────
def checksum(data: str) -> str:
    cs = 0
    for c in data:
        cs ^= ord(c)
    return f'{cs:02X}'

def to_lat(lat: float):
    d = int(abs(lat)); m = (abs(lat) - d) * 60
    return f'{d:02d}{m:07.4f}', 'N' if lat >= 0 else 'S'

def to_lon(lon: float):
    d = int(abs(lon)); m = (abs(lon) - d) * 60
    return f'{d:03d}{m:07.4f}', 'E' if lon >= 0 else 'W'

def bearing(p1: tuple, p2: tuple) -> float:
    la1, lo1 = math.radians(p1[0]), math.radians(p1[1])
    la2, lo2 = math.radians(p2[0]), math.radians(p2[1])
    dlo = lo2 - lo1
    x = math.sin(dlo) * math.cos(la2)
    y = math.cos(la1) * math.sin(la2) - math.sin(la1) * math.cos(la2) * math.cos(dlo)
    return (math.degrees(math.atan2(x, y)) + 360) % 360

def make_gprmc(dt: datetime, lat: float, lon: float, spd_kmh: float, hdg: float) -> str:
    la, ld = to_lat(lat); lo, lod = to_lon(lon)
    spd_kt = spd_kmh / 1.852
    body = (f'GPRMC,{dt.strftime("%H%M%S.00")},A,'
            f'{la},{ld},{lo},{lod},'
            f'{spd_kt:.1f},{hdg:.1f},{dt.strftime("%d%m%y")},')
    return f'${body}*{checksum(body)}'

def make_gpgga(dt: datetime, lat: float, lon: float, alt: float) -> str:
    la, ld = to_lat(lat); lo, lod = to_lon(lon)
    ns = random.randint(6, 12); hdop = round(random.uniform(0.8, 2.0), 1)
    body = (f'GPGGA,{dt.strftime("%H%M%S.00")},'
            f'{la},{ld},{lo},{lod},'
            f'1,{ns:02d},{hdop},{alt:.1f},M,0.0,M,,')
    return f'${body}*{checksum(body)}'


# ─── Route Track Generator ────────────────────────────────────────────────────
def interpolate(p1: tuple, p2: tuple, n: int) -> list:
    return [
        (p1[0] + (p2[0]-p1[0]) * i/n + random.gauss(0, 0.00003),
         p1[1] + (p2[1]-p1[1]) * i/n + random.gauss(0, 0.00003))
        for i in range(n)
    ]

def make_track(route: dict, n_pts: int = 500) -> list:
    wpts = route['pts']
    seg = max(1, n_pts // (len(wpts) - 1))
    pts = []
    for i in range(len(wpts) - 1):
        pts.extend(interpolate(wpts[i], wpts[i+1], seg))
    return pts

def speed_for_hour(hour: int, base: float) -> float:
    """Realistic speed variation by time of day"""
    if hour in (7, 8):      factor = 0.30   # morning rush
    elif hour in (18, 19):  factor = 0.35   # evening rush
    elif hour < 6:          factor = 1.20   # late night (fast)
    elif hour >= 22:        factor = 1.10   # night
    else:                   factor = 1.00   # normal daytime
    noise = random.gauss(0, base * 0.10)
    return max(5.0, min(130.0, base * factor + noise))


# ─── File Writer ──────────────────────────────────────────────────────────────
def write_log(path: str, route: dict, start_dt: datetime, n_pts: int = 500):
    pts = make_track(route, n_pts)
    dt = start_dt
    alt_base = 30.0 + random.uniform(0, 120)
    lines = []

    for i, (lat, lon) in enumerate(pts):
        if i < len(pts) - 1:
            hdg = bearing((lat, lon), pts[i+1])
        else:
            hdg = bearing(pts[i-1], (lat, lon))

        spd = speed_for_hour(dt.hour, route['base_speed'])
        alt = max(0, alt_base + random.gauss(0, 15))

        lines.append(make_gprmc(dt, lat, lon, spd, hdg))
        lines.append(make_gpgga(dt, lat, lon, alt))
        dt += timedelta(seconds=1)

    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines) + '\n')


# ─── Batch Generator ─────────────────────────────────────────────────────────
def generate(n_files: int):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    base_date = datetime(2024, 1, 2, 0, 0, 0)

    passes_per_route = max(1, n_files // len(ROUTES))
    day_interval = max(1, 365 // passes_per_route)

    created = 0
    for i in range(n_files):
        route = ROUTES[i % len(ROUTES)]
        pass_num = i // len(ROUTES)
        days_offset = min(pass_num * day_interval, 364)
        hour = SURVEY_HOURS[i % len(SURVEY_HOURS)]
        dt = base_date + timedelta(days=days_offset, hours=hour)
        fname = f"{dt.strftime('%Y%m%d')}_{hour:02d}_{route['id']}.LOG"
        fpath = os.path.join(OUTPUT_DIR, fname)

        if not os.path.exists(fpath):   # skip if already generated
            write_log(fpath, route, dt)

        created += 1
        if created % 10 == 0 or created == n_files:
            print(f'  [{created:3d}/{n_files}] {fname}')

    print(f'\n완료: {created}개 파일 생성 → {OUTPUT_DIR}')


if __name__ == '__main__':
    import sys
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 300
    print(f'NMEA LOG 파일 {n}개 생성 중...')
    generate(n)
