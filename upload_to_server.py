"""
Windows에서 실행하는 .LOG 파일 업로드 스크립트
사용법:
  1. 이 파일을 아무 폴더에 저장
  2. CMD에서: python upload_to_server.py
"""
import os, urllib.request, urllib.error

# ── 설정 ──────────────────────────────────────────────
LOG_FOLDER  = r"E:\ai\claude\gps\data\gps_log"   # LOG 파일 폴더
SERVER_URL  = "http://127.0.0.1:8765"             # 서버 주소 (보통 그대로 사용)
# ──────────────────────────────────────────────────────

def check_server():
    try:
        urllib.request.urlopen(f"{SERVER_URL}/ping", timeout=3)
        return True
    except Exception:
        return False

def upload_file(filepath):
    filename = os.path.basename(filepath)
    with open(filepath, 'rb') as f:
        data = f.read()
    req = urllib.request.Request(
        f"{SERVER_URL}/upload",
        data=data,
        headers={'X-Filename': filename, 'Content-Length': str(len(data))},
        method='POST'
    )
    urllib.request.urlopen(req, timeout=30)

def main():
    print(f"폴더 확인: {LOG_FOLDER}")

    if not os.path.isdir(LOG_FOLDER):
        print(f"오류: 폴더를 찾을 수 없습니다 — {LOG_FOLDER}")
        input("Enter 키를 눌러 종료...")
        return

    logs = [f for f in os.listdir(LOG_FOLDER) if f.upper().endswith('.LOG')]
    if not logs:
        print("LOG 파일 없음")
        input("Enter 키를 눌러 종료...")
        return

    print(f"LOG 파일 {len(logs)}개 발견")

    if not check_server():
        print("\n오류: 서버에 연결할 수 없습니다.")
        print("Linux 쪽에서 먼저 'python receive_files.py' 를 실행해주세요.")
        input("Enter 키를 눌러 종료...")
        return

    print(f"서버 연결 확인 ({SERVER_URL})\n업로드 시작...\n")

    ok = 0
    for i, fname in enumerate(sorted(logs), 1):
        fpath = os.path.join(LOG_FOLDER, fname)
        try:
            upload_file(fpath)
            ok += 1
            if i % 10 == 0 or i == len(logs):
                print(f"  [{i:3d}/{len(logs)}] {fname}")
        except Exception as e:
            print(f"  [실패] {fname}: {e}")

    print(f"\n완료: {ok}/{len(logs)}개 업로드 성공")
    input("Enter 키를 눌러 종료...")

if __name__ == '__main__':
    main()
