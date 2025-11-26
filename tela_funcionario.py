import customtkinter as ctk
from tkinter import messagebox
import subprocess
import sys
import json
import os
from database import (
    verificar_status_ponto, bater_ponto_entrada, bater_ponto_saida,
    listar_escalas_funcionario, obter_historico_ponto
)

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

# Tela do funcionário
tela = ctk.CTk()
tela.title(f"Sistema de Gestão - Funcionário: {usuario_logado['nome']}")
tela.geometry("700x650")
tela.resizable(False, False)

# Frame principal
frame_principal = ctk.CTkFrame(tela)
frame_principal.pack(fill="both", expand=True, padx=20, pady=20)

# Título e status
frame_header = ctk.CTkFrame(frame_principal)
frame_header.pack(fill="x", padx=20, pady=10)

titulo = ctk.CTkLabel(frame_header, text=f"👷 Olá, {usuario_logado['nome']}!", font=ctk.CTkFont(size=24, weight="bold"))
titulo.pack(pady=10)

# Status do ponto
status_atual = verificar_status_ponto(usuario_logado['id'])
cor_status = "green" if status_atual == "online" else "red"
texto_status = "🟢 ONLINE - Trabalhando" if status_atual == "online" else "🔴 OFFLINE"

label_status = ctk.CTkLabel(frame_header, text=f"Status: {texto_status}", 
                            font=ctk.CTkFont(size=16, weight="bold"),
                            text_color=cor_status)
label_status.pack(pady=5)

# Frame de registro de ponto
frame_ponto = ctk.CTkFrame(frame_principal)
frame_ponto.pack(fill="x", padx=20, pady=15)

ctk.CTkLabel(frame_ponto, text="⏰ Registro de Ponto", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=10)

frame_botoes_ponto = ctk.CTkFrame(frame_ponto)
frame_botoes_ponto.pack(pady=15)

def atualizar_status():
    status = verificar_status_ponto(usuario_logado['id'])
    cor = "green" if status == "online" else "red"
    texto = "🟢 ONLINE - Trabalhando" if status == "online" else "🔴 OFFLINE"
    label_status.configure(text=f"Status: {texto}", text_color=cor)
    atualizar_historico()

def bater_entrada():
    sucesso, mensagem = bater_ponto_entrada(usuario_logado['id'])
    if sucesso:
        messagebox.showinfo("Ponto Registrado", mensagem)
        atualizar_status()
    else:
        messagebox.showwarning("Aviso", mensagem)

def bater_saida():
    sucesso, mensagem = bater_ponto_saida(usuario_logado['id'])
    if sucesso:
        messagebox.showinfo("Ponto Registrado", mensagem)
        atualizar_status()
    else:
        messagebox.showwarning("Aviso", mensagem)

botao_entrada = ctk.CTkButton(frame_botoes_ponto, text="🟢 Bater Ponto ENTRADA", 
                              command=bater_entrada, width=200, height=50,
                              fg_color="green", hover_color="darkgreen",
                              font=ctk.CTkFont(size=14, weight="bold"))
botao_entrada.grid(row=0, column=0, padx=15)

botao_saida = ctk.CTkButton(frame_botoes_ponto, text="🔴 Bater Ponto SAÍDA", 
                            command=bater_saida, width=200, height=50,
                            fg_color="red", hover_color="darkred",
                            font=ctk.CTkFont(size=14, weight="bold"))
botao_saida.grid(row=0, column=1, padx=15)

# Frame de histórico de ponto
frame_historico = ctk.CTkFrame(frame_principal)
frame_historico.pack(fill="both", expand=True, padx=20, pady=10)

ctk.CTkLabel(frame_historico, text="📋 Histórico de Ponto", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=5)

scrollable_historico = ctk.CTkScrollableFrame(frame_historico, height=150)
scrollable_historico.pack(fill="both", expand=True, padx=10, pady=5)

# Cabeçalhos do histórico
frame_cab_hist = ctk.CTkFrame(scrollable_historico)
frame_cab_hist.pack(fill="x", pady=2)

ctk.CTkLabel(frame_cab_hist, text="Data", width=100, font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, padx=5)
ctk.CTkLabel(frame_cab_hist, text="Entrada", width=80, font=ctk.CTkFont(weight="bold")).grid(row=0, column=1, padx=5)
ctk.CTkLabel(frame_cab_hist, text="Saída", width=80, font=ctk.CTkFont(weight="bold")).grid(row=0, column=2, padx=5)
ctk.CTkLabel(frame_cab_hist, text="Status", width=80, font=ctk.CTkFont(weight="bold")).grid(row=0, column=3, padx=5)

lista_historico_widgets = []

def atualizar_historico():
    for widget in lista_historico_widgets:
        widget.destroy()
    lista_historico_widgets.clear()
    
    historico = obter_historico_ponto(usuario_logado['id'], 10)
    
    if not historico:
        frame_vazio = ctk.CTkFrame(scrollable_historico)
        frame_vazio.pack(fill="x", pady=10)
        lista_historico_widgets.append(frame_vazio)
        ctk.CTkLabel(frame_vazio, text="Nenhum registro de ponto encontrado", text_color="gray").pack()
        return
    
    for registro in historico:
        frame_reg = ctk.CTkFrame(scrollable_historico)
        frame_reg.pack(fill="x", pady=1)
        lista_historico_widgets.append(frame_reg)
        
        ctk.CTkLabel(frame_reg, text=registro[0], width=100).grid(row=0, column=0, padx=5)
        ctk.CTkLabel(frame_reg, text=registro[1] or "-", width=80).grid(row=0, column=1, padx=5)
        ctk.CTkLabel(frame_reg, text=registro[2] or "-", width=80).grid(row=0, column=2, padx=5)
        
        status_text = "🟢" if registro[3] == "online" else "🔴"
        ctk.CTkLabel(frame_reg, text=status_text, width=80).grid(row=0, column=3, padx=5)

atualizar_historico()

# Frame da escala
frame_escala = ctk.CTkFrame(frame_principal)
frame_escala.pack(fill="x", padx=20, pady=10)

ctk.CTkLabel(frame_escala, text="📅 Minha Escala", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=5)

def ver_escala():
    escalas = listar_escalas_funcionario(usuario_logado['id'])
    
    if not escalas:
        messagebox.showinfo("Escala", "Você não possui escalas cadastradas.")
        return
    
    texto_escalas = "Suas escalas:\n\n"
    for escala in escalas:
        status = "✅ Aprovada" if escala[4] == 1 else "⏳ Pendente"
        texto_escalas += f"📅 {escala[1]} | {escala[2]} | {escala[3]} | {status}\n"
    
    messagebox.showinfo("Minha Escala", texto_escalas)

botao_escala = ctk.CTkButton(frame_escala, text="📅 Ver Minha Escala", command=ver_escala, width=200)
botao_escala.pack(pady=10)

# Botão de logout
def fazer_logout():
    resposta = messagebox.askyesno("Logout", "Deseja realmente sair?")
    if resposta:
        # Remover arquivo de sessão
        if os.path.exists(SESSAO_PATH):
            os.remove(SESSAO_PATH)
        tela.destroy()
        subprocess.Popen([sys.executable, "tela_inicial.py"])

botao_logout = ctk.CTkButton(frame_principal, text="🚪 Sair (Logout)", command=fazer_logout, 
                             width=200, height=40, fg_color="gray", hover_color="darkgray")
botao_logout.pack(pady=15)

# Iniciar a tela
tela.mainloop()
