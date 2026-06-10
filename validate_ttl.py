#!/usr/bin/env python3
"""
TTL 파일 일괄 검증 스크립트

지정한 폴더의 모든 .ttl 파일을 rdflib로 파싱하여
문법 오류, 트리플 수, 네임스페이스 등을 검사하고 리포트를 출력합니다.

사용법:
    pip install rdflib
    python validate_ttl.py "E:\\ai\\claude\\POI_ON_KGRAPH\\...\\05_knowledge_graph\\output"

폴더를 지정하지 않으면 현재 폴더를 검사합니다.
"""
import sys
import io
from pathlib import Path

try:
    from rdflib import Graph
    from rdflib.namespace import RDF
except ImportError:
    print("rdflib가 설치되어 있지 않습니다. 다음 명령으로 설치하세요:")
    print("    pip install rdflib")
    sys.exit(1)

# Windows 콘솔에서 한글 출력 깨짐 방지
if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf8"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")


def validate_file(path: Path):
    """단일 TTL 파일을 파싱하고 (성공여부, 정보 dict 또는 오류 메시지)를 반환."""
    g = Graph()
    try:
        g.parse(str(path), format="turtle")
    except Exception as e:
        return False, str(e)

    subjects = set(g.subjects())
    classes = set(g.objects(predicate=RDF.type))
    info = {
        "triples": len(g),
        "subjects": len(subjects),
        "classes": len(classes),
        "namespaces": [str(ns) for _, ns in g.namespaces() if str(ns)],
        "empty": len(g) == 0,
    }
    return True, info


def main():
    folder = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    if not folder.is_dir():
        print(f"폴더를 찾을 수 없습니다: {folder}")
        sys.exit(1)

    ttl_files = sorted(folder.glob("*.ttl"))
    if not ttl_files:
        print(f"'{folder}' 에 .ttl 파일이 없습니다.")
        sys.exit(1)

    print(f"검사 대상: {folder}  ({len(ttl_files)}개 파일)")
    print("=" * 70)

    ok_count, fail_count, warn_count = 0, 0, 0
    failures = []

    for f in ttl_files:
        success, result = validate_file(f)
        if success:
            mark = "✅"
            note = ""
            if result["empty"]:
                mark = "⚠️ "
                note = "  (트리플 0개 — 빈 파일)"
                warn_count += 1
            else:
                ok_count += 1
            print(f"{mark} {f.name}")
            print(f"     트리플: {result['triples']:,}  주어: {result['subjects']:,}  "
                  f"클래스: {result['classes']}{note}")
        else:
            fail_count += 1
            failures.append((f.name, result))
            print(f"❌ {f.name}")
            print(f"     오류: {result}")

    print("=" * 70)
    print(f"결과: 정상 {ok_count}개 / 경고 {warn_count}개 / 오류 {fail_count}개")

    if failures:
        print("\n오류 상세:")
        for name, err in failures:
            print(f"\n[{name}]")
            print(f"  {err}")
        sys.exit(2)


if __name__ == "__main__":
    main()
