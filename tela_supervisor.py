import customtkinter as ctk
from tkinter import messagebox
import subprocess
import sys
import json
import os
from database import (
    listar_funcionarios_online, listar_funcionarios_offline,
    listar_escalas, listar_funcionarios, adicionar_escala, aprovar_escala
)

# Configurações de aparência
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# Carregar dados do usuário logado
SESSAO_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sessao.json')

def carregar_sessao():
    try:
        with open(SESSAO_PATH, 'r') as f:
            return json.load(f)
    except:
        return None

usuario_logado = carregar_sessao()

if not usuario_logado or usuario_logado['tipo'] != 'supervisor':
    messagebox.showerror("Erro", "Acesso negado. Você precisa ser supervisor.")
    subprocess.Popen([sys.executable, "tela_login.py"])
    sys.exit()

# Tela do supervisor
tela = ctk.CTk()
tela.title(f"Sistema de Gestão - Supervisor: {usuario_logado['nome']}")
tela.geometry("900x700")
tela.resizable(False, False)

# Frame principal
frame_principal = ctk.CTkFrame(tela)
frame_principal.pack(fill="both", expand=True, padx=20, pady=20)

# Título
titulo = ctk.CTkLabel(frame_principal, text=f"👔 Painel do Supervisor", font=ctk.CTkFont(size=24, weight="bold"))
titulo.pack(pady=10)

subtitulo = ctk.CTkLabel(frame_principal, text=f"Bem-vindo, {usuario_logado['nome']}!", font=ctk.CTkFont(size=14))
subtitulo.pack(pady=5)

# Notebook (abas)
tabview = ctk.CTkTabview(frame_principal)
tabview.pack(fill="both", expand=True, padx=10, pady=10)

# Aba de Funcionários Online/Offline
tab_funcionarios = tabview.add("👥 Funcionários")
tab_escalas = tabview.add("📅 Escalas")
tab_gerenciar = tabview.add("⚙️ Gerenciar")

# ==================== ABA FUNCIONÁRIOS ====================

frame_online = ctk.CTkFrame(tab_funcionarios)
frame_online.pack(fill="both", expand=True, padx=10, pady=10)

# Frame para online
frame_lista_online = ctk.CTkFrame(frame_online)
frame_lista_online.pack(side="left", fill="both", expand=True, padx=5)

ctk.CTkLabel(frame_lista_online, text="🟢 Funcionários ONLINE", font=ctk.CTkFont(size=16, weight="bold"), text_color="green").pack(pady=5)

scrollable_online = ctk.CTkScrollableFrame(frame_lista_online, height=300)
scrollable_online.pack(fill="both", expand=True, padx=5, pady=5)

# Frame para offline
frame_lista_offline = ctk.CTkFrame(frame_online)
frame_lista_offline.pack(side="right", fill="both", expand=True, padx=5)

ctk.CTkLabel(frame_lista_offline, text="🔴 Funcionários OFFLINE", font=ctk.CTkFont(size=16, weight="bold"), text_color="red").pack(pady=5)

scrollable_offline = ctk.CTkScrollableFrame(frame_lista_offline, height=300)
scrollable_offline.pack(fill="both", expand=True, padx=5, pady=5)

lista_widgets_online = []
lista_widgets_offline = []

