# BeezShield Prime Website (v3.4.1)

## Overview
This document outlines the v3.4.1 overhaul of the BeezShield website, transitioning it from a dashboard/admin panel aesthetic to a premium, investor-grade "Machine Trust Infrastructure" product page.

## Key Positioning
*   **Umbrella Brand**: BeezShield
*   **Live Product**: Sentinel Alpha
*   **Core Value**: "Pre-execution decision engine for agents."
*   **Target Audience**: Builders of autonomous systems and AI agents.

## Design Identity
*   **Visual Language**: Vercel/Linear quality. Clean, lots of breathing room, dark mode (not pure black #000, but deep #050505).
*   **Swarm Concept**: Transitioned from literal bees/hexagons to an abstract canvas particle visualization representing network nodes.
*   **Performance**: Max 40 particles, animated via `requestAnimationFrame`, pauses when the tab is hidden. No heavy external frameworks like React, strictly vanilla HTML/JS/CSS designed for easy migration to Next.js later if needed.

## Functional Changes
*   **Real API**: Kept the live integration with `/contracts/risk-score`.
*   **x402 Payments**: Emphasized Base USDC lane pricing.
*   **ERC-8004**: Linked the on-chain identity correctly.
*   **SEO Optimization**: Updated OpenGraph, JSON-LD, Twitter cards, and semantic HTML tags.

## Validation
*   No fake claims (removed "MCP live" / "A2A live").
*   No fear-selling language.
*   Interactive scan preview provides accurate simulated feedback and functional `cURL` copying.
