import customtkinter as ctk
from tkinter import messagebox, filedialog
import subprocess
import sys
import json
import os
import csv
from database import (
    listar_funcionarios_online, listar_funcionarios_offline,
    listar_escalas, listar_funcionarios, adicionar_escala, aprovar_escala,
    cadastrar_usuario, atualizar_usuario, deletar_usuario, exportar_relatorio_ponto,
    listar_feedbacks, criar_notificacao, obter_usuario_id_por_feedback, obter_usuario_id_por_escala
)
from utils import center_window

# Configurações de aparência
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# Carregar dados do usuário logado
SESSAO_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sessao.json')

def carregar_sessao():
    try:
        with open(SESSAO_PATH, 'r') as f:
            return json.load(f)
    except:
        return None

usuario_logado = carregar_sessao()

if not usuario_logado or usuario_logado['tipo'] != 'supervisor':
    messagebox.showerror("Erro", "Acesso negado. Você precisa ser supervisor.")
    subprocess.Popen([sys.executable, "tela_login.py"])
    sys.exit()

class SupervisorApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title(f"Sistema de Gestão - Supervisor: {usuario_logado['nome']}")
        self.geometry("1100x700")
        center_window(self, 1100, 700)

        # Layout principal (Grid 1x2)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(7, weight=1)

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="ATLAS\nGestão", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.btn_dashboard = self.create_sidebar_button("Dashboard", self.show_dashboard)
        self.btn_dashboard.grid(row=1, column=0, padx=20, pady=10)

        self.btn_funcionarios = self.create_sidebar_button("Funcionários", self.show_funcionarios)
        self.btn_funcionarios.grid(row=2, column=0, padx=20, pady=10)

        self.btn_escalas = self.create_sidebar_button("Escalas", self.show_escalas)
        self.btn_escalas.grid(row=3, column=0, padx=20, pady=10)
        
        self.btn_relatorios = self.create_sidebar_button("Relatórios", self.show_relatorios)
        self.btn_relatorios.grid(row=4, column=0, padx=20, pady=10)

        self.btn_feedbacks = self.create_sidebar_button("Feedbacks", self.show_feedbacks)
        self.btn_feedbacks.grid(row=5, column=0, padx=20, pady=10)

        self.btn_settings = self.create_sidebar_button("Configurações", self.show_settings)
        self.btn_settings.grid(row=6, column=0, padx=20, pady=10)

        self.btn_sair = ctk.CTkButton(self.sidebar_frame, text="Sair", command=self.fazer_logout, fg_color="red", hover_color="darkred")
        self.btn_sair.grid(row=8, column=0, padx=20, pady=20)

        # Área de Conteúdo
        self.content_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.content_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        # Inicializar telas
        self.show_dashboard()

    def create_sidebar_button(self, text, command):
        return ctk.CTkButton(self.sidebar_frame, text=text, command=command, 
                             fg_color="transparent", text_color=("gray10", "gray90"), 
                             hover_color=("gray70", "gray30"), anchor="w")

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def fazer_logout(self):
        if messagebox.askyesno("Logout", "Deseja realmente sair?"):
            if os.path.exists(SESSAO_PATH):
                os.remove(SESSAO_PATH)
            self.destroy()
            subprocess.Popen([sys.executable, "tela_login.py"])

    # ==================== DASHBOARD ====================
    def show_dashboard(self):
        self.clear_content()
        
        ctk.CTkLabel(self.content_frame, text="Painel de Controle", font=ctk.CTkFont(size=24, weight="bold")).pack(anchor="w", pady=(0, 20))

        # Cards de resumo
        frame_cards = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        frame_cards.pack(fill="x", pady=10)

        online = len(listar_funcionarios_online())
        total_funcs = len(listar_funcionarios())
        
        self.create_card(frame_cards, "Funcionários Online", str(online), "green").pack(side="left", padx=10, expand=True, fill="x")
        self.create_card(frame_cards, "Total Funcionários", str(total_funcs), "blue").pack(side="left", padx=10, expand=True, fill="x")

        # Listas rápidas
        frame_lists = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        frame_lists.pack(fill="both", expand=True, pady=20)

        # Online
        frame_online = ctk.CTkFrame(frame_lists)
        frame_online.pack(side="left", fill="both", expand=True, padx=10)
        ctk.CTkLabel(frame_online, text="🟢 Online Agora", font=ctk.CTkFont(weight="bold")).pack(pady=10)
        self.scroll_online = ctk.CTkScrollableFrame(frame_online)
        self.scroll_online.pack(fill="both", expand=True, padx=5, pady=5)
        self.update_online_list()

        # Offline
        frame_offline = ctk.CTkFrame(frame_lists)
        frame_offline.pack(side="right", fill="both", expand=True, padx=10)
        ctk.CTkLabel(frame_offline, text="🔴 Saídas Recentes", font=ctk.CTkFont(weight="bold")).pack(pady=10)
        self.scroll_offline = ctk.CTkScrollableFrame(frame_offline)
        self.scroll_offline.pack(fill="both", expand=True, padx=5, pady=5)
        self.update_offline_list()

    def create_card(self, parent, title, value, color):
        card = ctk.CTkFrame(parent, fg_color=color)
        ctk.CTkLabel(card, text=title, text_color="white").pack(pady=(10, 0))
        ctk.CTkLabel(card, text=value, font=ctk.CTkFont(size=30, weight="bold"), text_color="white").pack(pady=(0, 10))
        return card

    def update_online_list(self):
        for w in self.scroll_online.winfo_children(): w.destroy()
        for f in listar_funcionarios_online():
            ctk.CTkLabel(self.scroll_online, text=f"{f[1]} - {f[3]}").pack(anchor="w", padx=5)

    def update_offline_list(self):
        for w in self.scroll_offline.winfo_children(): w.destroy()
        for f in listar_funcionarios_offline():
            ctk.CTkLabel(self.scroll_offline, text=f"{f[1]} - {f[4]}").pack(anchor="w", padx=5)

    # ==================== FUNCIONÁRIOS (CRUD) ====================
    def show_funcionarios(self):
        self.clear_content()
        ctk.CTkLabel(self.content_frame, text="Gerenciar Funcionários", font=ctk.CTkFont(size=24, weight="bold")).pack(anchor="w", pady=(0, 20))

        # Botão Adicionar
        ctk.CTkButton(self.content_frame, text="+ Adicionar Funcionário", command=self.modal_adicionar_funcionario).pack(anchor="w", pady=10)

        # Lista
        self.scroll_funcs = ctk.CTkScrollableFrame(self.content_frame)
        self.scroll_funcs.pack(fill="both", expand=True)
        self.update_funcs_list()

    def update_funcs_list(self):
        for w in self.scroll_funcs.winfo_children(): w.destroy()
        
        funcs = listar_funcionarios()
        for f in funcs:
            row = ctk.CTkFrame(self.scroll_funcs)
            row.pack(fill="x", pady=2)
            
            ctk.CTkLabel(row, text=f"{f[2]} ({f[1]})", width=300, anchor="w").pack(side="left", padx=10)
            
            ctk.CTkButton(row, text="Editar", width=60, fg_color="orange", command=lambda id=f[0], n=f[2], u=f[1]: self.modal_editar_funcionario(id, n, u)).pack(side="right", padx=5)
            ctk.CTkButton(row, text="Excluir", width=60, fg_color="red", command=lambda id=f[0]: self.deletar_func(id)).pack(side="right", padx=5)

    def deletar_func(self, id):
        if messagebox.askyesno("Confirmar", "Tem certeza que deseja excluir este funcionário?"):
            deletar_usuario(id)
            self.update_funcs_list()

    def modal_adicionar_funcionario(self):
        self.modal_form("Adicionar Funcionário", self.save_new_func)

    def modal_editar_funcionario(self, id, nome, usuario):
        self.modal_form("Editar Funcionário", lambda n, u, s: self.save_edit_func(id, n, u, s), nome, usuario)

    def modal_form(self, title, save_command, nome_val="", user_val=""):
        top = ctk.CTkToplevel(self)
        top.title(title)
        top.geometry("400x300")
        top.transient(self)
        center_window(top, 400, 300)

        ctk.CTkLabel(top, text="Nome Completo:").pack(pady=5)
        entry_nome = ctk.CTkEntry(top, width=250)
        entry_nome.insert(0, nome_val)
        entry_nome.pack(pady=5)

        ctk.CTkLabel(top, text="Usuário:").pack(pady=5)
        entry_user = ctk.CTkEntry(top, width=250)
        entry_user.insert(0, user_val)
        entry_user.pack(pady=5)

        ctk.CTkLabel(top, text="Senha (deixe vazio para manter):" if user_val else "Senha:").pack(pady=5)
        entry_pass = ctk.CTkEntry(top, width=250, show="*")
        entry_pass.pack(pady=5)

        def submit():
            save_command(entry_nome.get(), entry_user.get(), entry_pass.get())
            top.destroy()
            self.update_funcs_list()

        ctk.CTkButton(top, text="Salvar", command=submit).pack(pady=20)

    def save_new_func(self, nome, user, password):
        if not nome or not user or not password:
            messagebox.showwarning("Erro", "Preencha todos os campos")
            return
        cadastrar_usuario(user, password, nome)

    def save_edit_func(self, id, nome, user, password):
        atualizar_usuario(id, nome, user, password if password else None)

    # ==================== ESCALAS ====================
    def show_escalas(self):
        self.clear_content()
        ctk.CTkLabel(self.content_frame, text="Gerenciar Escalas", font=ctk.CTkFont(size=24, weight="bold")).pack(anchor="w", pady=(0, 20))

        # Form Adicionar
        frame_add = ctk.CTkFrame(self.content_frame)
        frame_add.pack(fill="x", pady=10)
        
        ctk.CTkLabel(frame_add, text="Nova Escala:").pack(side="left", padx=10)
        
        self.combo_funcs = ctk.CTkComboBox(frame_add, values=[f[2] for f in listar_funcionarios()])
        self.combo_funcs.pack(side="left", padx=5)
        
        self.entry_data = ctk.CTkEntry(frame_add, placeholder_text="YYYY-MM-DD")
        self.entry_data.pack(side="left", padx=5)
        
        self.combo_turno = ctk.CTkComboBox(frame_add, values=["Manhã", "Tarde", "Noite"])
        self.combo_turno.pack(side="left", padx=5)
        
        ctk.CTkButton(frame_add, text="Adicionar", command=self.add_escala_handler).pack(side="left", padx=10)

        # Lista
        self.scroll_escalas = ctk.CTkScrollableFrame(self.content_frame)
        self.scroll_escalas.pack(fill="both", expand=True)
        self.update_escalas_list()

    def add_escala_handler(self):
        nome = self.combo_funcs.get()
        data = self.entry_data.get()
        turno = self.combo_turno.get()
        
        # Encontrar ID pelo nome (simplificado)
        funcs = listar_funcionarios()
        user_id = next((f[0] for f in funcs if f[2] == nome), None)
        
        if user_id and data:
            adicionar_escala(user_id, data, turno)
            criar_notificacao(user_id, f"Nova escala adicionada: {data} - {turno}")
            self.update_escalas_list()
        else:
            messagebox.showerror("Erro", "Dados inválidos")

    def update_escalas_list(self):
        for w in self.scroll_escalas.winfo_children(): w.destroy()
        for e in listar_escalas():
            row = ctk.CTkFrame(self.scroll_escalas)
            row.pack(fill="x", pady=2)
            
            status = "✅" if e[5] else "⏳"
            ctk.CTkLabel(row, text=f"{e[1]} | {e[2]} | {e[3]} | {status}").pack(side="left", padx=10)
            
            if not e[5]:
                ctk.CTkButton(row, text="Aprovar", width=60, fg_color="green", command=lambda id=e[0]: self.aprovar_esc_handler(id)).pack(side="right", padx=5)

    def aprovar_esc_handler(self, id):
        aprovar_escala(id)
        uid = obter_usuario_id_por_escala(id)
        if uid:
            criar_notificacao(uid, "Sua escala foi aprovada pelo supervisor.")
        self.update_escalas_list()

    # ==================== RELATÓRIOS ====================
    def show_relatorios(self):
        self.clear_content()
        ctk.CTkLabel(self.content_frame, text="Relatórios", font=ctk.CTkFont(size=24, weight="bold")).pack(anchor="w", pady=(0, 20))
        
        ctk.CTkLabel(self.content_frame, text="Exportar dados de ponto para CSV").pack(pady=10)
        
        ctk.CTkButton(self.content_frame, text="📥 Baixar Relatório de Ponto", command=self.baixar_relatorio).pack(pady=10)

    def baixar_relatorio(self):
        dados = exportar_relatorio_ponto()
        if not dados:
            messagebox.showinfo("Info", "Sem dados para exportar.")
            return
            
        filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        if filename:
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["Nome", "Data", "Entrada", "Saída"])
                writer.writerows(dados)
            messagebox.showinfo("Sucesso", "Relatório exportado!")

    # ==================== FEEDBACKS ====================
    def show_feedbacks(self):
        self.clear_content()
        ctk.CTkLabel(self.content_frame, text="Feedbacks dos Usuários", font=ctk.CTkFont(size=24, weight="bold")).pack(anchor="w", pady=(0, 20))

        self.scroll_feedbacks = ctk.CTkScrollableFrame(self.content_frame)
        self.scroll_feedbacks.pack(fill="both", expand=True)
        
        self.update_feedbacks_list()

    def update_feedbacks_list(self):
        for w in self.scroll_feedbacks.winfo_children(): w.destroy()
        
        feedbacks = listar_feedbacks()
        if not feedbacks:
            ctk.CTkLabel(self.scroll_feedbacks, text="Nenhum feedback recebido.").pack(pady=20)
            return

        for f in feedbacks:
            # f: id, nome, mensagem, data, resposta, data_resposta
            card = ctk.CTkFrame(self.scroll_feedbacks)
            card.pack(fill="x", pady=5)
            
            header = ctk.CTkFrame(card, fg_color="transparent")
            header.pack(fill="x", padx=10, pady=5)
            
            ctk.CTkLabel(header, text=f"{f[1]} ({f[3]})", font=ctk.CTkFont(weight="bold")).pack(side="left")
            
            status = "✅ Respondido" if f[4] else "⏳ Pendente"
            color = "green" if f[4] else "orange"
            ctk.CTkLabel(header, text=status, text_color=color).pack(side="right")

            ctk.CTkLabel(card, text=f[2], wraplength=600, justify="left").pack(anchor="w", padx=10, pady=(0, 10))

            if f[4]:
                reply_frame = ctk.CTkFrame(card, fg_color=("gray85", "gray20"))
                reply_frame.pack(fill="x", padx=10, pady=(0, 10))
                ctk.CTkLabel(reply_frame, text=f"Resposta ({f[5]}):", font=ctk.CTkFont(size=11, weight="bold")).pack(anchor="w", padx=5, pady=2)
                ctk.CTkLabel(reply_frame, text=f[4], wraplength=580, justify="left").pack(anchor="w", padx=5, pady=(0, 5))
            else:
                ctk.CTkButton(card, text="Responder", height=25, command=lambda id=f[0]: self.reply_modal(id)).pack(anchor="e", padx=10, pady=(0, 10))

    def reply_modal(self, feedback_id):
        top = ctk.CTkToplevel(self)
        top.title("Responder Feedback")
        top.geometry("400x300")
        top.transient(self)
        center_window(top, 400, 300)

        ctk.CTkLabel(top, text="Sua Resposta:").pack(pady=10)
        txt_resposta = ctk.CTkTextbox(top, width=350, height=150)
        txt_resposta.pack(pady=5)

        def submit():
            resp = txt_resposta.get("1.0", "end-1c")
            if not resp.strip():
                messagebox.showwarning("Aviso", "Digite uma resposta.")
                return
            
            from database import responder_feedback
            if responder_feedback(feedback_id, resp):
                uid = obter_usuario_id_por_feedback(feedback_id)
                if uid:
                    criar_notificacao(uid, "O supervisor respondeu seu feedback.")
                
                messagebox.showinfo("Sucesso", "Resposta enviada!")
                top.destroy()
                self.update_feedbacks_list()
            else:
                messagebox.showerror("Erro", "Falha ao enviar resposta.")

        ctk.CTkButton(top, text="Enviar", command=submit).pack(pady=20)

    # ==================== CONFIGURAÇÕES ====================
    def show_settings(self):
        self.clear_content()
        ctk.CTkLabel(self.content_frame, text="Configurações", font=ctk.CTkFont(size=24, weight="bold")).pack(anchor="w", pady=(0, 20))

        # Tema
        ctk.CTkLabel(self.content_frame, text="Aparência").pack(anchor="w", pady=10)
        
        def change_theme(mode):
            ctk.set_appearance_mode(mode)

        ctk.CTkSegmentedButton(self.content_frame, values=["Dark", "Light"], command=change_theme).pack(anchor="w", pady=5)

        # Sobre
        ctk.CTkLabel(self.content_frame, text="Sobre o Sistema", font=ctk.CTkFont(size=18, weight="bold")).pack(anchor="w", pady=(30, 10))
        ctk.CTkLabel(self.content_frame, text="Projeto ATLAS v2.0\nDesenvolvido para gestão eficiente de equipes.").pack(anchor="w")

if __name__ == "__main__":
    app = SupervisorApp()
    app.mainloop()
