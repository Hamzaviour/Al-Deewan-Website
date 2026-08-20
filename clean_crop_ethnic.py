from PIL import Image
import numpy as np

src_path = r"C:\Users\hamza\.gemini\antigravity-ide\brain\428edef7-d67e-4c8f-a214-01afb546c76c\.user_uploaded\media_1787248891810.png"
img = Image.open(src_path).convert("RGBA")
arr = np.array(img)

# Dark pixels
is_dark = (arr[:, :, 0] < 120) & (arr[:, :, 1] < 120) & (arr[:, :, 2] < 120)

col_sums = is_dark.sum(axis=0)
# Find columns with significant dark pixels (> 2 pixels high)
valid_cols = np.where(col_sums > 3)[0]
print("Valid cols range:", valid_cols.min(), valid_cols.max())

# Row range
row_sums = is_dark.sum(axis=1)
valid_rows = np.where(row_sums > 3)[0]
print("Valid rows range:", valid_rows.min(), valid_rows.max())

# Crop only the actual letters
x1 = valid_cols.min()
x2 = valid_cols.max() + 1
y1 = valid_rows.min()
y2 = valid_rows.max() + 1

cropped = img.crop((x1, y1, x2, y2))
print("Actual letters crop size:", cropped.size)

# Create 400x400 canvas
canvas_size = 400
canvas = Image.new("RGBA", (canvas_size, canvas_size), (255, 255, 255, 255))

# Scale to 85% width
target_w = int(canvas_size * 0.85)
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

print("Saved cleanly cropped Ethnic logo to:", dest_circle)
