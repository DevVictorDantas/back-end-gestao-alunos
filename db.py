"""
CAMADA DE BANCO (db.py)  —  ESQUELETO, implemente você mesmo
============================================================

Esta é a ÚNICA parte do projeto que "fala SQL". As rotas (main.py) nunca
escrevem SQL: elas chamam as funções daqui. Essa separação em camadas é o
coração do módulo.

REGRA DE OURO (segurança): os VALORES que vêm do cliente vão SEMPRE como %s
+ tupla de parâmetros. Nunca concatene dados do usuário na string SQL
(isso abre SQL Injection).

Ordem sugerida de implementação:
  1. Configuração + conectar()      -> abrir conexão com o PostgreSQL
  2. criar_tabelas()                -> criar alunos, disciplinas, matriculas
  3. CRUD de alunos                 -> inserir / listar / buscar / atualizar / excluir
  4. CRUD de disciplinas            (Desafio 2)
  5. matrículas + JOIN              (Desafio 3)

O modelo de dados (as 3 tabelas) está definido em `esquema.sql` — use como
referência ao escrever criar_tabelas().
"""

# DICA — bibliotecas que você provavelmente vai usar:
#   import os
#   import psycopg2
#   from psycopg2.extras import RealDictCursor   # faz o banco devolver dict, não tupla
#   from dotenv import load_dotenv               # lê o arquivo .env


# TODO: carregue as variáveis do .env (load_dotenv) e monte um CONFIG lendo
#       DB_HOST, DB_NAME, DB_USER, DB_PASSWORD (dica: os.getenv com um padrão).


# TODO: def conectar():
#   Abra e devolva uma conexão psycopg2 usando o CONFIG.
#   Dica: passe cursor_factory=RealDictCursor para as linhas virem como dicts.


# TODO: def criar_tabelas():
#   Crie as 3 tabelas com "CREATE TABLE IF NOT EXISTS ..." (veja esquema.sql).
#   Esta função é chamada no startup da API (main.py).


# --------------------------------------------------------------------------
# CRUD de ALUNOS
# --------------------------------------------------------------------------
# TODO: inserir_aluno(nome, idade, matricula, media=0)
#   INSERT na tabela alunos. Dica: use "RETURNING *" para já receber de volta
#   a linha criada (com o id gerado pelo banco).
#
# TODO: listar_alunos()
#   SELECT de todos os alunos, ordenados por id.
#   (Fazer aceitar filtros é o Desafio 1 — comece simples.)
#
# TODO: buscar_aluno(aluno_id)
#   SELECT de um aluno por id. Devolva None se não existir.
#
# TODO: atualizar_aluno(aluno_id, **campos)
#   UPDATE parcial: atualize só os campos recebidos. Dica: nomes de coluna
#   podem entrar por f-string (são do seu código); VALORES vão com %s.
#
# TODO: excluir_aluno(aluno_id)
#   DELETE por id. Devolva True/False (dica: cur.rowcount > 0).


# --------------------------------------------------------------------------
# CRUD de DISCIPLINAS  (Desafio 2)
# --------------------------------------------------------------------------
# TODO: inserir_disciplina, listar_disciplinas, buscar_disciplina,
#       excluir_disciplina — espelhando o CRUD de alunos.


# --------------------------------------------------------------------------
# MATRÍCULAS — relacionamento aluno <-> disciplina  (Desafio 3)
# --------------------------------------------------------------------------
# TODO: matricular(aluno_id, disciplina_id)
#   INSERT na tabela matriculas. Dica: "ON CONFLICT DO NOTHING" evita erro se
#   a matrícula já existir.
#
# TODO: disciplinas_do_aluno(aluno_id)
#   Liste as disciplinas em que o aluno está matriculado. Dica: use JOIN entre
#   disciplinas e matriculas.
