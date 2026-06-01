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
import { EffectDataPanel } from "./EffectDataPanel";
import { EligibilityPanel } from "./EligibilityPanel";

type TabId =
  | "draft"
  | "evidence"
  | "matrix"
  | "ladder"
  | "oa"
  | "effect"
  | "eligibility"
  | "review";

const TABS: { id: TabId; label: string; needsDraft: boolean; badge?: string }[] = [
  { id: "draft",       label: "1. 진단·초안",           needsDraft: false },
  { id: "evidence",    label: "2. 선행기술 DB",          needsDraft: false },
  { id: "matrix",      label: "3. All Elements",        needsDraft: true  },
  { id: "ladder",      label: "4. Claim Ladder",        needsDraft: true  },
  { id: "oa",          label: "5. 가상 OA",             needsDraft: true  },
  { id: "effect",      label: "6. 효과데이터",   needsDraft: true,  badge: "New" },
  { id: "eligibility", label: "7. SW·AI 적격성", needsDraft: true,  badge: "New" },
  { id: "review",      label: "8. 리뷰·승인",           needsDraft: true  },
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
      <nav className="flex flex-wrap gap-1.5 border-b border-slate-200 pb-3">
        {TABS.map((t) => {
          const disabled = t.needsDraft && !draft;
          return (
            <button
              key={t.id}
              onClick={() => !disabled && setTab(t.id)}
              disabled={disabled}
              className={`relative rounded-md px-3 py-1.5 text-xs font-medium transition ${
                tab === t.id
                  ? "bg-brand text-white"
                  : disabled
                    ? "cursor-not-allowed text-slate-300"
                    : "bg-slate-100 text-slate-600 hover:bg-slate-200"
              }`}
              title={disabled ? "먼저 초안을 생성하세요" : undefined}
            >
              {t.label}
              {t.badge && (
                <span className="ml-1.5 rounded bg-green-500 px-1 py-0.5 text-[10px] font-bold text-white">
                  {t.badge}
                </span>
              )}
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

      {tab === "oa" && draft && (
        <OAPanel draft={draft} evidence={evidence} />
      )}

      {tab === "effect" && draft && invention && (
        <EffectDataPanel invention={invention} />
      )}

      {tab === "eligibility" && draft && invention && (
        <EligibilityPanel invention={invention} draft={draft} />
      )}

      {tab === "review" && draft && (
        <ReviewGate
          draft={draft}
          approval={approval}
          setApproval={setApproval}
        />
      )}
    </div>
  );
}