def atualizar_listas_funcionarios():
    # Limpar listas
    for widget in lista_widgets_online:
        widget.destroy()
    lista_widgets_online.clear()
    
    for widget in lista_widgets_offline:
        widget.destroy()
    lista_widgets_offline.clear()
    
    # Funcionários online
    funcionarios_online = listar_funcionarios_online()
    
    if not funcionarios_online:
        frame_vazio = ctk.CTkFrame(scrollable_online)
        frame_vazio.pack(fill="x", pady=10)
        lista_widgets_online.append(frame_vazio)
        ctk.CTkLabel(frame_vazio, text="Nenhum funcionário online", text_color="gray").pack()
    else:
        for func in funcionarios_online:
            frame_func = ctk.CTkFrame(scrollable_online)
            frame_func.pack(fill="x", pady=2)
            lista_widgets_online.append(frame_func)
            
            ctk.CTkLabel(frame_func, text="🟢", width=30).grid(row=0, column=0, padx=5)
            ctk.CTkLabel(frame_func, text=func[1], width=150).grid(row=0, column=1, padx=5)
            ctk.CTkLabel(frame_func, text=f"Entrada: {func[3]}", width=100, text_color="gray").grid(row=0, column=2, padx=5)
    
    # Funcionários offline (que já trabalharam hoje)
    funcionarios_offline = listar_funcionarios_offline()
    
    if not funcionarios_offline:
        frame_vazio = ctk.CTkFrame(scrollable_offline)
        frame_vazio.pack(fill="x", pady=10)
        lista_widgets_offline.append(frame_vazio)
        ctk.CTkLabel(frame_vazio, text="Nenhum registro de saída hoje", text_color="gray").pack()
    else:
        for func in funcionarios_offline:
            frame_func = ctk.CTkFrame(scrollable_offline)
            frame_func.pack(fill="x", pady=2)
            lista_widgets_offline.append(frame_func)
            
            ctk.CTkLabel(frame_func, text="🔴", width=30).grid(row=0, column=0, padx=5)
            ctk.CTkLabel(frame_func, text=func[1], width=150).grid(row=0, column=1, padx=5)
            ctk.CTkLabel(frame_func, text=f"{func[3]} - {func[4]}", width=120, text_color="gray").grid(row=0, column=2, padx=5)

atualizar_listas_funcionarios()

botao_atualizar = ctk.CTkButton(tab_funcionarios, text="🔄 Atualizar", command=atualizar_listas_funcionarios, width=150)
botao_atualizar.pack(pady=10)

# ==================== ABA ESCALAS ====================

frame_escalas = ctk.CTkFrame(tab_escalas)
frame_escalas.pack(fill="both", expand=True, padx=10, pady=10)

# Frame para adicionar escala
frame_add_escala = ctk.CTkFrame(frame_escalas)
frame_add_escala.pack(fill="x", padx=10, pady=10)

ctk.CTkLabel(frame_add_escala, text="Adicionar Nova Escala", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=5)

frame_campos_escala = ctk.CTkFrame(frame_add_escala)
frame_campos_escala.pack(pady=10)

# Dropdown de funcionários
funcionarios = listar_funcionarios()
nomes_funcionarios = {f"{func[2]}": func[0] for func in funcionarios}
lista_nomes = list(nomes_funcionarios.keys()) if nomes_funcionarios else ["Nenhum funcionário"]

ctk.CTkLabel(frame_campos_escala, text="Funcionário:").grid(row=0, column=0, padx=5, pady=5)
combo_funcionario = ctk.CTkComboBox(frame_campos_escala, values=lista_nomes, width=180)
combo_funcionario.grid(row=0, column=1, padx=5, pady=5)

ctk.CTkLabel(frame_campos_escala, text="Data:").grid(row=0, column=2, padx=5, pady=5)
entrada_data = ctk.CTkEntry(frame_campos_escala, placeholder_text="DD/MM/AAAA", width=100)
entrada_data.grid(row=0, column=3, padx=5, pady=5)

ctk.CTkLabel(frame_campos_escala, text="Turno:").grid(row=1, column=0, padx=5, pady=5)
combo_turno = ctk.CTkComboBox(frame_campos_escala, values=["Manhã", "Tarde", "Noite", "Integral"], width=180)
combo_turno.grid(row=1, column=1, padx=5, pady=5)

ctk.CTkLabel(frame_campos_escala, text="Tipo:").grid(row=1, column=2, padx=5, pady=5)
combo_tipo = ctk.CTkComboBox(frame_campos_escala, values=["Trabalho", "Folga", "Férias", "Feriado"], width=100)
combo_tipo.grid(row=1, column=3, padx=5, pady=5)

def add_escala():
    funcionario_nome = combo_funcionario.get()
    data = entrada_data.get()
    turno = combo_turno.get()
    tipo = combo_tipo.get()
    
    if funcionario_nome == "Nenhum funcionário" or not data or not turno:
        messagebox.showwarning("Aviso", "Preencha todos os campos!")
        return
    
    funcionario_id = nomes_funcionarios.get(funcionario_nome)
    
    sucesso, mensagem = adicionar_escala(funcionario_id, data, turno, tipo.lower())
    
    if sucesso:
        messagebox.showinfo("Sucesso", mensagem)
        entrada_data.delete(0, 'end')
        atualizar_lista_escalas()
    else:
        messagebox.showerror("Erro", mensagem)

botao_add_escala = ctk.CTkButton(frame_add_escala, text="➕ Adicionar", command=add_escala, width=150)
botao_add_escala.pack(pady=10)

