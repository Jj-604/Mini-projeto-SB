import customtkinter as ctk
# configurações de aparência
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")
# tela de login
tela = ctk.CTk()
tela.title("Tela de cadastro")
tela.geometry("400x300")
informacoes_iniciais = ctk.CTkLabel(tela, text="Faça cadastro preenchendo os campos abaixo:")
informacoes_iniciais.grid(column=0, row=0, padx=10, pady=10)
# campo de entrada para o nome de usuário
entrada_usuario = ctk.CTkEntry(tela, placeholder_text="Nome de Usuário")
entrada_usuario.grid(column=0, row=1, padx=10, pady=10)
# campo de entrada para a senha
entrada_senha = ctk.CTkEntry(tela, placeholder_text="Senha", show="*")
entrada_senha.grid(column=0, row=2, padx=10, pady=10)
# botão para fazer cadastro
def fazer_login():
    usuario = entrada_usuario.get()
    senha = entrada_senha.get()
    # aqui você pode adicionar a lógica para verificar o login
    print(f"Tentando fazer cadastro com Usuário: {usuario} e Senha: {senha}")
botao_login = ctk.CTkButton(tela, text="Fazer cadastro", command=fazer_login)
botao_login.grid(column=0, row=3, padx=10, pady=10)
# código para manter a janela aberta
tela.mainloop()