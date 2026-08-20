from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    
    # 1. Login to Admin
    page.goto("http://localhost:8080/admin.html")
    page.fill("#admin-passcode-input", "deewan2026")
    page.click(".auth-btn")
    page.wait_for_selector("#admin-app", state="visible")
    
    # 2. Go to Articles / Products Tab
    page.click("button[data-tab='products']")
    time.sleep(0.5)
    
    # Check rows count
    rows = page.locator("#admin-products-tbody tr")
    count = rows.count()
    print(f"Total articles rendered in table: {count}")
    assert count >= 40, f"Expected at least 40 articles, found {count}"
    
    # Take screenshot of Articles / Products table
    page.screenshot(path="verification_screenshots/admin_products_table_fixed.png")
    
    # Test Search Input
    search_input = page.locator("#admin-search-input")
    search_input.fill("Ethnic")
    time.sleep(0.3)
    filtered_count = page.locator("#admin-products-tbody tr").count()
    print(f"Filtered articles for 'Ethnic': {filtered_count}")
    assert filtered_count > 0, "Search for 'Ethnic' should yield results"
    
    search_input.fill("")
    time.sleep(0.3)
    
    browser.close()

print("ALL ARTICLES & PRODUCTS TABLE TESTS PASSED SUCCESSFULLY!")
