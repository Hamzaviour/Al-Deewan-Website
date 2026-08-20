from PIL import Image, ImageOps, ImageEnhance

src_path = r"C:\Users\hamza\.gemini\antigravity-ide\brain\428edef7-d67e-4c8f-a214-01afb546c76c\.user_uploaded\media_1787247602579.png"
dest_path = r"e:\Work\Al-Deewan Website\assets\images\ethnic_circle_logo.png"
dest_path_flat = r"e:\Work\Al-Deewan Website\assets\images\ethnic_logo.png"

# Load image
img = Image.open(src_path).convert("RGBA")

# Crop tight bbox
gray = img.convert("L")
inv = ImageOps.invert(gray)
bbox = inv.getbbox()
if bbox:
    cropped_img = img.crop(bbox)
else:
    cropped_img = img

# Create square canvas 400x400
canvas_size = 400
canvas = Image.new("RGBA", (canvas_size, canvas_size), (255, 255, 255, 255))

# Target width 96%
target_width = int(canvas_size * 0.96)
aspect = cropped_img.width / cropped_img.height
target_height = int(target_width / aspect)

resized_img = cropped_img.resize((target_width, target_height), Image.Resampling.LANCZOS)

offset_x = (canvas_size - target_width) // 2
offset_y = (canvas_size - target_height) // 2
canvas.paste(resized_img, (offset_x, offset_y), resized_img)

canvas.save(dest_path, "PNG")
cropped_img.save(dest_path_flat, "PNG")
print("Saved maximal width Ethnic logo!")
