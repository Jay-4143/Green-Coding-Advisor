# Green Coding Advisor VS Code Extension (MVP)

Inline analysis for selected code using the Green Coding Advisor backend.

## Features
- Command Palette: `Green Coding Advisor: Analyze Selection`
- Uses backend `/advisor/analyze` endpoint with `{ code_content, language, filename }`
- Reads settings:
  - `greenCodingAdvisor.backendUrl` (default `http://127.0.0.1:8000`)
  - `greenCodingAdvisor.authToken` (Bearer token, optional)

## Setup (dev)
```bash
cd extensions/vscode
npm install
npm run compile
```

## Run the extension
1) Open VS Code → “Run and Debug” → “Launch Extension”.
2) In the Extension Development Host, open a file, select code, press `Ctrl+Shift+P`, choose `Green Coding Advisor: Analyze Selection`.

## Packaging (optional)
```bash
# install vsce once: npm i -g @vscode/vsce
vsce package
```

## Notes
- Backend must be running and reachable.
- If auth is enabled, set `greenCodingAdvisor.authToken` in VS Code settings.
- Adjust `backendUrl` for staging/production as needed.

