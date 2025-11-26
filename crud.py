import customtkinter as ctk
from tkinter import messagebox
import subprocess
import sys
import json
import os
from database import cadastrar_usuario, listar_funcionarios, buscar_usuario

# Configurações de aparência
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# Carregar sessão para verificar se é supervisor
SESSAO_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sessao.json')

def carregar_sessao():
    try:
        with open(SESSAO_PATH, 'r') as f:
            return json.load(f)
    except:
        return None

usuario_logado = carregar_sessao()

# Tela de CRUD
tela = ctk.CTk()
tela.title("Sistema de Gestão - Gerenciar Funcionários")
tela.geometry("800x600")
tela.resizable(False, False)

# Frame principal
frame_principal = ctk.CTkFrame(tela)
frame_principal.pack(fill="both", expand=True, padx=20, pady=20)

# Título
titulo = ctk.CTkLabel(frame_principal, text="Cadastro de Funcionários", font=ctk.CTkFont(size=24, weight="bold"))
titulo.pack(pady=15)

# Frame de formulário
frame_form = ctk.CTkFrame(frame_principal)
frame_form.pack(fill="x", padx=20, pady=10)

ctk.CTkLabel(frame_form, text="Cadastrar Novo Funcionário", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)

# Campos do formulário
frame_campos = ctk.CTkFrame(frame_form)
frame_campos.pack(pady=10)

ctk.CTkLabel(frame_campos, text="Nome Completo:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
entrada_nome = ctk.CTkEntry(frame_campos, width=250)
entrada_nome.grid(row=0, column=1, padx=5, pady=5)

ctk.CTkLabel(frame_campos, text="Usuário:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
entrada_usuario = ctk.CTkEntry(frame_campos, width=250)
entrada_usuario.grid(row=1, column=1, padx=5, pady=5)

ctk.CTkLabel(frame_campos, text="Senha:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
entrada_senha = ctk.CTkEntry(frame_campos, width=250, show="*")
entrada_senha.grid(row=2, column=1, padx=5, pady=5)

def limpar_campos():
    entrada_nome.delete(0, 'end')
    entrada_usuario.delete(0, 'end')
    entrada_senha.delete(0, 'end')

def adicionar_funcionario():
    nome = entrada_nome.get()
    usuario = entrada_usuario.get()
    senha = entrada_senha.get()
    
    if not nome or not usuario or not senha:
        messagebox.showwarning("Aviso", "Preencha todos os campos!")
        return
    
    if len(senha) < 4:
        messagebox.showwarning("Aviso", "A senha deve ter pelo menos 4 caracteres!")
        return
    
    sucesso, mensagem = cadastrar_usuario(usuario, senha, nome, 'funcionario')
    
    if sucesso:
        messagebox.showinfo("Sucesso", f"Funcionário {nome} cadastrado com sucesso!")
        limpar_campos()
        atualizar_lista()
    else:
        messagebox.showerror("Erro", mensagem)

# Botões de ação
frame_botoes = ctk.CTkFrame(frame_form)
frame_botoes.pack(pady=10)

botao_adicionar = ctk.CTkButton(frame_botoes, text="➕ Cadastrar Funcionário", command=adicionar_funcionario, width=200, fg_color="green", hover_color="darkgreen")
botao_adicionar.grid(row=0, column=0, padx=5)

botao_limpar = ctk.CTkButton(frame_botoes, text="🔄 Limpar", command=limpar_campos, width=120, fg_color="gray", hover_color="darkgray")
botao_limpar.grid(row=0, column=1, padx=5)

# Frame da lista de funcionários
frame_lista = ctk.CTkFrame(frame_principal)
frame_lista.pack(fill="both", expand=True, padx=20, pady=10)

ctk.CTkLabel(frame_lista, text="Funcionários Cadastrados", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=5)

# Scrollable frame para lista
scrollable_frame = ctk.CTkScrollableFrame(frame_lista, height=200)
scrollable_frame.pack(fill="both", expand=True, padx=10, pady=5)

# Cabeçalhos
frame_cabecalho = ctk.CTkFrame(scrollable_frame)
frame_cabecalho.pack(fill="x", pady=2)

ctk.CTkLabel(frame_cabecalho, text="ID", width=50, font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, padx=5)
ctk.CTkLabel(frame_cabecalho, text="Nome", width=200, font=ctk.CTkFont(weight="bold")).grid(row=0, column=1, padx=5)
ctk.CTkLabel(frame_cabecalho, text="Usuário", width=150, font=ctk.CTkFont(weight="bold")).grid(row=0, column=2, padx=5)

lista_widgets = []

def atualizar_lista():
    for widget in lista_widgets:
        widget.destroy()
    lista_widgets.clear()
    
    funcionarios = listar_funcionarios()
    
    if not funcionarios:
        frame_vazio = ctk.CTkFrame(scrollable_frame)
        frame_vazio.pack(fill="x", pady=10)
        lista_widgets.append(frame_vazio)
        ctk.CTkLabel(frame_vazio, text="Nenhum funcionário cadastrado", text_color="gray").pack()
        return
    
    for func in funcionarios:
        frame_func = ctk.CTkFrame(scrollable_frame)
        frame_func.pack(fill="x", pady=1)
        lista_widgets.append(frame_func)
        
        ctk.CTkLabel(frame_func, text=str(func[0]), width=50).grid(row=0, column=0, padx=5)
        ctk.CTkLabel(frame_func, text=func[2], width=200).grid(row=0, column=1, padx=5)
        ctk.CTkLabel(frame_func, text=func[1], width=150).grid(row=0, column=2, padx=5)

atualizar_lista()

# Botão de voltar
def voltar():
    tela.destroy()
    if usuario_logado and usuario_logado['tipo'] == 'supervisor':
        subprocess.Popen([sys.executable, "tela_supervisor.py"])
    else:
        subprocess.Popen([sys.executable, "tela_inicial.py"])

botao_voltar = ctk.CTkButton(frame_principal, text="⬅️ Voltar", command=voltar, width=200, height=40, fg_color="gray", hover_color="darkgray")
botao_voltar.pack(pady=15)

# Iniciar a tela
tela.mainloop()