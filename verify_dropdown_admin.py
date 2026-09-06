import asyncio
import os
from playwright.async_api import async_playwright

async def verify_dropdowns():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={"width": 1400, "height": 900})
        page = await context.new_page()

        file_path = os.path.abspath("admin.html")
        await page.goto(f"file:///{file_path}")
        print("Loaded Admin page")

        # 1. Login
        await page.fill("#admin-passcode-input", "deewan2026")
        await page.click("button[type='submit']")
        await page.wait_for_selector("#admin-app", state="visible")
        print("Logged into Admin Portal")

        # 2. Click Navigation Tab
        await page.click("button[data-tab='navigation']")
        await page.wait_for_selector("#tab-navigation", state="visible")
        print("Switched to Navigation Dropdown Menus tab")

        # Check existing items rendered
        u2pc_items = await page.query_selector_all("#unstitched-2pc-menu-list .menu-item-row")
        u3pc_items = await page.query_selector_all("#unstitched-3pc-menu-list .menu-item-row")
        rtw_items = await page.query_selector_all("#rtw-menu-list .menu-item-row")
        main_items = await page.query_selector_all("#main-nav-links-list .menu-item-row")

        print(f"2PC Items: {len(u2pc_items)}, 3PC Items: {len(u3pc_items)}, RTW Items: {len(rtw_items)}, Main Nav Items: {len(main_items)}")

        # 3. Add a new 2PC item
        await page.click("button:has-text('+ Add 2PC Link')")
        u2pc_items_after = await page.query_selector_all("#unstitched-2pc-menu-list .menu-item-row")
        last_row = u2pc_items_after[-1]
        label_input = await last_row.query_selector(".menu-label")
        url_input = await last_row.query_selector(".menu-url")
        await label_input.fill("Spring Festive")
        await url_input.fill("collections.html?category=Unstitched&type=2PC&season=Spring")

        # 4. Save
        await page.click("button:has-text('Save All Navigation Menus')")
        await page.wait_for_timeout(500)
        print("Saved All Navigation Menus from Admin Portal")

        # Take screenshot of admin tab 4
        await page.screenshot(path="screenshot_admin_dropdowns.png")

        # 5. Open index.html in the same browser context to check localStorage sync
        index_path = os.path.abspath("index.html")
        await page.goto(f"file:///{index_path}")
        print("Loaded index.html")

        # Verify Unstitched dropdown submenu has 'Spring Festive'
        submenu_links = await page.eval_on_selector_all(
            ".nav-submenu a",
            "elements => elements.map(el => el.textContent.trim())"
        )
        print("Index Submenu Links:", submenu_links)
        assert "Spring Festive" in submenu_links, f"Expected 'Spring Festive' in {submenu_links}"
        print("SUCCESS: 'Spring Festive' correctly reflected in index.html navbar dropdown!")

        # Take screenshot of index
        await page.screenshot(path="screenshot_index_nav.png")

        await browser.close()

asyncio.run(verify_dropdowns())
