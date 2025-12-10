import { test, expect } from '@playwright/test'

test.describe('Login modal UX (frontend only)', () => {
  test('can open login modal and type credentials', async ({ page }) => {
    await page.goto('/')

    await page.getByRole('button', { name: /login/i }).click()

    await expect(page.getByRole('heading', { name: /login/i })).toBeVisible()

    const emailInput = page.getByPlaceholder('your.email@example.com')
    const passwordInput = page.getByPlaceholder('Enter your password')

    await emailInput.fill('test@example.com')
    await passwordInput.fill('Password123!')

    await expect(emailInput).toHaveValue('test@example.com')
    await expect(passwordInput).toHaveValue('Password123!')
  })
})


