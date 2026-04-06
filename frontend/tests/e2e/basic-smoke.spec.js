import { test, expect } from '@playwright/test';

test.describe('Vaultwares Frontend Smoke Test', () => {
  test('homepage loads and displays main UI', async ({ page }) => {
    await page.goto('/');
    await expect(page).toHaveTitle(/vaultwares|react/i);
    await expect(page.locator('body')).toBeVisible();
    // Add more UI checks as needed
  });
});
