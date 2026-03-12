from PIL import Image, ImageDraw, ImageFont
import os

OUTPUT_DIR = "assets/outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def generate_thumbnail(image_path, text):
    if not os.path.exists(image_path):
        raise FileNotFoundError("Frame image not found.")

    # 1. Load & resize to YouTube thumbnail size
    img = Image.open(image_path).convert("RGB")
    img = img.resize((1280, 720))

    draw = ImageDraw.Draw(img)

    # 2. Add dark gradient overlay (bottom)
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)

    for y in range(400, 720):
        alpha = int((y - 400) / 320 * 180)
        overlay_draw.rectangle(
            [(0, y), (1280, y + 1)],
            fill=(0, 0, 0, alpha)
        )

    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(img)

    # 3. Load font (fallback safe)
    try:
        font = ImageFont.truetype("arialbd.ttf", 80)
    except:
        font = ImageFont.load_default()

    # 4. Draw bold title text (bottom-left)
    x, y = 60, 500

    # Text shadow
    draw.text((x + 4, y + 4), text, font=font, fill="black")
    draw.text((x, y), text, font=font, fill="white")

    # 5. Save thumbnail
    output_path = os.path.join(OUTPUT_DIR, "thumbnail.jpg")
    img.save(output_path, quality=95)

    return output_path
