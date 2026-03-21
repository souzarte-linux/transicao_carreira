import os
import math
import threading
import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Gerador de Poster Profissional")
        self.geometry("550x700")
        ctk.set_appearance_mode("dark")

        self.caminho_imagem = ""
        self.diretorio_destino = ""

        # UI - Título
        self.label_titulo = ctk.CTkLabel(self, text="Configurador de Poster", font=("Arial", 22, "bold"))
        self.label_titulo.pack(pady=(20, 10))

        # Seção Seleção
        self.btn_select = ctk.CTkButton(self, text="Selecionar Imagem de Origem", command=self.selecionar_arquivo)
        self.btn_select.pack(pady=10)

        self.label_path = ctk.CTkLabel(self, text="Nenhum arquivo selecionado", font=("Arial", 11), text_color="gray", wraplength=450)
        self.label_path.pack(pady=(0, 10))

        # 0. Linha Divisória 1
        self.line1 = ctk.CTkFrame(self, height=2, fg_color="gray30")
        self.line1.pack(fill="x", padx=30, pady=10)

        # 1. Seção Tamanho do Poster
        self.label_medidas = ctk.CTkLabel(self, text="Tamanho do seu Poster", font=("Arial", 14, "bold"))
        self.label_medidas.pack(anchor="w", padx=40, pady=(10, 5))

        # 1.1 Alinhamento à esquerda dos inputs
        self.frame_medidas = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_medidas.pack(anchor="w", padx=40, pady=5)

        self.entry_largura = ctk.CTkEntry(self.frame_medidas, placeholder_text="Largura (cm)", width=120)
        self.entry_largura.grid(row=0, column=0, padx=(0, 10))

        self.entry_altura = ctk.CTkEntry(self.frame_medidas, placeholder_text="Altura (cm)", width=120)
        self.entry_altura.grid(row=0, column=1)

        # 4. Campo de Margem (Padrão 0.8)
        self.label_margem = ctk.CTkLabel(self, text="Margem de segurança (cm):", font=("Arial", 12))
        self.label_margem.pack(anchor="w", padx=40, pady=(15, 0))
        
        self.entry_margem = ctk.CTkEntry(self, width=80)
        self.entry_margem.insert(0, "0.8")
        self.entry_margem.pack(anchor="w", padx=40, pady=5)

        # 2. Opções de Destino (Radio Buttons / Bullet Points)
        self.radio_var = ctk.IntVar(value=0)
        
        self.radio_origem = ctk.CTkRadioButton(self, text="Salvar na pasta de origem", variable=self.radio_var, value=0, command=self.reset_destino)
        self.radio_origem.pack(anchor="w", padx=40, pady=(20, 5))

        self.radio_outro = ctk.CTkRadioButton(self, text="Escolher local diferente", variable=self.radio_var, value=1, command=self.escolher_destino)
        self.radio_outro.pack(anchor="w", padx=40, pady=5)

        # 3. Linha Divisória 2
        self.line2 = ctk.CTkFrame(self, height=2, fg_color="gray30")
        self.line2.pack(fill="x", padx=30, pady=20)

        # Campo Nome do PDF
        self.entry_nome_pdf = ctk.CTkEntry(self, placeholder_text="Nome do arquivo final (ex: meu_poster)", width=400)
        self.entry_nome_pdf.pack(pady=10)

        # Barra de Progresso e Status
        self.label_status = ctk.CTkLabel(self, text="Pronto para iniciar", font=("Arial", 11))
        self.label_status.pack(pady=(10, 0))
        
        self.progress_bar = ctk.CTkProgressBar(self, width=400)
        self.progress_bar.set(0)
        self.progress_bar.pack(pady=10)

        # Botão Gerar
        self.btn_gerar = ctk.CTkButton(self, text="GERAR POSTER AGORA", fg_color="#2c8c2c", hover_color="#1e5e1e", height=45, font=("Arial", 14, "bold"), command=self.iniciar_thread)
        self.btn_gerar.pack(pady=20)

    def selecionar_arquivo(self):
        caminho = filedialog.askopenfilename(filetypes=[("Imagens", "*.jpg *.jpeg *.png")])
        if caminho:
            self.caminho_imagem = caminho
            self.label_path.configure(text=f"Arquivo: {os.path.basename(caminho)}")

    def escolher_destino(self):
        diretorio = filedialog.askdirectory()
        if diretorio:
            self.diretorio_destino = diretorio
            self.label_status.configure(text=f"Destino: {os.path.basename(diretorio)}")
        else:
            self.radio_var.set(0) # Volta para origem se cancelar

    def reset_destino(self):
        self.diretorio_destino = ""
        self.label_status.configure(text="Salvar na pasta de origem")

    def iniciar_thread(self):
        self.btn_gerar.configure(state="disabled")
        threading.Thread(target=self.processar_poster, daemon=True).start()

    def processar_poster(self):
        if not self.caminho_imagem:
            self.mostrar_erro("Selecione uma imagem primeiro!")
            return

        try:
            target_w = float(self.entry_largura.get())
            target_h = float(self.entry_altura.get())
            margem_val = float(self.entry_margem.get())
            nome_pdf = self.entry_nome_pdf.get() or "poster_final"
            
            # Define pasta final
            if self.radio_var.get() == 0:
                folder = os.path.dirname(self.caminho_imagem)
            else:
                folder = self.diretorio_destino or os.path.dirname(self.caminho_imagem)

            pdf_path = os.path.join(folder, f"{nome_pdf}.pdf")

            img = Image.open(self.caminho_imagem)
            orig_w, orig_h = img.size

            # Cálculo A4 com margem dinâmica
            a4_w, a4_h = A4[0]/cm, A4[1]/cm
            u_w, u_h = a4_w - (2 * margem_val), a4_h - (2 * margem_val)

            cols = math.ceil(target_w / u_w)
            rows = math.ceil(target_h / u_h)
            total = cols * rows
            
            c = canvas.Canvas(pdf_path, pagesize=A4)
            chunk_w, chunk_h = orig_w / cols, orig_h / rows

            for r in range(rows):
                for c_idx in range(cols):
                    idx = (r * cols) + c_idx + 1
                    self.progress_bar.set(idx / total)
                    self.label_status.configure(text=f"Página {idx} de {total}...")

                    left, top = c_idx * chunk_w, r * chunk_h
                    tile = img.crop((left, top, left + chunk_w, top + chunk_h))
                    tile_res = tile.resize((int(u_w * 118), int(u_h * 118)), Image.Resampling.LANCZOS)
                    
                    t_path = os.path.join(folder, f"tmp_{r}_{c_idx}.jpg")
                    tile_res.save(t_path, "JPEG", quality=90)
                    
                    c.drawImage(t_path, margem_val*cm, margem_val*cm, width=u_w*cm, height=u_h*cm)
                    c.setFont("Helvetica", 9)
                    c.drawString(margem_val*cm, (margem_val-0.4)*cm, f"Corte {chr(65+r)}{c_idx+1} | Margem {margem_val}cm")
                    c.showPage()
                    os.remove(t_path)

            c.save()
            self.label_status.configure(text="Concluído!")
            messagebox.showinfo("Sucesso", f"PDF criado com {total} páginas em:\n{pdf_path}")

        except Exception as e:
            messagebox.showerror("Erro", f"Falha: {str(e)}")
        finally:
            self.btn_gerar.configure(state="normal")

    def mostrar_erro(self, msg):
        messagebox.showerror("Erro", msg)
        self.btn_gerar.configure(state="normal")

if __name__ == "__main__":
    app = App()
    app.mainloop()