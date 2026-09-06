import asyncio
import os
from playwright.async_api import async_playwright

async def verify_multi_image_support():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={"width": 1400, "height": 900})
        page = await context.new_page()

        admin_path = os.path.abspath("admin.html")
        await page.goto(f"file:///{admin_path}")

        # 1. Login
        await page.fill("#admin-passcode-input", "deewan2026")
        await page.click("button[type='submit']")
        await page.wait_for_selector("#admin-app", state="visible")
        print("Logged into Admin")

        # 2. Open Add Product Modal
        await page.click("button:has-text('+ Add New Article')")
        await page.wait_for_selector("#product-modal.active", state="visible")
        print("Opened Add Article Modal")

        # 3. Add multiple images via URL input
        img1 = "assets/images/catalog/nishat-3pc-42206126-r-main.jpg"
        img2 = "assets/images/catalog/beechtree-3pc-5590-orange-1.jpg"
        img3 = "assets/images/catalog/beechtree-3pc-5590-orange-2.jpg"

        url_input = page.locator("#prod-image-url-input")
        add_btn = page.locator("button:has-text('+ Add URL')")

        await url_input.fill(img2)
        await add_btn.click()

        await url_input.fill(img3)
        await add_btn.click()

        # Check gallery cards count (default 1 + 2 added = 3)
        cards = await page.query_selector_all(".modal-gallery-card")
        print(f"Modal Gallery Cards Count: {len(cards)}")
        assert len(cards) == 3, f"Expected 3 cards, got {len(cards)}"

        # 4. Make img2 (index 1) primary
        make_main_btns = await page.query_selector_all(".btn-make-primary")
        if make_main_btns:
            await make_main_btns[0].click()
            print("Clicked make primary on 2nd image")

        # 5. Fill product details
        test_title = "Test Multi-Image Luxury Lawn 3PC"
        await page.fill("#prod-title", test_title)
        await page.fill("#prod-vendor", "Al-Deewan Exclusive")
        await page.fill("#prod-price", "3850")
        await page.fill("#prod-compare-price", "5500")

        # Save product
        await page.click("button:has-text('Save Article to Catalog')")
        await page.wait_for_timeout(500)
        print("Saved multi-image product")

        # Take screenshot of Admin Products Table
        await page.screenshot(path="screenshot_admin_multi_image.png")

        # 6. Verify in Store
        new_prod = await page.evaluate(f"""() => {{
            return Store.getProducts().find(p => p.title === '{test_title}');
        }}""")

        print("Saved Product in Store:", {
            "title": new_prod["title"],
            "handle": new_prod["handle"],
            "images_count": len(new_prod.get("images", [])),
            "featured_image": new_prod.get("featured_image"),
            "hover_image": new_prod.get("hover_image")
        })

        assert len(new_prod["images"]) == 3, f"Expected 3 images, got {len(new_prod['images'])}"
        assert new_prod["featured_image"] == img2, f"Expected featured_image to be {img2}"
        assert new_prod["hover_image"] == img1, f"Expected hover_image to be {img1}"

        # 7. Open Product Detail Page for this item
        pdp_path = os.path.abspath(f"product.html")
        await page.goto(f"file:///{pdp_path}?handle={new_prod['handle']}")
        await page.wait_for_selector("#pdp-images-stack", state="visible")

        pdp_images = await page.eval_on_selector_all(
            "#pdp-images-stack img",
            "imgs => imgs.map(i => i.getAttribute('src'))"
        )
        print(f"Product Page Rendered {len(pdp_images)} Gallery Images:", pdp_images)
        assert len(pdp_images) == 3, f"Expected 3 gallery images on product page, got {len(pdp_images)}"

        # Take screenshot of PDP gallery
        await page.screenshot(path="screenshot_pdp_multi_image.png")
        print("ALL TESTS PASSED: Multi-image feature fully verified!")

        await browser.close()

asyncio.run(verify_multi_image_support())
