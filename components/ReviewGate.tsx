"use client";

import { useState } from "react";
import { DraftResult, ReviewApproval } from "@/lib/types";

// STEP 24 + 24B: 전문가 리뷰 화면 + Human Authority Gate(승인 게이트)
// 사람(변리사)의 명시적 승인 없이는 "출원 패키지 확정"이 불가능하도록 막는 단계.
export function ReviewGate({
  draft,
  approval,
  setApproval,
}: {
  draft: DraftResult;
  approval: ReviewApproval;
  setApproval: (a: ReviewApproval) => void;
}) {
  const [reviewer, setReviewer] = useState(approval.reviewer);
  const [comment, setComment] = useState(approval.comment);

  function decide(status: "APPROVED" | "REJECTED") {
    setApproval({
      status,
      reviewer: reviewer.trim() || "(미기재)",
      comment,
      decidedAt: new Date().toISOString(),
    });
  }

  const decided = approval.status !== "PENDING";

  return (
    <div className="space-y-5">
      <div>
        <h2 className="text-base font-bold">전문가 리뷰 · 승인 게이트 (STEP 24 / 24B)</h2>
        <p className="mt-1 text-xs text-slate-500">
          AI 산출물은 변리사의 명시적 승인 전까지 초안 상태입니다. 승인 게이트를 통과해야 출원 패키지로 확정됩니다.
        </p>
      </div>

      {/* 검토 요약 */}
      <div className="rounded-lg border border-slate-200 bg-white p-4 text-sm">
        <h3 className="mb-2 font-bold">검토 대상 요약</h3>
        <ul className="space-y-1 text-slate-600">
          <li>• 명세서 4개 섹션 + 청구항 초안</li>
          <li>
            • 할루시네이션 종합 등급:{" "}
            <span className="font-semibold">{draft.overallTag}</span>
          </li>
          <li>• AI 판단 원장 기록 {draft.ledgerIds.length}건</li>
        </ul>
        {draft.overallTag === "RED" && (
          <p className="mt-2 rounded bg-red-50 p-2 text-xs text-red-700">
            ⚠️ RED 등급 항목이 있습니다. 승인 전 근거 확인을 권장합니다.
          </p>
        )}
      </div>

      {/* 승인 상태 */}
      <div
        className={`rounded-lg border p-4 ${
          approval.status === "APPROVED"
            ? "border-green-300 bg-green-50"
            : approval.status === "REJECTED"
              ? "border-red-300 bg-red-50"
              : "border-slate-200 bg-white"
        }`}
      >
        <p className="text-sm font-semibold">
          현재 상태:{" "}
          {approval.status === "PENDING"
            ? "승인 대기 (출원 패키지 확정 불가)"
            : approval.status === "APPROVED"
              ? `승인됨 — ${approval.reviewer}`
              : `반려됨 — ${approval.reviewer}`}
        </p>
        {decided && approval.decidedAt && (
          <p className="mt-1 text-xs text-slate-500">
            결정 시각: {new Date(approval.decidedAt).toLocaleString("ko-KR")}
          </p>
        )}
        {decided && approval.comment && (
          <p className="mt-1 text-xs text-slate-600">코멘트: {approval.comment}</p>
        )}
      </div>

      {/* 리뷰 입력 */}
      <div className="space-y-3 rounded-lg border border-slate-200 bg-white p-4">
        <input
          className="w-full rounded border border-slate-300 p-2 text-sm"
          placeholder="검토자 (변리사명)"
          value={reviewer}
          onChange={(e) => setReviewer(e.target.value)}
        />
        <textarea
          className="w-full rounded border border-slate-300 p-2 text-sm"
          placeholder="검토 코멘트"
          rows={3}
          value={comment}
          onChange={(e) => setComment(e.target.value)}
        />
        <div className="flex gap-3">
          <button
            onClick={() => decide("APPROVED")}
            className="flex-1 rounded-md bg-green-600 py-2 text-sm font-semibold text-white hover:bg-green-700"
          >
            승인 (출원 패키지 확정)
          </button>
          <button
            onClick={() => decide("REJECTED")}
            className="flex-1 rounded-md bg-red-600 py-2 text-sm font-semibold text-white hover:bg-red-700"
          >
            반려
          </button>
        </div>
        <p className="text-center text-xs text-slate-400">
          승인 이력은 변경 추적을 위해 기록됩니다(데모: 클라이언트 상태).
        </p>
      </div>
    </div>
  );
}
