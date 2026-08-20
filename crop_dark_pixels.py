from PIL import Image
import numpy as np

src_path = r"C:\Users\hamza\.gemini\antigravity-ide\brain\428edef7-d67e-4c8f-a214-01afb546c76c\.user_uploaded\media_1787248891810.png"
img = Image.open(src_path).convert("RGBA")
arr = np.array(img)

# Find coordinates where pixels are dark (black letters)
# arr[..., :3] is RGB
is_dark = (arr[:, :, 0] < 120) & (arr[:, :, 1] < 120) & (arr[:, :, 2] < 120)

coords = np.argwhere(is_dark)
print("Dark pixels bounding box coords:")
y_min, x_min = coords.min(axis=0)
y_max, x_max = coords.max(axis=0)
print(f"x_min: {x_min}, x_max: {x_max}, y_min: {y_min}, y_max: {y_max}")

# Crop exactly to the letters with a small padding
pad = 4
x1 = max(0, x_min - pad)
y1 = max(0, y_min - pad)
x2 = min(img.width, x_max + pad)
y2 = min(img.height, y_max + pad)

cropped = img.crop((x1, y1, x2, y2))
print("Cropped text size:", cropped.size)

# Create 400x400 white circular canvas
canvas_size = 400
canvas = Image.new("RGBA", (canvas_size, canvas_size), (255, 255, 255, 255))

# Scale to 86% width of canvas
target_w = int(canvas_size * 0.86)
aspect = cropped.width / cropped.height
target_h = int(target_w / aspect)

resized = cropped.resize((target_w, target_h), Image.Resampling.LANCZOS)

pos_x = (canvas_size - target_w) // 2
pos_y = (canvas_size - target_h) // 2
canvas.paste(resized, (pos_x, pos_y), resized)

dest_circle = r"e:\Work\Al-Deewan Website\assets\images\ethnic_circle_logo.png"
dest_flat = r"e:\Work\Al-Deewan Website\assets\images\ethnic_logo.png"

canvas.save(dest_circle, "PNG")
cropped.save(dest_flat, "PNG")

print("Saved perfectly cropped Ethnic logo to:", dest_circle)
