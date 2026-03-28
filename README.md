# Techlog Solutions CRM

![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.135-009688?logo=fastapi)
![SQLite](https://img.shields.io/badge/SQLite-3-003B57?logo=sqlite)
![Docker](https://img.shields.io/badge/Docker-ready-2496ED?logo=docker)
![pytest](https://img.shields.io/badge/Tests-pytest-yellow?logo=pytest)

Sistema de CRM (Customer Relationship Management) para a Techlog Solutions. Permite o gerenciamento completo de clientes com autenticação de usuários por sessão via cookie, interface web responsiva e API REST documentada.

---

## Stack

| Camada | Tecnologia |
|---|---|
| Framework web | [FastAPI](https://fastapi.tiangolo.com/) + [Starlette](https://www.starlette.io/) |
| Servidor ASGI | [Uvicorn](https://www.uvicorn.org/) |
| Templates HTML | [Jinja2](https://jinja.palletsprojects.com/) |
| Validação / modelos | [Pydantic v2](https://docs.pydantic.dev/) |
| Banco de dados | SQLite3 (stdlib) |
| Frontend | Bootstrap 5 (CDN) |
| Testes | [pytest](https://pytest.org/) + [pytest-asyncio](https://pytest-asyncio.readthedocs.io/) + [httpx](https://www.python-httpx.org/) |
| Container | Docker (`python:3.13-slim`) |

---

## Funcionalidades

- **Autenticação de usuários** — cadastro, login e logout com sessão gerenciada por cookie `session_token`
- **Middleware de autenticação** — rotas públicas liberadas (`/`, `/login`, `/registro`); API retorna `401`; páginas redirecionam para `/login`
- **CRUD de clientes** — criação, listagem, edição e exclusão via API REST e interface web
- **Interface web** — páginas HTML com Bootstrap para listar e gerenciar clientes
- **Documentação interativa** — disponível automaticamente em `/docs` (Swagger UI) e `/redoc`
- **Testes** — cobertura com testes unitários (modelos, repositórios, middleware) e testes de integração (rotas de login e registro)

---

## Pré-requisitos

- **Python 3.13+** e `pip` — para execução local
- **Docker** — para execução em container (opcional)

---

## Instalação e execução local

```bash
# 1. Clone o repositório
git clone https://github.com/seu-usuario/projeto-fastapi.git
cd projeto-fastapi

# 2. Crie e ative o ambiente virtual
python -m venv .venv

# Windows (PowerShell)
.venv\Scripts\Activate.ps1

# Linux / macOS
source .venv/bin/activate

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Inicie o servidor
uvicorn app.main:app --reload
```

A aplicação estará disponível em `http://localhost:8000`.

---

## Execução via Docker

```bash
# Build da imagem
docker build -t techlog-crm .

# Execução do container
docker run -p 8000:8000 techlog-crm
```

A aplicação estará disponível em `http://localhost:8000`.

---

## Testes

```bash
# Executar todos os testes
pytest

# Com saída detalhada
pytest -v
```

---

## Endpoints principais

### Autenticação

| Método | Rota | Descrição |
|---|---|---|
| `GET` | `/login` | Página de login |
| `POST` | `/login` | Autentica o usuário e define o cookie de sessão |
| `GET` | `/registro` | Página de cadastro |
| `POST` | `/registro` | Cria um novo usuário |
| `GET` | `/logout` | Encerra a sessão e remove o cookie |

### Clientes — API REST

| Método | Rota | Descrição |
|---|---|---|
| `GET` | `/api/clientes/` | Lista todos os clientes |
| `POST` | `/api/clientes/` | Cria um novo cliente |
| `GET` | `/api/clientes/{id}` | Retorna um cliente pelo ID |
| `PUT` | `/api/clientes/{id}` | Atualiza um cliente |
| `DELETE` | `/api/clientes/{id}` | Remove um cliente |

### Clientes — Interface Web

| Método | Rota | Descrição |
|---|---|---|
| `GET` | `/clientes` | Lista de clientes (página HTML) |
| `GET` | `/clientes/novo` | Formulário de criação |
| `GET` | `/clientes/{id}` | Formulário de edição |

### Utilitários

| Método | Rota | Descrição |
|---|---|---|
| `GET` | `/` | Health check (`{"status": "OK"}`) |
| `GET` | `/front` | Página inicial da aplicação |
| `GET` | `/docs` | Documentação Swagger UI |
| `GET` | `/redoc` | Documentação ReDoc |

---

## Estrutura do projeto

```
projeto-fastapi/
├── app/
│   ├── main.py                       # Configuração da aplicação FastAPI
│   ├── dependencias.py               # Injeção de dependências
│   ├── autenticacao_middleware.py    # Middleware de autenticação por cookie
│   ├── banco_de_dados/
│   │   ├── local.py                  # Conexão e inicialização do SQLite
│   │   ├── cliente_repositorio.py    # Repositório de clientes
│   │   └── usuario_repositorio.py    # Repositório de usuários
│   ├── modelos/
│   │   ├── cliente.py                # Modelos Pydantic de cliente
│   │   └── usuario.py                # Modelos Pydantic de usuário
│   └── rotas/
│       ├── cliente.py                # Rotas de clientes (API + UI)
│       ├── login.py                  # Rotas de autenticação
│       └── registro.py               # Rotas de cadastro
├── static/                           # Arquivos estáticos (CSS, JS)
├── templates/                        # Templates Jinja2 (HTML)
├── tests/                            # Testes unitários e de integração
├── Dockerfile
├── requirements.txt
└── techlog.db                        # Banco de dados SQLite (gerado em runtime)
```
