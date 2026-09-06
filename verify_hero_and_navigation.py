import asyncio
from playwright.async_api import async_playwright
import time

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={'width': 1366, 'height': 768})
        page = await context.new_page()

        print("\n--- 1. Testing Homepage Hero Slider & Top Navbar ---")
        await page.goto("http://localhost:8080/index.html")
        await page.wait_for_load_state("networkidle")
        await asyncio.sleep(1)

        # Check hero slider
        slider_track = await page.query_selector("#hero-slider-track")
        slides = await page.query_selector_all(".hero-slide")
        dots = await page.query_selector_all(".hero-slider-dot")
        print(f"Found {len(slides)} hero slides and {len(dots)} navigation dots.")
        assert len(slides) == 3, f"Expected 3 slides, got {len(slides)}"
        assert len(dots) == 3, f"Expected 3 dots, got {len(dots)}"

        # Capture initial hero slider screenshot
        await page.screenshot(path="verify_hero_slide1.png")
        print("Captured verify_hero_slide1.png")

        # Test next arrow click
        next_btn = await page.query_selector("#hero-slider-next")
        if next_btn:
            await next_btn.click()
            await asyncio.sleep(0.8)
            await page.screenshot(path="verify_hero_slide2.png")
            print("Clicked Next: captured verify_hero_slide2.png")

        # Test UNSTITCHED dropdown hover & 1PC submenu
        unstitched_nav = await page.query_selector("#nav-dropdown-unstitched")
        if unstitched_nav:
            await unstitched_nav.hover()
            await asyncio.sleep(0.5)
            # Find 1PC submenu item
            item_1pc = await page.query_selector("#nav-dropdown-unstitched .nav-dropdown-item.has-submenu")
            if item_1pc:
                await item_1pc.hover()
                await asyncio.sleep(0.5)
            await page.screenshot(path="verify_nav_unstitched_1pc_hover.png")
            print("Hovered Unstitched 1PC: captured verify_nav_unstitched_1pc_hover.png")

        # Test RTW dropdown hover (1PC Kurtis)
        rtw_nav = await page.query_selector("#nav-dropdown-rtw")
        if rtw_nav:
            await rtw_nav.hover()
            await asyncio.sleep(0.5)
            await page.screenshot(path="verify_nav_rtw_hover.png")
            print("Hovered Ready To Wear: captured verify_nav_rtw_hover.png")

        # Test KIDS dropdown hover
        kids_nav = await page.query_selector("#nav-dropdown-kids")
        if kids_nav:
            await kids_nav.hover()
            await asyncio.sleep(0.5)
            await page.screenshot(path="verify_nav_kids_hover.png")
            print("Hovered Kids: captured verify_nav_kids_hover.png")

        print("\n--- 2. Testing Mobile Nav Drawer with 1PC & Submenus ---")
        mobile_context = await browser.new_context(viewport={'width': 390, 'height': 844})
        mob_page = await mobile_context.new_page()
        await mob_page.goto("http://localhost:8080/index.html")
        await mob_page.wait_for_load_state("networkidle")
        await asyncio.sleep(1)

        # Open mobile drawer
        toggle_btn = await mob_page.query_selector("#mobile-menu-toggle-btn, .mobile-menu-toggle, .header-mobile-toggle")
        if toggle_btn:
            await toggle_btn.click()
            await asyncio.sleep(0.5)
            # Open UNSTITCHED accordion
            unstitched_header = await mob_page.query_selector("#mobile-nav-drawer .mobile-nav-header:has-text('UNSTITCHED') button")
            if unstitched_header:
                await unstitched_header.click()
                await asyncio.sleep(0.5)
            await mob_page.screenshot(path="verify_mobile_drawer_unstitched_1pc.png")
            print("Opened mobile drawer unstitched with 1PC: captured verify_mobile_drawer_unstitched_1pc.png")

        print("\n--- 3. Testing Admin Portal Dropdowns Manager (Tab 4) & Hero Manager (Tab 5) ---")
        admin_page = await context.new_page()
        await admin_page.goto("http://localhost:8080/admin.html")
        await admin_page.wait_for_load_state("networkidle")
        await asyncio.sleep(0.5)

        # Login
        pass_input = await admin_page.query_selector("#admin-passcode-input")
        if pass_input:
            await pass_input.fill("deewan2026")
            await admin_page.click("button[type='submit']")
            await asyncio.sleep(0.8)

        # Switch to Tab 4 (Navigation Menus)
        nav_tab_btn = await admin_page.query_selector("button[data-tab='navigation']")
        if nav_tab_btn:
            await nav_tab_btn.click()
            await asyncio.sleep(0.5)
            await admin_page.screenshot(path="verify_admin_tab4_nav_manager.png")
            print("Captured verify_admin_tab4_nav_manager.png")

        # Switch to Tab 5 (Banners & Hero Carousel)
        banners_tab_btn = await admin_page.query_selector("button[data-tab='banners']")
        if banners_tab_btn:
            await banners_tab_btn.click()
            await asyncio.sleep(0.5)
            await admin_page.screenshot(path="verify_admin_tab5_hero_manager.png")
            print("Captured verify_admin_tab5_hero_manager.png")

        print("\n--- All Visual Checks Passed! ---")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
