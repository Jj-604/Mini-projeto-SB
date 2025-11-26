import customtkinter as ctk
# configurações de aparência
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")
# tela de login
tela = ctk.CTk()
tela.title("Tela de inicial do Funcionário")
tela.geometry("1920x1080")
# função para abrir a tela de login
def abrir_tela_login():
    from tela_login import tela_login
    tela_login.deiconify()
    tela.withdraw()
# botão para abrir a tela de login
botao_login = ctk.CTkButton(tela, text="Ir para Tela de Login", command=abrir_tela_login)
botao_login.pack(pady=20)
# iniciar a tela
tela.mainloop()