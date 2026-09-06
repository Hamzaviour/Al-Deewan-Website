import asyncio
from playwright.async_api import async_playwright
import os
import pathlib

async def main():
    file_path = pathlib.Path(os.path.abspath("index.html")).as_uri()
    print("Navigating to:", file_path)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        
        # 1. Desktop Test (1440x900)
        context = await browser.new_context(viewport={"width": 1440, "height": 900})
        page = await context.new_page()
        await page.goto(file_path, wait_until="networkidle")
        await page.wait_for_timeout(1000)

        # Check Hero
        hero = await page.query_selector(".hero-banner-section")
        hero_box = await hero.bounding_box()
        print("Desktop Hero Bounding Box:", hero_box)

        # Check Announcement Bar
        ticker = await page.query_selector(".announcement-bar")
        ticker_box = await ticker.bounding_box()
        print("Desktop Ticker Bounding Box:", ticker_box)

        # Verify Ticker is directly below Hero
        assert abs(ticker_box['y'] - (hero_box['y'] + hero_box['height'])) < 2, f"Ticker should be directly below Hero: Hero bottom = {hero_box['y'] + hero_box['height']}, Ticker top = {ticker_box['y']}"
        print("[SUCCESS] Hero -> Ticker ordering verified (0px gap)")

        # Check Brands Section
        brands_sec = await page.query_selector(".brands-section")
        brands_box = await brands_sec.bounding_box()
        print("Brands Section Bounding Box:", brands_box)

        # Check Brand items count in ticker
        brand_items = await page.query_selector_all(".brands-ticker .brand-item")
        print("Brand items in ticker count:", len(brand_items))
        assert len(brand_items) >= 20, f"Expected at least 20 brand items, got {len(brand_items)}"

        # Check Season Section & Filters
        season_sec = await page.query_selector(".season-section")
        season_box = await season_sec.bounding_box()
        print("Season Section Bounding Box:", season_box)

        # Verify Season Product Grid has items
        season_cards = await page.query_selector_all("#season-product-grid .product-card")
        print("Initial Season Product Cards count:", len(season_cards))
        assert len(season_cards) > 0, "Expected season product cards"

        # Test clicking Summer filter
        summer_btn = await page.query_selector(".season-filters button:nth-of-type(2)")
        await summer_btn.click()
        await page.wait_for_timeout(500)
        summer_cards = await page.query_selector_all("#season-product-grid .product-card")
        print("Summer Filter Cards count:", len(summer_cards))

        # Test clicking Men filter
        men_btn = await page.query_selector(".season-filters button:nth-of-type(3)")
        await men_btn.click()
        await page.wait_for_timeout(500)
        men_cards = await page.query_selector_all("#season-product-grid .product-card")
        print("Men Filter Cards count:", len(men_cards))

        # Reset back to winter
        winter_btn = await page.query_selector(".season-filters button:nth-of-type(1)")
        await winter_btn.click()
        await page.wait_for_timeout(500)

        # Check WhatsApp Float button
        whatsapp = await page.query_selector(".whatsapp-float")
        wa_box = await whatsapp.bounding_box()
        print("WhatsApp Float Bounding Box:", wa_box)
        assert wa_box is not None, "WhatsApp float button not found"

        # Screenshots
        await page.screenshot(path="verify_desktop_full.png", full_page=False)
        
        # Scroll to Brands and Season section to capture close-up
        await brands_sec.scroll_into_view_if_needed()
        await page.wait_for_timeout(500)
        await page.screenshot(path="verify_brands_season_desktop.png")

        # 2. Mobile Test (390x844)
        m_context = await browser.new_context(viewport={"width": 390, "height": 844})
        m_page = await m_context.new_page()
        await m_page.goto(file_path, wait_until="networkidle")
        await m_page.wait_for_timeout(1000)

        await m_page.screenshot(path="verify_mobile_hero.png", full_page=False)

        m_brands = await m_page.query_selector(".brands-section-wrapper")
        await m_brands.scroll_into_view_if_needed()
        await m_page.wait_for_timeout(500)
        await m_page.screenshot(path="verify_mobile_brands_season.png")

        await browser.close()
        print("[SUCCESS] Verification completed successfully! All screenshots saved.")

asyncio.run(main())
