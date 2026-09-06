import json

brand_list = [
    {"name": "Hania Minahil", "img": "assets/images/brands/hania_minahil.png"},
    {"name": "Soha Afreen", "img": "assets/images/brands/soha_afreen.png"},
    {"name": "Nishat Linen", "img": "assets/images/brands/nishat.png"},
    {"name": "Agha Noor", "img": "assets/images/brands/agha_noor.png"},
    {"name": "Coco", "img": "assets/images/brands/coco.png"},
    {"name": "Mahnur", "img": "assets/images/brands/mahnur.png"},
    {"name": "Sana Safinaz", "img": "assets/images/brands/sana_safinaz.png"},
    {"name": "Saya", "img": "assets/images/brands/saya.png"},
    {"name": "Parishay", "img": "assets/images/brands/parishay.png"},
    {"name": "Al Karam", "img": "assets/images/brands/al_karam.png"},
    {"name": "Sapphire", "img": "assets/images/brands/sapphire_2pc.png"},
    {"name": "Suhana", "img": "assets/images/brands/suhana.png"},
    {"name": "Meerak", "img": "assets/images/brands/meerak_stitched_printed_3pc.png"},
    {"name": "J.", "img": "assets/images/brands/j_stitched_printed_khaddar_3pc.png"},
    {"name": "Gul Ahmed", "img": "assets/images/brands/gul_ahmed_unstitched_printed_3pc.png"},
    {"name": "Prime Point", "img": "assets/images/brands/prime_point.png"},
    {"name": "Rajbari", "img": "assets/images/brands/rajbari.png"},
    {"name": "Bin Saeed", "img": "assets/images/brands/bin_saeed_unstitched_3pc.png"},
    {"name": "Bareeze", "img": "assets/images/brands/bareeze.png"},
    {"name": "Baroque", "img": "assets/images/brands/baroque.png"},
    {"name": "Asim Jofa", "img": "assets/images/brands/asim_jofa.png"},
    {"name": "Khaadi", "img": "assets/images/brands/khaadi.png"},
    {"name": "Wirsa by Zainab", "img": "assets/images/brands/wirsa_by_zainab.png"},
    {"name": "Kayseria", "img": "assets/images/brands/kayseria.png"},
    {"name": "Ideas", "img": "assets/images/brands/ideas.png"},
    {"name": "Bonanza Satrangi", "img": "assets/images/brands/bonanza.png"},
    {"name": "Bin Ilyas", "img": "assets/images/brands/bin_ilyas.png"},
    {"name": "Beechtree", "img": "assets/images/brands/beechtree.png"},
    {"name": "Limelight", "img": "assets/images/brands/limelight.png"},
    {"name": "Ethnic", "img": "assets/images/brands/ethnic.png"},
    {"name": "Maria B", "img": "assets/images/brands/maria_b.png"},
]

cards = []
for b in brand_list:
    brand_param = b['name'].replace(' ', '+')
    card_html = f'''            <a href="collections.html?brand={brand_param}" class="brand-item" title="{b['name']}">
              <img src="{b['img']}" alt="{b['name']}" loading="lazy" />
            </a>'''
    cards.append(card_html)

all_cards_html = '\n'.join(cards) + '\n            <!-- Duplicate Set for Seamless Infinite Ticker Loop -->\n' + '\n'.join(cards)

with open('brand_ticker_markup.html', 'w', encoding='utf-8') as f:
    f.write(all_cards_html)

print('Updated brand ticker markup successfully, total brands:', len(cards))
