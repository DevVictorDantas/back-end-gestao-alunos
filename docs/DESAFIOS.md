# Desafios — API de Gestão Escolar

Este é o **enunciado oficial** da entrega. Você recebeu um projeto em forma de
**esqueleto**: os arquivos existem (`main.py`, `db.py`, `schemas.py`, ...) com
comentários indicando **onde cada coisa vai**, mas **sem código pronto**. Sua
tarefa é implementar o projeto **inteiro** — da conexão com o banco até as
rotas da API — seguindo as dicas.

> **Antes de começar:** monte o ambiente seguindo o
> [INSTALACAO_WSL.md](INSTALACAO_WSL.md). Estude os comentários `TODO` /
> `DICA` em cada arquivo — eles são o seu roteiro.

## Modelo de dados (a especificação)

O arquivo [esquema.sql](../esquema.sql) define as **3 tabelas** do sistema
(`alunos`, `disciplinas`, `matriculas`) e como elas se relacionam. Esse é o
contrato: você implementa exatamente esse modelo (em `db.criar_tabelas`).

## Como validar o seu trabalho

O [testar_api.sh](../testar_api.sh) é o seu **teste de aceitação**: ele bate em
todos os endpoints e mostra os status HTTP. Com a API no ar, rode em outro
terminal:

```bash
bash testar_api.sh
```

No começo tudo falha; conforme você implementa, mais testes passam. Quando
todos baterem com os status do enunciado, o projeto está completo.

---

## Etapa 0 — A base (infraestrutura + CRUD de alunos)

**Objetivo:** deixar a API de pé, com a entidade **aluno** funcionando ponta a
ponta. É a fundação — as etapas seguintes dependem dela.

**O que fazer:**

- `db.py`: implemente `conectar()`, `criar_tabelas()` (crie as 3 tabelas — veja
  `esquema.sql`) e o CRUD de aluno (`inserir_aluno`, `listar_alunos`,
  `buscar_aluno`, `atualizar_aluno`, `excluir_aluno`).
- `schemas.py`: implemente `AlunoEntrada`, `AlunoAtualizacao` e `AlunoSaida`.
- `main.py`: crie o `app`, o startup que chama `criar_tabelas`, e as 5 rotas
  de aluno.

**Critérios de aceitação:**

| Requisição | Resultado esperado |
|---|---|
| `uvicorn main:app` sobe sem erro e cria as tabelas | API no ar; `/docs` responde |
| `POST /alunos` válido | 201 · objeto criado com `id` |
| `POST /alunos` com matrícula repetida | 409 Conflict |
| `POST /alunos` com idade fora de 0–120 | 422 (validação Pydantic) |
| `GET /alunos` | 200 · lista |
| `GET /alunos/{id}` inexistente | 404 |
| `PATCH /alunos/{id}` com `{"media": 9.5}` | 200 · só a média muda |
| `DELETE /alunos/{id}` existente / inexistente | 204 / 404 |

---

## Desafio 1 — Filtros na listagem de alunos

**Objetivo:** fazer o `GET /alunos` aceitar filtros opcionais e combináveis.

**O que fazer:** em `db.listar_alunos`, aceite `idade_minima`, `media_minima` e
`q` (nome). Em `main.py`, receba-os como query parameters.

**Regras:** filtros combináveis (satisfazer todos); `q` ignora maiúsc/minúsc
(`ILIKE`); valores sempre parametrizados (`%s`).

**Critérios de aceitação:**

| Requisição | Resultado esperado |
|---|---|
| `GET /alunos?idade_minima=18` | 200 · só idade ≥ 18 |
| `GET /alunos?media_minima=7` | 200 · só média ≥ 7 |
| `GET /alunos?q=an` | 200 · só nomes contendo "an" |
| `GET /alunos?idade_minima=18&media_minima=7` | 200 · quem satisfaz **os dois** |

---

## Desafio 2 — CRUD de disciplinas

**Objetivo:** dar à entidade **disciplina** o mesmo CRUD do aluno.

**O que fazer:** schemas (`DisciplinaEntrada`/`DisciplinaSaida`), funções no
`db.py` e rotas no `main.py`.

**Regras:** nome único → 409 em duplicado; `carga_horaria > 0` (valide no
schema); excluir inexistente → 404.

**Critérios de aceitação:**

| Requisição | Resultado esperado |
|---|---|
| `POST /disciplinas` com `{"nome":"Python","carga_horaria":40}` | 201 · com `id` |
| `POST /disciplinas` "Python" de novo | 409 Conflict |
| `POST /disciplinas` com `carga_horaria` 0 | 422 |
| `GET /disciplinas` | 200 · lista |
| `DELETE /disciplinas/{id}` existente / inexistente | 204 / 404 |

---

## Desafio 3 — Matrículas (relacionamento)

**Objetivo:** ligar alunos e disciplinas. Depende do Desafio 2.

**O que fazer:** `db.matricular` e `db.disciplinas_do_aluno` (com **JOIN**);
rotas `POST /alunos/{aluno_id}/matricular/{disciplina_id}` e
`GET /alunos/{aluno_id}/disciplinas`.

**Regras:** 404 se aluno **ou** disciplina não existir; matricular duas vezes
não pode dar erro nem duplicar (`ON CONFLICT DO NOTHING`).

**Critérios de aceitação:**

| Requisição | Resultado esperado |
|---|---|
| `POST /alunos/1/matricular/1` (ambos existem) | 201 |
| `POST /alunos/9999/matricular/1` | 404 |
| `POST /alunos/1/matricular/9999` | 404 |
| `POST /alunos/1/matricular/1` repetido | 201, sem duplicar |
| `GET /alunos/1/disciplinas` | 200 · disciplinas do aluno (via JOIN) |

---

## Desafios bônus (opcionais — nota extra)

- Nova entidade `professores`/`turmas`/`notas` com CRUD completo.
- Testes automatizados (`pytest` + `TestClient` do FastAPI).
- `PUT /alunos/{id}` (substituição total) além do `PATCH`.
- Paginação na listagem (`?limite=&pagina=`).
- Deploy online (Docker + Render/Fly.io/Railway).

---

## Como entregar

1. Trabalhe no **seu** repositório (criado a partir deste template).
2. Use o Git ao longo do caminho: **vários commits descritivos**, não um só no
   final. O histórico mostra como você evoluiu.
3. Mantenha o **`README.md`** com instruções de como rodar o seu projeto.
4. **Nunca** comite o `.env` (está no `.gitignore`).
5. Entregue o **link do repositório**.

## Rubrica de avaliação (nota 0–10)

| Item | Pontos | O que se avalia |
|---|---:|---|
| **Etapa 0 — Base** | 3,0 | Conexão + tabelas + CRUD de alunos funcionando; API sobe |
| **Desafio 1 — Filtros** | 1,5 | 3 filtros combináveis; valores parametrizados |
| **Desafio 2 — Disciplinas** | 2,0 | 4 operações; 409 em duplicado; 404 ao excluir inexistente |
| **Desafio 3 — Matrículas** | 2,0 | Relacionamento com JOIN; 404 nos casos certos; sem duplicar |
| **Qualidade do código** | 1,0 | Camadas (rotas finas, SQL só no `db.py`); status HTTP corretos; SQL parametrizado |
| **Uso do Git** | 0,5 | Histórico com commits pequenos e descritivos |
| **Bônus** | +1,0 | Qualquer desafio bônus bem feito (teto de +1,0 na nota final) |

> **Pré-requisito:** o projeto precisa **subir e rodar**. Sem a Etapa 0, os
> demais desafios não têm como ser avaliados.
