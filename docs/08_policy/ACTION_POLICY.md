# Action Policy v1.8

## Decisions
- BLOCK
- REDUCE
- ALLOW
- REVIEW
- EXIT_NOW

## Current Logic
IF confidence < 0.5:
  REVIEW

IF oracle_dislocation OR liquidity_unlocked AND score >= 80:
  EXIT_NOW

IF score >= 85:
  BLOCK

IF score >= 65:
  REDUCE

ELSE:
  ALLOW

## Emergency Priority
EXIT_NOW overrides BLOCK when liquidity/oracle emergency exists.

## Current Threat Classes
- invalid_contract_address
- oracle_dislocation
- liquidity_rug
- execution_drift
- behavioral_launch_syndicate
- privilege_rug
- insufficient_data
- normal
