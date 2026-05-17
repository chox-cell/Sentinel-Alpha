# BeezShield brand & logo brief

**Purpose:** Prepare consistent marketplace and public-surface assets after **x402scan** registration. **Docs/planning only** — raster PNGs are not generated in this pass unless design tooling is run separately.

## Brand identity

| Field | Value |
| --- | --- |
| **Brand name** | BeezShield |
| **Product** | Sentinel Alpha |
| **Category** | Machine Trust Infrastructure |
| **Doctrine** | BeezShield builds guardians, not traders. |

## Logo direction

- **Shield** — protection at the decision boundary, not execution/trading
- **Bee / hexagon signal** — swarm intelligence without implying trading bots
- **Guardian / risk boundary** — pre-execution policy layer
- **Readable at 16px** — favicon, directory icons, npm/marketplace thumbnails (must remain readable at 16px)

## Color palette

- **Black** — primary background / wordmark contrast
- **Gold** — accent (trust, premium signal; use sparingly)
- **Electric blue** — tech / Base / API accent
- **White** — light backgrounds and inverse lockups

## Required asset paths (target)

| Asset | Path | Notes |
| --- | --- | --- |
| Full wordmark + mark | `apps/website/public/brand/beezshield-logo.svg` | Horizontal lockup for site header |
| Icon / mark only | `apps/website/public/brand/beezshield-icon.svg` | Square; **16px** legibility test required |
| Open Graph | `apps/website/public/brand/beezshield-og.png` | 1200×630 when raster export available |
| x402scan / directory card | `apps/website/public/brand/x402scan-logo.png` | Optional square card; match marketplace crop |

Do **not** commit placeholder PNGs without a deliberate design export pass.

## Marketplace card copy (x402scan-aligned)

| Field | Copy |
| --- | --- |
| **Title** | BeezShield \| Pre-execution decision engine for agents |
| **Subtitle** | Machine Trust Infrastructure for agentic contract risk decisions on Base. |

## Usage notes

- Pair logo assets with public-safe claims from `X402SCAN_REGISTRATION_EVIDENCE.md` and `X402_DIRECTORY_SUBMISSION_PACK.md`.
- Avoid “official x402,” “partner,” “endorsed,” or “guaranteed security” in visual taglines.

## Generated public SVG assets

- `apps/website/public/brand/beezshield-logo.svg`
- `apps/website/public/brand/beezshield-wordmark.svg`

These are simple first-pass vector assets for directory/profile use. They are not final brand identity assets.

