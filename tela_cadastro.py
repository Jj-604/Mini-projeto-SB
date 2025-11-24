# tela de cadastro
#biblioteca tkinter sendo usado para a criação da interface gráfica
from tkinter import * 
#codigo para criar a janela principal
Jenela = Tk()
Jenela.title("Tela de Cadastro")
Jenela.geometry("400x300")
Inomrações_iniciais = Label(Jenela, text="Realize seu cadastro preenchendo os campos abaixo:")
Inomrações_iniciais.grid(column=0, row=0, padx=10, pady=10)
#botão para cadastrar novo usuario
botao_cadastrar = Button(Jenela, text="Cadastrar Novo Usuario", command=cadastrar_usuario)
botao_cadastrar.grid(column=0, row=2, padx=10, pady=10)
texto_botao_cadastrar = Label(Jenela, text="Deseja cadastrar um novo usuario?")
texto_botao_cadastrar.grid(column=0, row=3, padx=10, pady=10)
def cadastrar_usuario():
    Jenela.destroy()
    import tela_cadastro
#botão para fazer login
botao_login = Button(Jenela, text="Fazer Login", command=fazer_login)
botao_login.grid(column=0, row=4, padx=10, pady=10)
texto_botao_login = Label(Jenela, text="Ja possui uma conta?")
texto_botao_login.grid(column=0, row=5, padx=10, pady=10)
def fazer_login():
    Jenela.destroy()
    import tela_login
#codigo para manter a janela aberta
Jenela.mainloop()