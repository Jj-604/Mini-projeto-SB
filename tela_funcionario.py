import customtkinter as ctk
from tkinter import messagebox
import subprocess
import sys
import json
import os
from database import (
    verificar_status_ponto, bater_ponto_entrada, bater_ponto_saida,
    listar_escalas_funcionario, obter_historico_ponto,
    listar_notificacoes, marcar_notificacao_lida, atualizar_usuario,
    enviar_feedback
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

if not usuario_logado:
    messagebox.showerror("Erro", "Sessão expirada. Faça login novamente.")
    subprocess.Popen([sys.executable, "tela_login.py"])
    sys.exit()

class FuncionarioApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title(f"Sistema de Gestão - Funcionário: {usuario_logado['nome']}")
        self.geometry("800x700")
        center_window(self, 800, 700)

        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True, padx=20, pady=20)

        self.tab_ponto = self.tabview.add("⏰ Ponto & Escala")
        self.tab_notificacoes = self.tabview.add("🔔 Notificações")
        self.tab_feedback = self.tabview.add("💬 Ajuda & Feedback")
        self.tab_perfil = self.tabview.add("👤 Perfil")

        self.setup_tab_ponto()
        self.setup_tab_notificacoes()
        self.setup_tab_feedback()
        self.setup_tab_perfil()

        # Botão Sair
        ctk.CTkButton(self, text="Sair", command=self.fazer_logout, fg_color="red", hover_color="darkred").pack(pady=10)

        # Auto-atualização
        self.after(5000, self.auto_atualizar)

    def setup_tab_ponto(self):
        # Header
        ctk.CTkLabel(self.tab_ponto, text=f"Olá, {usuario_logado['nome']}!", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=10)
        
        self.label_status = ctk.CTkLabel(self.tab_ponto, text="Carregando status...", font=ctk.CTkFont(size=16, weight="bold"))
        self.label_status.pack(pady=5)

        # Botoes Ponto
        frame_btns = ctk.CTkFrame(self.tab_ponto)
        frame_btns.pack(pady=15)
        
        ctk.CTkButton(frame_btns, text="🟢 Entrada", command=self.bater_entrada, width=150, height=40, fg_color="green").pack(side="left", padx=10)
        ctk.CTkButton(frame_btns, text="🔴 Saída", command=self.bater_saida, width=150, height=40, fg_color="red").pack(side="left", padx=10)

        # Histórico
        ctk.CTkLabel(self.tab_ponto, text="Histórico Recente", font=ctk.CTkFont(weight="bold")).pack(pady=(20, 5))
        self.scroll_hist = ctk.CTkScrollableFrame(self.tab_ponto, height=150)
        self.scroll_hist.pack(fill="x", padx=10)
        
        # Escala
        ctk.CTkLabel(self.tab_ponto, text="Minha Escala", font=ctk.CTkFont(weight="bold")).pack(pady=(20, 5))
        self.scroll_escala = ctk.CTkScrollableFrame(self.tab_ponto, height=150)
        self.scroll_escala.pack(fill="x", padx=10)

        self.atualizar_dados_ponto()

    def setup_tab_notificacoes(self):
        ctk.CTkButton(self.tab_notificacoes, text="🔄 Atualizar", command=self.carregar_notificacoes).pack(pady=10)
        self.scroll_notif = ctk.CTkScrollableFrame(self.tab_notificacoes)
        self.scroll_notif.pack(fill="both", expand=True, padx=10, pady=5)
        self.carregar_notificacoes()

    def setup_tab_feedback(self):
        # Formulario
        frame_form = ctk.CTkFrame(self.tab_feedback)
        frame_form.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(frame_form, text="Envie seu feedback ou dúvida:", font=ctk.CTkFont(size=14)).pack(pady=5)
        self.entry_feedback = ctk.CTkTextbox(frame_form, height=100)
        self.entry_feedback.pack(fill="x", padx=10, pady=5)
        ctk.CTkButton(frame_form, text="Enviar Feedback", command=self.enviar_feedback_handler).pack(pady=5)

        # Lista de meus feedbacks
        ctk.CTkLabel(self.tab_feedback, text="Meus Feedbacks", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(20, 5))
        self.scroll_feedbacks = ctk.CTkScrollableFrame(self.tab_feedback)
        self.scroll_feedbacks.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.carregar_meus_feedbacks()

    def setup_tab_perfil(self):
        frame = ctk.CTkFrame(self.tab_perfil)
        frame.pack(pady=20, padx=20, fill="both")

        ctk.CTkLabel(frame, text="Alterar Senha", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)
        
        self.entry_nova_senha = ctk.CTkEntry(frame, placeholder_text="Nova Senha", show="*", width=200)
        self.entry_nova_senha.pack(pady=5)
        
        ctk.CTkButton(frame, text="Salvar Nova Senha", command=self.alterar_senha).pack(pady=10)
        
        # Tema
        ctk.CTkLabel(frame, text="Aparência").pack(pady=(20, 5))
        ctk.CTkSegmentedButton(frame, values=["Dark", "Light"], command=lambda m: ctk.set_appearance_mode(m)).pack(pady=5)

    # Lógica Ponto
    def bater_entrada(self):
        sucesso, msg = bater_ponto_entrada(usuario_logado['id'])
        messagebox.showinfo("Info", msg)
        self.atualizar_dados_ponto()

    def bater_saida(self):
        sucesso, msg = bater_ponto_saida(usuario_logado['id'])
        messagebox.showinfo("Info", msg)
        self.atualizar_dados_ponto()

    def atualizar_dados_ponto(self):
        # Status
        status = verificar_status_ponto(usuario_logado['id'])
        if status == "online":
            self.label_status.configure(text="🟢 ONLINE - Trabalhando", text_color="green")
        else:
            self.label_status.configure(text="🔴 OFFLINE", text_color="red")

        # Histórico
        for w in self.scroll_hist.winfo_children(): w.destroy()
        hist = obter_historico_ponto(usuario_logado['id'], 5)
        for h in hist:
            ctk.CTkLabel(self.scroll_hist, text=f"{h[0]} | {h[1] or '-'} - {h[2] or '-'}").pack(anchor="w", padx=5)

        # Escala
        for w in self.scroll_escala.winfo_children(): w.destroy()
        escalas = listar_escalas_funcionario(usuario_logado['id'])
        for e in escalas:
            status_esc = "✅" if e[4] else "⏳"
            ctk.CTkLabel(self.scroll_escala, text=f"{e[1]} ({e[2]}) - {status_esc}").pack(anchor="w", padx=5)

    # Lógica Notificações
    def carregar_notificacoes(self):
        for w in self.scroll_notif.winfo_children(): w.destroy()
        notifs = listar_notificacoes(usuario_logado['id'])
        
        if not notifs:
            ctk.CTkLabel(self.scroll_notif, text="Nenhuma nova notificação.").pack(pady=20)
            return

        for n in notifs:
            frame = ctk.CTkFrame(self.scroll_notif)
            frame.pack(fill="x", pady=2)
            ctk.CTkLabel(frame, text=n[1], wraplength=400).pack(side="left", padx=10, pady=5)
            ctk.CTkButton(frame, text="Lida", width=50, command=lambda nid=n[0]: self.marcar_lida(nid)).pack(side="right", padx=5)

    def marcar_lida(self, nid):
        marcar_notificacao_lida(nid)
        self.carregar_notificacoes()

    # Lógica Feedback
    def setup_tab_feedback(self):
        # Formulario
        frame_form = ctk.CTkFrame(self.tab_feedback)
        frame_form.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(frame_form, text="Envie seu feedback ou dúvida:", font=ctk.CTkFont(size=14)).pack(pady=5)
        self.entry_feedback = ctk.CTkTextbox(frame_form, height=100)
        self.entry_feedback.pack(fill="x", padx=10, pady=5)
        ctk.CTkButton(frame_form, text="Enviar Feedback", command=self.enviar_feedback_handler).pack(pady=5)

        # Lista de meus feedbacks
        ctk.CTkLabel(self.tab_feedback, text="Meus Feedbacks", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(20, 5))
        self.scroll_feedbacks = ctk.CTkScrollableFrame(self.tab_feedback)
        self.scroll_feedbacks.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.carregar_meus_feedbacks()

    def carregar_meus_feedbacks(self):
        for w in self.scroll_feedbacks.winfo_children(): w.destroy()
        
        from database import listar_meus_feedbacks
        feedbacks = listar_meus_feedbacks(usuario_logado['id'])
        
        if not feedbacks:
            ctk.CTkLabel(self.scroll_feedbacks, text="Você ainda não enviou nenhum feedback.").pack(pady=20)
            return

        for f in feedbacks:
            # f: mensagem, data, resposta, data_resposta
            card = ctk.CTkFrame(self.scroll_feedbacks)
            card.pack(fill="x", pady=5)
            
            header = ctk.CTkFrame(card, fg_color="transparent")
            header.pack(fill="x", padx=10, pady=5)
            ctk.CTkLabel(header, text=f"Enviado em: {f[1]}", font=ctk.CTkFont(size=11)).pack(side="left")
            
            status = "✅ Respondido" if f[2] else "⏳ Pendente"
            color = "green" if f[2] else "orange"
            ctk.CTkLabel(header, text=status, text_color=color, font=ctk.CTkFont(weight="bold")).pack(side="right")

            ctk.CTkLabel(card, text=f[0], wraplength=600, justify="left").pack(anchor="w", padx=10, pady=(0, 10))

            if f[2]:
                reply_frame = ctk.CTkFrame(card, fg_color=("gray85", "gray20"))
                reply_frame.pack(fill="x", padx=10, pady=(0, 10))
                ctk.CTkLabel(reply_frame, text=f"Resposta ({f[3]}):", font=ctk.CTkFont(size=11, weight="bold")).pack(anchor="w", padx=5, pady=2)
                ctk.CTkLabel(reply_frame, text=f[2], wraplength=580, justify="left").pack(anchor="w", padx=5, pady=(0, 5))

    def enviar_feedback_handler(self):
        msg = self.entry_feedback.get("1.0", "end-1c")
        if not msg.strip():
            messagebox.showwarning("Aviso", "Escreva uma mensagem.")
            return
        
        if enviar_feedback(usuario_logado['id'], msg):
            messagebox.showinfo("Sucesso", "Feedback enviado!")
            self.entry_feedback.delete("1.0", "end")
            self.carregar_meus_feedbacks()
        else:
            messagebox.showerror("Erro", "Falha ao enviar.")

    # Lógica Perfil
    def alterar_senha(self):
        nova = self.entry_nova_senha.get()
        if len(nova) < 4:
            messagebox.showwarning("Erro", "Senha muito curta (min 4 chars)")
            return
        
        if atualizar_usuario(usuario_logado['id'], usuario_logado['nome'], usuario_logado['usuario'], nova):
            messagebox.showinfo("Sucesso", "Senha alterada!")
            self.entry_nova_senha.delete(0, 'end')
        else:
            messagebox.showerror("Erro", "Falha ao atualizar senha")

    def auto_atualizar(self):
        self.atualizar_dados_ponto()
        self.after(5000, self.auto_atualizar)

    def fazer_logout(self):
        if messagebox.askyesno("Logout", "Deseja realmente sair?"):
            if os.path.exists(SESSAO_PATH):
                os.remove(SESSAO_PATH)
            self.destroy()
            subprocess.Popen([sys.executable, "tela_login.py"])

if __name__ == "__main__":
    app = FuncionarioApp()
    app.mainloop()
