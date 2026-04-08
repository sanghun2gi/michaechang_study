"""
Windows에서 실행하는 DOC/DOCX 파일 업로드 스크립트
사용법:
  1. 이 파일을 아무 폴더에 저장
  2. CMD에서: python upload_doc.py
  3. 업로드할 파일 경로 입력
"""
import os, urllib.request, urllib.error

# ── 설정 ──────────────────────────────────────────────
SERVER_URL = "http://192.0.2.2:8765"   # 서버 주소
# ──────────────────────────────────────────────────────

def check_server():
    try:
        urllib.request.urlopen(f"{SERVER_URL}/ping", timeout=5)
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
    urllib.request.urlopen(req, timeout=60)
    print(f"  업로드 완료: {filename} ({len(data):,} bytes)")

def main():
    print("=" * 50)
    print("  DOC 파일 업로드 도구")
    print("=" * 50)

    if not check_server():
        print(f"\n오류: 서버에 연결할 수 없습니다 ({SERVER_URL})")
        print("Linux 쪽에서 먼저 'python receive_files.py' 를 실행해주세요.")
        input("\nEnter 키를 눌러 종료...")
        return

    print(f"서버 연결 성공 ({SERVER_URL})\n")

    filepath = input("업로드할 파일 경로를 입력하세요:\n> ").strip().strip('"')

    if not os.path.isfile(filepath):
        print(f"\n오류: 파일을 찾을 수 없습니다 — {filepath}")
        input("Enter 키를 눌러 종료...")
        return

    try:
        upload_file(filepath)
        print("\n업로드 성공!")
    except Exception as e:
        print(f"\n업로드 실패: {e}")

    input("\nEnter 키를 눌러 종료...")

if __name__ == '__main__':
    main()
