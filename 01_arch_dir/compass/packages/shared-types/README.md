# packages/shared-types

Compass shared TypeScript types — derived from real backend FastAPI/Pydantic schemas.

## Usage

```ts
import type {
  L0RawInputResponse,
  L1CandidateResponse,
  S2GovernanceCheckResponse,
  PendingConfirmationItem,
  ManualConfirmationReviewResponse,
  L2FactResponse,
  L3FactViewResponse,
} from "@compass/shared-types";
```

## Source

Generated from `packages/contracts/openapi/openapi.json` (backed by real running API).
Do not edit manually — update contracts and regenerate.
