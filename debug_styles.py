from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    page.goto("http://localhost:8080/collections.html")
    page.check("input[name='category'][value='Menswear']")
    
    # Evaluate styles
    info = page.evaluate("""() => {
        const main = document.querySelector('main.container');
        const layout = document.querySelector('.catalog-layout');
        const sidebar = document.querySelector('.catalog-sidebar');
        const section = document.querySelector('.catalog-layout > section');
        return {
            bodyWidth: document.body.clientWidth,
            main: { width: main.offsetWidth, style: getComputedStyle(main).display },
            layout: { width: layout.offsetWidth, style: getComputedStyle(layout).display, gridCols: getComputedStyle(layout).gridTemplateColumns },
            sidebar: { width: sidebar.offsetWidth, left: sidebar.getBoundingClientRect().left },
            section: { width: section.offsetWidth, left: section.getBoundingClientRect().left }
        };
    }""")
    print("Computed Info:", info)
    browser.close()
