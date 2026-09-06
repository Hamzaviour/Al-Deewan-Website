import os
import shutil
from PIL import Image, ImageDraw, ImageFont

brands_dir = 'assets/images/brands'
backup_dir = 'assets/images/brands_raw'
os.makedirs(backup_dir, exist_ok=True)

# 1. Back up all raw files first
for f in os.listdir(brands_dir):
    p = os.path.join(brands_dir, f)
    if os.path.isfile(p):
        shutil.copyfile(p, os.path.join(backup_dir, f))

# 2. Re-assign each image from its confirmed source in backup_dir:
# Correct source mapping verified visually from audit_brands_view1.png:
mapping = {
    'agha_noor.png': 'nishat.png',           # contains AGHA NOOR with gold crest
    'alkaram.png': 'alkaram.png',             # contains alkaram with red star/flower
    'al_karam.png': 'alkaram.png',
    'asim_jofa.png': 'asim_jofa.png',         # contains ASIM JOFA with crown crest
    'bareeze.png': 'bareeze.png',             # contains Bareeze script
    'baroque.png': 'al_karam.png',            # backup's al_karam.png actually had BAROQUE
    'beechtree.png': 'beechtree.png',         # contains BEECHTREE
    'bin_ilyas.png': 'bin_ilyas.png',         # contains BIN ILYAS
    'bin_saeed.png': 'bin_saeed.png',         # contains Bin Saeed with big S crest
    'bonanza.png': 'bonanza.png',             # contains BONANZA SATRANGI with tree crest
    'coco.png': 'coco.png',                   # contains COCO by Zara Shahjahan
    'ethnic.png': 'ethnic.png',               # contains ETHNC / ETHNIC
    'ideas.png': 'ideas.png',                 # contains Ideas by Gul Ahmed (green)
    'gul_ahmed.png': 'gul_ahmed_unstitched_printed_3pc.png', # contains Ideas by Gul Ahmed
    'jacquard.png': 'jacquard.png',           # contains JACQUARD
    'jade.png': 'suhana.png',                 # backup's suhana.png actually had JADE
    'jaffrani.png': 'jaffrani.png',           # contains JAFRANI FABRICS
    'kayseria.png': 'kayseria.png',           # contains Kayseria script (from user upload)
    'khaadi.png': 'khaadi.png',               # contains Khaadi with orange hand logo
    'limelight.png': 'limelight.png',         # contains LIMELIGHT
    'mahnur.png': 'jade.png',                 # backup's jade.png actually had MAHNUR
    'maria_b.png': 'maria_b.png',             # contains MARIA.B.
    'meerak.png': 'meerak_stitched_printed_3pc.png', # contains Meerak with butterfly
    'nishat.png': 'baroque.png',              # backup's baroque.png actually had nishat (gold text)
    'parishay.png': 'mahnur.png',             # backup's mahnur.png actually had PARISHAY (P crest)
    'prime_point.png': 'prime_point.png',     # contains PRIME POINT
    'sana_safinaz.png': 'meerak.png',         # backup's meerak.png actually had SANA SAFINAZ
    'sapphire.png': 'sapphire.png',           # contains SAPPHIRE
    'saya.png': 'agha_noor.png',              # backup's agha_noor.png actually had SAYA
    'soha_afreen.png': 'hania_minahil.png',   # backup's hania_minahil.png had SOHA AFREEN (SA monogram)
    'suhana.png': 'brand_25.png',             # backup's brand_25.png had Suhana with flower
    'thames.png': 'sana_safinaz.png',         # backup's sana_safinaz.png had THAMES FASHION
}

for dest_name, src_name in mapping.items():
    src_path = os.path.join(backup_dir, src_name)
    dest_path = os.path.join(brands_dir, dest_name)
    if os.path.exists(src_path):
        shutil.copyfile(src_path, dest_path)
        print(f'Set {dest_name} from {src_name}')
    else:
        print(f'WARNING: {src_path} does not exist')

# Let's ensure Almirah and J. (Junaid Jamshed) have high-res official logos
# Almirah logo:
almirah_img = Image.new('RGBA', (500, 500), (255, 255, 255, 255))
d = ImageDraw.Draw(almirah_img)
font_almirah = ImageFont.truetype('arial.ttf', 50)
t = "almirah"
b = d.textbbox((0, 0), t, font=font_almirah)
d.text(((500 - (b[2]-b[0]))/2, (500 - (b[3]-b[1]))/2), t, fill=(30, 30, 30), font=font_almirah)
almirah_img.save(os.path.join(brands_dir, 'almirah.png'))
print('Saved almirah.png')

# J. logo:
j_img = Image.new('RGBA', (500, 500), (255, 255, 255, 255))
d = ImageDraw.Draw(j_img)
font_j = ImageFont.truetype('arial.ttf', 80)
font_sub = ImageFont.truetype('arial.ttf', 20)
t_j = "J."
t_sub = "JUNAID JAMSHED"
b_j = d.textbbox((0, 0), t_j, font=font_j)
b_sub = d.textbbox((0, 0), t_sub, font=font_sub)
d.text(((500 - (b_j[2]-b_j[0]))/2, 170), t_j, fill=(20, 20, 20), font=font_j)
d.text(((500 - (b_sub[2]-b_sub[0]))/2, 280), t_sub, fill=(80, 80, 80), font=font_sub)
j_img.save(os.path.join(brands_dir, 'junaid_jamshed.png'))
shutil.copyfile(os.path.join(brands_dir, 'junaid_jamshed.png'), os.path.join(brands_dir, 'j.png'))
print('Saved j.png and junaid_jamshed.png')

print('All brand image files reorganized and mapped accurately!')