# Lista de escalas
frame_lista_escalas = ctk.CTkFrame(frame_escalas)
frame_lista_escalas.pack(fill="both", expand=True, padx=10, pady=10)

ctk.CTkLabel(frame_lista_escalas, text="Escalas Cadastradas", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=5)

scrollable_escalas = ctk.CTkScrollableFrame(frame_lista_escalas, height=200)
scrollable_escalas.pack(fill="both", expand=True, padx=5, pady=5)

lista_widgets_escalas = []

def atualizar_lista_escalas():
    for widget in lista_widgets_escalas:
        widget.destroy()
    lista_widgets_escalas.clear()
    
    escalas = listar_escalas()
    
    if not escalas:
        frame_vazio = ctk.CTkFrame(scrollable_escalas)
        frame_vazio.pack(fill="x", pady=10)
        lista_widgets_escalas.append(frame_vazio)
        ctk.CTkLabel(frame_vazio, text="Nenhuma escala cadastrada", text_color="gray").pack()
        return
    
    for escala in escalas:
        frame_esc = ctk.CTkFrame(scrollable_escalas)
        frame_esc.pack(fill="x", pady=2)
        lista_widgets_escalas.append(frame_esc)
        
        ctk.CTkLabel(frame_esc, text=escala[1][:15], width=120).grid(row=0, column=0, padx=3)
        ctk.CTkLabel(frame_esc, text=escala[2], width=80).grid(row=0, column=1, padx=3)
        ctk.CTkLabel(frame_esc, text=escala[3], width=70).grid(row=0, column=2, padx=3)
        ctk.CTkLabel(frame_esc, text=escala[4], width=70).grid(row=0, column=3, padx=3)
        
        status = "✅" if escala[5] == 1 else "⏳"
        ctk.CTkLabel(frame_esc, text=status, width=40).grid(row=0, column=4, padx=3)
        
        if escala[5] != 1:
            btn_aprovar = ctk.CTkButton(frame_esc, text="Aprovar", width=70, height=25,
                                        fg_color="green", hover_color="darkgreen",
                                        command=lambda id=escala[0]: aprovar_esc(id))
            btn_aprovar.grid(row=0, column=5, padx=3)

def aprovar_esc(escala_id):
    sucesso, mensagem = aprovar_escala(escala_id)
    if sucesso:
        messagebox.showinfo("Sucesso", mensagem)
        atualizar_lista_escalas()
    else:
        messagebox.showerror("Erro", mensagem)

atualizar_lista_escalas()

# ==================== ABA GERENCIAR ====================

frame_gerenciar = ctk.CTkFrame(tab_gerenciar)
frame_gerenciar.pack(fill="both", expand=True, padx=10, pady=10)

ctk.CTkLabel(frame_gerenciar, text="Gerenciamento de Funcionários", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=20)

def abrir_crud():
    subprocess.Popen([sys.executable, "crud.py"])

botao_crud = ctk.CTkButton(frame_gerenciar, text="⚙️ Gerenciar Funcionários (CRUD)", 
                           command=abrir_crud, width=280, height=45)
botao_crud.pack(pady=15)

# Lista de funcionários
ctk.CTkLabel(frame_gerenciar, text="Funcionários Cadastrados:", font=ctk.CTkFont(size=14)).pack(pady=10)

scrollable_funcs = ctk.CTkScrollableFrame(frame_gerenciar, height=200)
scrollable_funcs.pack(fill="both", expand=True, padx=20, pady=5)

for func in funcionarios:
    frame_f = ctk.CTkFrame(scrollable_funcs)
    frame_f.pack(fill="x", pady=2)
    ctk.CTkLabel(frame_f, text=f"👷 {func[2]} (@{func[1]})", width=300).pack(side="left", padx=10)

# Botão de logout
def fazer_logout():
    resposta = messagebox.askyesno("Logout", "Deseja realmente sair?")
    if resposta:
        if os.path.exists(SESSAO_PATH):
            os.remove(SESSAO_PATH)
        tela.destroy()
        subprocess.Popen([sys.executable, "tela_inicial.py"])

botao_logout = ctk.CTkButton(frame_principal, text="🚪 Sair (Logout)", command=fazer_logout, 
                             width=200, height=40, fg_color="red", hover_color="darkred")
botao_logout.pack(pady=10)

# Iniciar a tela
tela.mainloop()
