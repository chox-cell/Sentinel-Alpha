# Deployment Runbook v2.1

## Goal

Deploy Sentinel Alpha on a public HTTPS URL so bots and agents can call production endpoints without localhost or ngrok.

## Components

- API process managed by systemd:
  - `infra/deploy/systemd/sentinel-alpha.service`
- Nginx reverse proxy:
  - `infra/deploy/nginx/sentinel-alpha.conf`
- Production environment checker:
  - `scripts/production_env_check.py`

## Flow

1. Configure production `.env` on host.
2. Run:
   - `python3 scripts/production_env_check.py`
3. Start/enable service:
   - `sudo systemctl daemon-reload`
   - `sudo systemctl enable sentinel-alpha`
   - `sudo systemctl restart sentinel-alpha`
4. Apply nginx config and reload.
5. Verify health:
   - `GET /health`
   - `GET /internal/manifest`

## Safety

- Keep `/contracts/risk-score` endpoint and response schema unchanged.
- Do not expose `.env` or secret values in logs.
