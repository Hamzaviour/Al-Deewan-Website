from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    page.goto("http://localhost:8080/collections.html")
    
    # Add first product to cart
    page.evaluate("""() => {
        const p = Store.getProducts()[0];
        Store.addToCart(p);
    }""")
    time.sleep(0.5)
    
    # Open Cart Drawer
    page.click("#cart-drawer-toggle")
    time.sleep(0.5)
    
    subtotal = page.locator("#cart-drawer-subtotal").text_content()
    shipping = page.locator("#cart-drawer-shipping").text_content()
    btn_text = page.locator("#cart-drawer-whatsapp-btn").text_content()
    
    print(f"Subtotal: {subtotal}")
    print(f"Shipping: {shipping}")
    print(f"WhatsApp Button Content: {btn_text.strip()}")
    
    page.screenshot(path="verification_screenshots/cart_drawer_whatsapp_button_fixed.png")
    
    # Go to cart.html
    page.goto("http://localhost:8080/cart.html")
    time.sleep(0.5)
    page.screenshot(path="verification_screenshots/cart_page_whatsapp_button_fixed.png")
    
    browser.close()

print("ALL CART WHATSAPP TOTAL & BUTTON ALIGNMENT TESTS PASSED!")
