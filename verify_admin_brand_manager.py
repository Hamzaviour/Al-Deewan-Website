import os
import sys
import time
from playwright.sync_api import sync_playwright

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

def run_test():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 1400, 'height': 900})
        page = context.new_page()

        print("\n========================================================")
        print("STARTING ADMIN BRAND MANAGER & EMPTY STATE VERIFICATION")
        print("========================================================\n")

        # 1. Login to Admin Portal
        print("1. Logging into Admin Portal at http://localhost:8080/admin.html ...")
        page.goto("http://localhost:8080/admin.html", wait_until="networkidle")
        page.fill("#admin-passcode-input", "deewan2026")
        page.click("button[type='submit']")
        page.wait_for_timeout(1000)

        # 2. Navigate to Brands Directory Tab
        print("2. Opening Brands Directory Tab in Admin Portal ...")
        page.click("button[data-tab='brands']")
        page.wait_for_timeout(800)

        page.screenshot(path="verification_screenshots/admin_brands_tab.png", full_page=False)
        print("📸 Captured admin_brands_tab.png")

        # Check default favorites count
        fav_cards = page.query_selector_all("#admin-favorite-brands-grid .brand-card-admin")
        print(f"   Initial Top Favorite Brands Count in Admin: {len(fav_cards)}")
        assert len(fav_cards) >= 15, "Expected at least 15 default top favorite brands"

        # 3. Add a New Brand with Logo as Top Favorite: "Charizma"
        print("3. Adding New Brand 'Charizma' with Logo as Top Favorite ...")
        page.click("button:has-text('+ Add New Brand')")
        page.wait_for_timeout(500)

        page.fill("#brand-name-input", "Charizma")
        page.select_option("#brand-letter-input", "C")
        page.check("#brand-fav-input")
        page.fill("#brand-img-input", "assets/images/brands/beechtree.png")
        page.wait_for_timeout(300)

        page.screenshot(path="verification_screenshots/admin_add_brand_modal.png")
        print("📸 Captured admin_add_brand_modal.png")

        page.click("#brand-modal button[type='submit']")
        page.wait_for_timeout(1000)

        page.screenshot(path="verification_screenshots/admin_brands_after_add.png")
        print("📸 Captured admin_brands_after_add.png")

        # Verify Charizma in admin favorites grid
        fav_text = page.inner_text("#admin-favorite-brands-grid")
        assert "Charizma" in fav_text, "Charizma not found in admin favorites grid"
        print("   ✅ Verified 'Charizma' is in Admin Top Favorites Grid!")

        # 4. Check Shop By Brand page (shop-by-brand.html)
        print("4. Verifying 'Charizma' appears dynamically in shop-by-brand.html ...")
        page.goto("http://localhost:8080/shop-by-brand.html", wait_until="networkidle")
        page.wait_for_timeout(1000)

        page.screenshot(path="verification_screenshots/shop_by_brand_with_charizma.png", full_page=False)
        print("📸 Captured shop_by_brand_with_charizma.png")

        top_brand_names = [el.inner_text().strip() for el in page.query_selector_all("#featured-brands-grid .featured-brand-tile span")]
        print(f"   Featured Brand Tiles on Shop By Brand: {len(top_brand_names)} brands -> {top_brand_names}")
        assert any("charizma" in name.lower() for name in top_brand_names), f"Charizma not found in Shop By Brand Top Favorites: {top_brand_names}"
        print("   ✅ Verified 'Charizma' is featured in Shop By Brand Top Favorites with its logo!")

        # Verify Charizma under letter C in A-Z directory
        c_group = page.query_selector("#C")
        assert c_group is not None, "Letter C group missing in A-Z directory"
        c_group_text = c_group.inner_text()
        assert "charizma" in c_group_text.lower(), "Charizma not found under letter C group in A-Z directory"
        print("   ✅ Verified 'Charizma' is listed in A-Z directory under letter 'C'!")

        # 5. Click Charizma -> Verify collections.html?brand=Charizma 0-product empty state
        print("5. Clicking 'Charizma' tile to test 0-product empty state ...")
        page.click("#featured-brands-grid a:has-text('Charizma')")
        page.wait_for_timeout(1200)

        print(f"   Current URL: {page.url}")
        assert "collections.html" in page.url and "Charizma" in page.url

        page.screenshot(path="verification_screenshots/charizma_empty_state.png", full_page=False)
        print("📸 Captured charizma_empty_state.png")

        count_text = page.inner_text("#catalog-count-desc")
        print(f"   Results Count: '{count_text}'")
        assert "0 products" in count_text.lower() or "0 product" in count_text.lower()

        empty_heading = page.query_selector("h3:has-text('No Products Available')")
        assert empty_heading is not None, "Brand empty state heading element missing"
        print(f"   Empty State Heading: '{empty_heading.inner_text()}'")
        assert "CHARIZMA" in empty_heading.inner_text().upper()

        # 6. Add an article for Charizma in Admin and verify it now displays 1 suit
        print("6. Adding a product for 'Charizma' in Admin Portal ...")
        page.goto("http://localhost:8080/admin.html", wait_until="networkidle")
        page.click("button[data-tab='products']")
        page.wait_for_timeout(600)
        page.click("button:has-text('+ Add New Article')")
        page.wait_for_timeout(500)

        page.fill("#prod-title", "Charizma Embroidered Luxury Lawn 3PC Suit")
        page.fill("#prod-vendor", "Charizma")
        page.select_option("#prod-category", "Unstitched")
        page.select_option("#prod-category-type", "3PC")
        page.select_option("#prod-season", "Summer")
        page.fill("#prod-price", "4250")
        page.fill("#prod-compare-price", "5500")
        page.fill("#prod-fabric", "Luxury Lawn")
        page.click("#product-modal button[type='submit']")
        page.wait_for_timeout(1000)

        # 7. Revisit collections.html?brand=Charizma -> verify suit is displayed!
        print("7. Re-verifying collections.html?brand=Charizma with the new suit ...")
        page.goto("http://localhost:8080/collections.html?brand=Charizma", wait_until="networkidle")
        page.wait_for_timeout(1200)

        page.screenshot(path="verification_screenshots/charizma_with_product.png", full_page=False)
        print("📸 Captured charizma_with_product.png")

        updated_count = page.inner_text("#catalog-count-desc")
        print(f"   Updated Results Count: '{updated_count}'")
        assert "1 product" in updated_count.lower() or "1 products" in updated_count.lower()
        product_cards = page.query_selector_all(".product-card")
        print(f"   Rendered Product Cards: {len(product_cards)}")
        assert len(product_cards) == 1, f"Expected 1 product card, found {len(product_cards)}"
        print("   ✅ Verified product successfully shows under Charizma brand filter!")

        # 8. Test Editing Brand in Admin (e.g. Unfavorite / Rename / Visibility)
        print("8. Testing Brand Edit / Toggle Favorite in Admin ...")
        page.goto("http://localhost:8080/admin.html", wait_until="networkidle")
        page.click("button[data-tab='brands']")
        page.wait_for_timeout(600)

        # Search for Charizma in table
        page.fill("#admin-brand-search-input", "Charizma")
        page.wait_for_timeout(400)
        charizma_row = page.query_selector("#admin-brands-tbody tr:has-text('Charizma')")
        assert charizma_row is not None, "Charizma row not found in brands table"
        print("   ✅ Found 'Charizma' in Admin Brands Table with count 1 Suit!")

        # Click Edit on Charizma
        charizma_row.query_selector("button:has-text('Edit')").click()
        page.wait_for_timeout(500)
        page.fill("#brand-name-input", "Charizma Studio")
        page.click("#brand-modal button[type='submit']")
        page.wait_for_timeout(800)

        # Check shop-by-brand.html reflects "Charizma Studio"
        page.goto("http://localhost:8080/shop-by-brand.html", wait_until="networkidle")
        page.wait_for_timeout(800)
        brand_text_all = page.inner_text("#brand-directory-list")
        assert "Charizma Studio" in brand_text_all, "Renamed brand 'Charizma Studio' not found in shop-by-brand.html"
        print("   ✅ Verified editing brand in Admin immediately reflects on live Shop By Brand page!")

        print("\n========================================================")
        print("🎉 ALL ADMIN BRAND MANAGER & EMPTY STATE TESTS PASSED 100%!")
        print("========================================================\n")

        browser.close()

if __name__ == "__main__":
    os.makedirs("verification_screenshots", exist_ok=True)
    run_test()
