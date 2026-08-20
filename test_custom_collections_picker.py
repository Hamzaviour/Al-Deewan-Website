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
    
    # 2. Go to Featured Collections Tab
    page.click("button[data-tab='headings']")
    time.sleep(0.5)
    
    # Click Add More Featured Collection
    page.click("button:has-text('+ Add More Featured Collection')")
    time.sleep(0.5)
    
    # Fill in Collection 3 details
    cards = page.locator("#featured-collections-container .admin-card")
    last_card = cards.last
    
    title_input = last_card.locator("input[placeholder*='SUMMER 2026']")
    title_input.fill("EID FESTIVE ROYAL VELVET SPECIAL")
    
    sub_input = last_card.locator("input[placeholder*='Freshly dropped']")
    sub_input.fill("Handpicked luxury velvet and embroidered masterpieces")
    
    # Click Choose Articles
    last_card.locator("button:has-text('Choose Articles')").click()
    time.sleep(0.5)
    page.wait_for_selector("#article-picker-modal", state="visible")
    
    # Tick first 3 articles in picker
    checkboxes = page.locator("#picker-articles-grid input[type='checkbox']")
    checkboxes.nth(0).check()
    checkboxes.nth(1).check()
    checkboxes.nth(2).check()
    time.sleep(0.3)
    page.screenshot(path="verification_screenshots/admin_article_picker_modal.png")
    
    # Click Apply Selected Articles
    page.click("button:has-text('Apply Selected Articles')")
    time.sleep(0.5)
    
    # Click Save All Featured Collections
    page.click("button:has-text('Save All Featured Collections')")
    time.sleep(0.8)
    page.screenshot(path="verification_screenshots/admin_featured_collections_saved.png")
    print("Successfully configured new collection with ticked articles in Admin!")
    
    # 3. Verify on Homepage
    page.goto("http://localhost:8080/index.html", wait_until="domcontentloaded")
    time.sleep(1)
    
    homepage_content = page.content()
    assert "EID FESTIVE ROYAL VELVET SPECIAL" in homepage_content, "New collection section should render on homepage"
    print("Verified new custom collection on live index.html!")
    
    page.screenshot(path="verification_screenshots/live_homepage_with_3rd_featured_collection.png")
    browser.close()

print("ALL CUSTOM FEATURED COLLECTIONS & ARTICLE PICKER TESTS PASSED!")
