import asyncio
from playwright.async_api import async_playwright
import os
import pathlib

async def main():
    file_path = pathlib.Path(os.path.abspath('index.html')).as_uri()
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width': 1440, 'height': 900})
        await page.goto(file_path, wait_until='networkidle')
        
        header = await page.query_selector('.site-header')
        box1 = await header.bounding_box()
        print('Initial Header Position:', box1)
        
        # Scroll down 600px
        await page.evaluate('window.scrollTo(0, 600)')
        await page.wait_for_timeout(300)
        box2 = await header.bounding_box()
        print('Header Position after scroll 600px:', box2)
        
        # Scroll down 1500px
        await page.evaluate('window.scrollTo(0, 1500)')
        await page.wait_for_timeout(300)
        box3 = await header.bounding_box()
        print('Header Position after scroll 1500px:', box3)
        
        assert box2['y'] == 0, f"Expected header y=0 at scroll 600px, got {box2['y']}"
        assert box3['y'] == 0, f"Expected header y=0 at scroll 1500px, got {box3['y']}"
        print('[SUCCESS] Top Navigation Bar remains 100% sticky at y=0 throughout the scroll!')
        
        await page.screenshot(path='verify_sticky_header_scrolled.png')
        print('Saved verify_sticky_header_scrolled.png')
        await browser.close()

asyncio.run(main())
