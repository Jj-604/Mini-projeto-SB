import customtkinter as ctk
import subprocess
import sys
import constants as const

# Configurações de aparência
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# Tela inicial
tela = ctk.CTk()
tela.title(const.TITULO_JANELA_INICIAL)
tela.geometry("600x500")
tela.resizable(False, False)

# Frame principal centralizado
frame_principal = ctk.CTkFrame(tela)
frame_principal.place(relx=0.5, rely=0.5, anchor="center")

# Título
titulo = ctk.CTkLabel(frame_principal, text=const.LABEL_BEM_VINDO, font=ctk.CTkFont(size=24, weight="bold"))
titulo.pack(pady=30, padx=40)

subtitulo = ctk.CTkLabel(frame_principal, text=const.LABEL_ESCOLHA_OPCAO, font=ctk.CTkFont(size=14))
subtitulo.pack(pady=10)

# Botão para cadastrar novo usuário
def cadastrar_usuario():
    tela.destroy()
    subprocess.Popen([sys.executable, "tela_cadastro.py"])

botao_cadastrar = ctk.CTkButton(frame_principal, text=const.BOTAO_CADASTRAR_NOVO_USUARIO, command=cadastrar_usuario, width=200, height=40)
botao_cadastrar.pack(pady=10)

# Botão para fazer login
def fazer_login():
    tela.destroy()
    subprocess.Popen([sys.executable, "tela_login.py"])

botao_login = ctk.CTkButton(frame_principal, text=const.BOTAO_FAZER_LOGIN, command=fazer_login, width=200, height=40)
botao_login.pack(pady=10)

# Botão para sair
def sair():
    tela.destroy()

botao_sair = ctk.CTkButton(frame_principal, text=const.BOTAO_SAIR, command=sair, width=200, height=40, fg_color="red", hover_color="darkred")
botao_sair.pack(pady=20)

# Aviso acadêmico
aviso = ctk.CTkLabel(frame_principal, text=const.AVISO_ACADEMICO, font=ctk.CTkFont(size=12), text_color="#FF5555")
aviso.pack(pady=(0, 20))

# Código para manter a janela aberta
tela.mainloop()