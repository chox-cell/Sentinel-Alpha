# BeezShield Brand Asset Requirements

## Purpose

Define a practical checklist for visual assets used across BeezShield surfaces (website, README, social cards, npm, and docs) while preserving product truth and technical quality.

---

## 1) Logo Requirements

- Primary logo should combine **BeezShield wordmark** with a **2.5D abstract hive/shield** symbol.
- Symbol must read as security + network intelligence (hex, shield geometry, trust links).
- Provide:
  - horizontal lockup
  - stacked lockup
  - icon-only mark
- Export formats:
  - SVG (source of truth)
  - PNG @1x/@2x/@3x with transparent background
- Minimum clear space: at least 0.5x mark width around logo.
- Minimum digital size:
  - full logo: 120 px width
  - icon mark: 24 px

## 2) Favicon Requirements

- Include:
  - `favicon.ico` (multi-size)
  - `favicon-16x16.png`
  - `favicon-32x32.png`
  - `apple-touch-icon.png` (180x180)
- Favicon must use simplified shield/hive icon (not full wordmark).
- Keep strong contrast on dark and light browser tabs.

## 3) Social Preview Requirements

- Open Graph/Twitter preview image:
  - 1200x630 px PNG/WebP
  - <= 300 KB preferred
- Content should include:
  - BeezShield name
  - Sentinel Alpha positioning: pre-execution decision engine
  - subtle Base/x402/agent context
- Keep text readable on mobile crop.
- No fake badges, no fake security certifications.

## 4) GitHub README Banner Requirements

- Recommended size: 1280x640 px (safe center composition).
- Must include:
  - BeezShield brand
  - Sentinel Alpha product name
  - one-line value proposition
- Should avoid dense text; optimize for quick scan.
- Provide dark-mode-safe version (or neutral banner that works in both modes).

## 5) npm Package Visual Requirements

- npm listing visuals should remain truthful and minimal:
  - package name: `@beezshield/sentinel`
  - clear icon (shield/hive abstraction)
  - no “official AgentKit provider live” claim
- README badges/icons should be low-noise and factual.
- If screenshots are added later, use real product captures only.

## 6) Visual Do/Don't

### Do

- Use abstract geometric hive/shield language.
- Keep style modern, technical, and trust-oriented.
- Use consistent palette and typography.
- Prefer clarity over ornament.

### Don't

- No cartoon bees.
- No mascot-heavy, playful imagery for core trust surfaces.
- No fake claims (security guarantees, false integrations, fake audits).
- No fear-selling visuals (panic imagery, attack theatrics).

## 7) 2.5D Abstract Hive/Shield Direction

- Visual direction:
  - layered hex cells
  - shield silhouette
  - soft depth/parallax cues
  - thin trust-link lines and controlled glow
- Keep motion optional and subtle.
- Core identity should remain recognizable in static form.

## 8) Claims & Messaging Guardrails

- Never imply:
  - guaranteed protection
  - automatic x402 settlement in SDK
  - official AgentKit provider live (until truly shipped)
- All copy must match current product truth.

## 9) Accessibility Requirements

- Color contrast:
  - normal text: WCAG AA minimum (4.5:1)
  - large text: WCAG AA minimum (3:1)
- Do not rely on color alone for critical state.
- Provide alt text for meaningful brand images.
- Avoid flashing or aggressive motion.
- Ensure logos remain legible at small sizes.

## 10) Performance Constraints

- Prefer SVG for logos/icons.
- Compress raster assets (PNG/WebP) before commit.
- Target budgets:
  - individual brand asset <= 300 KB when possible
  - hero/social assets optimized to avoid layout jank
- Avoid shipping duplicate large variants unless required.

---

## Release Checklist (Asset Pack)

- [ ] Logo set exported (SVG + PNG variants)
- [ ] Favicon set generated
- [ ] OG/Twitter card generated and compressed
- [ ] README banner created and tested in dark/light contexts
- [ ] Copy reviewed for truthfulness (no fake claims)
- [ ] Accessibility spot-check complete
- [ ] Asset sizes meet performance budget
