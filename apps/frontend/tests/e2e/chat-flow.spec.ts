import { test, expect } from "@playwright/test";

test.describe("Chat tutoring flow", () => {
  test("user can request hint and see exercise card", async ({ page }) => {
    await page.goto("/chat");
    await page.getByPlaceholder("Tulis pertanyaanmu...").fill("Saya butuh hint persamaan linear");
    await page.getByRole("button", { name: "Kirim" }).click();

    await expect(page.getByTestId("hint-panel")).toBeVisible();
    await expect(page.getByTestId("code-runner"), "Code runner is rendered").toBeVisible();
  });
});
