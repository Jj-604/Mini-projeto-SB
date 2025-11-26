import customtkinter as ctk
from tkinter import messagebox
import subprocess
import sys

# Configurações de aparência
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# Tela de escala do funcionário
tela = ctk.CTk()
tela.title("Sistema de Gestão - Minha Escala")
tela.geometry("700x600")
tela.resizable(False, False)

# Frame principal
frame_principal = ctk.CTkFrame(tela)
frame_principal.pack(fill="both", expand=True, padx=20, pady=20)

# Título
titulo = ctk.CTkLabel(frame_principal, text="Minha Escala", font=ctk.CTkFont(size=24, weight="bold"))
titulo.pack(pady=15)

# Seções de informação
frame_escala = ctk.CTkFrame(frame_principal)
frame_escala.pack(fill="x", padx=20, pady=10)

ctk.CTkLabel(frame_escala, text="📅 Sua Escala Atual", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=10)
ctk.CTkLabel(frame_escala, text="Aqui você pode visualizar sua escala de trabalho", font=ctk.CTkFont(size=14)).pack(pady=5)

# Frame para solicitar troca
frame_troca = ctk.CTkFrame(frame_principal)
frame_troca.pack(fill="x", padx=20, pady=10)

ctk.CTkLabel(frame_troca, text="🔄 Solicitar Troca de Turno", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=10)

def solicitar_troca():
    messagebox.showinfo("Troca de Turno", "Solicitação de troca de turno enviada para aprovação!")

botao_solicitar_troca = ctk.CTkButton(frame_troca, text="Solicitar Troca", command=solicitar_troca, width=200)
botao_solicitar_troca.pack(pady=10)

# Frame para informações adicionais
frame_info = ctk.CTkFrame(frame_principal)
frame_info.pack(fill="x", padx=20, pady=10)

# Grid de informações
ctk.CTkLabel(frame_info, text="📋 Informações", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)

frame_grid = ctk.CTkFrame(frame_info)
frame_grid.pack(pady=10)

def mostrar_feriados():
    messagebox.showinfo("Feriados", "Lista de feriados:\n\n• 01/01 - Ano Novo\n• 21/04 - Tiradentes\n• 01/05 - Dia do Trabalho\n• 07/09 - Independência\n• 12/10 - N. Sra. Aparecida\n• 02/11 - Finados\n• 15/11 - Proclamação da República\n• 25/12 - Natal")

def mostrar_folgas():
    messagebox.showinfo("Folgas", "Suas próximas folgas serão exibidas aqui.\nConsulte o administrador para mais detalhes.")

def mostrar_ferias():
    messagebox.showinfo("Férias", "Informações sobre suas férias:\n\nConsulte o RH para verificar seu período de férias disponível.")

botao_feriados = ctk.CTkButton(frame_grid, text="🎉 Feriados", command=mostrar_feriados, width=150)
botao_feriados.grid(row=0, column=0, padx=10, pady=5)

botao_folgas = ctk.CTkButton(frame_grid, text="🛋️ Folgas", command=mostrar_folgas, width=150)
botao_folgas.grid(row=0, column=1, padx=10, pady=5)

botao_ferias = ctk.CTkButton(frame_grid, text="🏖️ Férias", command=mostrar_ferias, width=150)
botao_ferias.grid(row=0, column=2, padx=10, pady=5)

# Botão de voltar
def voltar():
    tela.destroy()
    subprocess.Popen([sys.executable, "funcionario.py"])

botao_voltar = ctk.CTkButton(frame_principal, text="⬅️ Voltar", command=voltar, width=200, height=40, fg_color="gray", hover_color="darkgray")
botao_voltar.pack(pady=20)

# Iniciar a tela
tela.mainloop()