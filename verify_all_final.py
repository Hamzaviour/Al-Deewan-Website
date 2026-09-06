import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context(viewport={"width": 1400, "height": 900})
        page = await context.new_page()

        # 1. Homepage & Dropdown Menu
        print("1. Testing Homepage & Unstitched -> 1PC Dropdown...")
        await page.goto("http://localhost:8080/index.html")
        await page.wait_for_selector("#top-header-announcement-bar", timeout=5000)
        
        # Check Top Purple Announcement Bar
        top_ann = await page.locator("#top-header-announcement-bar").inner_text()
        print(f"Top Announcement Text: {top_ann.strip()}")
        assert "Genuine Branded Cut Pieces" in top_ann or "Pakistan" in top_ann

        # Check Hero Ticker
        ticker_text = await page.locator(".announcement-bar__ticker").inner_text()
        print(f"Hero Ticker Text: {ticker_text[:60]}...")

        # Hover on Unstitched -> 1PC
        await page.hover("#nav-dropdown-unstitched .header-nav__link")
        await page.wait_for_timeout(300)
        await page.hover("#nav-dropdown-unstitched .nav-dropdown-item:has-text('1PC')")
        await page.wait_for_timeout(300)
        
        # Take screenshot of the Unstitched -> 1PC submenu showing Bedsheets
        await page.screenshot(path="C:/Users/hamza/.gemini/antigravity-ide/brain/6835ee2a-d400-453a-9276-c39c9757f28d/verify_unstitched_1pc_bedsheets.png")
        print("Saved verify_unstitched_1pc_bedsheets.png")

        # 2. Click Bedsheets and verify Collections Page
        print("2. Clicking Bedsheets sublink...")
        await page.click("#nav-dropdown-unstitched a:has-text('Bedsheets')")
        await page.wait_for_load_state("networkidle")
        await page.wait_for_timeout(1000)

        url = page.url
        print(f"Current URL: {url}")
        assert "type=Bedsheet" in url

        title = await page.locator("#collection-title").inner_text()
        print(f"Collection Title: {title}")
        assert "BEDSHEET" in title.upper()

        product_cards = await page.locator(".product-card").all_inner_texts()
        print(f"Bedsheet Products Count: {len(product_cards)}")
        assert len(product_cards) >= 3, f"Expected at least 3 bedsheets, got {len(product_cards)}"

        await page.screenshot(path="C:/Users/hamza/.gemini/antigravity-ide/brain/6835ee2a-d400-453a-9276-c39c9757f28d/verify_bedsheets_collection_page.png")
        print("Saved verify_bedsheets_collection_page.png")

        # 3. Test Order Tracking Clean Redesign
        print("3. Testing Order Tracking Page...")
        await page.goto("http://localhost:8080/order-tracking.html")
        await page.wait_for_selector("#tracking-search-input", timeout=5000)
        await page.screenshot(path="C:/Users/hamza/.gemini/antigravity-ide/brain/6835ee2a-d400-453a-9276-c39c9757f28d/verify_order_tracking_clean.png")
        print("Saved verify_order_tracking_clean.png")

        # Test lookup
        await page.fill("#tracking-search-input", "MP-88392019")
        await page.click("#tracking-search-btn")
        await page.wait_for_timeout(600)
        await page.screenshot(path="C:/Users/hamza/.gemini/antigravity-ide/brain/6835ee2a-d400-453a-9276-c39c9757f28d/verify_order_tracking_result.png")
        print("Saved verify_order_tracking_result.png")

        # 4. Mobile Drawer Check
        print("4. Testing Mobile Drawer...")
        m_page = await context.new_page()
        await m_page.set_viewport_size({"width": 390, "height": 844})
        await m_page.goto("http://localhost:8080/index.html")
        await m_page.click(".mobile-nav-toggle-btn, [aria-label='Toggle navigation menu']")
        await m_page.wait_for_timeout(400)
        
        # Open Unstitched in Mobile Drawer
        unstitched_btn = m_page.locator(".mobile-nav-item:has-text('UNSTITCHED') .mobile-nav-toggle").first
        if await unstitched_btn.is_visible():
            await unstitched_btn.click()
            await m_page.wait_for_timeout(300)
            
            # Open 1PC in Mobile Drawer
            one_pc_btn = m_page.locator(".mobile-nav-item:has-text('1PC') .mobile-nav-toggle").first
            if await one_pc_btn.is_visible():
                await one_pc_btn.click()
                await m_page.wait_for_timeout(300)
        
        await m_page.screenshot(path="C:/Users/hamza/.gemini/antigravity-ide/brain/6835ee2a-d400-453a-9276-c39c9757f28d/verify_mobile_drawer_bedsheets.png")
        print("Saved verify_mobile_drawer_bedsheets.png")

        await browser.close()
        print("ALL VERIFICATIONS COMPLETED SUCCESSFULLY!")

asyncio.run(run())
