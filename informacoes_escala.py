import customtkinter as ctk
from tkinter import messagebox
import subprocess
import sys
from database import listar_escalas, listar_funcionarios, adicionar_escala, aprovar_escala

# Configurações de aparência
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# Tela de escala
tela = ctk.CTk()
tela.title("Sistema de Gestão - Informações da Escala")
tela.geometry("800x650")
tela.resizable(False, False)

# Frame principal
frame_principal = ctk.CTkFrame(tela)
frame_principal.pack(fill="both", expand=True, padx=20, pady=20)

# Título
titulo = ctk.CTkLabel(frame_principal, text="Informações da Escala", font=ctk.CTkFont(size=24, weight="bold"))
titulo.pack(pady=15)

# Frame para adicionar escala
frame_adicionar = ctk.CTkFrame(frame_principal)
frame_adicionar.pack(fill="x", padx=20, pady=10)

ctk.CTkLabel(frame_adicionar, text="Adicionar Nova Escala", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=5)

frame_campos = ctk.CTkFrame(frame_adicionar)
frame_campos.pack(pady=10)

# Dropdown de funcionários
funcionarios = listar_funcionarios()
nomes_funcionarios = {f"{func[0]} - {func[1]}": func[0] for func in funcionarios}
lista_nomes = list(nomes_funcionarios.keys()) if nomes_funcionarios else ["Nenhum funcionário"]

ctk.CTkLabel(frame_campos, text="Funcionário:").grid(row=0, column=0, padx=5, pady=5)
combo_funcionario = ctk.CTkComboBox(frame_campos, values=lista_nomes, width=200)
combo_funcionario.grid(row=0, column=1, padx=5, pady=5)

ctk.CTkLabel(frame_campos, text="Data:").grid(row=0, column=2, padx=5, pady=5)
entrada_data = ctk.CTkEntry(frame_campos, placeholder_text="DD/MM/AAAA", width=120)
entrada_data.grid(row=0, column=3, padx=5, pady=5)

ctk.CTkLabel(frame_campos, text="Turno:").grid(row=1, column=0, padx=5, pady=5)
combo_turno = ctk.CTkComboBox(frame_campos, values=["Manhã", "Tarde", "Noite", "Integral"], width=200)
combo_turno.grid(row=1, column=1, padx=5, pady=5)

ctk.CTkLabel(frame_campos, text="Tipo:").grid(row=1, column=2, padx=5, pady=5)
combo_tipo = ctk.CTkComboBox(frame_campos, values=["Trabalho", "Folga", "Férias", "Feriado"], width=120)
combo_tipo.grid(row=1, column=3, padx=5, pady=5)

def adicionar_nova_escala():
    funcionario_selecionado = combo_funcionario.get()
    data = entrada_data.get()
    turno = combo_turno.get()
    tipo = combo_tipo.get()
    
    if funcionario_selecionado == "Nenhum funcionário" or not data or not turno:
        messagebox.showwarning("Aviso", "Preencha todos os campos!")
        return
    
    funcionario_id = nomes_funcionarios.get(funcionario_selecionado)
    
    sucesso, mensagem = adicionar_escala(funcionario_id, data, turno, tipo.lower())
    
    if sucesso:
        messagebox.showinfo("Sucesso", mensagem)
        entrada_data.delete(0, 'end')
        atualizar_lista_escalas()
    else:
        messagebox.showerror("Erro", mensagem)

botao_adicionar = ctk.CTkButton(frame_adicionar, text="➕ Adicionar Escala", command=adicionar_nova_escala, width=150)
botao_adicionar.pack(pady=10)

# Frame da lista de escalas
frame_lista = ctk.CTkFrame(frame_principal)
frame_lista.pack(fill="both", expand=True, padx=20, pady=10)

ctk.CTkLabel(frame_lista, text="Escalas Cadastradas", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=5)

# Scrollable frame para lista
scrollable_frame = ctk.CTkScrollableFrame(frame_lista, height=200)
scrollable_frame.pack(fill="both", expand=True, padx=10, pady=5)

# Cabeçalhos
frame_cabecalho = ctk.CTkFrame(scrollable_frame)
frame_cabecalho.pack(fill="x", pady=2)

