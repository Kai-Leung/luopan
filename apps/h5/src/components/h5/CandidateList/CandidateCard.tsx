import React from 'react';
import type { CandidateGovernanceItem } from '../../../modules/input_flow/h5Interaction';
import { getCandidateActionLabel } from '../../../modules/input_flow/h5Interaction';

export function CandidateCard({ item }: { item: CandidateGovernanceItem }) {
  const prompts = Array.isArray(item.prompts) ? item.prompts : [];
  return (
    <span>
      {item.typeLabel}：{item.summary}｜{getCandidateActionLabel(item.nextAction)}
      {prompts.length > 0 ? `｜${prompts.join('；')}` : ''}
    </span>
  );
}
