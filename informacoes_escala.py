import customtkinter as ctk
# configurações de aparência
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")
# tela de login
tela = ctk.CTk()
tela.title("Tela de escala")
tela.geometry("1920x1080")
informacoes_escala = ctk.CTkLabel(tela, text="Informações da escala", font=ctk.CTkFont(size=20, weight="bold"))
informacoes_escala.pack(pady=20)
informacoes_escala_2 = ctk.CTkLabel(tela, text="Aqui estarão as informações da escala", font=ctk.CTkFont(size=16))
informacoes_escala_2.pack(pady=10)
escala_equipes = ctk.CTkLabel(tela, text="Escala de equipes", font=ctk.CTkFont(size=18, weight="bold"))
escala_equipes.pack(pady=15)
escala_equipes_2 = ctk.CTkLabel(tela, text="Aqui estarão as equipes escaladas", font=ctk.CTkFont(size=16))
escala_equipes_2.pack(pady=10)
alteraçoes_escala = ctk.CTkLabel(tela, text="Alterações na escala", font=ctk.CTkFont(size=18, weight="bold"))
alteraçoes_escala.pack(pady=15)
alteraçoes_escala_2 = ctk.CTkLabel(tela, text="Aqui estarão as alterações na escala", font=ctk.CTkFont(size=16))
alteraçoes_escala_2.pack(pady=10)
aprovar_escala_btn = ctk.CTkButton(tela, text="Aprovar escala")
aprovar_escala_btn.pack(pady=20)
folgas_btn = ctk.CTkButton(tela, text="Folgas")
folgas_btn.pack(pady=10)
feriados_btn = ctk.CTkButton(tela, text="Feriados")
feriados_btn.pack(pady=10)
ferias_btn = ctk.CTkButton(tela, text="Férias")
ferias_btn.pack(pady=10)
# função para voltar à tela inicial
def voltar_tela_inicial():
    tela.destroy()
    import tela_inicial
# botão de voltar
botao_voltar = ctk.CTkButton(tela, text="Voltar", command=voltar_tela_inicial)
botao_voltar.pack(pady=20)
# iniciar a tela
tela.mainloop()