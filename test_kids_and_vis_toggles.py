import os
from playwright.sync_api import sync_playwright

def verify():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1400, "height": 900})
        
        print("1. Testing Homepage...")
        page.goto("http://localhost:8080/index.html")
        page.wait_for_timeout(1000)
        
        # Check Kids nav dropdown
        kids_nav = page.locator("#nav-dropdown-kids")
        print("Kids Nav Dropdown Count:", kids_nav.count())
        assert kids_nav.count() > 0, "Kids nav dropdown not found on homepage"
        
        # Check Homepage Block 3 (Ready to Wear) visibility
        rtw_block = page.locator("#section-block-rtw")
        is_rtw_visible = rtw_block.is_visible()
        print("Is Homepage Block 3 (Ready to Wear) visible?", is_rtw_visible)
        assert not is_rtw_visible, "Homepage Block 3 should be HIDDEN"
        
        # Check Homepage Block 1, 2, and 4 visibility
        binsaeed_block = page.locator("#section-block-binsaeed")
        unstitched_block = page.locator("#section-block-unstitched")
        designer_block = page.locator("#section-block-designer")
        print("Block 1 (Bin Saeed) visible:", binsaeed_block.is_visible())
        print("Block 2 (Unstitched) visible:", unstitched_block.is_visible())
        print("Block 4 (Designer) visible:", designer_block.is_visible())
        assert binsaeed_block.is_visible(), "Block 1 should be visible"
        assert unstitched_block.is_visible(), "Block 2 should be visible"
        assert designer_block.is_visible(), "Block 4 should be visible"
        
        # Hover over Kids nav
        kids_nav.hover()
        page.wait_for_timeout(500)
        page.screenshot(path="C:/Users/hamza/.gemini/antigravity-ide/brain/6835ee2a-d400-453a-9276-c39c9757f28d/test_kids_nav_hover.png")
        print("Saved test_kids_nav_hover.png")

        # Capture homepage state showing Block 1, 2, 4 (with Block 3 hidden)
        page.evaluate("window.scrollTo(0, 1000)")
        page.wait_for_timeout(500)
        page.screenshot(path="C:/Users/hamza/.gemini/antigravity-ide/brain/6835ee2a-d400-453a-9276-c39c9757f28d/test_homepage_hidden_rtw.png")
        print("Saved test_homepage_hidden_rtw.png")
        
        print("\n2. Testing Collections Page for Kids Category...")
        page.goto("http://localhost:8080/collections.html?category=Kids")
        page.wait_for_timeout(1000)
        
        # Verify title and products rendered
        catalog_title = page.locator("#catalog-title").inner_text()
        print("Catalog Title:", catalog_title)
        assert "KIDS" in catalog_title.upper(), f"Expected KIDS in catalog title, got {catalog_title}"
        
        product_cards = page.locator(".product-card")
        prod_count = product_cards.count()
        print("Kids Products Count:", prod_count)
        assert prod_count >= 4, f"Expected at least 4 Kids products, found {prod_count}"
        
        page.screenshot(path="C:/Users/hamza/.gemini/antigravity-ide/brain/6835ee2a-d400-453a-9276-c39c9757f28d/test_kids_collection_grid.png")
        print("Saved test_kids_collection_grid.png")
        
        print("\n3. Testing Admin Portal...")
        page.goto("http://localhost:8080/admin.html")
        page.wait_for_timeout(800)
        
        # Unlock admin dashboard
        page.fill("#admin-passcode-input", "deewan2026")
        page.click(".auth-btn")
        page.wait_for_timeout(1000)
        
        # Open Tab 3 (Featured Collections)
        page.click(".nav-tab-btn[data-tab='headings']")
        page.wait_for_timeout(800)
        
        # Check the visibility toggles exist in Tab 3
        vis_toggles = page.locator(".section-vis-toggle")
        print("Featured Collection Visibility Toggles Count:", vis_toggles.count())
        assert vis_toggles.count() >= 4, "Expected at least 4 visibility toggles"
        
        # Check Block 3 checkbox state
        block3_toggle = page.locator("#sec-vis-2")
        print("Block 3 toggle checked?", block3_toggle.is_checked())
        assert not block3_toggle.is_checked(), "Block 3 should be unchecked (Hidden)"
        
        page.screenshot(path="C:/Users/hamza/.gemini/antigravity-ide/brain/6835ee2a-d400-453a-9276-c39c9757f28d/test_admin_tab3_visibility_toggles.png")
        print("Saved test_admin_tab3_visibility_toggles.png")
        
        # Open Tab 4 (Navigation Menus)
        page.click(".nav-tab-btn[data-tab='navigation']")
        page.wait_for_timeout(800)
        kids_menu_list = page.locator("#kids-menu-list")
        print("Kids Menu List exists?", kids_menu_list.count() > 0)
        assert kids_menu_list.count() > 0, "Kids Menu list manager not found in Tab 4"
        
        page.screenshot(path="C:/Users/hamza/.gemini/antigravity-ide/brain/6835ee2a-d400-453a-9276-c39c9757f28d/test_admin_tab4_kids_nav.png")
        print("Saved test_admin_tab4_kids_nav.png")
        
        # Open Tab 1 (Products) and click Add New Product
        page.click(".nav-tab-btn[data-tab='products']")
        page.wait_for_timeout(800)
        page.click("#tab-products .btn-submit")
        page.wait_for_timeout(800)
        
        # Check category dropdown has Kids / Children
        cat_select = page.locator("#prod-category")
        cat_options = cat_select.locator("option").all_inner_texts()
        print("Product Category Options:", cat_options)
        assert any("Kids" in opt for opt in cat_options), "Kids option missing from Add Product modal"
        
        page.screenshot(path="C:/Users/hamza/.gemini/antigravity-ide/brain/6835ee2a-d400-453a-9276-c39c9757f28d/test_admin_add_product_kids.png")
        print("Saved test_admin_add_product_kids.png")
        
        browser.close()
        print("\nALL VERIFICATIONS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    verify()
