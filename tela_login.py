import customtkinter as ctk
from database import verificar_usuario
from tkinter import messagebox
import subprocess
import sys
import os

# configurações de aparência
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# tela de login
tela = ctk.CTk()
tela.title("Tela de Login")
tela.geometry("1920x1080")

informacoes_iniciais = ctk.CTkLabel(tela, text="Faça login preenchendo os campos abaixo:")
informacoes_iniciais.grid(column=0, row=0, padx=10, pady=10)

# campo de entrada para o nome de usuário
entrada_usuario = ctk.CTkEntry(tela, placeholder_text="Nome de Usuário")
entrada_usuario.grid(column=0, row=1, padx=10, pady=10)

# campo de entrada para a senha
entrada_senha = ctk.CTkEntry(tela, placeholder_text="Senha", show="*")
entrada_senha.grid(column=0, row=2, padx=10, pady=10)

# botão para fazer login
def realizar_login():
    usuario = entrada_usuario.get()
    senha = entrada_senha.get()
    
    if not usuario or not senha:
        messagebox.showwarning("Aviso", "Por favor, preencha todos os campos.")
        return

    sucesso, mensagem = verificar_usuario(usuario, senha)
    
    if sucesso:
        messagebox.showinfo("Sucesso", mensagem)
        tela.destroy()
        # Reabre a tela inicial
        subprocess.Popen([sys.executable, "tela_inicial.py"])
    else:
        messagebox.showerror("Erro", mensagem)

botao_login = ctk.CTkButton(tela, text="Fazer Login", command=realizar_login)
botao_login.grid(column=0, row=3, padx=10, pady=10)
# código para manter a janela aberta
tela.mainloop()