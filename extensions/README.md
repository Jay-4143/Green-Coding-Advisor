# Green Coding Advisor Extensions

This folder contains MVP implementations for browser and editor integrations.

## Chrome/Edge Extension
- Location: `extensions/chrome`
- Manifest v3 popup + context menu
- Sends code to backend `/advisor/analyze`
- See `extensions/chrome/README.md` for setup and loading via “Load unpacked”.

## VS Code Extension
- Location: `extensions/vscode`
- Command: `Green Coding Advisor: Analyze Selection`
- Uses backend `/advisor/analyze`
- Configure `greenCodingAdvisor.backendUrl` and optional `greenCodingAdvisor.authToken`.
- See `extensions/vscode/README.md` for build/run instructions.

## Backend expectation
- Backend endpoint `/advisor/analyze` accepts `{ code_content, language, filename }`.
- If auth is required, provide a valid bearer token.

