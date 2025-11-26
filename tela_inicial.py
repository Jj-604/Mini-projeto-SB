import customtkinter as ctk
import subprocess
import sys

# Configurações de aparência
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# Tela inicial
tela = ctk.CTk()
tela.title("Sistema de Gestão - Tela Inicial")
tela.geometry("600x400")
tela.resizable(False, False)

# Frame principal centralizado
frame_principal = ctk.CTkFrame(tela)
frame_principal.place(relx=0.5, rely=0.5, anchor="center")

# Título
titulo = ctk.CTkLabel(frame_principal, text="Bem-vindo ao Sistema de Gestão", font=ctk.CTkFont(size=24, weight="bold"))
titulo.pack(pady=30, padx=40)

subtitulo = ctk.CTkLabel(frame_principal, text="Escolha uma opção para continuar:", font=ctk.CTkFont(size=14))
subtitulo.pack(pady=10)

# Botão para cadastrar novo usuário
def cadastrar_usuario():
    tela.destroy()
    subprocess.Popen([sys.executable, "tela_cadastro.py"])

botao_cadastrar = ctk.CTkButton(frame_principal, text="Cadastrar Novo Usuário", command=cadastrar_usuario, width=200, height=40)
botao_cadastrar.pack(pady=10)

# Botão para fazer login
def fazer_login():
    tela.destroy()
    subprocess.Popen([sys.executable, "tela_login.py"])

botao_login = ctk.CTkButton(frame_principal, text="Fazer Login", command=fazer_login, width=200, height=40)
botao_login.pack(pady=10)

# Botão para sair
def sair():
    tela.destroy()

botao_sair = ctk.CTkButton(frame_principal, text="Sair", command=sair, width=200, height=40, fg_color="red", hover_color="darkred")
botao_sair.pack(pady=20)

# Código para manter a janela aberta
tela.mainloop()