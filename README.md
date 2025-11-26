# Projeto ATLAS - Interface de Gestão

O **Projeto ATLAS** é um sistema de gerenciamento com interface gráfica moderna, desenvolvido em Python. O objetivo é criar uma aplicação intuitiva para controle administrativo, com hierarquia de acessos e ferramentas de produtividade.

Atualmente, o projeto conta com um sistema de autenticação funcional (Cadastro e Login) integrado a um banco de dados local.

## 🛠️ Tecnologias Utilizadas

- **Python 3.x**
- **Tkinter**: Biblioteca padrão para interfaces gráficas.
- **CustomTkinter**: Para elementos visuais modernos, modo escuro e temas personalizados.
- **SQLite3**: Banco de dados relacional leve e local para armazenamento de usuários.
- **Hashlib**: Para criptografia segura de senhas (SHA-256).

## 📋 Pré-requisitos

Para executar este projeto, você precisará ter o Python instalado e adicionar a biblioteca `customtkinter`:

```bash
pip install customtkinter
```

## 🚀 Como Executar

1.  Clone o repositório ou baixe os arquivos.
2.  Certifique-se de que todos os arquivos `.py` estejam na mesma pasta.
3.  Execute o arquivo principal para iniciar o sistema:

```bash
python tela_inicial.py
```

> **Nota:** O sistema criará automaticamente um arquivo `usuarios.db` na primeira execução para armazenar os dados de login.

## 📂 Estrutura do Projeto

- `tela_inicial.py`: Ponto de entrada da aplicação. Permite escolher entre Login ou Cadastro.
- `tela_login.py`: Formulário de login. Verifica as credenciais no banco de dados.
- `tela_cadastro.py`: Formulário de registro. Salva novos usuários no banco de dados com senha criptografada.
- `database.py`: Módulo responsável pela conexão com o SQLite e operações de banco de dados (CRUD).

## 📅 Roadmap e Funcionalidades

Abaixo estão as funcionalidades planejadas e o estado atual do desenvolvimento.

### ✅ Implementado

- [x] Tela Inicial de navegação.
- [x] Tela de Login (`customtkinter`).
- [x] Tela de Cadastro (`customtkinter`).
- [x] **Integração com Banco de Dados SQLite.**
- [x] **Criptografia de senhas.**
- [x] Resolução padrão 1920x1080.
- [x] Tema escuro (Dark Mode) com detalhes em azul.

### 📝 Planejado (Backlog)

**Interface e Experiência (UI/UX)**

- [ ] Interface intuitiva e simples de usar.
- [ ] Tela de Configurações e Ajuda.
- [ ] Botões de navegação (Sair, Voltar, Avançar).
- [ ] Tela de Feedback dos usuários.

**Gestão e Segurança**

- [ ] **Hierarquia de acessos:** Níveis para Supervisor, Técnico e Usuário Comum.
- [ ] Adicionar e remover funcionários.
- [ ] Configurações de segurança.
- [ ] Tela de Perfil do Usuário.

**Ferramentas Administrativas**

- [ ] Tela de Notificações e Alertas.
- [ ] Relatórios e Estatísticas.
- [ ] Suporte Técnico.
- [ ] Atualizações do Sistema.
- [ ] Gerenciamento de Tarefas.
- [ ] Calendário e Agendamentos.
- [ ] Mensagens Internas (Chat).
- [ ] Gestão de Documentos e Arquivos.
- [ ] Ponto de Escala.

---

Desenvolvido para fins educativos.