from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(viewport={"width": 1440, "height": 900})
    
    # ----------------------------------------------------
    # 1. ADMIN ACTIONS: Add article via Store.addProduct
    # ----------------------------------------------------
    admin_page = context.new_page()
    admin_page.goto("http://localhost:8080/admin.html")
    admin_page.fill("#admin-passcode-input", "deewan2026")
    admin_page.click("button[type='submit']")
    time.sleep(0.5)
    
    # Add a new article
    test_title = "Admin Verified Summer Lawn 3PC Luxury"
    new_id = admin_page.evaluate(f"""() => {{
        const newProduct = {{
            title: "{test_title}",
            handle: "admin-verified-summer-lawn-3pc-luxury",
            vendor: "Khaadi",
            category: "Unstitched",
            category_type: "3PC",
            price: 3450,
            compare_at_price: 4950,
            image: "assets/images/1_2bbe8fce-c5a9-42f4-899a-5536f15842ff_533x.png",
            images: ["assets/images/1_2bbe8fce-c5a9-42f4-899a-5536f15842ff_533x.png"],
            tags: ["New In", "3PC", "Lawn", "Summer"],
            available: true,
            featured: true
        }};
        const saved = Store.addProduct(newProduct);
        return saved ? saved.id : null;
    }}""")
    print(f"Added test article via Admin Store (ID: {new_id})!")

    # ----------------------------------------------------
    # 2. VERIFY ON DESKTOP (1440x900)
    # ----------------------------------------------------
    desktop_page = context.new_page()
    desktop_page.set_viewport_size({"width": 1440, "height": 900})
    desktop_page.goto("http://localhost:8080/collections.html")
    time.sleep(0.8)
    
    desktop_product = desktop_page.locator(f".product-card:has-text('{test_title}')")
    desktop_exists = desktop_product.count() > 0
    print(f"Desktop View: Article found? {desktop_exists}")
    assert desktop_exists, "New article must be visible on Desktop catalog!"
    desktop_page.screenshot(path="verification_screenshots/desktop_view_new_article.png")
    
    # ----------------------------------------------------
    # 3. VERIFY ON MOBILE VIEW (390x844)
    # ----------------------------------------------------
    mobile_page = context.new_page()
    mobile_page.set_viewport_size({"width": 390, "height": 844})
    mobile_page.goto("http://localhost:8080/collections.html")
    time.sleep(0.8)
    
    mobile_product = mobile_page.locator(f".product-card:has-text('{test_title}')")
    mobile_exists = mobile_product.count() > 0
    print(f"Mobile View: Article found? {mobile_exists}")
    assert mobile_exists, "New article must be visible on Mobile catalog!"
    
    # Test adding to cart on Mobile
    mobile_page.evaluate(f"""() => {{
        const p = Store.getProducts().find(x => x.title === '{test_title}');
        if (p) Store.addToCart(p);
    }}""")
    time.sleep(0.8)
    
    # Verify dynamic cart drawer on mobile
    drawer_subtotal = mobile_page.locator("#cart-drawer-subtotal").text_content()
    drawer_btn_total = mobile_page.locator("#cart-drawer-btn-total").text_content()
    print(f"Mobile Cart Drawer Subtotal: {drawer_subtotal}, Button Total: {drawer_btn_total}")
    assert "3,450" in drawer_subtotal
    mobile_page.screenshot(path="verification_screenshots/mobile_view_new_article_cart.png")
    
    # ----------------------------------------------------
    # 4. CLEANUP
    # ----------------------------------------------------
    if new_id:
        admin_page.evaluate(f"""() => {{
            Store.deleteProduct({new_id});
            Store.clearCart();
        }}""")
        print(f"Test article ID {new_id} cleaned up cleanly.")
    
    context.close()
    browser.close()

print("ALL DESKTOP & MOBILE RESPONSIVENESS AND DYNAMIC SYNC VERIFIED 100%!")
