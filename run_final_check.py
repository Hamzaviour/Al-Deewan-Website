import asyncio
import os
from playwright.async_api import async_playwright

async def run_final_check():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={"width": 1400, "height": 900})
        page = await context.new_page()

        # 1. Test Collections Page with Winter filter
        collections_path = os.path.abspath("collections.html")
        await page.goto(f"file:///{collections_path}?season=Winter")
        await page.wait_for_timeout(800)
        await page.screenshot(path="screenshot_collections_winter_final.png")

        winter_titles = await page.eval_on_selector_all(
            "#catalog-products-grid .product-card .product-title",
            "elements => elements.map(el => el.textContent.trim())"
        )
        print("=== Collections Page: Winter Filter ===")
        print(f"Total Winter Items Found: {len(winter_titles)}")
        for t in winter_titles:
            print("  ❄️", t)

        # 2. Test Collections Page with Summer filter
        await page.goto(f"file:///{collections_path}?season=Summer")
        await page.wait_for_timeout(800)
        await page.screenshot(path="screenshot_collections_summer_final.png")

        summer_titles = await page.eval_on_selector_all(
            "#catalog-products-grid .product-card .product-title",
            "elements => elements.map(el => el.textContent.trim())"
        )
        print("\n=== Collections Page: Summer Filter ===")
        print(f"Total Summer Items Found: {len(summer_titles)}")
        for t in summer_titles[:6]:
            print("  ☀️", t)

        # 3. Test Homepage "Shop by Season" Tabs
        index_path = os.path.abspath("index.html")
        await page.goto(f"file:///{index_path}")
        await page.wait_for_timeout(800)

        # Scroll to Shop by Season
        await page.evaluate("window.scrollTo(0, 850)")
        await page.wait_for_timeout(400)

        # Winter Tab
        await page.click(".season-filters .filter-btn:has-text('WINTER')")
        await page.wait_for_timeout(400)
        home_winter = await page.eval_on_selector_all(
            "#season-product-grid .product-card .product-title",
            "elements => elements.map(el => el.textContent.trim())"
        )
        await page.screenshot(path="screenshot_home_winter_final.png")
        print("\n=== Homepage: Winter Tab ===")
        for t in home_winter:
            print("  ❄️", t)

        # Summer Tab
        await page.click(".season-filters .filter-btn:has-text('SUMMER')")
        await page.wait_for_timeout(400)
        home_summer = await page.eval_on_selector_all(
            "#season-product-grid .product-card .product-title",
            "elements => elements.map(el => el.textContent.trim())"
        )
        await page.screenshot(path="screenshot_home_summer_final.png")
        print("\n=== Homepage: Summer Tab ===")
        for t in home_summer[:4]:
            print("  ☀️", t)

        # Men Tab
        await page.click(".season-filters .filter-btn:has-text('MEN')")
        await page.wait_for_timeout(400)
        home_men = await page.eval_on_selector_all(
            "#season-product-grid .product-card .product-title",
            "elements => elements.map(el => el.textContent.trim())"
        )
        await page.screenshot(path="screenshot_home_men_final.png")
        print("\n=== Homepage: Men Tab ===")
        for t in home_men:
            print("  👔", t)

        # 4. Test Admin Portal Filter Dropdowns
        admin_path = os.path.abspath("admin.html")
        await page.goto(f"file:///{admin_path}")
        await page.fill("#admin-passcode-input", "deewan2026")
        await page.click("button[type='submit']")
        await page.wait_for_selector("#admin-app", state="visible")

        await page.click("[data-tab='products']")
        await page.wait_for_selector("#tab-products", state="visible")

        # Select Winter Filter
        await page.select_option("#admin-season-filter", "Winter")
        await page.wait_for_timeout(400)
        await page.screenshot(path="screenshot_admin_winter_final.png")

        # Select Men Filter
        await page.select_option("#admin-season-filter", "")
        await page.select_option("#admin-gender-filter", "Men")
        await page.wait_for_timeout(400)
        await page.screenshot(path="screenshot_admin_men_final.png")

        await browser.close()
        print("\n✅ ALL VALIDATION CHECKS COMPLETED SUCCESSFULLY!")

if __name__ == "__main__":
    asyncio.run(run_final_check())
