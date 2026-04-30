# Risk Feed Strategy v2.9

## Concept: Top Risky Contracts on Base
Sentinel Alpha can publish a public risk intelligence feed that highlights sample high-risk patterns on Base in machine-readable form. This helps builders understand how to use risk signals in execution policy pipelines.

## Sample Feed Fields
- `address`
- `chain`
- `score`
- `threat_class`
- `action`
- `emergency_signal`
- `observed_at`
- `source`

## Initial Feed Approach
The first public feed can be curated/demo content until a live scanner pipeline is activated. Demo records must be clearly labeled as examples and not accusations.

## Roadmap to Live Scanner
1. Start with static demo feed artifacts and public schema.
2. Add ingestion pipeline for monitored Base contract events.
3. Add scoring and classification pass with review safeguards.
4. Publish periodic signed feed updates with provenance metadata.
5. Expose incremental feed endpoints for partner integrations.