ctk.CTkLabel(frame_cabecalho, text="ID", width=40, font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, padx=2)
ctk.CTkLabel(frame_cabecalho, text="Funcionário", width=150, font=ctk.CTkFont(weight="bold")).grid(row=0, column=1, padx=2)
ctk.CTkLabel(frame_cabecalho, text="Data", width=100, font=ctk.CTkFont(weight="bold")).grid(row=0, column=2, padx=2)
ctk.CTkLabel(frame_cabecalho, text="Turno", width=80, font=ctk.CTkFont(weight="bold")).grid(row=0, column=3, padx=2)
ctk.CTkLabel(frame_cabecalho, text="Tipo", width=80, font=ctk.CTkFont(weight="bold")).grid(row=0, column=4, padx=2)
ctk.CTkLabel(frame_cabecalho, text="Status", width=80, font=ctk.CTkFont(weight="bold")).grid(row=0, column=5, padx=2)
ctk.CTkLabel(frame_cabecalho, text="Ação", width=80, font=ctk.CTkFont(weight="bold")).grid(row=0, column=6, padx=2)

lista_widgets_escala = []

def aprovar_escala_click(escala_id):
    sucesso, mensagem = aprovar_escala(escala_id)
    if sucesso:
        messagebox.showinfo("Sucesso", mensagem)
        atualizar_lista_escalas()
    else:
        messagebox.showerror("Erro", mensagem)

def atualizar_lista_escalas():
    for widget in lista_widgets_escala:
        widget.destroy()
    lista_widgets_escala.clear()
    
    escalas = listar_escalas()
    
    for escala in escalas:
        frame_escala = ctk.CTkFrame(scrollable_frame)
        frame_escala.pack(fill="x", pady=1)
        lista_widgets_escala.append(frame_escala)
        
        ctk.CTkLabel(frame_escala, text=str(escala[0]), width=40).grid(row=0, column=0, padx=2)
        ctk.CTkLabel(frame_escala, text=escala[1][:18] if escala[1] else "", width=150).grid(row=0, column=1, padx=2)
        ctk.CTkLabel(frame_escala, text=escala[2] or "", width=100).grid(row=0, column=2, padx=2)
        ctk.CTkLabel(frame_escala, text=escala[3] or "", width=80).grid(row=0, column=3, padx=2)
        ctk.CTkLabel(frame_escala, text=escala[4] or "", width=80).grid(row=0, column=4, padx=2)
        
        status = "✅ Aprovado" if escala[5] == 1 else "⏳ Pendente"
        ctk.CTkLabel(frame_escala, text=status, width=80).grid(row=0, column=5, padx=2)
        
        if escala[5] != 1:
            btn_aprovar = ctk.CTkButton(frame_escala, text="Aprovar", width=70, height=25, 
                                        fg_color="green", hover_color="darkgreen",
                                        command=lambda id=escala[0]: aprovar_escala_click(id))
            btn_aprovar.grid(row=0, column=6, padx=2)
        else:
            ctk.CTkLabel(frame_escala, text="-", width=70).grid(row=0, column=6, padx=2)

# Carregar lista inicial
atualizar_lista_escalas()

# Botões de navegação
frame_botoes = ctk.CTkFrame(frame_principal)
frame_botoes.pack(pady=15)

def abrir_folgas():
    messagebox.showinfo("Folgas", "Funcionalidade de folgas em desenvolvimento!")

def abrir_feriados():
    messagebox.showinfo("Feriados", "Funcionalidade de feriados em desenvolvimento!")

def abrir_ferias():
    messagebox.showinfo("Férias", "Funcionalidade de férias em desenvolvimento!")

botao_folgas = ctk.CTkButton(frame_botoes, text="📋 Folgas", command=abrir_folgas, width=120)
botao_folgas.grid(row=0, column=0, padx=5)

botao_feriados = ctk.CTkButton(frame_botoes, text="🎉 Feriados", command=abrir_feriados, width=120)
botao_feriados.grid(row=0, column=1, padx=5)

botao_ferias = ctk.CTkButton(frame_botoes, text="🏖️ Férias", command=abrir_ferias, width=120)
botao_ferias.grid(row=0, column=2, padx=5)

# Botão de voltar
def voltar():
    tela.destroy()
    subprocess.Popen([sys.executable, "tela_funcoes.py"])

botao_voltar = ctk.CTkButton(frame_principal, text="⬅️ Voltar ao Menu", command=voltar, width=200, height=40, fg_color="gray", hover_color="darkgray")
botao_voltar.pack(pady=10)

# Iniciar a tela
tela.mainloop()