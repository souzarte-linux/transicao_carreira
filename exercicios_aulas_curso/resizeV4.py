import os
import math
import threading
import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageDraw
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Poster Pro v4.0 - Engenharia de Impressão")
        self.geometry("1100x950")
        ctk.set_appearance_mode("dark")

        self.caminho_imagem = ""
        self.diretorio_destino = ""
        self.img_original = None
        self.bloquear_atualizacao = False 

        # Configuração do Grid Principal
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1) 

        # --- SEÇÃO 0: TOPO ---
        self.frame_topo = ctk.CTkFrame(self, fg_color="gray10", corner_radius=15)
        self.frame_topo.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        
        self.frame_topo.grid_columnconfigure(0, weight=1)
        self.frame_topo.grid_columnconfigure(1, weight=1)

        self.btn_select = ctk.CTkButton(self.frame_topo, text="1. Localizar Imagem", 
                                       fg_color="#1f538d", hover_color="#14375e",
                                       command=self.selecionar_arquivo)
        self.btn_select.grid(row=0, column=0, padx=20, pady=(20, 5))
        self.label_nome_arquivo = ctk.CTkLabel(self.frame_topo, text="Nenhum arquivo...", font=("Arial", 11, "bold"))
        self.label_nome_arquivo.grid(row=1, column=0)

        self.radio_var = ctk.IntVar(value=0)
        self.f_destino = ctk.CTkFrame(self.frame_topo, fg_color="transparent")
        self.f_destino.grid(row=0, column=1, rowspan=2, padx=20, pady=10)
        
        ctk.CTkRadioButton(self.f_destino, text="Salvar na pasta de origem", variable=self.radio_var, value=0).pack(anchor="w")
        self.rb_custom = ctk.CTkRadioButton(self.f_destino, text="Escolher local personalizado", variable=self.radio_var, value=1, command=self.escolher_destino)
        self.rb_custom.pack(anchor="w", pady=(5, 0))
        self.label_destino = ctk.CTkLabel(self.f_destino, text="Destino: Automático", font=("Arial", 9), text_color="gray")
        self.label_destino.pack(anchor="w")

        # --- SEÇÃO 1: MEIO ---
        self.frame_meio = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_meio.grid(row=1, column=0, padx=20, pady=0, sticky="nsew")
        self.frame_meio.grid_columnconfigure(0, weight=3)
        self.frame_meio.grid_columnconfigure(1, weight=7)
        self.frame_meio.grid_rowconfigure(0, weight=1)

        # Painel Esquerdo (Entradas)
        self.frame_inputs = ctk.CTkFrame(self.frame_meio, corner_radius=15)
        self.frame_inputs.grid(row=0, column=0, padx=(0, 10), sticky="nsew")
        
        ctk.CTkLabel(self.frame_inputs, text="Dimensões do Poster", font=("Arial", 16, "bold")).pack(pady=15)
        self.container_medidas = ctk.CTkFrame(self.frame_inputs, fg_color="transparent")
        self.container_medidas.pack(fill="x", padx=15)
        
        fields = [("ALTURA (CM)", "entry_h"), ("LARGURA (CM)", "entry_w"), 
                  ("PÁG. VERTICAL", "entry_pag_v"), ("PÁG. HORIZONTAL", "entry_pag_h")]
        
        for i, (label_text, attr_name) in enumerate(fields):
            r, c_idx = divmod(i, 2)
            ctk.CTkLabel(self.container_medidas, text=label_text, font=("Arial", 9, "bold"), text_color="gray").grid(row=r*2, column=c_idx, sticky="w")
            entry = ctk.CTkEntry(self.container_medidas, height=35)
            entry.grid(row=r*2+1, column=c_idx, padx=5, pady=(0, 10), sticky="ew")
            setattr(self, attr_name, entry)
            
        self.entry_h.bind("<KeyRelease>", lambda e: self.calc_pelas_medidas())
        self.entry_w.bind("<KeyRelease>", lambda e: self.calc_pelas_medidas())
        self.entry_pag_v.bind("<KeyRelease>", lambda e: self.calc_pelas_folhas())
        self.entry_pag_h.bind("<KeyRelease>", lambda e: self.calc_pelas_folhas())

        # Distribuição
        self.frame_dist = ctk.CTkFrame(self.frame_inputs, fg_color="gray20")
        self.frame_dist.pack(fill="x", padx=20, pady=(20, 10))
        self.label_info_paginas = ctk.CTkLabel(self.frame_dist, text="0 COL × 0 LIN", font=("Arial", 20, "bold"))
        self.label_info_paginas.pack(pady=(10, 0))
        self.label_total_a4 = ctk.CTkLabel(self.frame_dist, text="Total: 0 folhas", font=("Arial", 11), text_color="gray")
        self.label_total_a4.pack(pady=(0, 10))

        # Nome do PDF
        self.f_nome_final = ctk.CTkFrame(self.frame_inputs, fg_color="transparent")
        self.f_nome_final.pack(fill="x", padx=20, pady=(20, 0))
        ctk.CTkLabel(self.f_nome_final, text="NOME DO ARQUIVO FINAL", font=("Arial", 9, "bold"), text_color="gray").pack(anchor="w")
        self.entry_nome_pdf = ctk.CTkEntry(self.f_nome_final, placeholder_text="Ex: Meu_Poster", height=35)
        self.entry_nome_pdf.pack(fill="x", pady=(5, 0))
        self.entry_nome_pdf.insert(0, "Poster_Final_Pronto")

        # Painel Direito (Preview)
        self.frame_preview = ctk.CTkFrame(self.frame_meio, corner_radius=15)
        self.frame_preview.grid(row=0, column=1, sticky="nsew")
        ctk.CTkLabel(self.frame_preview, text="VISUALIZAÇÃO TÉCNICA (GRID A4)", font=("Arial", 11, "bold"), text_color="gray").pack(pady=10)
        self.canvas_preview = ctk.CTkLabel(self.frame_preview, text="Carregue uma imagem", text_color="gray30")
        self.canvas_preview.pack(expand=True, fill="both", padx=20, pady=20)

        # --- SEÇÃO 2: AJUSTES E BOTÃO GERAR ---
        self.frame_inferior = ctk.CTkFrame(self, corner_radius=15)
        self.frame_inferior.grid(row=2, column=0, padx=20, pady=20, sticky="nsew")
        
        self.entry_margem = ctk.CTkEntry(self.frame_inferior, width=80)
        self.entry_margem.insert(0, "0.8")
        self.entry_margem.pack(side="left", padx=20, pady=15)
        ctk.CTkLabel(self.frame_inferior, text="Margem (cm)").pack(side="left")

        self.switch_legendas = ctk.CTkSwitch(self.frame_inferior, text="Legendas de Identificação")
        self.switch_legendas.pack(side="left", padx=30)
        self.switch_legendas.select()

        self.btn_gerar = ctk.CTkButton(self.frame_inferior, text="GERAR PDF FINAL", width=200, height=40, font=("Arial", 14, "bold"), command=self.iniciar_thread)
        self.btn_gerar.pack(side="right", padx=20)

        self.progresso = ctk.CTkProgressBar(self)
        self.progresso.grid(row=3, column=0, padx=20, pady=(0, 10), sticky="ew")
        self.progresso.set(0)

        # --- RODAPÉ ---
        self.frame_footer = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_footer.grid(row=4, column=0, padx=20, pady=(0, 10), sticky="ew")
        ctk.CTkLabel(self.frame_footer, text="Desenvolvido por Souzarte", font=("Arial", 10), text_color="gray").pack(side="left")
        self.btn_doacao = ctk.CTkButton(self.frame_footer, text="☕ Apoiar Projeto / Contato", font=("Arial", 11, "bold"), fg_color="#2b2b2b", hover_color="#3d3d3d", command=self.mostrar_doacao)
        self.btn_doacao.pack(side="right")

    # --- FUNÇÕES ---

    def selecionar_arquivo(self):
        caminho = filedialog.askopenfilename(filetypes=[("Imagens", "*.jpg *.jpeg *.png *.tiff")])
        if caminho:
            self.caminho_imagem = caminho
            self.img_original = Image.open(caminho)
            self.label_nome_arquivo.configure(text=os.path.basename(caminho))
            nome_base = os.path.splitext(os.path.basename(caminho))[0]
            self.entry_nome_pdf.delete(0, "end")
            self.entry_nome_pdf.insert(0, f"{nome_base}_Poster")
            self.carregar_preview()
            self.calc_pelas_medidas()

    def escolher_destino(self):
        pasta = filedialog.askdirectory()
        if pasta:
            self.diretorio_destino = pasta
            self.label_destino.configure(text=f"Destino: {pasta}")
        else: self.radio_var.set(0)

    def carregar_preview(self):
        if not self.img_original: return
        largura_max, altura_max = 600, 480
        img_temp = self.img_original.copy()
        img_temp.thumbnail((largura_max, altura_max), Image.Resampling.LANCZOS)
        self.desenhar_grid_no_preview(img_temp)

    def desenhar_grid_no_preview(self, img_pil):
        try:
            cols = int(self.entry_pag_h.get() or 1)
            rows = int(self.entry_pag_v.get() or 1)
        except: cols, rows = 1, 1
        draw = ImageDraw.Draw(img_pil, "RGBA")
        w, h = img_pil.size
        for i in range(1, cols):
            x = (w / cols) * i
            draw.line([(x, 0), (x, h)], fill=(0, 255, 255, 120), width=2)
        for i in range(1, rows):
            y = (h / rows) * i
            draw.line([(0, y), (w, y)], fill=(0, 255, 255, 120), width=2)
        img_tk = ImageTk.PhotoImage(img_pil)
        self.canvas_preview.configure(image=img_tk, text="")
        self.canvas_preview.image = img_tk

    def get_dim_util(self):
        try: m = float(self.entry_margem.get())
        except: m = 0.8
        return 21.0 - (2 * m), 29.7 - (2 * m)

    def calc_pelas_medidas(self):
        if self.bloquear_atualizacao or not self.img_original: return
        try:
            self.bloquear_atualizacao = True
            h, w = float(self.entry_h.get() or 0), float(self.entry_w.get() or 0)
            u_w, u_h = self.get_dim_util()
            cols, rows = math.ceil(w / u_w) if w > 0 else 0, math.ceil(h / u_h) if h > 0 else 0
            self.entry_pag_h.delete(0, "end"); self.entry_pag_h.insert(0, str(cols))
            self.entry_pag_v.delete(0, "end"); self.entry_pag_v.insert(0, str(rows))
            self.atualizar_status(cols, rows)
        except: pass
        finally: 
            self.bloquear_atualizacao = False
            self.carregar_preview()

    def calc_pelas_folhas(self):
        if self.bloquear_atualizacao or not self.img_original: return
        try:
            self.bloquear_atualizacao = True
            cols, rows = int(self.entry_pag_h.get() or 0), int(self.entry_pag_v.get() or 0)
            u_w, u_h = self.get_dim_util()
            self.entry_w.delete(0, "end"); self.entry_w.insert(0, f"{cols * u_w:.1f}")
            self.entry_h.delete(0, "end"); self.entry_h.insert(0, f"{rows * u_h:.1f}")
            self.atualizar_status(cols, rows)
        except: pass
        finally: 
            self.bloquear_atualizacao = False
            self.carregar_preview()

    def atualizar_status(self, cols, rows):
        self.label_info_paginas.configure(text=f"{cols} COL × {rows} LIN")
        self.label_total_a4.configure(text=f"Total: {cols*rows} folhas A4")

    def mostrar_doacao(self):
        janela_apoio = ctk.CTkToplevel(self)
        janela_apoio.title("Apoie o Desenvolvedor Open Source")
        janela_apoio.geometry("450x300")
        janela_apoio.attributes("-topmost", True)
        janela_apoio.resizable(False, False)

        ctk.CTkLabel(janela_apoio, text="Gostou da ferramenta?", font=("Arial", 18, "bold")).pack(pady=(20, 10))
        ctk.CTkLabel(janela_apoio, text="Se este programa facilitou seu trabalho,\nconsidere fazer uma doação de qualquer valor.", 
                     justify="center").pack(pady=5)
        
        f_pix = ctk.CTkFrame(janela_apoio, fg_color="gray20", corner_radius=10)
        f_pix.pack(padx=20, pady=15, fill="x")
        
        ctk.CTkLabel(f_pix, text="CHAVE PIX:", font=("Arial", 10, "bold"), text_color="gray").pack(pady=(10, 0))
        entry_pix = ctk.CTkEntry(f_pix, placeholder_text="71982030433", width=250, justify="center", border_width=0)
        entry_pix.insert(0, "71 9.8203-0433")
        entry_pix.configure(state="readonly")
        entry_pix.pack(pady=10)

        ctk.CTkLabel(janela_apoio, text="Contato: cyber.souza@hotmail.com", font=("Arial", 11, "italic"), text_color="#1f538d").pack()
        
        btn_fechar = ctk.CTkButton(janela_apoio, text="Fechar", command=janela_apoio.destroy)
        btn_fechar.pack(pady=20)

    def iniciar_thread(self):
        if not self.caminho_imagem: return
        self.btn_gerar.configure(state="disabled")
        threading.Thread(target=self.processar_poster, daemon=True).start()

    def abrir_pasta_destino(self, pasta):
        """Abre a pasta de destino automaticamente no Windows Explorer"""
        try:
            os.startfile(os.path.normpath(pasta))
        except Exception as e:
            print(f"Erro ao abrir pasta: {e}")

    def processar_poster(self):
        try:
            m = float(self.entry_margem.get())
            u_w, u_h = self.get_dim_util()
            cols, rows = int(self.entry_pag_h.get()), int(self.entry_pag_v.get())
            total = cols * rows
            
            nome_limpo = self.entry_nome_pdf.get().strip()
            if not nome_limpo: nome_limpo = "Poster_Final"
            if not nome_limpo.lower().endswith(".pdf"): nome_limpo += ".pdf"

            folder = os.path.dirname(self.caminho_imagem) if self.radio_var.get() == 0 else self.diretorio_destino
            pdf_path = os.path.join(folder, nome_limpo)
            
            img = Image.open(self.caminho_imagem)
            orig_w, orig_h = img.size
            c = canvas.Canvas(pdf_path, pagesize=A4)
            chunk_w, chunk_h = orig_w / cols, orig_h / rows
            
            for r in range(rows):
                for c_idx in range(cols):
                    idx = (r * cols) + c_idx + 1
                    self.progresso.set(idx / total)
                    tile = img.crop((c_idx * chunk_w, r * chunk_h, (c_idx+1) * chunk_w, (r+1) * chunk_h))
                    t_path = os.path.join(folder, f"temp_{idx}.jpg")
                    tile.save(t_path, "JPEG", quality=95)
                    c.drawImage(t_path, m*cm, m*cm, width=u_w*cm, height=u_h*cm)
                    if self.switch_legendas.get():
                        c.setFont("Helvetica", 9)
                        c.drawString(m*cm, (m-0.4)*cm, f"Linha {r+1}, Coluna {c_idx+1} | Folha {idx}/{total}")
                    c.showPage()
                    os.remove(t_path)
            
            c.save()
            
            # Feedback e abertura automática da pasta
            self.abrir_pasta_destino(folder)
            messagebox.showinfo("Sucesso", f"PDF salvo como:\n{nome_limpo}\n\nA pasta de destino foi aberta automaticamente.")
            
        except Exception as e: messagebox.showerror("Erro", str(e))
        finally:
            self.btn_gerar.configure(state="normal")
            self.progresso.set(0)

if __name__ == "__main__":
    app = App()
    app.mainloop()