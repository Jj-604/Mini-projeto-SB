import customtkinter as ctk
# configurações de aparência
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")
# tela de login
tela = ctk.CTk()
tela.title("Tela de escala do Funcionário")
tela.geometry("1920x1080")
ver_escala = ctk.CTkLabel(tela, text="Aqui você verá sua escala", font=ctk.CTkFont(size=20, weight="bold"))
solicitar_troca = ctk.CTkLabel(tela, text="Aqui você poderá solicitar trocas de turno", font=ctk.CTkFont(size=20, weight="bold"))
ver_escala.pack(pady=20)
solicitar_troca.pack(pady=20)
feriados = ctk.CTkLabel(tela, text="Aqui você verá os feriados", font=ctk.CTkFont(size=20, weight="bold"))
feriados.pack(pady=20)
folgas = ctk.CTkLabel(tela, text="Aqui você verá suas folgas", font=ctk.CTkFont(size=20, weight="bold"))
folgas.pack(pady=20)
troca_folgas = ctk.CTkLabel(tela, text="Aqui você poderá trocar suas folgas com outros funcionários", font=ctk.CTkFont(size=20, weight="bold"))
troca_folgas.pack(pady=20)
ver_ferias = ctk.CTkLabel(tela, text="Aqui você verá suas férias", font=ctk.CTkFont(size=20, weight="bold"))
ver_ferias.pack(pady=20)
# função para fechar a tela
def fechar_tela():
    tela.destroy()
# botão de fechar
botao_fechar = ctk.CTkButton(tela, text="Fechar", command=fechar_tela)
botao_fechar.pack(pady=20)
# iniciar a tela
tela.mainloop()