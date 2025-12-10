import { test, expect } from '@playwright/test'

test.describe('Home and submit flow (frontend only)', () => {
  test('landing page shows main hero content', async ({ page }) => {
    await page.goto('/')

    // There are two h1s with the same text (navbar + hero); target the main hero heading
    await expect(
      page.getByRole('main').getByRole('heading', { name: 'Green Coding Advisor', exact: true })
    ).toBeVisible()
    await expect(page.getByText(/AI-Enhanced Platform for Sustainable Coding Practices/i)).toBeVisible()

    await expect(page.getByRole('link', { name: /get started/i })).toBeVisible()
    await expect(page.getByRole('link', { name: /learn more/i })).toBeVisible()
  })

  test('can navigate to submit page and type code', async ({ page }) => {
    await page.goto('/')

    await page.getByRole('link', { name: /get started/i }).click()

    await expect(page.getByRole('heading', { name: /submit code for analysis/i })).toBeVisible()

    const codeInput = page.getByPlaceholder('Paste your code here...')
    await codeInput.fill('def hello():\n    return "world"')

    await expect(codeInput).toHaveValue(/hello/)
  })
})


