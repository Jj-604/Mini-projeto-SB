# Projeto ATLAS - Interface de Gestão

O **Projeto ATLAS** é um sistema de gerenciamento com interface gráfica moderna, desenvolvido em Python. O objetivo é criar uma aplicação intuitiva para controle administrativo, com hierarquia de acessos e ferramentas de produtividade.

Atualmente, o projeto conta com um sistema de autenticação e navegação entre telas iniciais.

## 🛠️ Tecnologias Utilizadas

* **Python 3.x**
* **Tkinter**: Biblioteca padrão para interfaces gráficas.
* **CustomTkinter**: Para elementos visuais modernos, modo escuro e temas personalizados.

## 📋 Pré-requisitos

Para executar este projeto, você precisará ter o Python instalado e adicionar a biblioteca `customtkinter`:

```bash
pip install customtkinter
````

## 🚀 Como Executar

1.  Clone o repositório ou baixe os arquivos.
2.  Certifique-se de que todos os arquivos `.py` estejam na mesma pasta.
3.  Execute o arquivo principal para iniciar o sistema:

<!-- end list -->

```bash
python tela_inicial.py
```

> **Nota:** O sistema navega entre janelas fechando a atual e importando a próxima etapa (Login ou Cadastro).

## 📅 Roadmap e Funcionalidades

Abaixo estão as funcionalidades planejadas e o estado atual do desenvolvimento (baseado nas ideias iniciais do projeto).

### ✅ Implementado

  - [x] Tela Inicial de navegação.
  - [x] Tela de Login (`customtkinter`).
  - [x] Tela de Cadastro (`customtkinter`).
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

-----

Desenvolvido para fins educativos.

```

### O que foi melhorado:

1.  **Título e Descrição:** Adicionei um título claro e uma breve explicação do que o código faz, baseada nos arquivos que você enviou.
2.  **Instalação:** Como seus arquivos `tela_login.py` e `tela_cadastro.py` usam `import customtkinter`, é essencial avisar ao usuário que ele precisa instalar essa biblioteca (`pip install`), caso contrário o código dará erro.
3.  **Organização das Ideias:** Peguei sua lista de 20 ideias e as agrupei por categorias (UI, Gestão, Ferramentas). Isso mostra profissionalismo e clareza sobre onde você quer chegar.
4.  **Correção Ortográfica:** Corrigi termos como "loguin" para "Login" e "ierarquia" para "Hierarquia".

Você gostaria que eu ajudasse a implementar alguma dessas funcionalidades da lista "Planejado", como o botão de "Voltar" nas telas de login/cadastro?
```
