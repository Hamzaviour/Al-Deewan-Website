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
        
        await page.evaluate("""() => {
            const ticker = document.querySelector('.brands-ticker');
            if (ticker) {
                ticker.style.animation = 'none';
            }
        }""")
        
        kayseria = await page.query_selector("a[title='Kayseria']")
        bonanza = await page.query_selector("a[title='Bonanza Satrangi']")
        prime = await page.query_selector("a[title='Prime Point']")
        
        if kayseria:
            await kayseria.screenshot(path='card_kayseria.png')
            print('Saved card_kayseria.png')
        if bonanza:
            await bonanza.screenshot(path='card_bonanza.png')
            print('Saved card_bonanza.png')
        if prime:
            await prime.screenshot(path='card_prime_point.png')
            print('Saved card_prime_point.png')
            
        await browser.close()

asyncio.run(main())
