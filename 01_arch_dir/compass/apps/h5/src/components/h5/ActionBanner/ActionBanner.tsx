import React from 'react';
import type { InteractionHints } from '../../../modules/input_flow/h5Interaction';

export function ActionBanner({ hints }: { hints: InteractionHints }) {
  const statusItems = Array.isArray(hints?.statusItems) ? hints.statusItems : [];
  if (!hints?.visible) return null;
  return (
    <div className="h5-interaction-status" aria-label="当前输入提示">
      {statusItems.map((item) => <span key={item}>{item}</span>)}
    </div>
  );
}
