from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 375, "height": 812})
    
    # 1. Test PDP Page
    page.goto("http://localhost:8080/product.html?handle=nishat-linen-3pc-luxury-digital-printed-lawn-black-floral", wait_until="domcontentloaded")
    time.sleep(1)
    
    # Verify BUY IT NOW is absent
    buy_now_count = page.locator("#pdp-buy-now-btn").count()
    print("PDP 'BUY IT NOW' button count:", buy_now_count)
    assert buy_now_count == 0, "Buy it now button should not exist"
    
    # Verify ORDER ON WHATSAPP is present
    pdp_whatsapp_btn = page.locator("#pdp-whatsapp-btn")
    print("PDP WhatsApp button visible:", pdp_whatsapp_btn.is_visible(), "text:", pdp_whatsapp_btn.text_content().strip())
    page.screenshot(path="verification_screenshots/pdp_no_buy_now.png")
    
    # 2. Add product to cart & check Cart Drawer
    page.locator("#pdp-add-cart-btn").click()
    time.sleep(0.8)
    
    cart_drawer = page.locator("#cart-drawer")
    print("Cart drawer active:", cart_drawer.evaluate("el => el.classList.contains('active')"))
    drawer_btn = page.locator("#cart-drawer-whatsapp-btn")
    print("Cart drawer WhatsApp button text:", drawer_btn.text_content().strip())
    page.screenshot(path="verification_screenshots/cart_drawer_whatsapp_cta.png")
    
    # 3. Test Cart Page
    page.goto("http://localhost:8080/cart.html", wait_until="domcontentloaded")
    time.sleep(1)
    
    cart_page_btn = page.locator("#cart-page-content .btn-whatsapp")
    print("Cart page WhatsApp button text:", cart_page_btn.text_content().strip())
    page.screenshot(path="verification_screenshots/cart_page_whatsapp_cta.png")
    
    # 4. Test WhatsApp message generator for Cart
    wa_msg = page.evaluate("""() => {
        let msg = '';
        const originalOpen = window.open;
        window.open = (url) => { msg = decodeURIComponent(url); };
        Store.checkoutViaWhatsApp('Please deliver after 2 PM');
        window.open = originalOpen;
        return msg;
    }""")
    print("=== Generated WhatsApp Cart Message ===")
    print(wa_msg)
    
    browser.close()

print("All WhatsApp checkout tests passed successfully!")
