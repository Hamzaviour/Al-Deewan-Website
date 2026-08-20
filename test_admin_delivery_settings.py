from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    
    # 1. Login to admin.html
    page.goto("http://localhost:8080/admin.html")
    page.fill("#admin-passcode-input", "deewan2026")
    page.click("button[type='submit']")
    time.sleep(0.5)
    
    # 2. Click Delivery & Shipping Tab
    page.click("button[data-tab='delivery']")
    time.sleep(0.5)
    
    # 3. Update standard delivery to 300 and free delivery threshold to 5000
    page.fill("#standard-shipping-fee", "300")
    page.fill("#free-shipping-threshold", "5000")
    page.click("button:has-text('SAVE DELIVERY SETTINGS')")
    time.sleep(0.5)
    page.screenshot(path="verification_screenshots/admin_delivery_settings_tab.png")
    print("Admin delivery settings saved!")
    
    # 4. Open collections.html and test Cart Drawer
    page.goto("http://localhost:8080/collections.html")
    page.evaluate("""() => {
        Store.clearCart();
        const p = Store.getProducts()[0]; // Rs. 2990
        Store.addToCart(p); // This automatically opens the cart drawer
    }""")
    time.sleep(0.8)
    
    subtotal = page.locator("#cart-drawer-subtotal").text_content()
    shipping = page.locator("#cart-drawer-shipping").text_content()
    btn_total = page.locator("#cart-drawer-btn-total").text_content()
    
    print(f"Cart 1 Item -> Subtotal: {subtotal}, Shipping: {shipping}, Button Total: {btn_total}")
    assert "300" in shipping, f"Expected 300 shipping, got {shipping}"
    assert "3,290" in btn_total, f"Expected 3,290 in button total, got {btn_total}"
    page.screenshot(path="verification_screenshots/cart_drawer_with_admin_delivery_rate.png")
    
    # 5. Increase qty to 2 to exceed 5000 threshold (2 * 2990 = 5980)
    page.click(".qty-btn.plus")
    time.sleep(0.8)
    
    subtotal2 = page.locator("#cart-drawer-subtotal").text_content()
    shipping2 = page.locator("#cart-drawer-shipping").text_content()
    btn_total2 = page.locator("#cart-drawer-btn-total").text_content()
    
    print(f"Cart 2 Items -> Subtotal: {subtotal2}, Shipping: {shipping2}, Button Total: {btn_total2}")
    assert "FREE" in shipping2, f"Expected FREE shipping, got {shipping2}"
    assert "5,980" in btn_total2, f"Expected 5,980 in button total, got {btn_total2}"
    page.screenshot(path="verification_screenshots/cart_drawer_free_shipping_unlocked.png")
    
    # 6. Reset delivery back to standard 250 / 3500 default
    page.goto("http://localhost:8080/admin.html")
    page.click("button[data-tab='delivery']")
    time.sleep(0.3)
    page.fill("#standard-shipping-fee", "250")
    page.fill("#free-shipping-threshold", "3500")
    page.click("button:has-text('SAVE DELIVERY SETTINGS')")
    time.sleep(0.5)
    
    browser.close()

print("ALL ADMIN DELIVERY SETTINGS & DYNAMIC CART TESTS PASSED PERFECTLY!")
