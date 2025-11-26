import customtkinter as ctk
# configurações de aparência
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")
# tela de login
tela = ctk.CTk()
tela.title("Tela de funcionários logados")
tela.geometry("1920x1080")
funcionarios = ["Funcionário 1", "Funcionário 2", "Funcionário 3"]
funcionarios_var = ctk.StringVar(value=funcionarios)
# lista de funcionários logados
lista_funcionarios = ctk.CTkListbox(tela, listvariable=funcionarios_var, height=500, width=400)
lista_funcionarios.pack(pady=50)
# função para voltar à tela inicial
def voltar_tela_inicial():
    tela.destroy()
    import tela_inicial
# botão de voltar
botao_voltar = ctk.CTkButton(tela, text="Voltar", command=voltar_tela_inicial)
botao_voltar.pack(pady=20)
# iniciar a tela
tela.mainloop()