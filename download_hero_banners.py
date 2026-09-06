import os
import urllib.request

os.makedirs('assets/images/banners', exist_ok=True)

banners = [
    {
        'name': 'hero_slide_luxury.png',
        'url': 'https://brandedcutpieces.com.pk/cdn/shop/files/Luxury_Web_Banner.png?v=1772272143',
        'title': 'Luxury Lawn Collection 2026',
        'link': 'collections.html?category=Unstitched'
    },
    {
        'name': 'hero_slide_winter.png',
        'url': 'https://brandedcutpieces.com.pk/cdn/shop/files/Winter_Web_Banner_BCP.png?v=1788341510',
        'title': 'Winter Khaddar & Karandi Shawl Collection',
        'link': 'collections.html?season=Winter'
    },
    {
        'name': 'hero_slide_summer.png',
        'url': 'https://brandedcutpieces.com.pk/cdn/shop/files/Summer_Web_Banner.png?v=1772272128',
        'title': 'Summer Lawn 2026 Launch',
        'link': 'collections.html?season=Summer'
    },
    {
        'name': 'hero_slide_luxury_mob.png',
        'url': 'https://brandedcutpieces.com.pk/cdn/shop/files/Luxury_Mobile_Banner.png?v=1772272143',
        'title': 'Luxury Mobile Banner',
        'link': 'collections.html?category=Unstitched'
    },
    {
        'name': 'hero_slide_winter_mob.png',
        'url': 'https://brandedcutpieces.com.pk/cdn/shop/files/Winter_BCP_Mobile.png?v=1788435038',
        'title': 'Winter Mobile Banner',
        'link': 'collections.html?season=Winter'
    },
    {
        'name': 'hero_slide_summer_mob.png',
        'url': 'https://brandedcutpieces.com.pk/cdn/shop/files/Summer_Mobile_Banner.png?v=1772272127',
        'title': 'Summer Mobile Banner',
        'link': 'collections.html?season=Summer'
    }
]

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

for b in banners:
    path = os.path.join('assets/images/banners', b['name'])
    try:
        req = urllib.request.Request(b['url'], headers=headers)
        with urllib.request.urlopen(req) as resp, open(path, 'wb') as out:
            out.write(resp.read())
        size = os.path.getsize(path)
        print(f"Downloaded {b['name']} ({size} bytes)")
    except Exception as e:
        print(f"Failed to download {b['name']}: {e}")
