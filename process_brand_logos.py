import os
from PIL import Image, ImageOps
import numpy as np

def process_logo(src_path, dest_circle_path, dest_flat_path, width_ratio=0.88):
    img = Image.open(src_path).convert("RGBA")
    arr = np.array(img)
    
    # Identify non-white/colored pixels (R, G, B not all > 245 or alpha > 50)
    # Check if pixel has color/is not white background
    is_content = (arr[:, :, 0] < 240) | (arr[:, :, 1] < 240) | (arr[:, :, 2] < 240)
    if arr.shape[2] == 4:
        is_content = is_content & (arr[:, :, 3] > 30)
        
    coords = np.argwhere(is_content)
    if len(coords) > 0:
        y_min, x_min = coords.min(axis=0)
        y_max, x_max = coords.max(axis=0)
        pad = 6
        x1 = max(0, x_min - pad)
        y1 = max(0, y_min - pad)
        x2 = min(img.width, x_max + pad + 1)
        y2 = min(img.height, y_max + pad + 1)
        cropped = img.crop((x1, y1, x2, y2))
    else:
        cropped = img
        
    print(f"Processed {src_path} -> Cropped size: {cropped.size}")
    
    # Create 400x400 white circular canvas
    canvas_size = 400
    canvas = Image.new("RGBA", (canvas_size, canvas_size), (255, 255, 255, 255))
    
    target_w = int(canvas_size * width_ratio)
    aspect = cropped.width / cropped.height
    target_h = int(target_w / aspect)
    
    if target_h > int(canvas_size * 0.85):
        target_h = int(canvas_size * 0.85)
        target_w = int(target_h * aspect)
        
    resized = cropped.resize((target_w, target_h), Image.Resampling.LANCZOS)
    
    pos_x = (canvas_size - target_w) // 2
    pos_y = (canvas_size - target_h) // 2
    canvas.paste(resized, (pos_x, pos_y), resized)
    
    canvas.save(dest_circle_path, "PNG")
    cropped.save(dest_flat_path, "PNG")
    print(f"Saved: {dest_circle_path} and {dest_flat_path}")

# 1. Ethnic Logo
ethnic_src = r"C:\Users\hamza\.gemini\antigravity-ide\brain\428edef7-d67e-4c8f-a214-01afb546c76c\.user_uploaded\media_1787248891810.png"
process_logo(
    ethnic_src,
    r"e:\Work\Al-Deewan Website\assets\images\ethnic_circle_logo.png",
    r"e:\Work\Al-Deewan Website\assets\images\ethnic_logo.png",
    width_ratio=0.88
)

# 2. Gul Ahmed Logo
gul_src = r"C:\Users\hamza\.gemini\antigravity-ide\brain\428edef7-d67e-4c8f-a214-01afb546c76c\.user_uploaded\media_1787248933518.png"
process_logo(
    gul_src,
    r"e:\Work\Al-Deewan Website\assets\images\gul_ahmed_circle_logo.png",
    r"e:\Work\Al-Deewan Website\assets\images\gul_ahmed_logo.png",
    width_ratio=0.86
)

print("All brand logos processed successfully!")
