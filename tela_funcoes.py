import customtkinter as ctk
# configurações de aparência
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")
# tela de login
tela = ctk.CTk()
tela.title("Tela de Funções")
tela.geometry("1920x1080")
informacoes_iniciais = ctk.CTkLabel(tela, text="Escolha uma das opções abaixo:")
informacoes_iniciais.grid(column=0, row=0, padx=10, pady=10)
# botão para função 1
def funcao_1():
    print("INFORMAÇÕES SOBRE ESCALA")
botao_funcao_1 = ctk.CTkButton(tela, text="Função 1", command=funcao_1)
botao_funcao_1.grid(column=0, row=1, padx=10, pady=10)
# botão para função 2
def funcao_2():
    print("FUNCIONARIOS LOGADOS")
botao_funcao_2 = ctk.CTkButton(tela, text="Função 2", command=funcao_2)
botao_funcao_2.grid(column=0, row=2, padx=10, pady=10)
# botão para função 3
def funcao_3():
    print("CRUD DE USUÁRIOS")
botao_funcao_3 = ctk.CTkButton(tela, text="Função 3", command=funcao_3)
botao_funcao_3.grid(column=0, row=3, padx=10, pady=10)
# código para manter a janela aberta
tela.mainloop()