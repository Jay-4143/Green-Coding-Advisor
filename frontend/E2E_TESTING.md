# End-to-end (E2E) testing with Playwright

This project uses **Playwright** for browser-level E2E tests of critical frontend flows.

## Installation

From the `frontend` folder:

```bash
npm install
npx playwright install
```

The `npx playwright install` step downloads the browser binaries Playwright needs.

## Scripts

From the `frontend` directory:

- Run all E2E tests (headless):

```bash
npm run test:e2e
```

- Run E2E tests in headed mode:

```bash
npm run test:e2e:headed
```

- Open Playwright UI:

```bash
npm run test:e2e:ui
```

## What is currently covered

- `tests/e2e/home-and-submit.spec.ts`
  - Verifies the **Home** page hero content renders.
  - Clicks **Get Started** and navigates to the `/submit` page.
  - Types code into the **\"Paste your code here...\"** textarea.

- `tests/e2e/login-modal.spec.ts`
  - Opens the **Login** modal from the navbar.
  - Types an email and password into the inputs.

These tests focus on **frontend UX and routing** only. Backend API calls are not yet asserted in E2E tests; they will be added later (with either a real backend running or HTTP mocking).


