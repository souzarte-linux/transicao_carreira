import os
import math
from PIL import Image
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas

print ("\n======================================================")
print ("| --- Gerador de Poster Retangular em A4 ---         |")
print ("======================================================\n")


# --- 1. ENTRADA DE DADOS ---
img_path = input("1. Cole o caminho completo da imagem: ").strip(' "')

if not os.path.exists(img_path):
    print(f"\n[ERRO] O arquivo '{img_path}' não foi encontrado.")
    exit()

folder = os.path.dirname(img_path)
pdf_name = input("2. Digite o nome para o PDF (sem .pdf): ").strip()
if not pdf_name:
    pdf_name = "poster_gerado"
pdf_path = os.path.join(folder, f"{pdf_name}.pdf")

try:
    target_width_cm = float(input("3. Qual a LARGURA total do poster em cm? (ex: 200): "))
    target_height_cm = float(input("4. Qual a ALTURA total do poster em cm? (ex: 150): "))
except ValueError:
    print("\n[ERRO] Por favor, digite apenas números.")
    exit()

# --- 2. CONFIGURAÇÕES TÉCNICAS ---
img = Image.open(img_path)
largura_a4_pts, altura_a4_pts = A4
largura_a4_cm = largura_a4_pts / cm
altura_a4_cm = altura_a4_pts / cm

margin_cm = 0.5
usable_w = largura_a4_cm - (2 * margin_cm)
usable_h = altura_a4_cm - (2 * margin_cm)

cols = math.ceil(target_width_cm / usable_w)
rows = math.ceil(target_height_cm / usable_h)

# --- 3. PROCESSAMENTO ---
final_w_px = int((cols * usable_w) * 118.11) 
final_h_px = int((rows * usable_h) * 118.11)

print(f"\nProcessando imagem...")
img_resized = img.resize((final_w_px, final_h_px), Image.Resampling.LANCZOS)

tile_w_px = final_w_px // cols
tile_h_px = final_h_px // rows

# --- 4. GERAÇÃO DO PDF ---
c = canvas.Canvas(pdf_path, pagesize=A4)
temp_files = []


print(f"\nCriando o PDF do seu poster que terá {cols} colunas e {rows} linhas. Total de {cols * rows} folhas A4.")
#print(f"Criando PDF com {cols * rows} paginas...")

for r in range(rows):
    for c_idx in range(cols):
        left = c_idx * tile_w_px
        upper = r * tile_h_px
        right = left + tile_w_px
        lower = upper + tile_h_px
        
        tile = img_resized.crop((left, upper, right, lower))
        
        tile_filename = f"temp_tile_{r}_{c_idx}.jpg"
        full_tile_path = os.path.join(folder, tile_filename)
        
        tile.save(full_tile_path, "JPEG", quality=95)
        temp_files.append(full_tile_path)
        
        c.drawImage(full_tile_path, margin_cm*cm, margin_cm*cm, 
                    width=usable_w*cm, height=usable_h*cm)
        
        label = f"{chr(65+r)}{c_idx+1}"
        c.setFont("Helvetica", 12)
        c.drawString(1*cm, (altura_a4_cm - 1.5) * cm, f"Posicao: {label}")
        
        c.showPage()

c.save()
print(f"\n[SUCESSO] PDF salvo em: {pdf_path}")

# --- 5. LIMPEZA ---
print("Limpando arquivos temporários...")
for file in temp_files:
    try:
        os.remove(file)
    except:
        pass
print("Concluído!")