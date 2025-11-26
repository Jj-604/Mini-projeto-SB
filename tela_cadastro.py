import customtkinter as ctk
from database import cadastrar_usuario
from tkinter import messagebox
import subprocess
import sys

# Configurações de aparência
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# Tela de cadastro
tela = ctk.CTk()
tela.title("Sistema de Gestão - Cadastro")
tela.geometry("500x550")
tela.resizable(False, False)

# Frame principal centralizado
frame_principal = ctk.CTkFrame(tela)
frame_principal.place(relx=0.5, rely=0.5, anchor="center")

# Título
titulo = ctk.CTkLabel(frame_principal, text="Cadastro de Usuário", font=ctk.CTkFont(size=24, weight="bold"))
titulo.pack(pady=20, padx=40)

informacoes_iniciais = ctk.CTkLabel(frame_principal, text="Preencha os campos abaixo:", font=ctk.CTkFont(size=14))
informacoes_iniciais.pack(pady=10)

# Campo de nome completo
entrada_nome = ctk.CTkEntry(frame_principal, placeholder_text="Nome Completo", width=250, height=35)
entrada_nome.pack(pady=10)

# Campo de entrada para o nome de usuário
entrada_usuario = ctk.CTkEntry(frame_principal, placeholder_text="Nome de Usuário", width=250, height=35)
entrada_usuario.pack(pady=10)

# Campo de entrada para a senha
entrada_senha = ctk.CTkEntry(frame_principal, placeholder_text="Senha", show="*", width=250, height=35)
entrada_senha.pack(pady=10)

# Campo de confirmação de senha
entrada_confirma_senha = ctk.CTkEntry(frame_principal, placeholder_text="Confirmar Senha", show="*", width=250, height=35)
entrada_confirma_senha.pack(pady=10)

# Seleção de tipo de usuário
label_tipo = ctk.CTkLabel(frame_principal, text="Tipo de Usuário:", font=ctk.CTkFont(size=14))
label_tipo.pack(pady=(10, 5))

tipo_usuario = ctk.StringVar(value="funcionario")

frame_tipo = ctk.CTkFrame(frame_principal)
frame_tipo.pack(pady=5)

radio_funcionario = ctk.CTkRadioButton(frame_tipo, text="👷 Funcionário", variable=tipo_usuario, value="funcionario")
radio_funcionario.grid(row=0, column=0, padx=10)

radio_supervisor = ctk.CTkRadioButton(frame_tipo, text="👔 Supervisor", variable=tipo_usuario, value="supervisor")
radio_supervisor.grid(row=0, column=1, padx=10)

# Botão para fazer cadastro
def realizar_cadastro():
    nome = entrada_nome.get()
    usuario = entrada_usuario.get()
    senha = entrada_senha.get()
    confirma_senha = entrada_confirma_senha.get()
    tipo = tipo_usuario.get()
    
    if not nome or not usuario or not senha or not confirma_senha:
        messagebox.showwarning("Aviso", "Por favor, preencha todos os campos.")
        return
    
    if senha != confirma_senha:
        messagebox.showerror("Erro", "As senhas não coincidem.")
        return
    
    if len(senha) < 4:
        messagebox.showwarning("Aviso", "A senha deve ter pelo menos 4 caracteres.")
        return

    sucesso, mensagem = cadastrar_usuario(usuario, senha, nome, tipo)
    
    if sucesso:
        messagebox.showinfo("Sucesso", mensagem)
        tela.destroy()
        subprocess.Popen([sys.executable, "tela_login.py"])
    else:
        messagebox.showerror("Erro", mensagem)

botao_cadastro = ctk.CTkButton(frame_principal, text="Cadastrar", command=realizar_cadastro, width=250, height=40)
botao_cadastro.pack(pady=15)

# Botão para voltar
def voltar():
    tela.destroy()
    subprocess.Popen([sys.executable, "tela_inicial.py"])

botao_voltar = ctk.CTkButton(frame_principal, text="Voltar", command=voltar, width=250, height=40, fg_color="gray", hover_color="darkgray")
botao_voltar.pack(pady=5)

# Código para manter a janela aberta
tela.mainloop()
