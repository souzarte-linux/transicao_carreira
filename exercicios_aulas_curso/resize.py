# Create a tiled A4 PDF (2m x 2m) with margins and numbering using reportlab

from reportlab.platypus import SimpleDocTemplate, Image as RLImage, Spacer
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from PIL import Image
import math
import os

img_path = "C:/Users/cyber/OneDrive/Imagens/Semana Satna 2026 Inteira.jpg"

print ("\n Aguarde enquanto o trabalho é realizado... \n")
# Load image
img = Image.open(img_path)

# Target size: 1.5m x 1.5m = 150cm x 150cm
target_cm = 150

# A4 size in cm (approx)
a4_width_cm = 21.0
a4_height_cm = 29.7

# Margins (medium border)
margin_cm = 0.9

usable_w = a4_width_cm - 1.5 * margin_cm
usable_h = a4_height_cm - 1.5 * margin_cm

# Number of tiles
cols = math.ceil(target_cm / usable_w)
rows = math.ceil(target_cm / usable_h)

# Resize image proportionally to exact grid size
final_w_cm = cols * usable_w
final_h_cm = rows * usable_h

# Convert cm to pixels (assume 300 DPI)
dpi = 300
cm_to_inch = 0.393701
final_w_px = int(final_w_cm * cm_to_inch * dpi)
final_h_px = int(final_h_cm * cm_to_inch * dpi)

img_resized = img.resize((final_w_px, final_h_px))

# Tile size in px
tile_w_px = final_w_px // cols
tile_h_px = final_h_px // rows

pdf_path = "C:/Users/cyber/OneDrive/Imagens/poster_2x2m_A4_tiles.pdf"

c = canvas.Canvas(pdf_path, pagesize=A4)

for r in range(rows):
    for c_idx in range(cols):
        left = c_idx * tile_w_px
        upper = r * tile_h_px
        right = left + tile_w_px
        lower = upper + tile_h_px
        
        tile = img_resized.crop((left, upper, right, lower))
        
        tile_path = f"C:/Users/cyber/OneDrive/Imagens/tile_{r}_{c_idx}.jpg"
        tile.save(tile_path, "JPEG", quality=95)
        
        # Draw on A4
        c.drawImage(
            tile_path,
            margin_cm * cm,
            margin_cm * cm,
            width=usable_w * cm,
            height=usable_h * cm
        )
        
        # Add numbering in margins
        label = f"{chr(65+r)}{c_idx+1}"
        c.setFont("Helvetica", 10)
        c.drawString(1*cm, a4_height_cm*cm - 1*cm, label)
        
        c.showPage()

c.save()

pdf_path