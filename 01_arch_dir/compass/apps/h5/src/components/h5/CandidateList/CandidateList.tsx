import React from 'react';
import type { CandidateGovernanceItem } from '../../../modules/input_flow/h5Interaction';
import { CandidateCard } from './CandidateCard';

export function CandidateList({ items }: { items: CandidateGovernanceItem[] }) {
  const candidateItems = Array.isArray(items) ? items : [];
  if (candidateItems.length === 0) return null;
  return (
    <div className="h5-interaction-status" aria-label="候选治理列表">
      {candidateItems.map((item) => <CandidateCard item={item} key={item.candidateId} />)}
    </div>
  );
}
