import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context(viewport={"width": 1400, "height": 900})
        page = await context.new_page()

        print("=== STEP 1: Verify Top Purple Header Bar is REMOVED ===")
        await page.goto("http://localhost:8080/index.html")
        top_bar = await page.query_selector("#top-header-announcement-bar, .top-announcement-bar")
        assert top_bar is None, "Top header announcement bar should be removed from DOM!"
        print("PASS: Top header purple bar is removed from index.html.")

        await page.goto("http://localhost:8080/collections.html")
        top_bar_c = await page.query_selector("#top-header-announcement-bar, .top-announcement-bar")
        assert top_bar_c is None, "Top header announcement bar should be removed from collections.html!"
        print("PASS: Top header purple bar is removed from collections.html.")

        await page.goto("http://localhost:8080/order-tracking.html")
        top_bar_ot = await page.query_selector("#top-header-announcement-bar, .top-announcement-bar")
        assert top_bar_ot is None, "Top header announcement bar should be removed from order-tracking.html!"
        print("PASS: Top header purple bar is removed from order-tracking.html.")

        print("=== STEP 2: Verify Hero Ticker Marquee on Homepage ===")
        await page.goto("http://localhost:8080/index.html")
        await page.wait_for_selector(".announcement-bar__ticker", timeout=5000)
        ticker_items = await page.locator(".announcement-bar__ticker .announcement-bar__item").all_inner_texts()
        print(f"PASS: Hero ticker has {len(ticker_items)} items rendered.")
        assert len(ticker_items) > 0

        # Hover on Unstitched -> 1PC to check Bedsheets submenu
        print("=== STEP 3: Verify Unstitched -> 1PC -> Bedsheets Submenu ===")
        await page.hover("#nav-dropdown-unstitched .header-nav__link")
        await page.wait_for_timeout(300)
        await page.hover("#nav-dropdown-unstitched .nav-dropdown-item:has-text('1PC')")
        await page.wait_for_timeout(300)

        bedsheets_sublink = page.locator("#nav-dropdown-unstitched .nav-submenu a:has-text('Bedsheets')")
        is_sublink_visible = await bedsheets_sublink.is_visible()
        print(f"Bedsheets sublink visible: {is_sublink_visible}")
        assert is_sublink_visible, "Bedsheets sublink must be visible under 1PC submenu!"

        await page.screenshot(path="C:/Users/hamza/.gemini/antigravity-ide/brain/6835ee2a-d400-453a-9276-c39c9757f28d/verify_submenu_bedsheets.png")
        print("Saved verify_submenu_bedsheets.png")

        # Click Bedsheets sublink
        print("=== STEP 4: Navigate to Bedsheets Collection ===")
        await bedsheets_sublink.click()
        await page.wait_for_load_state("networkidle")
        await page.wait_for_timeout(1000)

        assert "type=Bedsheet" in page.url
        title_text = await page.locator("#catalog-title").inner_text()
        print(f"Collection Title: {title_text}")
        assert "BEDSHEET" in title_text.upper()

        product_count = await page.locator(".product-card").count()
        print(f"Bedsheet products found: {product_count}")
        assert product_count >= 3, f"Expected >= 3 products, got {product_count}"

        await page.screenshot(path="C:/Users/hamza/.gemini/antigravity-ide/brain/6835ee2a-d400-453a-9276-c39c9757f28d/verify_bedsheets_page.png")
        print("Saved verify_bedsheets_page.png")

        # Admin Portal Test
        print("=== STEP 5: Test Admin Portal Announcement Editor ===")
        await page.goto("http://localhost:8080/admin.html")
        # Login
        pass_input = page.locator("#admin-passcode-input")
        if await pass_input.is_visible():
            await pass_input.fill("deewan2026")
            await page.click(".auth-btn, button[type='submit']")
            await page.wait_for_timeout(500)

        # Switch to Tickers Tab
        await page.click("[data-tab='tickers']")
        await page.wait_for_timeout(300)

        ann_input = page.locator("#announcement-text-input")
        await ann_input.fill("Mega Sale 70% Off • Luxury Bedsheets Live • 100% Genuine Lawn Cut Pieces")
        await page.click("button:has-text('Save Announcement Text')")
        await page.wait_for_timeout(600)
        print("PASS: Saved new announcement text in Admin.")

        # Revisit Homepage to confirm below-hero ticker reflects new text
        await page.goto("http://localhost:8080/index.html")
        await page.wait_for_timeout(800)
        new_ticker_text = await page.locator(".announcement-bar__ticker").inner_text()
        print("Updated ticker preview:", new_ticker_text[:60].encode('ascii', 'ignore').decode('ascii'))
        assert "Luxury Bedsheets Live" in new_ticker_text or "Mega Sale" in new_ticker_text
        print("PASS: Homepage below-hero ticker updated successfully!")

        await page.screenshot(path="C:/Users/hamza/.gemini/antigravity-ide/brain/6835ee2a-d400-453a-9276-c39c9757f28d/verify_updated_hero_ticker.png")
        print("Saved verify_updated_hero_ticker.png")

        await browser.close()
        print("ALL VERIFICATION CHECKS PASSED PERFECTLY!")

asyncio.run(run())
