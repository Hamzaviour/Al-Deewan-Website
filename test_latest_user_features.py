import asyncio
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from playwright.async_api import async_playwright

async def verify_new_features():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        
        # Test Desktop View
        context = await browser.new_context(viewport={"width": 1280, "height": 900})
        page = await context.new_page()

        print("=== TEST 1: Admin Announcement Bar sync to Homepage Ticker ===")
        await page.goto("http://localhost:8080/admin.html")
        await page.wait_for_timeout(600)
        
        # Login if auth screen visible
        if await page.locator("#auth-screen").is_visible():
            await page.fill("#admin-passcode-input", "deewan2026")
            await page.click("button[type='submit']")
            await page.wait_for_timeout(800)

        await page.click("button[data-tab='tickers']")
        await page.wait_for_timeout(600)

        # Update Announcement Text
        test_announce = "⚡ Flash Summer Sale 2026 • 100% Original Designer Lawn • Instant WhatsApp Booking ⚡"
        await page.fill("#announcement-text-input", test_announce)
        await page.click("button:has-text('Save Announcement Text')")
        await page.wait_for_timeout(800)

        # Verify on Homepage
        await page.goto("http://localhost:8080/index.html")
        await page.wait_for_timeout(800)
        ticker_text = await page.locator(".announcement-bar__ticker").inner_text()
        print(f"Homepage ticker text: {ticker_text[:120]}...")
        assert "Flash Summer Sale 2026" in ticker_text, "Announcement text not synced to homepage ticker"
        assert "Instant WhatsApp Booking" in ticker_text, "Announcement text missing parts"
        print("✓ Live Announcement Bar sync verified!")

        print("\n=== TEST 2: Admin Hero Slides Single Responsive Banner (No Mobile Field/Preview) ===")
        await page.goto("http://localhost:8080/admin.html")
        await page.wait_for_timeout(600)
        await page.click("button[data-tab='banners']")
        await page.wait_for_timeout(600)

        # Verify no mobile url input exists
        mob_url_inputs = await page.locator("input[placeholder*='hero_slide_luxury_mob.png']").count()
        print(f"Mobile separate URL inputs found: {mob_url_inputs}")
        assert mob_url_inputs == 0, "Mobile separate image URL input should be removed"

        # Verify responsive banner preview exists
        banner_prevs = await page.locator("img[id^='slide-desk-prev-']").count()
        print(f"Responsive banner previews found: {banner_prevs}")
        assert banner_prevs > 0, "Responsive banner preview missing"
        await page.screenshot(path="verify_admin_hero_single_banner.png")
        print("✓ Hero banner single responsive input verified!")

        print("\n=== TEST 3: Admin Add Article Modal with 'Bedsheet', '4PC', '5PC' ===")
        await page.goto("http://localhost:8080/admin.html")
        await page.wait_for_timeout(600)
        await page.click("button[data-tab='products']")
        await page.wait_for_timeout(500)
        await page.click("#tab-products button:has-text('+ Add New Article')")
        await page.wait_for_timeout(500)

        bedsheet_opt = await page.locator("#prod-category-type option[value='Bedsheet']").count()
        four_pc_opt = await page.locator("#prod-category-type option[value='4PC']").count()
        five_pc_opt = await page.locator("#prod-category-type option[value='5PC']").count()
        print(f"Suit Type Options - Bedsheet: {bedsheet_opt}, 4PC: {four_pc_opt}, 5PC: {five_pc_opt}")
        assert bedsheet_opt == 1, "Bedsheet option missing in add article modal"
        assert four_pc_opt == 1 and five_pc_opt == 1, "4PC/5PC options missing in add article modal"
        await page.screenshot(path="verify_admin_add_bedsheet_option.png")
        print("✓ Bedsheet suit type option in modal verified!")
        await page.click("#product-modal .modal-close")
        await page.wait_for_timeout(400)

        print("\n=== TEST 4: Navigation Dropdown 4PC/5PC & Custom Submenu Column Management ===")
        await page.click("button[data-tab='navigation']")
        await page.wait_for_timeout(600)

        # Check 4PC and 5PC toggles exist
        toggle_4pc = page.locator("#unstitched-4pc-vis")
        toggle_5pc = page.locator("#unstitched-5pc-vis")
        assert await toggle_4pc.count() == 1, "4PC toggle missing in Unstitched manager"
        assert await toggle_5pc.count() == 1, "5PC toggle missing in Unstitched manager"
        
        # Toggle 4PC to visible
        await toggle_4pc.check()

        # Add a Custom Submenu Column
        print("Adding custom column: 'Shawls & Dupattas'...")
        await page.click("button:has-text('+ Add Custom Submenu Column')")
        await page.wait_for_timeout(400)

        # Edit the last column's title to 'Shawls & Dupattas'
        last_col_input = page.locator("#unstitched-columns-container .col-label-input").last
        await last_col_input.fill("Shawls & Dupattas")
        await page.wait_for_timeout(300)

        await page.click("button:has-text('Save Unstitched')")
        await page.wait_for_timeout(600)
        await page.screenshot(path="verify_admin_unstitched_custom_columns.png")

        # Check Homepage navigation for 4PC and Custom column
        await page.goto("http://localhost:8080/index.html")
        await page.wait_for_timeout(600)
        nav_html = await page.locator("#nav-dropdown-unstitched .nav-dropdown-menu").inner_html()
        print("Unstitched dropdown HTML:")
        print(nav_html)
        assert "4PC" in nav_html, "4PC submenu should appear when toggled visible"
        assert "Shawls &amp; Dupattas" in nav_html or "Shawls & Dupattas" in nav_html, "Custom submenu column should appear on homepage"
        print("✓ 4PC, 5PC, and custom submenu columns verified!")

        print("\n=== TEST 5: Option to Remove/Delete Featured Collection Section ===")
        await page.goto("http://localhost:8080/admin.html")
        await page.wait_for_timeout(600)
        await page.click("button[data-tab='headings']")
        await page.wait_for_timeout(600)

        # Check delete button on sections
        delete_btns = await page.locator("#featured-collections-container .action-btn.delete").count()
        print(f"Delete Section buttons available: {delete_btns}")
        assert delete_btns >= 4, "Every section should have a Delete Section button"

        # Delete Section 3 (Ready to Wear)
        page.on("dialog", lambda dialog: dialog.accept())
        await page.evaluate("""() => {
            deleteFeaturedCollectionCard(2); // Delete index 2
            saveAllFeaturedCollections();
        }""")
        await page.wait_for_timeout(600)

        # Verify on Homepage that deleted section is removed
        await page.goto("http://localhost:8080/index.html")
        await page.wait_for_timeout(600)
        rtw_block_display = await page.locator("#section-block-rtw").evaluate("el => window.getComputedStyle(el).display")
        print(f"RTW Section block display on homepage: {rtw_block_display}")
        assert rtw_block_display == "none", "Deleted section should be hidden/removed on homepage"
        print("✓ Featured Collection removal from admin and homepage verified!")

        print("\n=== TEST 6: Mobile Auto-Responsiveness of Hero Banner ===")
        mobile_context = await browser.new_context(viewport={"width": 375, "height": 667})
        mobile_page = await mobile_context.new_page()
        await mobile_page.goto("http://localhost:8080/index.html")
        await mobile_page.wait_for_timeout(800)
        
        hero_img = mobile_page.locator(".hero-slide-img").first
        box = await hero_img.bounding_box()
        print(f"Mobile Hero Banner size: width={box['width']}px, height={box['height']}px")
        assert box['width'] > 300 and box['height'] > 120, "Mobile hero banner should be properly sized and responsive"
        await mobile_page.screenshot(path="verify_mobile_hero_responsive.png")
        print("verify_mobile_hero_responsive.png saved")

        await browser.close()
        print("\n=======================================================")
        print("🎉 ALL 5 USER FEATURE REQUIREMENTS TESTED & PASSED! 🎉")
        print("=======================================================")

if __name__ == "__main__":
    asyncio.run(verify_new_features())
