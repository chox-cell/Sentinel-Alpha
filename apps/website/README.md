# BeezShield Website v1

This is the static frontend for the BeezShield umbrella brand and Sentinel Alpha product.

## Tech Stack
- HTML5
- Vanilla CSS (Custom design system, flexbox/grid layouts, light/dark mode)
- Vanilla JavaScript (Micro-animations, smooth scrolling, theme persistence)
- **No build step required.**

## Local Development
To preview the website locally, you can use any static server. For example, if you have Python installed:

```bash
cd apps/website
python3 -m http.server 8080
```
Then open `http://localhost:8080` in your browser.

## Deployment Instructions

Since this is a pure static site (HTML/CSS/JS), it can be deployed instantly on any modern static hosting provider. 

### Deploying to Cloudflare Pages (Recommended for Speed & Security)
1. Push this code to the `main` branch of your GitHub repository.
2. Log into Cloudflare Dashboard and navigate to **Pages**.
3. Click **Create a project** -> **Connect to Git**.
4. Select the `Sentinel-Alpha` repository.
5. In the build settings:
   - Framework preset: `None`
   - Build command: *(leave empty)*
   - Build output directory: `apps/website`
6. Click **Save and Deploy**.
7. Go to **Custom Domains** and add `beezshield.com`. Update your DNS records as instructed by Cloudflare.

### Deploying to Vercel
1. Log into Vercel and click **Add New Project**.
2. Import the `Sentinel-Alpha` repository.
3. Set the **Root Directory** to `apps/website`.
4. Leave build commands empty.
5. Click **Deploy**.
6. Navigate to Project Settings -> Domains and add `beezshield.com`.

### Deploying to Netlify
1. Log into Netlify and click **Add new site** -> **Import an existing project**.
2. Connect your GitHub and select the `Sentinel-Alpha` repo.
3. Set the **Base directory** to `apps/website`.
4. Set the **Publish directory** to `apps/website`.
5. Click **Deploy site**.
6. Go to **Domain management** and add `beezshield.com`.

## Modifying Content
- All content and markup is in `index.html`.
- Styles and tokens (colors, fonts, etc.) are in `styles.css`.
- Interactivity (animations, smooth scroll, theme toggle) is in `main.js`. 

## Note on Architecture
This site purposely avoids heavy frameworks to optimize for speed, trust, and machine-native credibility. No complex state or hydration is used.
