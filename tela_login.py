import customtkinter as ctk
from database import verificar_usuario
from tkinter import messagebox
import subprocess
import sys
import json
import os
import constants as const

# Configurações de aparência
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# Arquivo para armazenar dados do usuário logado
SESSAO_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sessao.json')

def salvar_sessao(usuario_data):
    with open(SESSAO_PATH, 'w') as f:
        json.dump(usuario_data, f)

# Tela de login
tela = ctk.CTk()
tela.title(const.TITULO_JANELA_LOGIN)
tela.geometry("500x400")
tela.resizable(False, False)

# Frame principal centralizado
frame_principal = ctk.CTkFrame(tela)
frame_principal.place(relx=0.5, rely=0.5, anchor="center")

# Título
titulo = ctk.CTkLabel(frame_principal, text=const.LABEL_LOGIN, font=ctk.CTkFont(size=24, weight="bold"))
titulo.pack(pady=20, padx=40)

informacoes_iniciais = ctk.CTkLabel(frame_principal, text=const.LABEL_PREENCHA_CAMPOS, font=ctk.CTkFont(size=14))
informacoes_iniciais.pack(pady=10)

# Campo de entrada para o nome de usuário
entrada_usuario = ctk.CTkEntry(frame_principal, placeholder_text=const.PLACEHOLDER_NOME_USUARIO, width=250, height=35)
entrada_usuario.pack(pady=10)

# Campo de entrada para a senha
entrada_senha = ctk.CTkEntry(frame_principal, placeholder_text=const.PLACEHOLDER_SENHA, show="*", width=250, height=35)
entrada_senha.pack(pady=10)

# Botão para fazer login
def realizar_login():
    usuario = entrada_usuario.get()
    senha = entrada_senha.get()
    
    if not usuario or not senha:
        messagebox.showwarning(const.TITULO_AVISO, const.MSG_PREENCHA_CAMPOS)
        return

    sucesso, mensagem, usuario_data = verificar_usuario(usuario, senha)
    
    if sucesso:
        # Salvar dados do usuário na sessão
        salvar_sessao(usuario_data)
        
        messagebox.showinfo(const.TITULO_SUCESSO, const.MSG_BEM_VINDO.format(usuario_data['nome']))
        tela.destroy()
        
        # Redirecionar baseado no tipo de usuário
        if usuario_data['tipo'] == 'supervisor':
            subprocess.Popen([sys.executable, "tela_supervisor.py"])
        else:
            subprocess.Popen([sys.executable, "tela_funcionario.py"])
    else:
        messagebox.showerror(const.TITULO_ERRO, mensagem)

botao_login = ctk.CTkButton(frame_principal, text=const.BOTAO_ENTRAR, command=realizar_login, width=250, height=40)
botao_login.pack(pady=15)

# Botão para voltar
def voltar():
    tela.destroy()
    subprocess.Popen([sys.executable, "tela_inicial.py"])

botao_voltar = ctk.CTkButton(frame_principal, text=const.BOTAO_VOLTAR, command=voltar, width=250, height=40, fg_color="gray", hover_color="darkgray")
botao_voltar.pack(pady=5)

# Código para manter a janela aberta
tela.mainloop()