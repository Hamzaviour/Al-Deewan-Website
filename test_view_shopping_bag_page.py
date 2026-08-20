from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    
    # 1. Add item on collections page
    page.goto("http://localhost:8080/collections.html")
    page.evaluate("""() => {
        Store.clearCart();
        const p = Store.getProducts()[0]; // Rs. 2990
        Store.addToCart(p);
    }""")
    time.sleep(0.5)
    
    # 2. Click "VIEW SHOPPING BAG" link in drawer
    page.click("a:has-text('VIEW SHOPPING BAG')")
    time.sleep(0.8)
    
    # Verify current URL is cart.html
    print("Navigated URL:", page.url)
    assert "cart.html" in page.url
    
    # 3. Verify content rendered on cart.html
    items_count = page.locator("#cart-page-items .cart-item").count()
    subtotal = page.locator("#cart-page-subtotal").text_content()
    shipping = page.locator("#cart-page-shipping").text_content()
    btn_total = page.locator("#cart-page-btn-total").text_content()
    
    print(f"Cart Items Count: {items_count}")
    print(f"Subtotal: {subtotal}")
    print(f"Shipping: {shipping}")
    print(f"WhatsApp Button Total: {btn_total}")
    
    assert items_count == 1, f"Expected 1 item, got {items_count}"
    assert "2,990" in subtotal
    assert "250" in shipping
    assert "3,240" in btn_total
    
    page.screenshot(path="verification_screenshots/cart_page_working_1_item.png")
    
    # 4. Increase quantity to 2
    page.click("#cart-page-items .qty-btn:has-text('+')")
    time.sleep(0.5)
    
    subtotal2 = page.locator("#cart-page-subtotal").text_content()
    shipping2 = page.locator("#cart-page-shipping").text_content()
    btn_total2 = page.locator("#cart-page-btn-total").text_content()
    
    print(f"Updated (2 items) -> Subtotal: {subtotal2}, Shipping: {shipping2}, Button Total: {btn_total2}")
    assert "5,980" in subtotal2
    assert "FREE" in shipping2
    assert "5,980" in btn_total2
    
    page.screenshot(path="verification_screenshots/cart_page_working_2_items_free_shipping.png")
    
    browser.close()

print("ALL SHOPPING BAG (CART.HTML) TESTS PASSED PERFECTLY!")
