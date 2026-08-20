import os
import re

new_email = 'aldewanbrandedcollection@gmail.com'
old_emails = [
    'care@aldeewanbrand.com',
    'aldeewanbrand@gmail.com',
    'support@aldeewanbrand.com',
    'info@aldeewanbrand.com',
    'care@brandedcutpieces.com.pk',
    'brandedcutpieces.info@gmail.com'
]

fb_url = 'https://www.facebook.com/profile.php?id=61592005074273'
insta_url = 'https://www.instagram.com/aldewanbrandedcollection1/'
tiktok_url = 'https://www.tiktok.com/@al.dewan.branded'
yt_url = 'https://www.youtube.com/channel/UCC8WRZg3dNGdAvlRoow4Szw'

for root, dirs, files in os.walk('.'):
    # skip .git and node_modules if any
    if '.git' in root or '.gemini' in root or 'verification_screenshots' in root:
        continue
    for fname in files:
        if not (fname.endswith('.html') or fname.endswith('.js') or fname.endswith('.md')):
            continue
        filepath = os.path.join(root, fname)
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        orig_content = content
        
        # Replace old emails
        for old_e in old_emails:
            content = content.replace(old_e, new_email)
            content = content.replace(f'mailto:{old_e}', f'mailto:{new_email}')
        
        # Replace social links
        # Facebook
        content = re.sub(r'href=["\']https?://(?:www\.)?facebook\.com[^"\']*["\']', f'href="{fb_url}"', content)
        # Instagram
        content = re.sub(r'href=["\']https?://(?:www\.)?instagram\.com[^"\']*["\']', f'href="{insta_url}"', content)
        # TikTok
        content = re.sub(r'href=["\']https?://(?:www\.)?tiktok\.com[^"\']*["\']', f'href="{tiktok_url}"', content)
        # YouTube
        content = re.sub(r'href=["\']https?://(?:www\.)?youtube\.com[^"\']*["\']', f'href="{yt_url}"', content)
        
        if content != orig_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f'Updated {filepath}')

print('All emails and social links updated successfully!')
