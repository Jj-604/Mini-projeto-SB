# 🚀 Projeto ATLAS - Interface de Gestão (Finalizado)

![Status](https://img.shields.io/badge/STATUS-CONCLUÍDO-green)

O **Projeto ATLAS** é um sistema de gerenciamento completo com interface gráfica moderna, desenvolvido em Python. A aplicação oferece controle administrativo robusto, com hierarquia de acessos (Supervisor e Funcionário) e ferramentas de produtividade integradas.

> [!WARNING] > **AVISO:** Este projeto é somente para fins acadêmicos e não está pronto para ser implementado em um plano real.

## 🛠️ Tecnologias Utilizadas

- **Python 3.x**
- **Tkinter & CustomTkinter**: Interface gráfica moderna com tema escuro.
- **SQLite3**: Banco de dados local para usuários, escalas, ponto e feedbacks.
- **Hashlib**: Criptografia segura de senhas (SHA-256).

## 📋 Funcionalidades Implementadas

### 🔐 Autenticação e Segurança

- [x] Login e Cadastro com validação.
- [x] Criptografia de senhas.
- [x] Hierarquia de usuários: **Supervisor** e **Funcionário**.
- [x] Sessão persistente local.

### 👔 Módulo do Supervisor

- [x] **Dashboard**: Visão geral de funcionários online/offline.
- [x] **Gestão de Funcionários**: Adicionar, editar e remover usuários.
- [x] **Gestão de Escalas**: Criar e aprovar escalas de trabalho.
- [x] **Feedbacks**: Visualizar e responder feedbacks dos funcionários.
- [x] **Relatórios**: Exportação de registros de ponto para CSV.

### 👷 Módulo do Funcionário

- [x] **Ponto Eletrônico**: Registro de entrada e saída com histórico.
- [x] **Minha Escala**: Visualização de escalas de trabalho.
- [x] **Feedbacks**: Envio de dúvidas/sugestões e visualização de respostas.
- [x] **Notificações Automáticas**: Avisos em tempo real sobre respostas e escalas.
- [x] **Perfil**: Alteração de senha e tema.

### ⚙️ Melhorias Técnicas

- [x] **Centralização de Strings**: Uso de `constants.py` para fácil manutenção.
- [x] **Notificações Inteligentes**: Sistema de gatilhos automáticos para avisos importantes.

## 🚀 Como Executar

1.  Clone o repositório.
2.  Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```
3.  Execute o sistema:
    ```bash
    python tela_inicial.py
    ```

## 📂 Estrutura do Projeto

- `tela_inicial.py`: Tela de boas-vindas.
- `tela_login.py` / `tela_cadastro.py`: Autenticação.
- `tela_supervisor.py`: Painel administrativo completo.
- `tela_funcionario.py`: Painel do colaborador.
- `database.py`: Camada de persistência e regras de negócio.
- `constants.py`: Centralização de textos e configurações.
- `utils.py`: Funções utilitárias (ex: centralizar janelas).

---

Desenvolvido para fins educativos.
