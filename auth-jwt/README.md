# Flask User Management API

Esta é uma API para gerenciamento de usuários, construída com **Flask**, **SQLAlchemy**, **Flask-JWT-Extended** e **Marshmallow**. A aplicação permite registrar, autenticar e gerenciar usuários, com autenticação baseada em tokens JWT.

## Índice

- [Descrição do Projeto](#descrição-do-projeto)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Pré-requisitos](#pré-requisitos)
- [Instalação](#instalação)
- [Configuração do Ambiente](#configuração-do-ambiente)
- [Rodando a Aplicação](#rodando-a-aplicação)
- [Rotas da API](#rotas-da-api)
- [Estrutura de Pastas](#estrutura-de-pastas)
- [Licença](#licença)

## Descrição do Projeto

Este projeto fornece uma API para gerenciar usuários, com funcionalidades de:

- **Cadastro de usuário** (`POST /register`)
- **Login de usuário** (`POST /login`)
- **Recuperação dos dados do usuário logado** (`GET /me`)
- **Listar todos os usuários** (somente administradores) (`GET /users`)
- **Atualizar dados do usuário** (`PUT /users/<user_id>`)
- **Deletar usuário** (`DELETE /users/<user_id>`)

A API utiliza autenticação baseada em tokens JWT para garantir a segurança das rotas.

## Tecnologias Utilizadas

- **Flask**: Framework web para Python.
- **Flask-SQLAlchemy**: ORM para interagir com bancos de dados SQL.
- **Flask-JWT-Extended**: Extensão para trabalhar com JSON Web Tokens (JWT).
- **Marshmallow**: Biblioteca para serialização e validação de dados.
- **Werkzeug**: Biblioteca para hashing de senhas.

## Pré-requisitos

Antes de começar, você precisa ter o seguinte instalado em sua máquina:

- **Python 3.x**
- **pip** (gerenciador de pacotes Python)

Recomenda-se também usar um ambiente virtual para isolar as dependências do seu projeto.

## Instalação

1. Clone o repositório para sua máquina local:

   ```bash
   git clone https://github.com/seu-usuario/nome-do-repositorio.git
   cd nome-do-repositorio
   ```

2. Crie e ative um ambiente virtual:

   - **No Windows**:
     ```bash
     python -m venv venv
     .\venv\Scripts\activate
     ```

   - **No macOS/Linux**:
     ```bash
     python -m venv venv
     source venv/bin/activate
     ```

3. Instale as dependências do projeto:

   ```bash
   pip install -r requirements.txt
   ```

4. Se não tiver o arquivo `requirements.txt`, você pode gerá-lo com:

   ```bash
   pip freeze > requirements.txt
   ```

## Configuração do Ambiente

1. Crie um arquivo `.env` na raiz do projeto (caso não exista). Exemplo de conteúdo:

   ```env
   FLASK_APP=app.py
   FLASK_ENV=development
   JWT_SECRET_KEY=supersecretkey
   SQLALCHEMY_DATABASE_URI=sqlite:///instance/users.db
   ```

   Certifique-se de configurar a chave secreta JWT (`JWT_SECRET_KEY`) e o URI do banco de dados (`SQLALCHEMY_DATABASE_URI`).

## Rodando a Aplicação

1. Inicialize o banco de dados e crie o usuário administrador padrão (caso ainda não exista):

   ```bash
   flask run
   ```

2. A aplicação estará rodando em `http://127.0.0.1:5000/`.

## Rotas da API

### Cadastro de Usuário (`POST /register`)

- **Descrição**: Registra um novo usuário.
- **Corpo da Requisição**:
  ```json
  {
    "name": "Nome do Usuário",
    "email": "email@example.com",
    "password": "senha123",
    "role": "CLIENT"  // Opcional, padrão "CLIENT"
  }
  ```

- **Resposta**:
  - Sucesso:
    ```json
    {
      "id": 1,
      "name": "Nome do Usuário",
      "email": "email@example.com",
      "role": "CLIENT"
    }
    ```
  - Erro:
    ```json
    {
      "name": ["Shorter than minimum length 2."]
    }
    ```

### Login de Usuário (`POST /login`)

- **Descrição**: Autentica um usuário e retorna um token JWT.
- **Corpo da Requisição**:
  ```json
  {
    "email": "email@example.com",
    "password": "senha123"
  }
  ```

- **Resposta**:
  - Sucesso:
    ```json
    {
      "access_token": "jwt_token"
    }
    ```
  - Erro:
    ```json
    {
      "message": "Invalid credentials"
    }
    ```

### Obter Dados do Usuário Logado (`GET /me`)

- **Descrição**: Retorna os dados do usuário autenticado.
- **Cabeçalho**:
  - `Authorization: Bearer <jwt_token>`
- **Resposta**:
  ```json
  {
    "id": 1,
    "name": "Nome do Usuário",
    "email": "email@example.com",
    "role": "CLIENT"
  }
  ```

### Listar Todos os Usuários (`GET /users`)

- **Descrição**: Lista todos os usuários (somente para ADMIN).
- **Cabeçalho**:
  - `Authorization: Bearer <jwt_token>`
- **Resposta**:
  ```json
  [
    {
      "id": 1,
      "name": "Nome do Usuário",
      "email": "email@example.com",
      "role": "CLIENT"
    },
    {
      "id": 2,
      "name": "Outro Usuário",
      "email": "outro@example.com",
      "role": "ADMIN"
    }
  ]
  ```

### Atualizar Usuário (`PUT /users/<user_id>`)

- **Descrição**: Atualiza os dados de um usuário específico.
- **Corpo da Requisição**:
  ```json
  {
    "name": "Novo Nome",
    "email": "novo_email@example.com",
    "password": "nova_senha123"
  }
  ```

### Deletar Usuário (`DELETE /users/<user_id>`)

- **Descrição**: Deleta um usuário específico.

## Estrutura de Pastas

```
my_flask_app/
│
├── app.py                      # Arquivo principal (inicialização da aplicação)
├── config.py                   # Arquivo de configuração
│
├── models/
│   └── user.py                 # Modelo de Usuário
│
├── schemas/
│   └── user_schema.py          # Esquema Marshmallow para Usuário
│
├── routes/
│   ├── auth_routes.py          # Rotas de autenticação
│   ├── user_routes.py          # Rotas de usuário
│
├── migrations/                 # Arquivos de migração (se usar Alembic)
│
├── instance/
│   └── users.db                # Banco de dados SQLite
│
├── requirements.txt            # Dependências do projeto
├── .gitignore                  # Arquivo de ignorados (banco de dados ambiente virtual, etc.)
└── README.md                   # Documentação do projeto
```