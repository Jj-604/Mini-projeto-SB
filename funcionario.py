# Este arquivo foi substituído pelas funções em database.py
# Mantido para compatibilidade, mas não é mais utilizado

import customtkinter as ctk
import subprocess
import sys

# Configurações de aparência
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# Tela inicial do funcionário
tela = ctk.CTk()
tela.title("Sistema de Gestão - Área do Funcionário")
tela.geometry("600x400")
tela.resizable(False, False)

# Frame principal centralizado
frame_principal = ctk.CTkFrame(tela)
frame_principal.place(relx=0.5, rely=0.5, anchor="center")

# Título
titulo = ctk.CTkLabel(frame_principal, text="Área do Funcionário", font=ctk.CTkFont(size=24, weight="bold"))
titulo.pack(pady=20, padx=40)

subtitulo = ctk.CTkLabel(frame_principal, text="Bem-vindo à área do funcionário", font=ctk.CTkFont(size=14))
subtitulo.pack(pady=10)

# Botão para ver escala
def abrir_escala():
    tela.destroy()
    subprocess.Popen([sys.executable, "escala_funcionario.py"])

botao_escala = ctk.CTkButton(frame_principal, text="📅 Ver Minha Escala", command=abrir_escala, width=200, height=40)
botao_escala.pack(pady=10)

# Botão para voltar
def voltar():
    tela.destroy()
    subprocess.Popen([sys.executable, "tela_inicial.py"])

botao_voltar = ctk.CTkButton(frame_principal, text="⬅️ Voltar", command=voltar, width=200, height=40, fg_color="gray", hover_color="darkgray")
botao_voltar.pack(pady=20)

# Iniciar a tela
tela.mainloop()