from PIL import Image, ImageOps

src_path = r"C:\Users\hamza\.gemini\antigravity-ide\brain\428edef7-d67e-4c8f-a214-01afb546c76c\.user_uploaded\media_1787248891810.png"
dest_circle = r"e:\Work\Al-Deewan Website\assets\images\ethnic_circle_logo.png"
dest_flat = r"e:\Work\Al-Deewan Website\assets\images\ethnic_logo.png"

img = Image.open(src_path).convert("RGBA")
print("Original size:", img.size)

# Convert to grayscale and crop bounding box
gray = img.convert("L")
inv = ImageOps.invert(gray)
bbox = inv.getbbox()
print("BBox:", bbox)
if bbox:
    cropped = img.crop(bbox)
else:
    cropped = img

print("Cropped size:", cropped.size)

# Create 400x400 white canvas
canvas_size = 400
canvas = Image.new("RGBA", (canvas_size, canvas_size), (255, 255, 255, 255))

# Scale to 90% width of canvas
target_w = int(canvas_size * 0.90)
aspect = cropped.width / cropped.height
target_h = int(target_w / aspect)

resized = cropped.resize((target_w, target_h), Image.Resampling.LANCZOS)

# Paste in center
pos_x = (canvas_size - target_w) // 2
pos_y = (canvas_size - target_h) // 2
canvas.paste(resized, (pos_x, pos_y), resized)

canvas.save(dest_circle, "PNG")
cropped.save(dest_flat, "PNG")

print("Saved new Ethnic logo successfully to:", dest_circle, "and", dest_flat)
