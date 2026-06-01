"use client";

import { useState } from "react";
import {
  InventionInput,
  DraftResult,
  Evidence,
  MatrixRow,
  ReviewApproval,
} from "@/lib/types";
import { InventionForm } from "./InventionForm";
import { EvidenceDB } from "./EvidenceDB";
import { AllElementsMatrix } from "./AllElementsMatrix";
import { ClaimLadderPanel } from "./ClaimLadderPanel";
import { OAPanel } from "./OAPanel";
import { ReviewGate } from "./ReviewGate";

type TabId = "draft" | "evidence" | "matrix" | "ladder" | "oa" | "review";

const TABS: { id: TabId; label: string; needsDraft: boolean }[] = [
  { id: "draft", label: "1. 진단·초안 (STEP 1/3/18/19)", needsDraft: false },
  { id: "evidence", label: "2. 선행기술 DB (STEP 6)", needsDraft: false },
  { id: "matrix", label: "3. All Elements (STEP 9)", needsDraft: true },
  { id: "ladder", label: "4. Claim Ladder (STEP 14/15/16)", needsDraft: true },
  { id: "oa", label: "5. 가상 OA (STEP 21)", needsDraft: true },
  { id: "review", label: "6. 리뷰·승인 (STEP 24/24B)", needsDraft: true },
];

export function Workspace() {
  const [tab, setTab] = useState<TabId>("draft");
  const [invention, setInvention] = useState<InventionInput | null>(null);
  const [draft, setDraft] = useState<DraftResult | null>(null);
  const [evidence, setEvidence] = useState<Evidence[]>([]);
  const [matrix, setMatrix] = useState<MatrixRow[]>([]);
  const [approval, setApproval] = useState<ReviewApproval>({
    status: "PENDING",
    reviewer: "",
    comment: "",
    decidedAt: null,
  });

  function handleDraft(inv: InventionInput, d: DraftResult) {
    setInvention(inv);
    setDraft(d);
  }

  return (
    <div className="space-y-6">
      <nav className="flex flex-wrap gap-2 border-b border-slate-200 pb-2">
        {TABS.map((t) => {
          const disabled = t.needsDraft && !draft;
          return (
            <button
              key={t.id}
              onClick={() => !disabled && setTab(t.id)}
              disabled={disabled}
              className={`rounded-md px-3 py-1.5 text-xs font-medium transition ${
                tab === t.id
                  ? "bg-brand text-white"
                  : disabled
                    ? "cursor-not-allowed text-slate-300"
                    : "bg-slate-100 text-slate-600 hover:bg-slate-200"
              }`}
              title={disabled ? "먼저 초안을 생성하세요" : undefined}
            >
              {t.label}
            </button>
          );
        })}
      </nav>

      {tab === "draft" && <InventionForm onResult={handleDraft} />}

      {tab === "evidence" && (
        <EvidenceDB evidence={evidence} setEvidence={setEvidence} />
      )}

      {tab === "matrix" && draft && (
        <AllElementsMatrix
          components={draft.structureCard.components}
          evidence={evidence}
          matrix={matrix}
          setMatrix={setMatrix}
        />
      )}

      {tab === "ladder" && draft && invention && (
        <ClaimLadderPanel invention={invention} draft={draft} />
      )}

      {tab === "oa" && draft && <OAPanel draft={draft} evidence={evidence} />}

      {tab === "review" && draft && (
        <ReviewGate draft={draft} approval={approval} setApproval={setApproval} />
      )}
    </div>
  );
}
