# Green Coding Advisor Chrome Extension (MVP)

## What it does
- Popup to send code snippets to the backend `/advisor/analyze` endpoint.
- Context menu: select code on any page, right-click → “Analyze code with Green Coding Advisor”.
- Stores backend URL and optional bearer token in extension storage.

## Files
- `manifest.json` — Manifest v3 definition.
- `popup.html`, `popup.js`, `styles.css` — UI for quick analysis.
- `background.js` — Registers context menu and forwards selection.
- `content.js` — Sends selected code to the backend and shows a quick alert with the result.
- `icons/` — Add `icon16.png`, `icon48.png`, `icon128.png`.

## Configure
1) In the popup, set:
   - Backend: `http://127.0.0.1:8000` (or your deployed URL)
   - Token (optional): paste JWT if your backend requires auth.
2) The content script also reads `backendUrl` and `authToken` from `chrome.storage.sync`. You can set them by opening DevTools > Console in the popup and running:
   ```js
   chrome.storage.sync.set({ backendUrl: "http://127.0.0.1:8000", authToken: "" })
   ```

## Load the extension
1) Build assets are already static; no bundling required.
2) In Chrome/Edge: `chrome://extensions` → enable Developer Mode → “Load unpacked” → select `extensions/chrome`.
3) Pin the extension and open the popup, or right-click selected code to analyze.

## Notes
- The backend call targets `/advisor/analyze` with `{ code_content, language, filename }`.
- If your backend enforces auth, provide a valid bearer token.
- Update `host_permissions` in `manifest.json` to match your deployed host.

