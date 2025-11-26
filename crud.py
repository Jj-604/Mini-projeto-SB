import customtkinter as ctk
# configurações de aparência
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")
# tela de login
tela = ctk.CTk()
tela.title("CRUD")
tela.geometry("1920x1080")
adicionar_funcionario = ctk.CTkButton(tela, text="Adicionar Funcionário")
adicionar_funcionario.place(relx=0.5, rely=0.5, anchor="center")
desligamento_funcionario = ctk.CTkButton(tela, text="Desligamento de Funcionário")
desligamento_funcionario.place(relx=0.5, rely=0.6, anchor="center")
suspender_funcionario = ctk.CTkButton(tela, text="Suspender Funcionário")
suspender_funcionario.place(relx=0.5, rely=0.7, anchor="center")
# função para voltar à tela inicial
def voltar_tela_inicial():
    tela.destroy()
    import tela_inicial
# botão de voltar
botao_voltar = ctk.CTkButton(tela, text="Voltar", command=voltar_tela_inicial)
botao_voltar.pack(pady=20)
# iniciar a tela
tela.mainloop()