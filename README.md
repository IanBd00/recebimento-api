# API de Recebimento de Estoque

API REST para controle de recebimento de mercadorias via leitura de código DUN-14, desenvolvida como projeto de estudo em infraestrutura e cloud.

## Tecnologias

- Python 3.13 + FastAPI
- PostgreSQL (Supabase)
- Deploy: Railway (CI/CD via GitHub Actions)

## Arquitetura

App Android → API REST (Railway) → PostgreSQL (Supabase)

## Endpoints

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | /produto/{dun14} | Busca produto pelo DUN-14 |
| POST | /recebimento/ | Inicia novo recebimento |
| POST | /recebimento/{id}/item | Adiciona item ao recebimento |
| GET | /recebimento/{id}/relatorio | Relatório final |

## Como rodar localmente

```bash
git clone https://github.com/IanBd00/recebimento-api
cd recebimento-api
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

## Variáveis de ambiente

Crie um arquivo `.env` na raiz com as variáveis:

DB_HOST=
DB_PORT=
DB_NAME=
DB_USER=
DB_PASSWORD=

Suba o servidor:

```bash
uvicorn main:app --reload
```

A documentação interativa estará disponível em `http://localhost:8000/docs`.

## Projeto relacionado

App Android: [recebimento-app](https://github.com/IanBd00/recebimento-app)
