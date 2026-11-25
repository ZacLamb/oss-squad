# Oss! Squad (working title) — hidden test build

Grappling reskin of Everlight Heroes. Standalone game: own save keys (`ossSquad.*`), own service-worker cache (`oss-squad-v*`), cloud saves off until it has its own save server.

- `public/index.html` is the built game (from the source project's `story/make_game.py`).
- `server.js` serves `public/` on Railway (`npm start`). Every response sends `X-Robots-Tag: noindex`; `robots.txt` blocks crawlers.
- Art (heroes, belts, Pressure King, prologue, banner) loads from one Higgs CDN bundle. Before public launch, bundle it locally so the game works offline.

To update: rebuild the game in the source project, copy it to `public/index.html`, bump `public/sw.js` cache version, commit, push. Railway redeploys automatically.
