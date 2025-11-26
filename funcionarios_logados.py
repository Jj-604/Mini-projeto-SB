import customtkinter as ctk
from tkinter import messagebox
import subprocess
import sys
from database import listar_usuarios_logados

# Configurações de aparência
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# Tela de funcionários logados
tela = ctk.CTk()
tela.title("Sistema de Gestão - Funcionários Logados")
tela.geometry("600x500")
tela.resizable(False, False)

# Frame principal
frame_principal = ctk.CTkFrame(tela)
frame_principal.pack(fill="both", expand=True, padx=20, pady=20)

# Título
titulo = ctk.CTkLabel(frame_principal, text="Funcionários Logados", font=ctk.CTkFont(size=24, weight="bold"))
titulo.pack(pady=15)

subtitulo = ctk.CTkLabel(frame_principal, text="Lista de usuários atualmente conectados ao sistema", font=ctk.CTkFont(size=14))
subtitulo.pack(pady=5)

# Frame da lista
frame_lista = ctk.CTkFrame(frame_principal)
frame_lista.pack(fill="both", expand=True, padx=20, pady=10)

# Scrollable frame para lista
scrollable_frame = ctk.CTkScrollableFrame(frame_lista, height=250)
scrollable_frame.pack(fill="both", expand=True, padx=10, pady=10)

# Cabeçalhos
frame_cabecalho = ctk.CTkFrame(scrollable_frame)
frame_cabecalho.pack(fill="x", pady=5)

ctk.CTkLabel(frame_cabecalho, text="👤 Usuário", width=200, font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, padx=10)
ctk.CTkLabel(frame_cabecalho, text="🕐 Data/Hora Login", width=200, font=ctk.CTkFont(weight="bold")).grid(row=0, column=1, padx=10)

lista_widgets = []

def atualizar_lista():
    for widget in lista_widgets:
        widget.destroy()
    lista_widgets.clear()
    
    usuarios = listar_usuarios_logados()
    
    if not usuarios:
        frame_vazio = ctk.CTkFrame(scrollable_frame)
        frame_vazio.pack(fill="x", pady=20)
        lista_widgets.append(frame_vazio)
        
        ctk.CTkLabel(frame_vazio, text="Nenhum usuário logado no momento", 
                    font=ctk.CTkFont(size=14), text_color="gray").pack()
        return
    
    for usuario in usuarios:
        frame_usuario = ctk.CTkFrame(scrollable_frame)
        frame_usuario.pack(fill="x", pady=2)
        lista_widgets.append(frame_usuario)
        
        # Indicador de online
        ctk.CTkLabel(frame_usuario, text="🟢", width=30).grid(row=0, column=0, padx=5)
        ctk.CTkLabel(frame_usuario, text=usuario[0], width=170).grid(row=0, column=1, padx=5)
        ctk.CTkLabel(frame_usuario, text=usuario[1] or "Não disponível", width=200).grid(row=0, column=2, padx=5)

# Carregar lista inicial
atualizar_lista()

# Botão de atualizar
def btn_atualizar():
    atualizar_lista()
    messagebox.showinfo("Atualizado", "Lista atualizada com sucesso!")

botao_atualizar = ctk.CTkButton(frame_principal, text="🔄 Atualizar Lista", command=btn_atualizar, width=200, height=40)
botao_atualizar.pack(pady=10)

# Botão de voltar
def voltar():
    tela.destroy()
    subprocess.Popen([sys.executable, "tela_funcoes.py"])

botao_voltar = ctk.CTkButton(frame_principal, text="⬅️ Voltar ao Menu", command=voltar, width=200, height=40, fg_color="gray", hover_color="darkgray")
botao_voltar.pack(pady=5)

# Iniciar a tela
tela.mainloop()