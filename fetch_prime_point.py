import urllib.request
import re
from PIL import Image, ImageDraw, ImageFont
import os

url = 'https://primepointstore.com.pk/'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
saved = False
try:
    with urllib.request.urlopen(req, timeout=10) as resp:
        html = resp.read().decode('utf-8')
    print('Fetched primepointstore length:', len(html))
    logos = re.findall(r'(//[^\s\"\']+(?:logo|Prime|prime)[^\s\"\']*\.(?:png|jpg|webp))', html, re.I)
    print('Logos found:', logos)
    for l in logos:
        if 'cdn/shop' in l or 'logo' in l.lower():
            l_url = 'https:' + l if l.startswith('//') else l
            with urllib.request.urlopen(urllib.request.Request(l_url, headers={'User-Agent': 'Mozilla/5.0'})) as resp2:
                with open('assets/images/brands/prime_point.png', 'wb') as f:
                    f.write(resp2.read())
            print('Saved official Prime Point logo from:', l_url)
            saved = True
            break
except Exception as e:
    print('Error fetching official logo:', e)

if not saved:
    # Create clean square brand tile for Prime Point matching the brand theme
    im = Image.new('RGBA', (500, 500), (255, 255, 255, 255))
    draw = ImageDraw.Draw(im)
    # We can use default or standard serif font
    # Draw sleek minimalist typography
    print('Creating styled typography logo for Prime Point')
    # Try finding Montserrat or Arial or Georgia
    font_large = ImageFont.truetype('arial.ttf', 44)
    font_sub = ImageFont.truetype('arial.ttf', 24)
    
    # Text
    t1 = "PRIME POINT"
    t2 = "C L O T H I N G"
    
    # Calculate bounding boxes
    b1 = draw.textbbox((0, 0), t1, font=font_large)
    w1 = b1[2] - b1[0]
    h1 = b1[3] - b1[1]
    
    b2 = draw.textbbox((0, 0), t2, font=font_sub)
    w2 = b2[2] - b2[0]
    h2 = b2[3] - b2[1]
    
    x1 = (500 - w1) / 2
    y1 = 200
    x2 = (500 - w2) / 2
    y2 = y1 + h1 + 25
    
    draw.text((x1, y1), t1, fill=(20, 20, 20), font=font_large)
    draw.line([(x2 - 10, y2 - 12), (x2 + w2 + 10, y2 - 12)], fill=(180, 180, 180), width=2)
    draw.text((x2, y2), t2, fill=(100, 100, 100), font=font_sub)
    
    im.save('assets/images/brands/prime_point.png')
    print('Created styled prime_point.png')
