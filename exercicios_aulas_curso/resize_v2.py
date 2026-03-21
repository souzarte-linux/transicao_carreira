from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from PIL import Image
import math
import os

# --- INTERAÇÃO COM O USUÁRIO ---
print ("\n====================================================")
print ("| --- Gerador de Poster Retangular em A4 ---          |")
print ("=====================================================\n")

img_path = input("Cole o caminho completo da imagem: ").strip(' "')

if not os.path.exists(img_path):
    print(f"Erro: O arquivo '{img_path}' não foi encontrado.")
    exit()

folder = os.path.dirname(img_path)
pdf_name = input("Digite o nome para o PDF (sem .pdf): ").strip()
pdf_path = os.path.join(folder, f"{pdf_name}.pdf")

# AGORA PEDIMOS AS DUAS MEDIDAS:
try:
    target_width_cm = float(input("Qual a LARGURA total do poster em cm? (ex: 200): "))
    target_height_cm = float(input("Qual a ALTURA total do poster em cm? (ex: 150): "))
except ValueError:
    print("Por favor, digite apenas números.")
    exit()

# --- CONFIGURAÇÕES TÉCNICAS ---
img = Image.open(img_path)
a4_width_cm, a4_h_cm = A4[0]/cm, A4[1]/cm

margin_cm = 0.5
usable_w = a4_width_cm - (2 * margin_cm)
usable_h = a4_h_cm - (2 * margin_cm)

# Cálculo independente para colunas (largura) e linhas (altura)
cols = math.ceil(target_width_cm / usable_w)
rows = math.ceil(target_height_cm / usable_h)

# Ajuste do redimensionamento para o novo formato retangular
final_w_px = int((cols * usable_w) * 118.11) 
final_h_px = int((rows * usable_h) * 118.11)
img_resized = img.resize((final_w_px, final_h_px), Image.Resampling.LANCZOS)

tile_w_px = final_w_px // cols
tile_h_px = final_h_px // rows

c = canvas.Canvas(pdf_path, pagesize=A4)
temp_files = []

print(f"\nIniciando: O poster terá {cols} colunas e {rows} linhas ({cols * rows} folhas A4).")

for r in range(rows):
    for c_idx in range(cols):
        # Define a área de corte (crop)
        left = c_idx * tile_w_px
        upper = r * tile_h_px
        right = left + tile_w_px
        lower = upper + tile_h_px
        
        tile = img_resized.crop((left, upper, right, lower))
        
        # Salva o retalho temporário
        tile_filename = f"temp_tile_{r}_{c_idx}.jpg"
        full_tile_path = os.path.join(folder, tile_filename)
        
        tile.save(full_tile_path, "JPEG", quality=95)
        temp_files.append(full_tile_path)
        
        # Desenha a imagem centralizada no A4 respeitando a margem
        c.drawImage(full_tile_path, margin_cm*cm, margin_cm*cm, 
                    width=usable_w*cm, height=usable_h*cm)
        
        # Adiciona identificação na margem (Ex: A1, B2)
        label = f"{chr(65+r)}{c_idx+1}"
        c.setFont("Helvetica", 12)
        c.drawString(1*cm, a4_h_cm*cm - 1.5*cm, f"Posicao: {label}")
        
        c.showPage()

c.save()
print(f"\n[SUCESSO] PDF salvo em: {pdf_path}")

# --- 5. LIMPEZA DE TEMPORÁRIOS ---
print("Limpando arquivos temporários...")
for file in temp_files:
    try:
        os.remove(file)
    except:
        pass
print("Concluído! O sistema está limpo.")

if __name__ == "__main__":
    gerar_poster()