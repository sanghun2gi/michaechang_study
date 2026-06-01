import type { Metadata } from "next";
import "./globals.css";
import { LegalBanner } from "@/components/LegalBanner";

export const metadata: Metadata = {
  title: "AI 특허출원 대시보드",
  description:
    "발명 아이디어를 넣으면 등록 가능성 진단과 명세서·청구항 초안, 가상 거절이유까지 만들어 출원 준비를 돕는 AI 특허 비서.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="ko">
      <body>
        <LegalBanner />
        <header className="border-b border-slate-200 bg-white">
          <div className="mx-auto flex max-w-5xl items-center justify-between px-4 py-4">
            <div className="flex items-center gap-2">
              <span className="text-lg font-bold text-brand">⚖️ AI 특허출원 대시보드</span>
              <span className="rounded bg-slate-100 px-2 py-0.5 text-xs text-slate-500">
                MVP · 1차 스프린트
              </span>
            </div>
          </div>
        </header>
        <main className="mx-auto max-w-5xl px-4 py-8">{children}</main>
        <footer className="border-t border-slate-200 bg-white py-6 text-center text-xs text-slate-400">
          최종 판단은 변리사가 합니다. · 발명정보는 영업비밀로 보호됩니다.
        </footer>
      </body>
    </html>
  );
}
