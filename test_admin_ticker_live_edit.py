import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context(viewport={"width": 1400, "height": 900})
        page = await context.new_page()

        print("=== STEP 1: Open Admin Portal and Test Tab 6 Announcement Editor ===")
        await page.goto("http://localhost:8080/admin.html")
        
        # Unlock admin dashboard
        pass_input = page.locator("#admin-passcode-input")
        if await pass_input.is_visible():
            await pass_input.fill("deewan2026")
            await page.click(".auth-btn, button[type='submit']")
            await page.wait_for_timeout(500)

        # Switch to Tickers Tab
        await page.click("[data-tab='tickers']")
        await page.wait_for_timeout(400)

        # Verify live preview box exists in admin
        preview_box = page.locator("#admin-ticker-preview")
        assert await preview_box.is_visible(), "Admin live preview box should be visible!"

        # Enter a distinct custom announcement text
        custom_announcement = "⚡ SPECIAL MEGA OPENING 2026 • 100% ORIGINAL BRANDED CUT PIECES • FLAT 40% OFF NEW SUMMER ARRIVALS ⚡"
        ann_input = page.locator("#announcement-text-input")
        await ann_input.fill("")
        await ann_input.fill(custom_announcement)
        await page.wait_for_timeout(300)

        # Check that live preview in Admin updated immediately
        preview_text = await preview_box.inner_text()
        print("Admin Preview Text:", preview_text[:60].encode('ascii', 'ignore').decode('ascii'))
        assert "SPECIAL MEGA OPENING 2026" in preview_text

        # Click Save button
        await page.click("button:has-text('Save Announcement Text to Live Homepage'), button:has-text('Save Ticker Text')")
        await page.wait_for_timeout(600)

        await page.screenshot(path="C:/Users/hamza/.gemini/antigravity-ide/brain/6835ee2a-d400-453a-9276-c39c9757f28d/verify_admin_ticker_tab.png")
        print("Saved verify_admin_ticker_tab.png")

        print("=== STEP 2: Verify Homepage Below-Banner Marquee Ticker ===")
        homepage = await context.new_page()
        await homepage.goto("http://localhost:8080/index.html")
        await homepage.wait_for_selector(".announcement-bar__ticker", timeout=5000)
        await homepage.wait_for_timeout(500)

        ticker_text = await homepage.locator(".announcement-bar__ticker").inner_text()
        print("Homepage Ticker Text:", ticker_text[:80].encode('ascii', 'ignore').decode('ascii'))

        assert "SPECIAL MEGA OPENING 2026" in ticker_text, "Homepage ticker must reflect the text saved in Admin Portal!"
        assert "FLAT 40% OFF NEW SUMMER ARRIVALS" in ticker_text, "Homepage ticker must contain all bullet parts!"

        ticker_items = await homepage.locator(".announcement-bar__ticker .announcement-bar__item").count()
        print(f"PASS: Homepage ticker rendered {ticker_items} items.")
        assert ticker_items >= 6, f"Expected >= 6 ticker items for infinite seamless scroll, got {ticker_items}"

        await homepage.screenshot(path="C:/Users/hamza/.gemini/antigravity-ide/brain/6835ee2a-d400-453a-9276-c39c9757f28d/verify_homepage_below_banner_ticker.png")
        print("Saved verify_homepage_below_banner_ticker.png")

        print("=== STEP 3: Verify Mobile Responsiveness ===")
        mobile_page = await context.new_page()
        await mobile_page.set_viewport_size({"width": 390, "height": 844})
        await mobile_page.goto("http://localhost:8080/index.html")
        await mobile_page.wait_for_selector(".announcement-bar__ticker", timeout=5000)
        
        m_ticker_text = await mobile_page.locator(".announcement-bar__ticker").inner_text()
        assert "SPECIAL MEGA OPENING 2026" in m_ticker_text

        await mobile_page.screenshot(path="C:/Users/hamza/.gemini/antigravity-ide/brain/6835ee2a-d400-453a-9276-c39c9757f28d/verify_mobile_below_banner_ticker.png")
        print("Saved verify_mobile_below_banner_ticker.png")

        await browser.close()
        print("ALL TESTS PASSED: Announcement Ticker is 100% editable through Admin Portal and dynamically updates the below-banner homepage marquee!")

asyncio.run(run())
