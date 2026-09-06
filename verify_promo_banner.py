import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context(viewport={"width": 1400, "height": 900})
        page = await context.new_page()

        print("Testing Homepage Promotional Welcome Banner...")
        await page.goto("http://localhost:8080/index.html")
        await page.wait_for_selector(".welcome-promo-banner img", timeout=5000)

        promo_img = page.locator(".welcome-promo-banner img")
        assert await promo_img.is_visible(), "Promotional banner image must be visible!"

        # Check natural width and height (not broken 0x0)
        img_info = await promo_img.evaluate("img => ({ src: img.src, naturalWidth: img.naturalWidth, naturalHeight: img.naturalHeight, complete: img.complete })")
        print(f"Promo Image Info: {img_info}")

        assert img_info["complete"] == True, "Image must be loaded completely!"
        assert img_info["naturalWidth"] > 0, "Image natural width must be greater than 0!"
        assert img_info["naturalHeight"] > 0, "Image natural height must be greater than 0!"

        # Scroll to promo banner and take snapshot
        await promo_img.scroll_into_view_if_needed()
        await page.wait_for_timeout(300)
        await page.screenshot(path="C:/Users/hamza/.gemini/antigravity-ide/brain/6835ee2a-d400-453a-9276-c39c9757f28d/verify_welcome_promo_banner.png")
        print("Saved verify_welcome_promo_banner.png")

        await browser.close()
        print("PROMOTIONAL WELCOME BANNER VERIFICATION PASSED SUCCESSFULLY!")

asyncio.run(run())
