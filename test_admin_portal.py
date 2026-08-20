from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    
    # 1. Test Admin Login Gate
    page.goto("http://localhost:8080/admin.html", wait_until="domcontentloaded")
    time.sleep(1)
    
    # Verify Auth screen is visible
    auth_screen = page.locator("#auth-screen")
    assert auth_screen.is_visible(), "Auth screen should be visible initially"
    page.screenshot(path="verification_screenshots/admin_login_screen.png")
    
    # Enter correct passcode
    page.fill("#admin-passcode-input", "deewan2026")
    page.click("button[type='submit']")
    time.sleep(1)
    
    # Verify Dashboard loaded
    admin_app = page.locator("#admin-app")
    assert admin_app.is_visible(), "Admin dashboard should be visible after login"
    page.screenshot(path="verification_screenshots/admin_dashboard_overview.png")
    
    # 2. Test Tab Navigation & Add Product
    page.click("button[data-tab='products']")
    time.sleep(0.5)
    page.screenshot(path="verification_screenshots/admin_products_table.png")
    
    # Click Add Article on active products tab
    page.click("#tab-products button:has-text('+ Add New Article')")
    time.sleep(0.5)
    
    # Fill product form
    page.fill("#prod-title", "Al-Deewan Royal Crimson 3PC Luxury Embroidered Velvet Suit")
    page.fill("#prod-vendor", "Al-Deewan Couture")
    page.select_option("#prod-category", "Unstitched")
    page.select_option("#prod-category-type", "3PC")
    page.fill("#prod-sku", "ALD-ROYAL-888")
    page.fill("#prod-price", "4890")
    page.fill("#prod-compare-price", "6990")
    page.fill("#prod-description", "Exclusive festive unstitched velvet edition with gold metallic thread work.")
    page.screenshot(path="verification_screenshots/admin_add_product_modal.png")
    
    # Save product
    page.click("#product-modal button[type='submit']")
    time.sleep(1)
    
    # Verify new product in table
    table_text = page.locator("#admin-products-tbody").text_content()
    assert "Al-Deewan Royal Crimson" in table_text, "New article should appear in admin table"
    print("Added new article successfully to Admin table!")
    
    # 3. Test Banners & Announcements update
    page.click("button[data-tab='tickers']")
    time.sleep(0.5)
    page.fill("#announcement-text-input", "🔥 Flash Eid Sale - 50% Off On All Luxury Lawn • Free Delivery 🔥")
    page.click("#tab-tickers button[type='submit']")
    time.sleep(0.8)
    page.screenshot(path="verification_screenshots/admin_tickers_tab.png")
    
    # 4. Verify Live Store Reflection
    # Check Collections Page
    page.goto("http://localhost:8080/collections.html", wait_until="domcontentloaded")
    time.sleep(1)
    collections_text = page.locator("#catalog-products-grid").text_content()
    assert "Al-Deewan Royal Crimson" in collections_text, "New article should appear on live Collections page"
    print("Verified new article on live collections.html!")
    page.screenshot(path="verification_screenshots/live_collections_with_new_article.png")
    
    # Check Homepage Announcement
    page.goto("http://localhost:8080/index.html", wait_until="domcontentloaded")
    time.sleep(1)
    announcement_text = page.locator(".announcement-bar, .announcement-ticker").text_content()
    assert "Flash Eid Sale" in announcement_text, "Announcement should update on live homepage"
    print("Verified live announcement update on index.html!")
    page.screenshot(path="verification_screenshots/live_homepage_updated_announcement.png")
    
    browser.close()

print("All Admin Portal CRUD and Live Store integration tests passed successfully!")
