import asyncio
import os
from playwright.async_api import async_playwright

async def verify_site():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={'width': 1440, 'height': 900})
        page = await context.new_page()

        workspace_dir = os.path.abspath('.')
        
        # 1. Verify Home Page Navigation & Dropdowns
        home_url = f"file:///{workspace_dir}/index.html"
        print(f"Loading Home Page: {home_url}")
        await page.goto(home_url)
        await page.wait_for_timeout(1000)

        # Hover on UNSTITCHED dropdown
        unstitched_item = page.locator('.nav-item-dropdown:has-text("UNSTITCHED")')
        await unstitched_item.hover()
        await page.wait_for_timeout(500)
        await page.screenshot(path="screenshot_home_unstitched_dropdown.png")
        print("Captured screenshot_home_unstitched_dropdown.png")

        # Hover on 2PC inside UNSTITCHED to reveal submenu
        sub_2pc = page.locator('.nav-dropdown-item:has-text("2PC")').first
        await sub_2pc.hover()
        await page.wait_for_timeout(500)
        await page.screenshot(path="screenshot_home_unstitched_submenu.png")
        print("Captured screenshot_home_unstitched_submenu.png")

        # Hover on READY TO WEAR
        rtw_item = page.locator('.nav-item-dropdown:has-text("READY TO WEAR")')
        await rtw_item.hover()
        await page.wait_for_timeout(500)
        await page.screenshot(path="screenshot_home_rtw_dropdown.png")
        print("Captured screenshot_home_rtw_dropdown.png")

        # 2. Verify Shop By Brand Page
        brand_url = f"file:///{workspace_dir}/shop-by-brand.html"
        print(f"Loading Shop By Brand: {brand_url}")
        await page.goto(brand_url)
        await page.wait_for_timeout(1000)
        await page.screenshot(path="screenshot_shop_by_brand.png", full_page=False)
        print("Captured screenshot_shop_by_brand.png")

        # 3. Verify Collections Page
        col_url = f"file:///{workspace_dir}/collections.html?category=Unstitched&type=2PC&season=Winter"
        print(f"Loading Collections Page: {col_url}")
        await page.goto(col_url)
        await page.wait_for_timeout(1000)
        await page.screenshot(path="screenshot_collections_unstitched.png", full_page=False)
        print("Captured screenshot_collections_unstitched.png")

        # 4. Verify Product Details Page
        prod_url = f"file:///{workspace_dir}/product.html"
        print(f"Loading Product Page: {prod_url}")
        await page.goto(prod_url)
        await page.wait_for_timeout(1000)
        await page.screenshot(path="screenshot_product_page.png", full_page=False)
        print("Captured screenshot_product_page.png")

        # Mobile Viewport Test
        mobile_context = await browser.new_context(viewport={'width': 390, 'height': 844})
        mobile_page = await mobile_context.new_page()
        await mobile_page.goto(home_url)
        await mobile_page.wait_for_timeout(1000)
        
        # Open mobile drawer
        await mobile_page.click('.mobile-menu-toggle')
        await mobile_page.wait_for_timeout(500)
        # Click UNSTITCHED toggle
        toggles = await mobile_page.query_selector_all('.mobile-nav-toggle')
        if toggles:
            await toggles[0].click()
            await mobile_page.wait_for_timeout(300)
        await mobile_page.screenshot(path="screenshot_mobile_drawer.png")
        print("Captured screenshot_mobile_drawer.png")

        await browser.close()
        print("All verification steps completed successfully!")

if __name__ == '__main__':
    asyncio.run(verify_site())
