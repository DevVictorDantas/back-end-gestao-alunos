# Comece aqui — guia do aluno

Este é o seu roteiro do começo ao fim: **preparar → entender → implementar →
testar → entregar**. Siga na ordem. Cada etapa aponta para o documento com os
detalhes — não precisa decorar nada, só seguir os passos.

## O que é este projeto

Você recebeu o **esqueleto** de uma API de gestão escolar (FastAPI +
PostgreSQL). Os arquivos existem, mas estão **vazios**, com comentários
`TODO`/`DICA` mostrando **onde** cada coisa vai. Seu trabalho é **implementar o
projeto inteiro**, do banco às rotas, seguindo as dicas. Ao final, você terá uma
API que cadastra, lista, atualiza e apaga alunos e disciplinas, salvando tudo
num banco de dados.

---

## Etapa 1 — Crie o SEU repositório

Não trabalhe no repositório do professor — crie o seu a partir dele.

1. Na página do template no GitHub, clique em **"Use this template" → "Create a
   new repository"**.
2. Dê um nome ao seu projeto e crie.
3. Você terá agora um repositório **seu**, idêntico ao template.

---

## Etapa 2 — Prepare o ambiente

Siga o **[INSTALACAO_WSL.md](INSTALACAO_WSL.md)** — ele instala tudo que você
precisa (Python, PostgreSQL, Git) e cria o banco. Em resumo, depois de clonar o
SEU repositório:

```bash
python3 -m venv venv
source venv/bin/activate            # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env                # ajuste as credenciais se precisar
```

E deixe o **PostgreSQL rodando** com o banco criado (no WSL:
`sudo service postgresql start`).

> ⚠️ Neste ponto, `uvicorn main:app` **ainda não sobe** — o `main.py` está
> vazio. Isso é esperado: você vai preenchê-lo na Etapa 4.

**Checklist da Etapa 2:**
- [ ] `pip list` mostra `fastapi`, `uvicorn`, `psycopg2-binary`, `python-dotenv`
- [ ] Existe um arquivo `.env` (cópia do `.env.example`)
- [ ] `sudo service postgresql status` mostra o banco no ar

---

## Etapa 3 — Entenda o projeto (antes de codar)

Abra e leia, nesta ordem:

1. **[esquema.sql](../esquema.sql)** — é o **modelo de dados**: as 3 tabelas
   (`alunos`, `disciplinas`, `matriculas`) e como se ligam. Você NÃO precisa
   inventar as colunas; elas estão aqui.
2. **[DESAFIOS.md](DESAFIOS.md)** — o enunciado oficial: o que implementar, os
   critérios de aceitação e a **rubrica de nota**.
3. Os arquivos de código, para ver a estrutura e os comentários `TODO`/`DICA`:
   - `db.py` — a "cozinha": a única parte que fala SQL com o banco.
   - `schemas.py` — o "conferente": valida os dados que entram e saem.
   - `main.py` — o "garçom": as rotas que recebem os pedidos HTTP.

> A regra das camadas: rota **fina** (só recebe e responde), SQL **só** no
> `db.py`, validação **só** no `schemas.py`.

---

## Etapa 4 — Implemente (na ordem certa)

Siga a ordem do `DESAFIOS.md`. Cada etapa depende da anterior.

1. **Etapa 0 — A base:** faça a conexão, a criação das tabelas e o **CRUD de
   alunos** funcionarem. É a fundação — sem ela, nada roda.
2. **Desafio 1 — Filtros:** faça o `GET /alunos` aceitar filtros
   (`?idade_minima=&media_minima=&q=`).
3. **Desafio 2 — Disciplinas:** o mesmo CRUD, agora para disciplinas.
4. **Desafio 3 — Matrículas:** ligue alunos e disciplinas (com `JOIN`).

**Como trabalhar sem travar:**
- Implemente **uma função de cada vez** e teste logo.
- Bateu erro? Leia a mensagem — ela quase sempre diz o arquivo e a linha.
- A `DICA` no comentário aponta o caminho (o SQL, o verbo, o status).
- Suba a API com `--reload` para ela reiniciar sozinha a cada vez que você salva:
  ```bash
  uvicorn main:app --reload
  ```

---

## Etapa 5 — Teste o seu trabalho

Você tem duas formas de conferir:

**A) Pela documentação interativa** (mais visual): com a API no ar, abra
<http://127.0.0.1:8000/docs> e teste cada endpoint clicando.

**B) Pelo teste de aceitação** (o alvo): em outro terminal, rode

```bash
bash testar_api.sh
```

Ele bate em todos os endpoints e mostra o **status** de cada resposta. No
começo tudo falha; conforme você implementa, mais testes passam. **Quando todos
baterem com os status do enunciado, o projeto está completo.**

> Confira sempre o **status code**, não só se "não deu erro": criar deve dar
> 201, apagar 204, não encontrado 404, duplicado 409.

---

## Etapa 6 — Versione com Git (durante todo o caminho)

Não deixe para commitar tudo no fim. Faça **commits pequenos e descritivos** à
medida que avança — o histórico mostra como você construiu.

```bash
git add .
git commit -m "Implementa CRUD de alunos (Etapa 0)"
git push
```

Sugestão de commits: um por etapa/desafio concluído (ex.: "Adiciona filtros na
listagem", "Implementa CRUD de disciplinas", "Adiciona matrículas com JOIN").

> **Nunca** comite o arquivo `.env` (ele tem senha e está no `.gitignore`).

---

## Etapa 7 — Entregue o trabalho

Antes de entregar, confira:

- [ ] A API **sobe** (`uvicorn main:app`) sem erro.
- [ ] O `testar_api.sh` passa nos testes das etapas que você concluiu.
- [ ] O `README.md` explica como rodar o seu projeto.
- [ ] O `.env` **não** está no repositório (só o `.env.example`).
- [ ] Há **vários commits** descrevendo a evolução (não um único no final).
- [ ] Você fez `git push` de tudo.

**O que entregar:** o **link do seu repositório** no GitHub. (Prazo e onde
enviar o link, seu professor combina com a turma.)

---

## Dicas finais

- **Comece cedo.** A Etapa 0 é a mais importante; o resto flui a partir dela.
- **Um passo de cada vez.** Implemente, teste, commite. Repita.
- **Leia os erros.** A mensagem quase sempre diz o que e onde corrigir.
- **Quer nota extra?** Veja os **desafios bônus** no `DESAFIOS.md` (nova
  entidade, testes automatizados, deploy...).
