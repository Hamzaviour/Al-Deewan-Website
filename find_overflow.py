from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 390, "height": 844})
    
    for page_name in ["index.html", "cart.html", "order-tracking.html", "collections.html"]:
        page.goto(f"http://localhost:8080/{page_name}")
        page.wait_for_load_state("networkidle")
        
        # Check elements that exceed viewport width or have excessive height/margin
        res = page.evaluate("""() => {
            const docWidth = document.documentElement.clientWidth;
            const docHeight = document.documentElement.clientHeight;
            const scrollWidth = document.documentElement.scrollWidth;
            const scrollHeight = document.documentElement.scrollHeight;
            
            // Find wide elements (horizontal overflow)
            const wideElements = [];
            document.querySelectorAll('*').forEach(el => {
                const rect = el.getBoundingClientRect();
                if (rect.right > docWidth + 2) {
                    wideElements.push({
                        tag: el.tagName,
                        id: el.id,
                        className: el.className,
                        right: rect.right,
                        width: rect.width
                    });
                }
            });
            
            // Get bottom-most elements
            const allElements = Array.from(document.querySelectorAll('body *'));
            allElements.sort((a, b) => b.getBoundingClientRect().bottom - a.getBoundingClientRect().bottom);
            const bottomElements = allElements.slice(0, 5).map(el => ({
                tag: el.tagName,
                id: el.id,
                className: el.className,
                bottom: el.getBoundingClientRect().bottom,
                top: el.getBoundingClientRect().top,
                height: el.getBoundingClientRect().height
            }));
            
            return {
                docWidth,
                docHeight,
                scrollWidth,
                scrollHeight,
                wideElements: wideElements.slice(0, 5),
                bottomElements
            };
        }""")
        print(f"\n--- PAGE: {page_name} ---")
        print(f"Viewport Width: {res['docWidth']}, Scroll Width: {res['scrollWidth']}")
        print(f"Viewport Height: {res['docHeight']}, Scroll Height: {res['scrollHeight']}")
        if res['wideElements']:
            print("Wide overflowing elements:", res['wideElements'])
        print("Bottom-most elements:", res['bottomElements'])
    
    browser.close()
