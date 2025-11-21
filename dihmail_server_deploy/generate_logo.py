from PIL import Image, ImageDraw, ImageFont
import os

# Create a simple PNG logo for dihmail
width, height = 200, 200
image = Image.new('RGB', (width, height), color=(102, 126, 234))

draw = ImageDraw.Draw(image)

# Draw a simple envelope shape
envelope_color = (255, 255, 255)
# Envelope body
draw.rectangle([40, 70, 160, 130], fill=envelope_color, outline=(200, 200, 200), width=2)
# Envelope flap
draw.polygon([40, 70, 100, 100, 160, 70], fill=(230, 230, 230))
draw.line([40, 70, 100, 100], fill=(150, 150, 150), width=2)
draw.line([160, 70, 100, 100], fill=(150, 150, 150), width=2)

# Draw lock symbol
lock_x, lock_y = 85, 95
draw.rectangle([lock_x, lock_y, lock_x+30, lock_y+20], fill=(102, 126, 234), outline=(80, 100, 200), width=2)
draw.arc([lock_x+5, lock_y-15, lock_x+25, lock_y+5], start=0, end=180, fill=(102, 126, 234), width=3)

# Save the image
output_path = os.path.join(os.path.dirname(__file__), 'static', 'dihmail.png')
os.makedirs(os.path.dirname(output_path), exist_ok=True)
image.save(output_path)
print(f"Logo created at: {output_path}")
