brand_items = [
    {"name": "Kayseria", "img": "assets/images/brands/kayseria.png", "param": "Kayseria"},
    {"name": "Agha Noor", "img": "assets/images/brands/agha_noor.png", "param": "Agha+Noor"},
    {"name": "Al Karam", "img": "assets/images/brands/al_karam.png", "param": "Al+Karam"},
    {"name": "Asim Jofa", "img": "assets/images/brands/asim_jofa.png", "param": "Asim+Jofa"},
    {"name": "Bareeze", "img": "assets/images/brands/bareeze.png", "param": "Bareeze"},
    {"name": "Baroque", "img": "assets/images/brands/baroque.png", "param": "Baroque"},
    {"name": "Beechtree", "img": "assets/images/brands/beechtree.png", "param": "Beechtree"},
    {"name": "Bin Ilyas", "img": "assets/images/brands/bin_ilyas.png", "param": "Bin+Ilyas"},
    {"name": "Bin Saeed", "img": "assets/images/brands/bin_saeed.png", "param": "Bin+Saeed"},
    {"name": "Bonanza Satrangi", "img": "assets/images/brands/bonanza.png", "param": "Bonanza+Satrangi"},
    {"name": "Coco", "img": "assets/images/brands/coco.png", "param": "Coco"},
    {"name": "Ethnic", "img": "assets/images/brands/ethnic.png", "param": "Ethnic"},
    {"name": "Ideas by Gul Ahmed", "img": "assets/images/brands/ideas.png", "param": "Ideas"},
    {"name": "J.", "img": "assets/images/brands/j.png", "param": "Junaid+Jamshed"},
    {"name": "Jacquard", "img": "assets/images/brands/jacquard.png", "param": "Jacquard"},
    {"name": "Jade", "img": "assets/images/brands/jade.png", "param": "Jade"},
    {"name": "Jafrani Fabrics", "img": "assets/images/brands/jaffrani.png", "param": "Jafrani"},
    {"name": "Khaadi", "img": "assets/images/brands/khaadi.png", "param": "Khaadi"},
    {"name": "Limelight", "img": "assets/images/brands/limelight.png", "param": "Limelight"},
    {"name": "Mahnur", "img": "assets/images/brands/mahnur.png", "param": "Mahnur"},
    {"name": "Maria B", "img": "assets/images/brands/maria_b.png", "param": "Maria+B"},
    {"name": "Meerak", "img": "assets/images/brands/meerak.png", "param": "Meerak"},
    {"name": "Nishat Linen", "img": "assets/images/brands/nishat.png", "param": "Nishat"},
    {"name": "Parishay", "img": "assets/images/brands/parishay.png", "param": "Parishay"},
    {"name": "Prime Point", "img": "assets/images/brands/prime_point.png", "param": "Prime+Point"},
    {"name": "Sana Safinaz", "img": "assets/images/brands/sana_safinaz.png", "param": "Sana+Safinaz"},
    {"name": "Sapphire", "img": "assets/images/brands/sapphire.png", "param": "Sapphire"},
    {"name": "Saya", "img": "assets/images/brands/saya.png", "param": "Saya"},
    {"name": "Soha Afreen", "img": "assets/images/brands/soha_afreen.png", "param": "Soha+Afreen"},
    {"name": "Suhana", "img": "assets/images/brands/suhana.png", "param": "Suhana"},
    {"name": "Thames", "img": "assets/images/brands/thames.png", "param": "Thames"},
]

cards = []
for b in brand_items:
    card = f'''            <a href="collections.html?brand={b['param']}" class="brand-item" title="{b['name']}">
              <img src="{b['img']}" alt="{b['name']}" loading="lazy" />
            </a>'''
    cards.append(card)

# Set 1 and Set 2 (for infinite loop)
full_ticker_html = '\n'.join(cards) + '\n            <!-- Duplicate Set for Seamless Infinite Ticker Loop -->\n' + '\n'.join(cards)

# Read index.html and replace brands-ticker content
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

import re
pattern = r'(<div class="brands-ticker">)(.*?)(</div>\s*</div>\s*</div>\s*</div>\s*</div>\s*<!-- 2\. Shop By Season)'
replacement = r'\1\n' + full_ticker_html + r'\n          \3'

new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print(f'Successfully updated index.html with {len(brand_items)} verified brand ticker cards!')
