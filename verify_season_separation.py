import asyncio
import os
from playwright.async_api import async_playwright

async def verify_seasons():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={"width": 1400, "height": 900})
        page = await context.new_page()

        # 1. Clear any old custom catalog from localStorage to start fresh
        admin_path = os.path.abspath("admin.html")
        await page.goto(f"file:///{admin_path}")
        await page.evaluate("() => { localStorage.removeItem('aldeewan_custom_catalog'); }")

        # 2. Test Collections Page with ?season=Winter
        collections_path = os.path.abspath("collections.html")
        await page.goto(f"file:///{collections_path}?season=Winter")
        await page.wait_for_timeout(600)

        winter_titles = await page.eval_on_selector_all(
            "#catalog-products-grid .product-card .product-title",
            "elements => elements.map(el => el.textContent.trim())"
        )
        print(f"Collections Winter Products ({len(winter_titles)}):")
        for t in winter_titles:
            print("  ❄️", t)

        # Check that NO summer lawn suit appears in Winter
        has_lawn_in_winter = any("lawn" in t.lower() for t in winter_titles)
        print("Contains Lawn in Winter?", has_lawn_in_winter, "(Must be False)")
        assert not has_lawn_in_winter, "Lawn suits must not appear in Winter!"

        await page.screenshot(path="screenshot_collections_winter_verified.png")

        # 3. Test Collections Page with ?season=Summer
        await page.goto(f"file:///{collections_path}?season=Summer")
        await page.wait_for_timeout(600)

        summer_titles = await page.eval_on_selector_all(
            "#catalog-products-grid .product-card .product-title",
            "elements => elements.map(el => el.textContent.trim())"
        )
        print(f"\nCollections Summer Products ({len(summer_titles)}):")
        for t in summer_titles[:6]:
            print("  ☀️", t)

        # Check that NO velvet/khaddar winter suit appears in Summer
        has_winter_in_summer = any(any(w in t.lower() for w in ["velvet", "khaddar", "pashmina shawl", "karandi"]) for t in summer_titles)
        print("Contains Velvet/Khaddar in Summer?", has_winter_in_summer, "(Must be False)")
        assert not has_winter_in_summer, "Velvet/Khaddar winter suits must not appear in Summer!"

        await page.screenshot(path="screenshot_collections_summer_verified.png")

        # 4. Test Homepage Tabs
        index_path = os.path.abspath("index.html")
        await page.goto(f"file:///{index_path}")
        await page.wait_for_timeout(600)

        # Click Winter
        await page.click(".season-filters .filter-btn:has-text('WINTER')")
        await page.wait_for_timeout(400)
        home_winter_titles = await page.eval_on_selector_all(
            "#season-product-grid .product-card .product-title",
            "elements => elements.map(el => el.textContent.trim())"
        )
        print(f"\nHomepage Winter Tab ({len(home_winter_titles)}):")
        for t in home_winter_titles:
            print("  ❄️", t)
        assert not any("lawn" in t.lower() for t in home_winter_titles), "Homepage Winter must not have Lawn!"

        # Click Summer
        await page.click(".season-filters .filter-btn:has-text('SUMMER')")
        await page.wait_for_timeout(400)
        home_summer_titles = await page.eval_on_selector_all(
            "#season-product-grid .product-card .product-title",
            "elements => elements.map(el => el.textContent.trim())"
        )
        print(f"\nHomepage Summer Tab ({len(home_summer_titles)}):")
        for t in home_summer_titles[:4]:
            print("  ☀️", t)
        assert not any("velvet" in t.lower() or "khaddar" in t.lower() for t in home_summer_titles), "Homepage Summer must not have Velvet/Khaddar!"

        # Click Men
        await page.click(".season-filters .filter-btn:has-text('MEN')")
        await page.wait_for_timeout(400)
        home_men_titles = await page.eval_on_selector_all(
            "#season-product-grid .product-card .product-title",
            "elements => elements.map(el => el.textContent.trim())"
        )
        print(f"\nHomepage Men Tab ({len(home_men_titles)}):")
        for t in home_men_titles:
            print("  👔", t)
        assert len(home_men_titles) == 4, f"Expected 4 men items, got {len(home_men_titles)}"
        assert not any("women" in t.lower() or "silk suit" in t.lower() for t in home_men_titles), "Homepage Men must not have Women suits!"

        await browser.close()
        print("\n🎉 ALL SEASON SEPARATION TESTS PASSED PERFECTLY!")

if __name__ == "__main__":
    asyncio.run(verify_seasons())
