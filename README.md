# API de Gestão de Alunos — projeto base (template)

API REST de **gestão escolar**, feita com **FastAPI** e **PostgreSQL**. Este
repositório é um **template de estudo em forma de esqueleto**: os arquivos já
existem (`main.py`, `db.py`, `schemas.py`, ...), mas **sem código pronto** —
apenas comentários `TODO`/`DICA` indicando **onde cada coisa vai**.

Você implementa o projeto **inteiro**, da conexão com o banco até as rotas da
API. É aprender construindo de verdade: a estrutura te guia, o código é seu.

> 👉 **Novo por aqui? Comece pelo [COMECE_AQUI.md](docs/COMECE_AQUI.md)** — o
> roteiro do começo ao fim (preparar → entender → implementar → testar → entregar).

> **Como usar este template:** no GitHub, clique em **"Use this template" →
> "Create a new repository"** para gerar o *seu* repositório a partir deste.
> Depois siga o [guia de instalação](docs/INSTALACAO_WSL.md).

## O que vem no template

- **A estrutura** dos arquivos, cada um com sua responsabilidade de camada.
- Comentários **`TODO`/`DICA`** guiando o que implementar em cada ponto.
- O **modelo de dados** definido em [esquema.sql](esquema.sql) (as 3 tabelas).
- Config de projeto pronta: `requirements.txt`, `.env.example`, `.gitignore`.
- O **teste de aceitação** ([testar_api.sh](testar_api.sh)) e o **guia de
  instalação** ([INSTALACAO_WSL.md](docs/INSTALACAO_WSL.md)).

Nenhum código de aplicação vem pronto — isso é com você.

## O que VOCÊ implementa

Siga o roteiro completo em **[DESAFIOS.md](docs/DESAFIOS.md)** (com critérios de
aceitação e rubrica de nota). Em resumo:

| Etapa | Onde | O que fazer |
|---|---|---|
| **0 — Base** | `db.py` + `schemas.py` + `main.py` | Conexão, criar tabelas e CRUD de alunos (a fundação) |
| **1 — Filtros** | `db.py` + `main.py` | `GET /alunos` com `?idade_minima=&media_minima=&q=` |
| **2 — Disciplinas** | `schemas.py` + `db.py` + `main.py` | CRUD de disciplinas |
| **3 — Matrículas** | `db.py` + `main.py` | Relacionar aluno ↔ disciplina (`JOIN`) |

**Como validar:** rode o `testar_api.sh` (é o alvo). No começo tudo falha;
conforme você implementa, os testes passam. Quando todos baterem, terminou.

## Estrutura

```
.
├── main.py            # ESQUELETO — rotas FastAPI (você implementa)
├── schemas.py         # ESQUELETO — modelos Pydantic (você implementa)
├── db.py              # ESQUELETO — conexão e queries SQL (você implementa)
├── esquema.sql        # o modelo de dados (as 3 tabelas) — sua especificação
├── testar_api.sh      # teste de aceitação com curl (o alvo)
├── requirements.txt   # bibliotecas do projeto
├── .env.example       # modelo de credenciais (copie para .env)
├── .gitignore
├── README.md
└── docs/              # documentação (guias)
    ├── COMECE_AQUI.md     # guia do aluno do começo ao fim (leia primeiro)
    ├── INSTALACAO_WSL.md  # passo a passo de instalação no WSL Ubuntu
    └── DESAFIOS.md        # enunciado dos desafios + rubrica de avaliação
```

Cada arquivo tem **uma responsabilidade** (arquitetura em camadas): mudar o
banco não afeta as rotas; mudar a validação não afeta o SQL.

## Início rápido

> Para o passo a passo completo (instalar Python, PostgreSQL, Git e configurar
> o banco no WSL Ubuntu), veja **[INSTALACAO_WSL.md](docs/INSTALACAO_WSL.md)**.

Resumo, assumindo Python 3 e um PostgreSQL já rodando com o banco criado:

```bash
# 1. Ambiente virtual + dependências
python3 -m venv venv
source venv/bin/activate            # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 2. Credenciais
cp .env.example .env                # ajuste os valores se necessário

# 3. Implemente o projeto (comece pela Etapa 0 do DESAFIOS.md).
#    Enquanto o main.py não tiver o `app`, o comando abaixo ainda não sobe.

# 4. Depois de implementar, suba a API:
uvicorn main:app --reload
```

Com a API no ar, abra <http://127.0.0.1:8000/docs> para explorar os endpoints,
e rode `bash testar_api.sh` (em outro terminal) para checar os status.

## Endpoints

Todos os endpoints abaixo são **para você implementar** (veja `DESAFIOS.md`):

| Método | Rota | O que faz | Etapa |
|---|---|---|---|
| POST | `/alunos` | Cria aluno (201) · matrícula duplicada → 409 | 0 |
| GET | `/alunos` | Lista alunos (com filtros) | 0 + 1 |
| GET | `/alunos/{id}` | Busca um · 404 se não existir | 0 |
| PATCH | `/alunos/{id}` | Atualização parcial | 0 |
| DELETE | `/alunos/{id}` | Exclui (204) · 404 se não existir | 0 |
| POST | `/disciplinas` | Cria disciplina | 2 |
| GET | `/disciplinas` | Lista disciplinas | 2 |
| DELETE | `/disciplinas/{id}` | Exclui disciplina | 2 |
| POST | `/alunos/{id}/matricular/{disc_id}` | Matricula aluno em disciplina | 3 |
| GET | `/alunos/{id}/disciplinas` | Disciplinas do aluno (JOIN) | 3 |

## Depois dos desafios: como ir além

Terminou os desafios acima? Sugestões para levar o projeto ao próximo nível:

- **Nova entidade:** adicione `professores` (ou `turmas`, `notas`) com o mesmo
  padrão de camadas — um bom exercício para fixar o CRUD.
- **Testes automatizados:** `pytest` + o `TestClient` do FastAPI, para o
  computador conferir a API a cada mudança.
- **ORM:** troque o SQL manual do `db.py` por **SQLAlchemy**; use **Alembic**
  para versionar mudanças no banco (migrations).
- **Autenticação:** proteja os endpoints com **JWT** (OAuth2 do FastAPI).
- **Deploy:** empacote com **Docker** e publique (Render, Fly.io, Railway).
- **Frontend:** consuma a API a partir de um app React/Flutter ou um HTML
  simples com `fetch()`.

## Tecnologias

- [Python 3](https://www.python.org/)
- [FastAPI](https://fastapi.tiangolo.com/) + [Uvicorn](https://www.uvicorn.org/)
- [PostgreSQL](https://www.postgresql.org/) via [psycopg2](https://www.psycopg.org/)
- [Pydantic](https://docs.pydantic.dev/) para validação
- [python-dotenv](https://pypi.org/project/python-dotenv/) para credenciais
