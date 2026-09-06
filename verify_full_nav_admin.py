import asyncio
import os
from playwright.async_api import async_playwright

async def verify_full_nav():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={"width": 1400, "height": 900})
        page = await context.new_page()

        file_path = os.path.abspath("admin.html")
        await page.goto(f"file:///{file_path}")

        # 1. Login
        await page.fill("#admin-passcode-input", "deewan2026")
        await page.click("button[type='submit']")
        await page.wait_for_selector("#admin-app", state="visible")

        # 2. Switch to Navigation Tab
        await page.click("button[data-tab='navigation']")
        await page.wait_for_selector("#tab-navigation", state="visible")

        # 3. Add item to Ready To Wear
        await page.click("button:has-text('+ Add Stitched Link')")
        rtw_items = await page.query_selector_all("#rtw-menu-list .menu-item-row")
        last_rtw = rtw_items[-1]
        await (await last_rtw.query_selector(".menu-label")).fill("Kurtis & Tops")
        await (await last_rtw.query_selector(".menu-url")).fill("collections.html?category=Ready+to+Wear&type=Kurtis")

        # 4. Save RTW Menu
        await page.click("button:has-text('Save Ready To Wear Menu')")
        await page.wait_for_timeout(400)

        # 5. Open Collections page to verify RTW dropdown
        col_path = os.path.abspath("collections.html")
        await page.goto(f"file:///{col_path}")

        rtw_links = await page.eval_on_selector_all(
            ".nav-item-dropdown:nth-of-type(4) .nav-dropdown-menu a, .header-nav a",
            "elements => elements.map(el => el.textContent.trim())"
        )
        print("Collections Page Nav Links:", rtw_links)
        assert any("Kurtis & Tops" in link for link in rtw_links), "Expected 'Kurtis & Tops' in navigation links"
        print("SUCCESS: RTW update dynamically reflected on collections.html!")

        # 6. Check Mobile Nav Drawer
        mobile_drawer_links = await page.eval_on_selector_all(
            "#mobile-nav-drawer a",
            "elements => elements.map(el => el.textContent.trim())"
        )
        print("Mobile Drawer Links count:", len(mobile_drawer_links))
        print("Mobile Drawer RTW Links:", [l for l in mobile_drawer_links if "Kurtis" in l])
        assert any("Kurtis & Tops" in link for link in mobile_drawer_links), "Expected 'Kurtis & Tops' in mobile drawer"
        print("SUCCESS: Mobile Drawer navigation updated and synchronized!")

        await browser.close()

asyncio.run(verify_full_nav())
