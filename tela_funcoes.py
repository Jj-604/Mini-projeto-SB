import customtkinter as ctk
import subprocess
import sys

# Configurações de aparência
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# Tela de funções
tela = ctk.CTk()
tela.title("Sistema de Gestão - Menu Principal")
tela.geometry("600x500")
tela.resizable(False, False)

# Frame principal centralizado
frame_principal = ctk.CTkFrame(tela)
frame_principal.place(relx=0.5, rely=0.5, anchor="center")

# Título
titulo = ctk.CTkLabel(frame_principal, text="Menu Principal", font=ctk.CTkFont(size=24, weight="bold"))
titulo.pack(pady=20, padx=50)

informacoes_iniciais = ctk.CTkLabel(frame_principal, text="Escolha uma das opções abaixo:", font=ctk.CTkFont(size=14))
informacoes_iniciais.pack(pady=10)

# Botão para Informações sobre Escala
def abrir_informacoes_escala():
    tela.destroy()
    subprocess.Popen([sys.executable, "informacoes_escala.py"])

botao_escala = ctk.CTkButton(frame_principal, text="📅 Informações sobre Escala", command=abrir_informacoes_escala, width=280, height=45)
botao_escala.pack(pady=10)

# Botão para Funcionários Logados
def abrir_funcionarios_logados():
    tela.destroy()
    subprocess.Popen([sys.executable, "funcionarios_logados.py"])

botao_logados = ctk.CTkButton(frame_principal, text="👥 Funcionários Logados", command=abrir_funcionarios_logados, width=280, height=45)
botao_logados.pack(pady=10)

# Botão para CRUD de Funcionários
def abrir_crud():
    tela.destroy()
    subprocess.Popen([sys.executable, "crud.py"])

botao_crud = ctk.CTkButton(frame_principal, text="⚙️ Gerenciar Funcionários (CRUD)", command=abrir_crud, width=280, height=45)
botao_crud.pack(pady=10)

# Botão para Logout
def fazer_logout():
    from tkinter import messagebox
    resposta = messagebox.askyesno("Logout", "Deseja realmente sair?")
    if resposta:
        tela.destroy()
        subprocess.Popen([sys.executable, "tela_inicial.py"])

botao_logout = ctk.CTkButton(frame_principal, text="🚪 Sair (Logout)", command=fazer_logout, width=280, height=45, fg_color="red", hover_color="darkred")
botao_logout.pack(pady=20)

# Código para manter a janela aberta
tela.mainloop()