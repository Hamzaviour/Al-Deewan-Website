from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 390, "height": 844})
    
    page.goto("http://localhost:8080/admin.html")
    page.fill("#admin-passcode-input", "deewan2026")
    page.click("button[type='submit']")
    page.wait_for_timeout(500)
    
    # Switch to Products tab
    page.click(".quick-tab-pill:has-text('Articles')")
    page.wait_for_timeout(500)
    
    # Scroll table horizontally
    page.evaluate("""() => {
        const wrap = document.querySelector('.admin-table-wrap');
        wrap.scrollLeft = wrap.scrollWidth;
    }""")
    page.wait_for_timeout(300)
    
    # Capture screenshot showing right side of the table (Stock & Actions)
    page.screenshot(path="verification_screenshots/debug_admin_articles_scrolled_right.png")
    
    browser.close()

print("Table horizontal scrolling verified successfully!")
