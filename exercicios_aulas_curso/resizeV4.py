import os
import math
import threading # Novo: Para o programa não travar
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
        self.geometry("500x500")
        ctk.set_appearance_mode("dark")

        self.caminho_imagem = ""

        # UI - Título
        self.label_titulo = ctk.CTkLabel(self, text="Configurações do Poster", font=("Arial", 20, "bold"))
        self.label_titulo.pack(pady=20)

        # Botão Selecionar
        self.btn_select = ctk.CTkButton(self, text="1. Selecionar Imagem", command=self.selecionar_arquivo)
        self.btn_select.pack(pady=10)

        self.label_path = ctk.CTkLabel(self, text="Nenhum arquivo selecionado", font=("Arial", 10), wraplength=400)
        self.label_path.pack()

        # Inputs
        self.frame_inputs = ctk.CTkFrame(self)
        self.frame_inputs.pack(pady=15, padx=20, fill="x")

        self.entry_largura = ctk.CTkEntry(self.frame_inputs, placeholder_text="Largura total (cm)")
        self.entry_largura.grid(row=0, column=0, padx=10, pady=10)

        self.entry_altura = ctk.CTkEntry(self.frame_inputs, placeholder_text="Altura total (cm)")
        self.entry_altura.grid(row=0, column=1, padx=10, pady=10)

        self.entry_nome_pdf = ctk.CTkEntry(self, placeholder_text="Nome do arquivo PDF", width=300)
        self.entry_nome_pdf.pack(pady=10)

        # BARRA DE PROGRESSO (Novo)
        self.label_status = ctk.CTkLabel(self, text="Aguardando início...", font=("Arial", 12))
        self.label_status.pack(pady=(10, 0))
        
        self.progress_bar = ctk.CTkProgressBar(self, width=400)
        self.progress_bar.set(0) # Inicia em 0%
        self.progress_bar.pack(pady=10)

        # Botão Gerar
        self.btn_gerar = ctk.CTkButton(self, text="GERAR POSTER PDF", fg_color="green", 
                                       hover_color="darkgreen", command=self.iniciar_thread)
        self.btn_gerar.pack(pady=20)

    def selecionar_arquivo(self):
        caminho = filedialog.askopenfilename(filetypes=[("Imagens", "*.jpg *.jpeg *.png")])
        if caminho:
            self.caminho_imagem = caminho
            self.label_path.configure(text=f"Selecionado: {os.path.basename(caminho)}")

    def iniciar_thread(self):
        """Inicia o processamento em uma linha separada para não travar a janela"""
        # Desativa o botão para evitar múltiplos cliques
        self.btn_gerar.configure(state="disabled")
        t = threading.Thread(target=self.processar_poster)
        t.start()

    def processar_poster(self):
        if not self.caminho_imagem:
            self.finalizar_erro("Selecione uma imagem primeiro!")
            return

        try:
            target_w = float(self.entry_largura.get())
            target_h = float(self.entry_altura.get())
            nome_pdf = self.entry_nome_pdf.get() or "meu_poster"
            
            folder = os.path.dirname(self.caminho_imagem)
            pdf_path = os.path.join(folder, f"{nome_pdf}.pdf")

            img = Image.open(self.caminho_imagem)
            orig_w, orig_h = img.size

            a4_w, a4_h = A4[0]/cm, A4[1]/cm
            margin = 0.5
            u_w, u_h = a4_w - (2*margin), a4_h - (2*margin)

            cols = math.ceil(target_w / u_w)
            rows = math.ceil(target_h / u_h)
            total_paginas = cols * rows
            
            c = canvas.Canvas(pdf_path, pagesize=A4)
            chunk_w = orig_w / cols
            chunk_h = orig_h / rows

            contador = 0
            for r in range(rows):
                for c_idx in range(cols):
                    # Atualiza a interface (Progresso)
                    contador += 1
                    progresso = contador / total_paginas
                    self.progress_bar.set(progresso)
                    self.label_status.configure(text=f"Processando página {contador} de {total_paginas}...")

                    # Lógica de corte
                    left, top = c_idx * chunk_w, r * chunk_h
                    right, bottom = (c_idx + 1) * chunk_w, (r + 1) * chunk_h
                    
                    tile = img.crop((left, top, right, bottom))
                    tile_res = tile.resize((int(u_w * 118), int(u_h * 118)), Image.Resampling.LANCZOS)
                    
                    t_path = os.path.join(folder, f"tmp_{r}_{c_idx}.jpg")
                    tile_res.save(t_path, "JPEG", quality=85)
                    
                    c.drawImage(t_path, margin*cm, margin*cm, width=u_w*cm, height=u_h*cm)
                    c.setFont("Helvetica", 10)
                    c.drawString(1*cm, 0.5*cm, f"Posicao: {chr(65+r)}{c_idx+1}")
                    c.showPage()
                    os.remove(t_path)

            c.save()
            self.label_status.configure(text="Concluído!")
            messagebox.showinfo("Sucesso", f"Poster gerado com {total_paginas} páginas!")

        except ValueError:
            messagebox.showerror("Erro", "Valores inválidos.")
        except Exception as e:
            messagebox.showerror("Erro", str(e))
        finally:
            self.btn_gerar.configure(state="normal")
            self.progress_bar.set(0)

    def finalizar_erro(self, msg):
        messagebox.showerror("Erro", msg)
        self.btn_gerar.configure(state="normal")

if __name__ == "__main__":
    app = App()
    app.mainloop()