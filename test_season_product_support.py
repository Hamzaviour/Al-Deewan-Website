import asyncio
import os
from playwright.async_api import async_playwright

async def run_verification():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={"width": 1400, "height": 900})
        page = await context.new_page()

        # 1. Open Admin Page
        admin_path = os.path.abspath("admin.html")
        await page.goto(f"file:///{admin_path}")
        print("Loaded Admin page")

        # Login
        await page.fill("#admin-passcode-input", "deewan2026")
        await page.click("button[type='submit']")
        await page.wait_for_selector("#admin-app", state="visible")
        print("Logged into Admin Portal")

        # Switch to Products Tab
        await page.click("button[data-tab='products'], a[data-tab='products']")
        await page.wait_for_selector("#tab-products", state="visible")
        print("Switched to Products Tab")

        # Screenshot Admin Table with Season Badges
        await page.screenshot(path="screenshot_admin_season_table.png")
        print("Saved screenshot_admin_season_table.png")

        # Open Add Product Modal via direct call
        await page.evaluate("openAddProductModal()")
        await page.wait_for_selector("#product-modal.active", state="visible")
        print("Opened Add Product Modal")

        # Fill Product Details with Winter, Women, Micro Velvet
        await page.fill("#prod-title", "Baroque Luxury Winter Velvet Embroidered Shawl Suit")
        await page.fill("#prod-vendor", "Baroque")
        await page.select_option("#prod-category", "Unstitched")
        await page.select_option("#prod-category-type", "3PC")
        await page.select_option("#prod-season", "Winter")
        await page.select_option("#prod-gender", "Women")
        await page.fill("#prod-fabric", "Micro Velvet & Kashmiri Pashmina Shawl")
        await page.fill("#prod-price", "7850")
        await page.fill("#prod-compare-price", "11500")

        await page.screenshot(path="screenshot_admin_season_modal.png")
        print("Saved screenshot_admin_season_modal.png")

        # Save product via submit button
        await page.click("#product-modal button[type='submit']")
        await page.wait_for_timeout(600)
        print("Saved new Winter suit in Admin Portal")

        # Filter by Winter in Admin Table
        await page.select_option("#admin-season-filter", "Winter")
        await page.wait_for_timeout(400)
        await page.screenshot(path="screenshot_admin_winter_filter.png")
        print("Saved screenshot_admin_winter_filter.png")

        # Filter by Men in Admin Table
        await page.select_option("#admin-season-filter", "")
        await page.select_option("#admin-gender-filter", "Men")
        await page.wait_for_timeout(400)
        await page.screenshot(path="screenshot_admin_men_filter.png")
        print("Saved screenshot_admin_men_filter.png")

        # 2. Open index.html in the same context to verify Shop by Season
        index_path = os.path.abspath("index.html")
        await page.goto(f"file:///{index_path}")
        print("Loaded index.html")

        # Scroll to Shop by Season
        await page.evaluate("window.scrollTo(0, 850)")
        await page.wait_for_timeout(400)

        # Click Winter tab
        await page.click(".season-filters .filter-btn:has-text('WINTER')")
        await page.wait_for_timeout(400)
        await page.screenshot(path="screenshot_homepage_winter_season.png")
        print("Saved screenshot_homepage_winter_season.png")

        # Click Summer tab
        await page.click(".season-filters .filter-btn:has-text('SUMMER')")
        await page.wait_for_timeout(400)
        await page.screenshot(path="screenshot_homepage_summer_season.png")
        print("Saved screenshot_homepage_summer_season.png")

        # Click Men tab
        await page.click(".season-filters .filter-btn:has-text('MEN')")
        await page.wait_for_timeout(400)
        await page.screenshot(path="screenshot_homepage_men_season.png")
        print("Saved screenshot_homepage_men_season.png")

        # 3. Open Collections with Season Filter
        collections_path = os.path.abspath("collections.html")
        await page.goto(f"file:///{collections_path}?season=Winter")
        await page.wait_for_timeout(600)
        await page.screenshot(path="screenshot_collections_winter_url.png")
        print("Saved screenshot_collections_winter_url.png")

        await browser.close()
        print("ALL VERIFICATIONS COMPLETED SUCCESSFULLY!")

if __name__ == "__main__":
    asyncio.run(run_verification())
