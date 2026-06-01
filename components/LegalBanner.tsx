// 법적 경계 문구 — 전역 노출 (문서 A-1, 절대규칙 #3)
// 모든 화면에 일관되게 표시되어야 한다.
export function LegalBanner() {
  return (
    <div className="border-b border-amber-200 bg-amber-50 px-4 py-2 text-center text-xs text-amber-800">
      본 서비스는 출원 준비를 돕는 <strong>초안·진단·참고</strong> 도구입니다.
      특허등록을 보장하지 않으며, 변리사·변호사의 법률 자문을 대체하지 않습니다.
      최종 출원 판단은 사용자/전문가의 책임입니다.
    </div>
  );
}
